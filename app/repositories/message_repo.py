from sqlalchemy.orm import Session
from app.models.entities import MessageEntity
from typing import List, Optional


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, message_entity: MessageEntity) -> MessageEntity:
        self.db.add(message_entity)
        self.db.commit()
        self.db.refresh(message_entity)
        return message_entity

    def get_by_session(
            self,
            session_id: str,
            limit: int = 10,
            offset: int = 0,
            sender: Optional[str] = None
    ) -> List[MessageEntity]:

        query = self.db.query(MessageEntity).filter(MessageEntity.session_id == session_id)

        if sender:
            query = query.filter(MessageEntity.sender == sender)

        return query.offset(offset).limit(limit).all()