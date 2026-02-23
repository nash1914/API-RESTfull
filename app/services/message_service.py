from datetime import datetime, timezone
from app.repositories.message_repo import MessageRepository
from app.models.entities import MessageEntity
from app.models.schemas import MessageRequest


class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    def process_and_save(self, message_data: MessageRequest) -> dict:
        content_procesado = self._filter_content(message_data.content)

        # Metadatos
        word_count = len(content_procesado.split())
        character_count = len(content_procesado)
        processed_at = datetime.now(timezone.utc)

        new_message = MessageEntity(
            message_id=message_data.message_id,
            session_id=message_data.session_id,
            content=content_procesado,
            timestamp=message_data.timestamp,
            sender=message_data.sender,
            word_count=word_count,
            character_count=character_count,
            processed_at=processed_at
        )

        saved_entity = self.repository.save(new_message)

        return self._format_response(saved_entity)

    def get_session_messages(self, session_id: str, limit: int, offset: int, sender: str = None):
        messages = self.repository.get_by_session(session_id, limit, offset, sender)
        return [self._format_response(m) for m in messages]

    def _filter_content(self, text: str) -> str:
        palabras_prohibidas = ["spam", "ofensivo", "inapropiado"]
        for palabra in palabras_prohibidas:
            text = text.replace(palabra, "***")
        return text

    def _format_response(self, entity: MessageEntity) -> dict:
        return {
            "message_id": entity.message_id,
            "session_id": entity.session_id,
            "content": entity.content,
            "timestamp": entity.timestamp.isoformat() if isinstance(entity.timestamp, datetime) else entity.timestamp,
            "sender": entity.sender,
            "metadata": {
                "word_count": entity.word_count,
                "character_count": entity.character_count,
                "processed_at": entity.processed_at.isoformat() + "Z"
            }
        }