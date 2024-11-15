from haystack_integrations.components.generators.mistral import MistralChatGenerator
from utils.config import MISTRAL_API_KEY

model = "open-mistral-nemo"  
mistral_client = MistralChatGenerator(model=model)
