from pydantic import BaseModel


class ChatResponseDTO(BaseModel):
    reply: str
    model_used: str
