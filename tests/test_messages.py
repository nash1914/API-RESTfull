import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# CONFIGURACIÓN DE SEGURIDAD PARA TESTS
HEADERS = {"X-API-KEY": "nequi_secret_token_2026"}


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


#TESTS

def test_unauthorized_access():
    payload = {"message_id": "no-key", "session_id": "s1", "content": "hola", "sender": "user",
               "timestamp": "2023-06-15T14:30:00Z"}

    response_post = client.post("/api/messages", json=payload)
    assert response_post.status_code == 401

    response_get = client.get("/api/messages/s1")
    assert response_get.status_code == 401


def test_create_message_success():
    payload = {
        "message_id": "test-1",
        "session_id": "session-test",
        "content": "Hola mundo",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user"
    }
    response = client.post("/api/messages", json=payload, headers=HEADERS)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["metadata"]["word_count"] == 2

def test_create_message_invalid_sender():
    payload = {
        "message_id": "test-2",
        "session_id": "session-test",
        "content": "Mensaje fallido",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "admin"
    }
    response = client.post("/api/messages", json=payload, headers=HEADERS)
    assert response.status_code == 422


def test_get_messages_pagination():

    client.post("/api/messages", json={
        "message_id": "m1", "session_id": "s1", "content": "test",
        "timestamp": "2023-06-15T14:30:00Z", "sender": "user"
    }, headers=HEADERS)

    response = client.get("/api/messages/s1?limit=1&offset=0", headers=HEADERS)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1