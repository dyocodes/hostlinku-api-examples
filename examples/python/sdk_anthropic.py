"""Official Anthropic Python SDK pointed at Hostlinku.

Note: the Anthropic SDK base_url has NO /v1 suffix (the SDK appends /v1/messages itself).

pip install -r requirements.txt
"""
import os

import anthropic

client = anthropic.Anthropic(
    base_url=os.environ.get("HOSTLINKU_BASE_URL", "https://api.hostlinku.com").rstrip("/"),
    api_key=os.environ["HOSTLINKU_API_KEY"],
)
model = os.environ.get("HOSTLINKU_MODEL", "claude-haiku-4-5")

message = client.messages.create(
    model=model,
    max_tokens=256,
    messages=[{"role": "user", "content": "Explain what an API gateway is in two sentences."}],
)
print(message.content[0].text)
print(message.usage.input_tokens, message.usage.output_tokens)

with client.messages.stream(
    model=model,
    max_tokens=256,
    messages=[{"role": "user", "content": "Count from 1 to 5."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print()
