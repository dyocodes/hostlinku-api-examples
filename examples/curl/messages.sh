#!/usr/bin/env bash
# POST /v1/messages (Anthropic Messages-compatible). Set STREAM=1 to stream (SSE).
set -euo pipefail

: "${HOSTLINKU_API_KEY:?Set HOSTLINKU_API_KEY (see .env.example)}"
BASE="${HOSTLINKU_BASE_URL:-https://api.hostlinku.com}"
MODEL="${HOSTLINKU_MODEL:-claude-haiku-4-5}"
STREAM="${STREAM:-0}"

if [ "$STREAM" = "1" ]; then STREAM_JSON=true; else STREAM_JSON=false; fi

curl -sS -N "$BASE/v1/messages" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $HOSTLINKU_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d "{
    \"model\": \"$MODEL\",
    \"stream\": $STREAM_JSON,
    \"max_tokens\": 256,
    \"messages\": [
      {\"role\": \"user\", \"content\": \"Explain what an API gateway is in two sentences.\"}
    ]
  }"
echo
