import re
from fastapi import APIRouter, HTTPException
from models.models import SentimentRequest, SentimentResponse
from db.queries import get_chat_by_id, get_chat_messages
from clients.mistral_client import mistral_client

# Initialize FastAPI router
router = APIRouter()

# Initialize the Mistral client with the sentiment analysis model
sentiment_model = "mistral-large-latest"  # Replace with the actual model name

def generate_sentiment_analysis(messages: list) -> str:
  try:
    response = mistral_client.chat.complete(
      model=sentiment_model,
      messages=messages
    )
    full_response = response.choices[0].message.content
    return full_response
  except Exception as e:
    error_message = f"Error during sentiment analysis: {str(e)}"
    print(error_message)
    raise HTTPException(status_code=500, detail=error_message)

# Endpoint for sentiment analysis
@router.post("/sentiment")
async def sentiment_analysis(request: SentimentRequest):
  try:
    chat_id = request.chat_id

    # Verify that the chat exists
    chat = get_chat_by_id(chat_id)
    if not chat:
      raise HTTPException(status_code=404, detail="Chat not found")

    # Fetch messages from the chat
    messages_data = get_chat_messages(chat_id)
    if not messages_data:
      raise HTTPException(status_code=404, detail="No messages found in chat")

    # Prepare the conversation text
    conversation_text = ""
    for msg in messages_data:
      role = msg["role"]
      content = msg["content"]
      conversation_text += f"{role.capitalize()}: {content}\n"

    # Craft the prompt
    prompt = (
      "Por favor, analiza el sentimiento de la siguiente conversación entre un usuario y un asistente. "
      "Califica el sentimiento general de la conversación en una escala de 0 (extremadamente negativo) a 100 (extremadamente positivo). "
      "Proporciona la calificación y una breve justificación para tu evaluación.\n\n"
      "Conversación:\n"
      f"{conversation_text}\n"
      "Proporciona tu respuesta en el siguiente formato, ningun cambio sobre este formato es permitido:\n"
      "Calificación: [0-100]\n"
      "Justificación: [Tu justificación aquí]"
    )

    # Prepare messages for the model
    messages = [
      {"role": "system", "content": "Eres un asistente de IA especializado en análisis de sentimiento."},
      {"role": "user", "content": prompt}
    ]

    # Generate sentiment analysis
    analysis_response = generate_sentiment_analysis(messages)

    # Parse the response to extract rating and justification
    rating_match = re.search(r"Calificación:\s*(\d+)", analysis_response)
    justification_match = re.search(r"Justificación:\s*(.*)", analysis_response, re.DOTALL)

    if rating_match and justification_match:
      rating = int(rating_match.group(1))
      justification = justification_match.group(1).strip()
    else:
      raise HTTPException(status_code=500, detail="Error parsing sentiment analysis response")

    # Validate rating range
    if not 0 <= rating <= 100:
      raise HTTPException(status_code=400, detail="Rating must be between 0 and 100")

    # Return the rating and justification
    return SentimentResponse(rating=rating, justification=justification)

  except HTTPException as http_err:
    raise http_err
  except Exception as e:
    print(f"Unexpected error: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")
