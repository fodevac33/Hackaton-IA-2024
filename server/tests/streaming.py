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

  try:
    response = requests.post(url, json=data, headers=headers, stream=True)

    # Check if the request was successful
    if response.status_code != 200:
      error_message = response.text or response.reason
      yield {"error": f"{response.status_code} - {error_message}"}
      return

    # Log time to first byte (TTFB)
    ttfb = time.time() - start_time
    print(f"Time to First Byte (TTFB): {ttfb:.2f} seconds")

    # Iterate over the streamed content
    first_chunk_received = False
    for chunk in response.iter_lines(decode_unicode=True):
      if chunk:  # Only process non-empty chunks
        if not first_chunk_received:
          first_chunk_received = True
          first_chunk_time = time.time() - start_time
          print(f"Time to First Chunk: {first_chunk_time:.2f} seconds")

        # Decode the chunk as a JSON object
        try:
          json_data = json.loads(chunk)
          yield json_data
        except json.JSONDecodeError as e:
          yield {"error": f"JSON decode error: {str(e)}", "raw_chunk": chunk}

    # Log the completion of the stream
    end_time = time.time() - start_time
    print(f"Stream completed in {end_time:.2f} seconds")

  except requests.exceptions.RequestException as e:
    yield {"error": f"Connection error: {str(e)}"}

# Use the generator function and print each chunk as a separate JSON entry
if __name__ == "__main__":
  for json_entry in stream_response():
    print(json.dumps(json_entry, indent=2, ensure_ascii=False))
