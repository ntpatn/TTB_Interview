from fastapi import APIRouter, HTTPException
from services import service_rag
from dtos.reschatdto import ChatResponseDTO
from dtos.reqchatdto import ChatRequestDTO

router = APIRouter()


@router.post("/chat/rag", response_model=ChatResponseDTO, tags=["RAG Chat"])
async def chat_with_rag(request: ChatRequestDTO):
    try:
        config = {
            "model": "gemini-3-flash-preview:latest",
            "temperature": 0.7,
            "stream": False,
        }
        result = await service_rag.process_chat(request, config)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
