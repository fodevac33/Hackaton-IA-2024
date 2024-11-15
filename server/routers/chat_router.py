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

# Database connection path
DB_PATH = "db/hackaton.db"

# Function to fetch client information from the SQLite database
def get_client_info(user_id: int) -> Client:
  try:
    # Corrected use of `with` statement for connection and cursor
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
    return None

# Generator function for streaming responses
async def generate_response(client_context: str, user_message: str):
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

    # Split the response into sentences
    sentences = re.split(r'(?<=[.!?])\s+', mistral_reply)

    # Yield each sentence as a separate chunk
    for sentence in sentences:
      if sentence.strip():
        yield sentence + " "

  except Exception as e:
    yield f"Error: {str(e)}"

# Endpoint for chat completion
@router.post("/chat")
async def chat_completion(request: ChatRequest):
  try:
    # Fetch client information using the provided user ID
    client_info = get_client_info(request.user_id)

    if not client_info:
      raise HTTPException(status_code=404, detail="Client not found")

    # Build the static client context with checks for optional fields
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

    # Return streaming response
    return StreamingResponse(generate_response(client_context, request.message), media_type="text/plain")

  except HTTPException as http_err:
    raise http_err
  except Exception as e:
    print(f"Unexpected error: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")
