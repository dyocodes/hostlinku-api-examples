#!/usr/bin/env python3
"""POST /v1/chat/completions (OpenAI-compatible). Standard library only.

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
MODEL = os.environ.get("HOSTLINKU_MODEL", "gpt-5-5")
STREAM = os.environ.get("STREAM") == "1"

body = {
    "model": MODEL,
    "stream": STREAM,
    "max_tokens": 256,
    "messages": [
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "Explain what an API gateway is in two sentences."},
    ],
}
request = urllib.request.Request(
    f"{BASE}/v1/chat/completions",
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
            print(data["choices"][0]["message"]["content"])
            print("usage:", data.get("usage"), "| hostlinku:", data.get("hostlinku"))
        else:
            for raw in response:
                line = raw.decode("utf-8").strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload == "[DONE]":
                    break
                choices = json.loads(payload).get("choices") or []
                delta = choices[0].get("delta", {}).get("content") if choices else None
                if delta:
                    print(delta, end="", flush=True)
            print()
except urllib.error.HTTPError as error:
    sys.exit(f"HTTP {error.code}: {error.read().decode('utf-8', 'replace')}")
