from pydantic import BaseModel
from typing import Optional

# ChatRequest Model
class ChatRequest(BaseModel):
  user_id: int
  message: str

# Client Model (for 'clientes' table)
class Client(BaseModel):
  id: int
  nombre: str
  fecha_nacimiento: str
  cc: str
  telefono: Optional[str] = None
  email: Optional[str] = None
  monto_deuda: Optional[float] = None
  fecha_vencimiento: Optional[str] = None
  estado_cuenta: Optional[str] = None
  historial_pagos: Optional[str] = None

# ChatMessage Model (for Mistral Client)
class ChatMessage(BaseModel):
  id_cliente: int
  role: str
  mensaje: str
