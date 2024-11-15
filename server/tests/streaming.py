import requests
import time
import json

url = "http://localhost:8000/api/chat"
headers = {"Content-Type": "application/json"}
data = {
  "user_id": 1,
  "message": "Quiero negociar mi deuda."
}

def stream_response():
  # Start the timer before sending the request
  start_time = time.time()

  response = requests.post(url, json=data, headers=headers, stream=True)

  # Check if the request was successful
  if response.status_code != 200:
    yield {"error": f"{response.status_code} - {response.reason}"}
    return

  # Extract the Chat ID from the response headers
  chat_id = response.headers.get("X-Chat-Id", None)
  if not chat_id:
    yield {"error": "Missing Chat ID in response headers"}
    return

  # Log time to first byte (TTFB)
  ttfb = time.time() - start_time
  print(f"Time to First Byte (TTFB): {ttfb:.2f} seconds")


  # Iterate over the streamed content
  first_chunk_received = False
  for chunk in response.iter_content(chunk_size=None):
    if chunk:  # Only process non-empty chunks
      if not first_chunk_received:
        first_chunk_received = True
        first_chunk_time = time.time() - start_time
        print(f"Time to First Chunk: {first_chunk_time:.2f} seconds")

      # Decode the chunk and wrap it in a JSON object
      try:
        sentence = chunk.decode().strip()
        if sentence:
          json_chunk = {"chat_id": chat_id, "chunk": sentence}
          yield json.dumps(json_chunk)
      except Exception as e:
        yield json.dumps({"error": str(e)})

  # Log the completion of the stream and return the full response
  end_time = time.time() - start_time
  print(f"Stream completed in {end_time:.2f} seconds")
  yield json.dumps(full_response)

# Use the generator function and print each chunk as a separate JSON entry
for json_entry in stream_response():
  print(json_entry)
