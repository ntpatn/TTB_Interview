from typing import List, Dict
import os
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dtos.reschatdto import ChatResponseDTO
from dtos.reqchatdto import ChatRequestDTO
from dtos.reqchatconversationdto import ChatConversationRequestDTO
from models.chatlog import ChatLog
from langfuse import observe

DB_USER = os.getenv("CHATBOT_INTERVIEW_USER", "admin")
DB_PASSWORD = os.getenv("CHATBOT_INTERVIEW_PASSWORD", "admin")
DB_NAME = os.getenv("CHATBOT_INTERVIEW_DB_NAME", "chatbotinterview")
DB_HOST = os.getenv("DB_HOST", "db_chatbot_section_interview")
DB_PORT = os.getenv("DB_PORT", "5432")

con = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(con)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@observe(name="process_chat_interview")
async def process_chat(request: ChatRequestDTO, config: dict) -> ChatResponseDTO:
    OLLAMA_URL = "http://ollama:11434/api/generate"
    full_prompt = f"User: {request.message}:"
    payload = {
        "model": config["model"],
        "prompt": full_prompt,
        "stream": config["stream"],
        "temperature": config["temperature"],
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_URL, json=payload, timeout=60.0)
            response.raise_for_status()

            data = response.json()
            raw_reply = data.get("response", "")
            try:
                with SessionLocal() as db:
                    new_log = ChatLog(
                        id=None,
                        user_message=request.message,
                        ai_response=raw_reply,
                        model_used=config["model"],
                        user_name=request.user_id,
                    )
                    db.add(new_log)
                    db.commit()

                print(f"Saved chat to DB (Model: {config['model']})")

            except Exception as e:
                print(f"Error: {e}")

            return ChatResponseDTO(reply=raw_reply, model_used=config["model"])

        except Exception as e:
            print(f"Error calling Ollama: {e}")
            raise e


@observe(name="process_chat_interview_conversation")
async def process_chat_conversation(
    request: ChatConversationRequestDTO, config: dict
) -> ChatResponseDTO:
    OLLAMA_URL = "http://ollama:11434/api/chat"
    messages = []
    # system prompt
    messages.append(
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Remember the conversation context.",
        }
    )
    # Front conversation history
    if request.conversation_history:
        messages.extend(request.conversation_history)
        print(f"{len(request.conversation_history)} previous messages")

    messages.append({"role": "user", "content": request.message})

    payload = {
        "model": config["model"],
        "messages": messages,
        "stream": config["stream"],
        "options": {"temperature": config["temperature"]},
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_URL, json=payload, timeout=60.0)
            response.raise_for_status()

            data = response.json()
            raw_reply = data.get("message", {}).get("content", "")

            try:
                with SessionLocal() as db:
                    new_log = ChatLog(
                        id=None,
                        user_message=request.message,
                        ai_response=raw_reply,
                        model_used=config["model"],
                        user_name=request.user_id,
                    )
                    db.add(new_log)
                    db.commit()

                print(
                    f"Saved conversation to DB (Model: {config['model']}, History: {len(request.conversation_history or [])} msgs)"
                )

            except Exception as e:
                print(f"Error: {e}")

            return ChatResponseDTO(reply=raw_reply, model_used=config["model"])

        except Exception as e:
            print(f"Error calling Ollama: {e}")
            raise e


@observe(name="get_conversation_history_from_db")
def get_conversation_history(user_id: str, limit: int = 10) -> List[Dict[str, str]]:
    try:
        with SessionLocal() as db:
            logs = (
                db.query(ChatLog)
                .filter(ChatLog.user_name == user_id)
                .order_by(ChatLog.created_at.desc())
                .limit(limit)
                .all()
            )

            messages = []
            for log in reversed(logs):
                messages.append({"role": "user", "content": log.user_message})
                messages.append({"role": "assistant", "content": log.ai_response})

            print(f"{len(messages)} messages from DB for user {user_id}")
            return messages

    except Exception as e:
        print(f"Error getting history: {e}")
        return []
