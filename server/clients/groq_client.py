from groq import Groq
from utils.config import GROQ_API_KEY

# Initialize the Groq client
groq_client = Groq(api_key=GROQ_API_KEY)
