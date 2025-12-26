import os
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dtos.reschatdto import ChatResponseDTO
from dtos.reqchatdto import ChatRequestDTO
from models.chatlog import ChatLog

DB_USER = os.getenv("CHATBOT_INTERVIEW_USER", "admin")
DB_PASSWORD = os.getenv("CHATBOT_INTERVIEW_PASSWORD", "admin")
DB_NAME = os.getenv("CHATBOT_INTERVIEW_DB_NAME", "chatbotinterview")
DB_HOST = os.getenv("DB_HOST", "db_chatbot_section_interview")
DB_PORT = os.getenv("DB_PORT", "5432")

con = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(con)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

OLLAMA_URL = "http://ollama:11434/api/generate"


async def process_chat(request: ChatRequestDTO, config: dict) -> ChatResponseDTO:
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
                    from sqlalchemy.dialects.postgresql import UUID

                    new_log = ChatLog(
                        id=None,
                        user_message=request.message,
                        ai_response=raw_reply,
                        model_used=config["model"],
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
