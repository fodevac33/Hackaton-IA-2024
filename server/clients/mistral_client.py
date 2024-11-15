from haystack_integrations.components.generators.mistral import MistralChatGenerator
from utils.config import MISTRAL_API_KEY

model = "open-mistral-nemo"  # Specify your desired model
client = MistralChatGenerator(model=model)
