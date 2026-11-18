# Changelog

## 0.1.0 - 2026-11-18

- Initial release.
- curl, Node.js (>= 18, no dependencies) and Python (standard library) examples for
  `POST /v1/chat/completions`, `POST /v1/messages` and `POST /v1/responses`, each with
  optional SSE streaming (`STREAM=1`).
- Python examples using the official OpenAI and Anthropic SDKs.
- CI that checks syntax only (no API calls, no secrets).
