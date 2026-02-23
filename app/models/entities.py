from sqlalchemy import Column, String, Integer, DateTime
from app.core.database import Base
from datetime import datetime


class MessageEntity(Base):
    __tablename__ = "messages"

    message_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    content = Column(String)
    timestamp = Column(DateTime)
    sender = Column(String)

    # Metadata
    word_count = Column(Integer)
    character_count = Column(Integer)
    processed_at = Column(DateTime, default=datetime.utcnow)