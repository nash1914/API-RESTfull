from fastapi import FastAPI
from app.api.messages import router as messages_router

# Creamos la instancia de FastAPI
app = FastAPI(
    title="Nequi Message Processor API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
app.include_router(messages_router, prefix="/api", tags=["Messages"])