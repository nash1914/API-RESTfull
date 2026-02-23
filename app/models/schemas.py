from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Dict, List

class MessageRequest(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str

    @field_validator('sender')
    @classmethod
    def validate_sender(cls, v: str):
        if v not in ['user', 'system']:
            raise ValueError("El campo 'sender' debe ser 'user' o 'system'")
        return v

class MessageMetadata(BaseModel):
    word_count: int
    character_count: int
    processed_at: str

class MessageResponseData(BaseModel):
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: str
    metadata: MessageMetadata

class APIResponse(BaseModel):
    status: str
    data: Optional[MessageResponseData] = None
    error: Optional[Dict] = None