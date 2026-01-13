import json
import csv
import httpx
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dtos.reschatdto import ChatResponseDTO
from dtos.reqchatdto import ChatRequestDTO
from models.chatlog import ChatLog
from langfuse import observe
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = os.getenv("CHATBOT_INTERVIEW_USER", "admin")
DB_PASSWORD = os.getenv("CHATBOT_INTERVIEW_PASSWORD", "admin")
DB_NAME = os.getenv("CHATBOT_INTERVIEW_DB_NAME", "chatbotinterview")
DB_HOST = os.getenv("DB_HOST", "db_chatbot_section_interview")
DB_PORT = os.getenv("DB_PORT", "5432")

con = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(con)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
OLLAMA_URL = "http://ollama:11434/api/generate"


def load_embeddings_from_csv(
    csv_file: str = "data/news_features_202601131130.csv",
) -> List[Dict]:
    embeddings = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        for idx, row in enumerate(reader):
            text_content = row[0]
            emb_str = row[1].strip('"')
            emb_list = json.loads(emb_str)

            embeddings.append(
                {
                    "embedding": np.array(emb_list),
                    "index": idx,
                    "content": text_content,
                }
            )
    return embeddings


def search_similar(query: str, top_k: int = 3) -> List[Dict]:
    EMBEDDINGS = load_embeddings_from_csv()
    q_emb = embedder.encode(query)
    similarities = []
    for item in EMBEDDINGS:
        similarity = cosine_similarity([q_emb], [item["embedding"]])[0][0]

        similarities.append(
            {
                "index": item["index"],
                "score": float(similarity),
                "content": item["content"],
            }
        )

    similarities.sort(key=lambda x: x["score"], reverse=True)
    for i, r in enumerate(similarities[:top_k], 1):
        print(f"  {i}. Doc #{r['index']}: score={r['score']:.4f}")
    return similarities[:top_k]


@observe(name="process_chat_with_rag")
async def process_chat(request: ChatRequestDTO, config: dict) -> ChatResponseDTO:
    results = search_similar(request.message, top_k=3)
    context_parts = []
    for i, result in enumerate(results, 1):
        context_parts.append(
            f"[Document {i}] (Similarity: {result['score']:.4f})\n{result['content']}"
        )

    context = "\n\n".join(context_parts)
    prompt = f"""
            ตอบคำถามโดยอ้างอิงจากข้อมูลข่าวที่ให้มา
            {context}
            คำถาม: {request.message}
            คำตอบ:
            """
    payload = {
        "model": config["model"],
        "prompt": prompt,
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
                print(f"Database error: {e}")

            return ChatResponseDTO(reply=raw_reply, model_used=config["model"])

        except Exception as e:
            print(f"Error calling Ollama: {e}")
            raise e
