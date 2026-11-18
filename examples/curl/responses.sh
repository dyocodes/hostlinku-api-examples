#!/usr/bin/env bash
# POST /v1/responses (OpenAI Responses-compatible, stateless). Set STREAM=1 to stream (SSE).
# Reasoning models count thinking tokens toward max_output_tokens: keep it >= 256.
set -euo pipefail

: "${HOSTLINKU_API_KEY:?Set HOSTLINKU_API_KEY (see .env.example)}"
BASE="${HOSTLINKU_BASE_URL:-https://api.hostlinku.com}"
MODEL="${HOSTLINKU_MODEL:-gpt-5-5}"
STREAM="${STREAM:-0}"

if [ "$STREAM" = "1" ]; then STREAM_JSON=true; else STREAM_JSON=false; fi

curl -sS -N "$BASE/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $HOSTLINKU_API_KEY" \
  -d "{
    \"model\": \"$MODEL\",
    \"stream\": $STREAM_JSON,
    \"max_output_tokens\": 256,
    \"instructions\": \"Answer briefly.\",
    \"input\": \"What is an API gateway?\"
  }"
echo
