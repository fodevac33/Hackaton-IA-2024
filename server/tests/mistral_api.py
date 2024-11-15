import requests
import json
import time

# Define the API URL
url = "https://api.mistral.ai/v1/chat/completions"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer Ze9nfYD2dNgN30B1lBLpaj6ugjlOCxsv"  # Replace with your API key
}

# Define the request payload
payload = {
    "model": "open-mistral-nemo",
    "temperature": 0.7,
    "top_p": 1.0,
    "max_tokens": 100,
    "stream": True,  # Set to True for streaming response
    "messages": [
        {
            "role": "user",
            "content": "Quiero negociar mi deuda."
        }
    ],
    "response_format": {
        "type": "text"
    },
    "tool_choice": "auto",
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "n": 1,
    "safe_prompt": False
}

# Make the POST request and measure TTFT
try:
    # Start the timer
    start_time = time.time()

    # Send the POST request with streaming enabled
    response = requests.post(url, headers=headers, json=payload, stream=True)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
    else:
        # Measure TTFB (Time to First Byte)
        ttfb = time.time() - start_time
        print(f"Time to First Byte (TTFB): {ttfb:.2f} seconds")

        # Iterate over the streamed content to measure TTFT
        first_chunk_received = False
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                if not first_chunk_received:
                    first_chunk_received = True
                    ttft = time.time() - start_time
                    print(f"Time to First Token (TTFT): {ttft:.2f} seconds")

                # Print the content of the chunk (decoded)
                print(chunk.decode(), end="")

except Exception as e:
    print(f"An error occurred: {str(e)}")
