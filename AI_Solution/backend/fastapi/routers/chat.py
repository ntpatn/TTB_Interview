from fastapi import APIRouter, HTTPException
from dtos.reschatdto import ChatResponseDTO
from dtos.reqchatdto import ChatRequestDTO
from services import service

router = APIRouter()


@router.post("/chat", response_model=ChatResponseDTO, tags=["AI Chat"])
async def chat_endpoint(request: ChatRequestDTO):
    try:
        config = {
            "model": "gemini-3-flash-preview:latest",
            "temperature": 0.7,
            "stream": False,
        }
        result = await service.process_chat(request, config)
        return result

    except Exception as e:
        print(f"Error in router: {e}")
        raise HTTPException(status_code=500, detail=str(e))
