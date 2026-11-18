"""Official OpenAI Python SDK pointed at Hostlinku: only base_url and api_key change.

pip install -r requirements.txt
"""
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.environ.get("HOSTLINKU_BASE_URL", "https://api.hostlinku.com").rstrip("/") + "/v1",
    api_key=os.environ["HOSTLINKU_API_KEY"],
)
model = os.environ.get("HOSTLINKU_MODEL", "gpt-5-5")

# Chat Completions
completion = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Explain what an API gateway is in two sentences."}],
    max_tokens=256,
)
print(completion.choices[0].message.content)

# Chat Completions, streaming
stream = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Count from 1 to 5."}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content if chunk.choices else None
    if delta:
        print(delta, end="", flush=True)
print()

# Responses API (stateless: always send the full history in `input`)
response = client.responses.create(
    model=model,
    instructions="Answer briefly.",
    input="What is an API gateway?",
    max_output_tokens=256,
)
print(response.output_text)
