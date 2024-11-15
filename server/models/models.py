from pydantic import BaseModel, Field, constr
from typing import Optional, Literal
from datetime import datetime

# Client Model (for 'clientes' table)
class Client(BaseModel):
  id: int
  nombre: str
  fecha_nacimiento: str  # YYYY-MM-DD format
  cc: str
  telefono: Optional[str] = None
  email: Optional[str] = None
  monto_deuda: Optional[float] = None
  fecha_vencimiento: Optional[str] = None  # YYYY-MM-DD format
  estado_cuenta: Optional[Literal['Pendiente', 'En mora', 'Pagada']] = None
  historial_pagos: Optional[str] = None

# Chat Model (for 'chats' table)
class Chat(BaseModel):
  id: int
  id_cliente: int
  fecha_inicio: Optional[datetime] = Field(default_factory=datetime.utcnow)
  fecha_fin: Optional[datetime] = None

# Message Model (for 'mensajes' table)
class Message(BaseModel):
  id: int
  id_chat: int
  enviado_por: Literal['user', 'assistant']
  mensaje: str
  timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

# ChatRequest Model (for API request input)
class ChatRequest(BaseModel):
  user_id: int
  message: str

# ChatMessage Model (for response or interaction representation)
class ChatMessage(BaseModel):
  id_cliente: int
  role: Literal['user', 'assistant']
  mensaje: str
  timestamp: Optional[str] = None
