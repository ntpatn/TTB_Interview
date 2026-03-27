from pydantic import BaseModel
from typing import List, Optional, Dict


class ChatConversationRequestDTO(BaseModel):
    message: str
    user_id: str = "guest"
    conversation_history: Optional[List[Dict[str, str]]] = None
