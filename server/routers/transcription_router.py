from fastapi import APIRouter, File, UploadFile, HTTPException
from clients.groq_client import groq_client

router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
  if not file.filename.endswith((".m4a", ".mp3", ".wav")):
    raise HTTPException(status_code=400, detail="Invalid file type. Only audio files are supported.")

  audio_bytes = await file.read()

  try:
    transcription = groq_client.audio.transcriptions.create(
      file=(file.filename, audio_bytes),
      model="whisper-large-v3-turbo",
      language="es",
    )
    return {"transcription": transcription.text}

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
