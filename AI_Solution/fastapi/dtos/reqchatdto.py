from pydantic import BaseModel


class ChatRequestDTO(BaseModel):
    message: str
    user_id: str = "guest"
