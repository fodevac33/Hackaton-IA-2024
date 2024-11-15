from fastapi import APIRouter, HTTPException
from models.models import ChatRequest, Client, ChatMessage
from clients.mistral_client import mistral_client
from haystack.dataclasses import ChatMessage as MistralChatMessage
from haystack_integrations.components.generators.mistral import MistralChatGenerator
import sqlite3

router = APIRouter()

# Initialize the Mistral client
client = MistralChatGenerator(model="mistral-medium")

# Function to fetch client information from the SQLite database
def get_client_info(user_id: int) -> Client:
  try:
    conn = sqlite3.connect("db/hackaton.db")
    cursor = conn.cursor()

    query = """
      SELECT id, nombre, fecha_nacimiento, cc, telefono, email, monto_deuda,
             fecha_vencimiento, estado_cuenta, historial_pagos
      FROM clientes
      WHERE id = ?
    """
    cursor.execute(query, (user_id,))
    client_data = cursor.fetchone()
    conn.close()

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

@router.post("/chat")
async def chat_completion(request: ChatRequest):
  try:
    client_info = get_client_info(request.user_id)

    if not client_info:
      raise HTTPException(status_code=404, detail="Client not found")

    client_context = (
      "Eres un bot de negociación financiera. Tu objetivo es lograr una propuesta favorable tanto para el banco como para el cliente.\n"
      f"Información del Cliente:\n"
      f"- Nombre: {client_info.nombre}\n"
      f"- Email: {client_info.email}\n"
      f"- Celular: {client_info.telefono}\n"
      f"- Monto de Deuda: ${client_info.monto_deuda}\n"
      f"- Fecha de Vencimiento de la Deuda: {client_info.fecha_vencimiento}\n"
      f"- Estado de la Cuenta: {client_info.estado_cuenta}\n"
      f"- Historial de Pagos: {client_info.historial_pagos}\n\n"
    )

    full_message = f"{client_context}Mensaje del Cliente: {request.message}"

    # Use Mistral's ChatMessage factory method
    chat_message = MistralChatMessage.from_user(full_message)

    mistral_response = client.run(messages=[chat_message])
    mistral_reply = mistral_response['replies'][0].content

    return {"response": mistral_reply}

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
