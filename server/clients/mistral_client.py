from mistralai import Mistral
from utils.config import MISTRAL_API_KEY


model = "open-mistral-nemo"  
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

