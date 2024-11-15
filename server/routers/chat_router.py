from fastapi import APIRouter, HTTPException
from models.chat_request import ChatRequest
from services.chat_service import generate_chat_response

router = APIRouter()

@router.post("/chat")
async def chat_completion(request: ChatRequest):
  try:
    response = generate_chat_response(request.message)
    return {"response": response}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
