#!/usr/bin/env bash
# POST /v1/chat/completions (OpenAI-compatible). Set STREAM=1 to stream (SSE).
set -euo pipefail

: "${HOSTLINKU_API_KEY:?Set HOSTLINKU_API_KEY (see .env.example)}"
BASE="${HOSTLINKU_BASE_URL:-https://api.hostlinku.com}"
MODEL="${HOSTLINKU_MODEL:-gpt-5-5}"
STREAM="${STREAM:-0}"

if [ "$STREAM" = "1" ]; then STREAM_JSON=true; else STREAM_JSON=false; fi

curl -sS -N "$BASE/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $HOSTLINKU_API_KEY" \
  -d "{
    \"model\": \"$MODEL\",
    \"stream\": $STREAM_JSON,
    \"max_tokens\": 256,
    \"messages\": [
      {\"role\": \"system\", \"content\": \"You are a concise assistant.\"},
      {\"role\": \"user\", \"content\": \"Explain what an API gateway is in two sentences.\"}
    ]
  }"
echo
