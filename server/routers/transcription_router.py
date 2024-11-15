from fastapi import APIRouter, File, UploadFile, HTTPException
from services.transcription_service import transcribe_audio

router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
  if not file.filename.endswith((".m4a", ".mp3", ".wav")):
    raise HTTPException(status_code=400, detail="Invalid file type. Only audio files are supported.")

  audio_bytes = await file.read()
  transcription = transcribe_audio(file.filename, audio_bytes)
  return {"transcription": transcription}
