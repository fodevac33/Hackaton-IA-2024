from haystack.dataclasses import ChatMessage
from clients.mistral_client import client

def generate_chat_response(user_message: str) -> str:
  message = ChatMessage.from_user(user_message)
  response = client.run(messages=[message])
  return response['replies'][0].content
