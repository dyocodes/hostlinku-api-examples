#!/usr/bin/env python3
"""POST /v1/messages (Anthropic Messages-compatible). Standard library only.

Set STREAM=1 to stream (SSE).
"""
import json
import os
import sys
import urllib.error
import urllib.request

API_KEY = os.environ.get("HOSTLINKU_API_KEY")
if not API_KEY:
    sys.exit("Set HOSTLINKU_API_KEY (see .env.example)")
BASE = os.environ.get("HOSTLINKU_BASE_URL", "https://api.hostlinku.com").rstrip("/")
MODEL = os.environ.get("HOSTLINKU_MODEL", "claude-haiku-4-5")
STREAM = os.environ.get("STREAM") == "1"

body = {
    "model": MODEL,
    "stream": STREAM,
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "Explain what an API gateway is in two sentences."}],
}
request = urllib.request.Request(
    f"{BASE}/v1/messages",
    data=json.dumps(body).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "User-Agent": "hostlinku-api-examples/0.1.0",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=120) as response:
        if not STREAM:
            data = json.load(response)
            text = next((b["text"] for b in data["content"] if b.get("type") == "text"), "")
            print(text)
            print("usage:", data.get("usage"), "| hostlinku:", data.get("hostlinku"))
        else:
            for raw in response:
                line = raw.decode("utf-8").strip()
                if not line.startswith("data:"):
                    continue
                event = json.loads(line[5:].strip())
                if event.get("type") == "content_block_delta" and event["delta"].get("type") == "text_delta":
                    print(event["delta"]["text"], end="", flush=True)
                elif event.get("type") == "error":
                    sys.exit(f"\nstream error: {event.get('error')}")
            print()
except urllib.error.HTTPError as error:
    sys.exit(f"HTTP {error.code}: {error.read().decode('utf-8', 'replace')}")
