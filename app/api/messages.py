from fastapi import APIRouter, Depends, Query, HTTPException, Security, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.models.schemas import MessageRequest, APIResponse
from app.repositories.message_repo import MessageRepository
from app.services.message_service import MessageService
from app.core.security import get_api_key
from app.core.websocket_manager import manager

router = APIRouter()


def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    repository = MessageRepository(db)
    return MessageService(repository)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.post("/messages", response_model=APIResponse, status_code=201)
async def create_message(
        msg: MessageRequest,
        service: MessageService = Depends(get_message_service),
        api_key: str = Depends(get_api_key)
):
    try:
        processed_message = service.process_and_save(msg)

        await manager.broadcast({
            "event": "NEW_MESSAGE",
            "data": processed_message
        })

        return {
            "status": "success",
            "data": processed_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/messages/{session_id}")
async def get_messages(
        session_id: str,
        sender: Optional[str] = Query(None, pattern="^(user|system)$"),
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        service: MessageService = Depends(get_message_service),
        api_key: str = Depends(get_api_key)
):
    messages = service.get_session_messages(session_id, limit, offset, sender)
    return {
        "status": "success",
        "data": messages
    }