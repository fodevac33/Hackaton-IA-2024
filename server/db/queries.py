import sqlite3
from models.models import ChatRequest, Client

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
