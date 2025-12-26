from sqlalchemy import Column, String
from .base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Text, DateTime, text
import uuid


class ChatLog(Base):
    __table_args__ = {"schema": "chatbot"}
    __tablename__ = "chat_logs"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    user_message = Column(Text)
    ai_response = Column(Text)
    model_used = Column(String)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
