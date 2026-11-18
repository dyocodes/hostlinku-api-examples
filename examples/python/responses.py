#!/usr/bin/env python3
"""POST /v1/responses (OpenAI Responses-compatible, stateless). Standard library only.

Set STREAM=1 to stream (SSE).
Reasoning models count thinking tokens toward max_output_tokens: keep it >= 256.
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
MODEL = os.environ.get("HOSTLINKU_MODEL", "gpt-5-5")
STREAM = os.environ.get("STREAM") == "1"

body = {
    "model": MODEL,
    "stream": STREAM,
    "max_output_tokens": 256,
    "instructions": "Answer briefly.",
    "input": "What is an API gateway?",
}
request = urllib.request.Request(
    f"{BASE}/v1/responses",
    data=json.dumps(body).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "hostlinku-api-examples/0.1.0",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=120) as response:
        if not STREAM:
            data = json.load(response)
            message = next((o for o in data["output"] if o.get("type") == "message"), None)
            text = next((p["text"] for p in (message or {}).get("content", []) if p.get("type") == "output_text"), None)
            print(text if text is not None else f"(status: {data.get('status')})")
            print("usage:", data.get("usage"), "| hostlinku:", data.get("hostlinku"))
        else:
            for raw in response:
                line = raw.decode("utf-8").strip()
                if not line.startswith("data:"):
                    continue
                event = json.loads(line[5:].strip())
                if event.get("type") == "response.output_text.delta":
                    print(event["delta"], end="", flush=True)
                elif event.get("type") == "error":
                    sys.exit(f"\nstream error: {event}")
            print()
except urllib.error.HTTPError as error:
    sys.exit(f"HTTP {error.code}: {error.read().decode('utf-8', 'replace')}")
