from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.models import ChatRequest, Client
from clients.mistral_client import mistral_client
import sqlite3
import re
import os

# Initialize FastAPI router
router = APIRouter()

# Initialize the Mistral client
model = "open-mistral-nemo"
DB_PATH = "db/hackaton.db"

# Function to fetch client information from the SQLite database
def get_client_info(user_id: int) -> Client:
  try:
    with sqlite3.connect(DB_PATH) as conn:
      cursor = conn.cursor()

      query = """
        SELECT id, nombre, fecha_nacimiento, cc, telefono, email, monto_deuda,
               fecha_vencimiento, estado_cuenta, historial_pagos
        FROM clientes
        WHERE id = ?
      """
      cursor.execute(query, (user_id,))
      client_data = cursor.fetchone()

      if client_data:
        return Client(
          id=client_data[0],
          nombre=client_data[1],
          fecha_nacimiento=client_data[2],
          cc=client_data[3],
          telefono=client_data[4],
          email=client_data[5],
          monto_deuda=client_data[6],
          fecha_vencimiento=client_data[7],
          estado_cuenta=client_data[8],
          historial_pagos=client_data[9]
        )
      else:
        return None
  except Exception as e:
    print(f"Error fetching client info: {str(e)}")
    raise HTTPException(status_code=500, detail="Error fetching client info")

# Function to create a new chat in the database
def create_chat(user_id: int) -> int:
  try:
    with sqlite3.connect(DB_PATH) as conn:
      cursor = conn.cursor()
      cursor.execute(
        "INSERT INTO chats (id_cliente) VALUES (?)",
        (user_id,)
      )
      chat_id = cursor.lastrowid
      return chat_id
  except Exception as e:
    print(f"Error creating chat: {str(e)}")
    raise HTTPException(status_code=500, detail="Error creating chat")

# Function to store a message in the database
def store_message(chat_id: int, role: str, message: str):
  try:
    with sqlite3.connect(DB_PATH) as conn:
      cursor = conn.cursor()
      cursor.execute(
        "INSERT INTO mensajes (id_chat, enviado_por, mensaje) VALUES (?, ?, ?)",
        (chat_id, role, message)
      )
  except Exception as e:
    print(f"Error storing message: {str(e)}")
    raise HTTPException(status_code=500, detail="Error storing message")

# Async generator function for streaming the model response
async def response_generator(chat_id: int, client_context: str, user_message: str):
  full_response = ""

  try:
    # Prepare the chat completion request
    messages = [
      {"role": "system", "content": client_context},
      {"role": "user", "content": user_message}
    ]

    # Call the Mistral API
    chat_response = mistral_client.chat.complete(
      model=model,
      messages=messages
    )

    # Extract the response content
    mistral_reply = chat_response.choices[0].message.content

    # Split the response into sentences and yield each chunk
    sentences = re.split(r'(?<=[.!?])\s+', mistral_reply)
    for sentence in sentences:
      if sentence.strip():
        chunk = sentence + " "
        full_response += chunk
        yield chunk

    # After streaming is complete, store the full response
    store_message(chat_id, "assistant", full_response)

  except Exception as e:
    error_message = f"Error during response generation: {str(e)}"
    print(error_message)
    yield error_message

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

    # Return the streaming response
    response = StreamingResponse(
      response_generator(chat_id, client_context, request.message),
      media_type="text/plain"
    )
    response.headers["X-Chat-Id"] = str(chat_id)
    return response

  except HTTPException as http_err:
    raise http_err
  except Exception as e:
    print(f"Unexpected error: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")
