# backend/api/chatbot.py

from fastapi import APIRouter, HTTPException
from services.gemini_service import ask_gemini

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/ask")
def ask_chatbot(payload: dict):
    question = payload.get("question")
    context = payload.get("context")

    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    if not context:
        raise HTTPException(status_code=400, detail="Context is required")

    answer = ask_gemini(question, context)

    return {
        "answer": answer
    }
