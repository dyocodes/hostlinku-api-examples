# Hostlinku API examples

[![CI](https://github.com/dyocodes/hostlinku-api-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/dyocodes/hostlinku-api-examples/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**English** | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

Small, runnable examples for calling the [Hostlinku](https://hostlinku.com) AI API from **curl**, **Node.js** and **Python**. One API key and one USD balance work across three protocols:

| Protocol | Endpoint | Typical clients |
|---|---|---|
| OpenAI Chat Completions | `POST /v1/chat/completions` | OpenAI SDKs, LangChain, Cursor, Cline |
| Anthropic Messages | `POST /v1/messages` | Anthropic SDKs, Claude Code |
| OpenAI Responses | `POST /v1/responses` | Codex CLI, OpenAI Agents SDK |

Base URL: `https://api.hostlinku.com`. The curl, Node.js and Python scripts use the standard library only. The official-SDK examples need `pip install -r examples/python/requirements.txt`.

## Quick start

1. Sign in to the [Console](https://console.hostlinku.com), top up your USD balance and create a key under **API Keys**. Pick a Service Mode (**Performance**, **Economy** or **Dedicated**); it decides which models and prices apply to the key.
2. Export the key (never commit it):

   ```bash
   export HOSTLINKU_API_KEY=sk-your-api-key
   ```

3. Run an example:

   ```bash
   bash examples/curl/chat.sh
   node examples/node/messages.mjs
   python examples/python/responses.py
   ```

Add `STREAM=1` to any of them to stream the answer over SSE, for example `STREAM=1 node examples/node/chat.mjs`.

## What is in here

```text
examples/
  curl/    chat.sh  messages.sh  responses.sh
  node/    chat.mjs messages.mjs responses.mjs        (Node.js >= 18, no dependencies)
  python/  chat.py  messages.py  responses.py         (standard library only)
           sdk_openai.py  sdk_anthropic.py            (official SDKs, see requirements.txt)
```

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `HOSTLINKU_API_KEY` | none (required) | Your `sk-…` API key. |
| `HOSTLINKU_BASE_URL` | `https://api.hostlinku.com` | Override only for testing. |
| `HOSTLINKU_MODEL` | `gpt-5-5` (chat, responses), `claude-haiku-4-5` (messages) | Public model slug. |
| `STREAM` | `0` | `1` enables SSE streaming. |

## Good to know

- The models you can call depend on the key's Service Mode. List them with `GET /v1/models`; if a default slug is unavailable for your key, set `HOSTLINKU_MODEL`.
- The default `claude-haiku-4-5` used by the Messages examples is available on Economy keys. On a Performance key, set `HOSTLINKU_MODEL` to a slug from `GET /v1/models` (for example `claude-haiku-5-5`).
- Official SDK base URLs differ: OpenAI SDKs use `https://api.hostlinku.com/v1`, the Anthropic SDK and Claude Code use `https://api.hostlinku.com` (no `/v1`).
- `/v1/responses` is stateless: send the full history in `input`. Reasoning models count thinking tokens toward `max_output_tokens`, so keep it at 256 or more.
- Successful non-streaming responses include a `hostlinku` block with the request cost in USD and latency. The scripts print it when present.
- Errors follow each protocol's envelope; see the [error reference](https://docs.hostlinku.com/en/errors).

## Verified

On 2026-11-18 every script was run against the production API with an Economy key: all 9 curl, Node.js and Python examples, with and without `STREAM=1`, plus both official-SDK examples (`openai` 3.55.0, `anthropic` 2.10.0). Responses and streams completed with HTTP 200 and non-empty output. This is a point-in-time check, not a guarantee; model slugs and availability change.

## Links

- Documentation: <https://docs.hostlinku.com>
- Console (keys, billing, logs): <https://console.hostlinku.com>
- Model catalog and pricing: <https://hostlinku.com>

## License

[MIT](LICENSE). These examples are provided as-is and contain no credentials.
