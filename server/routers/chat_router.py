import re
import json
import os

from db.queries import (
  get_client_info,
  create_chat,
  store_message,
  get_chat_by_id,
  get_chat_messages,
)
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.models import ChatRequest, Client
from clients.mistral_client import mistral_client

# Initialize FastAPI router
router = APIRouter()

# Initialize the Mistral client
model = "open-mistral-nemo"

def generate_full_response_from_messages(messages: list) -> str:
  try:
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

    # Build the client context
    client_context = (
      "Eres un bot de negociación financiera. Tu objetivo es lograr una propuesta favorable tanto para el banco como para el cliente. Se consico en tus respuestas\n"
      f"Información del Cliente:\n"
      f"- Nombre: {client_info.nombre}\n"
      f"- Email: {client_info.email or 'No proporcionado'}\n"
      f"- Celular: {client_info.telefono or 'No proporcionado'}\n"
      f"- Monto de Deuda: ${client_info.monto_deuda or 'No especificado'}\n"
      f"- Fecha de Vencimiento de la Deuda: {client_info.fecha_vencimiento or 'No especificada'}\n"
      f"- Estado de la Cuenta: {client_info.estado_cuenta or 'No especificado'}\n"
      f"- Historial de Pagos: {client_info.historial_pagos or 'No disponible'}\n\n"
    )

    # If chat_id is provided, continue the conversation
    if request.chat_id:
      chat_id = request.chat_id

      # Verify that the chat exists and belongs to the user
      chat = get_chat_by_id(chat_id)
      if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
      if chat.id_cliente != request.user_id:
        raise HTTPException(status_code=403, detail="Chat does not belong to the user")

      # Fetch previous messages
      previous_messages = get_chat_messages(chat_id)

      # Build messages array for the model
      messages = [{"role": "system", "content": client_context}]
      messages.extend(previous_messages)

      # Append the new user message
      messages.append({"role": "user", "content": request.message})

      # Store the user's message
      store_message(chat_id, "user", request.message)

    else:
      # Create a new chat entry in the database
      chat_id = create_chat(request.user_id)

      # Build messages array starting with system message and user's message
      messages = [
        {"role": "system", "content": client_context},
        {"role": "user", "content": request.message}
      ]

      # Store the user's message
      store_message(chat_id, "user", request.message)

    # Generate the full response
    full_response = generate_full_response_from_messages(messages)

    # Store the assistant's response in the database
    store_message(chat_id, "assistant", full_response)

    # Return a JSON object with the chat_id and the full response
    return JSONResponse(content={"chat_id": chat_id, "response": full_response})

  except HTTPException as http_err:
    raise http_err
  except Exception as e:
    print(f"Unexpected error: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")
