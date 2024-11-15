import re
import json
import os

from db.queries import get_client_info, create_chat, store_message
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.models import ChatRequest, Client
from clients.mistral_client import mistral_client

# Initialize FastAPI router
router = APIRouter()

# Initialize the Mistral client
model = "open-mistral-nemo"

def generate_full_response(client_context: str, user_message: str) -> str:
  try:
    messages = [
      {"role": "system", "content": client_context},
      {"role": "user", "content": user_message}
    ]

    # Use the synchronous completion API from Mistral (no streaming)
    response = mistral_client.chat.complete(
      model=model,
      messages=messages
    )

    # Extract the full response text
    full_response = response.choices[0].message.content
    return full_response

  except Exception as e:
    error_message = f"Error during response generation: {str(e)}"
    print(error_message)
    return f"Error: {error_message}"


# Endpoint for chat completion
@router.post("/chat")
async def chat_completion(request: ChatRequest):
  try:
    # Fetch client information using the provided user ID
    client_info = get_client_info(request.user_id)
    if not client_info:
      raise HTTPException(status_code=404, detail="Client not found")

    # Create a new chat entry in the database
    chat_id = create_chat(request.user_id)

    # Store the first user message
    store_message(chat_id, "user", request.message)

    # Build the client context
    client_context = (
      "Eres un bot de negociación financiera. Tu objetivo es lograr una propuesta favorable tanto para el banco como para el cliente.\n"
      f"Información del Cliente:\n"
      f"- Nombre: {client_info.nombre}\n"
      f"- Email: {client_info.email or 'No proporcionado'}\n"
      f"- Celular: {client_info.telefono or 'No proporcionado'}\n"
      f"- Monto de Deuda: ${client_info.monto_deuda or 'No especificado'}\n"
      f"- Fecha de Vencimiento de la Deuda: {client_info.fecha_vencimiento or 'No especificada'}\n"
      f"- Estado de la Cuenta: {client_info.estado_cuenta or 'No especificado'}\n"
      f"- Historial de Pagos: {client_info.historial_pagos or 'No disponible'}\n\n"
    )

    # Generate the full response
    full_response = generate_full_response(client_context, request.message)

    # Store the assistant's response in the database
    store_message(chat_id, "assistant", full_response)

    # Return a JSON object with the chat_id and the full response
    return JSONResponse(content={"chat_id": chat_id, "response": full_response})

  except HTTPException as http_err:
    raise http_err
  except Exception as e:
    print(f"Unexpected error: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")