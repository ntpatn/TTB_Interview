from fastapi import APIRouter, HTTPException
from dtos.reschatdto import ChatResponseDTO
from dtos.reqchatdto import ChatRequestDTO
from dtos.reqchatconversationdto import ChatConversationRequestDTO
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


@router.post(
    "/chat/conversation", response_model=ChatResponseDTO, tags=["AI Chat Conversation"]
)
async def chat_endpoint_conversation(request: ChatConversationRequestDTO):
    try:
        config = {
            "model": "gemini-3-flash-preview:latest",
            "temperature": 0.7,
            "stream": False,
        }
        result = await service.process_chat_conversation(request, config)
        return result

    except Exception as e:
        print(f"Error in router: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/chat/conversation/auto",
    response_model=ChatResponseDTO,
    tags=["AI Chat Conversation"],
)
async def chat_conversation_auto(request: ChatRequestDTO):
    try:
        conversation_history = service.get_conversation_history(
            user_id=request.user_id, limit=10
        )
        conversation_request = ChatConversationRequestDTO(
            message=request.message,
            user_id=request.user_id,
            conversation_history=conversation_history,
        )
        config = {
            "model": "gemini-3-flash-preview:latest",
            "temperature": 0.7,
            "stream": False,
        }

        result = await service.process_chat_conversation(conversation_request, config)
        return result

    except Exception as e:
        print(f"Error in router: {e}")
        raise HTTPException(status_code=500, detail=str(e))
