from fastapi import APIRouter, HTTPException
from haystack.dataclasses import ChatMessage
from models.chat_request import ChatRequest
from clients.mistral_client import mistral_client

router = APIRouter()

@router.post("/chat")
async def chat_completion(request: ChatRequest):
  try:
    # Create a chat message from the user's input
    message = ChatMessage.from_user(request.message)

    # Generate a response using the Mistral client
    mistral_response = mistral_client.run(messages=[message])
    mistral_reply = mistral_response['replies'][0].content

    # Return the Mistral reply directly
    return {"response": mistral_reply}

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
