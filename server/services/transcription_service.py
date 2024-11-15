from clients.groq_client import groq_client
from fastapi import HTTPException

def transcribe_audio(file_name: str, audio_bytes: bytes) -> str:
  try:
    transcription = groq_client.audio.transcriptions.create(
      file=(file_name, audio_bytes),
      model="whisper-large-v3-turbo",
      response_format="json",
      language="es",
    )
    return transcription.text
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
