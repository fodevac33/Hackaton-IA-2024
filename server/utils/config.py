import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not GROQ_API_KEY:
  raise RuntimeError("API key not found. Please set GROQ_API_KEY in the .env file.")

if not MISTRAL_API_KEY:
  raise RuntimeError("API key not found. Please set MISTRAL_API_KEY in the .env file.")
