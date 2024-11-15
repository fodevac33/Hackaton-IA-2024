import os
from typing import Union
from fastapi import FastAPI, File, UploadFile, HTTPException
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Retrieve the API key from environment variables
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("API key not found. Please set GROQ_API_KEY in the .env file.")

# Initialize the Groq client with the API key
client = Groq(api_key=api_key)

# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Transcribe audio endpoint
@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename.endswith((".m4a", ".mp3", ".wav")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only audio files are supported.")

    audio_bytes = await file.read()

    try:
        transcription = client.audio.transcriptions.create(
            file=(file.filename, audio_bytes),
            model="whisper-large-v3-turbo",
            prompt="Specify context or spelling",
            response_format="json",
            language="en",
            temperature=0.0
        )
        return {"transcription": transcription.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
