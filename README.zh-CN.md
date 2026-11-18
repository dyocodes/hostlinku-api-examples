# Hostlinku API 示例

[![CI](https://github.com/dyocodes/hostlinku-api-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/dyocodes/hostlinku-api-examples/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | [Bahasa Indonesia](README.id.md) | [日本語](README.ja.md) | **简体中文**

这是一组可直接运行的小示例，用 **curl**、**Node.js** 和 **Python** 调用 [Hostlinku](https://hostlinku.com) 的 AI API。一个 API Key 和一份 USD 余额即可使用三种协议：

| 协议 | 端点 | 常见客户端 |
|---|---|---|
| OpenAI Chat Completions | `POST /v1/chat/completions` | OpenAI SDK、LangChain、Cursor、Cline |
| Anthropic Messages | `POST /v1/messages` | Anthropic SDK、Claude Code |
| OpenAI Responses | `POST /v1/responses` | Codex CLI、OpenAI Agents SDK |

Base URL：`https://api.hostlinku.com`。curl、Node.js 和 Python 脚本只使用标准库。官方 SDK 示例需要先执行 `pip install -r examples/python/requirements.txt`。

## 快速开始

1. 登录 [Console](https://console.hostlinku.com)，充值 USD 余额，并在 **API Keys** 中创建密钥。选择 Service Mode（**Performance**、**Economy** 或 **Dedicated**），模式决定该密钥可用的模型和价格。
2. 导出密钥（切勿提交到仓库）：

   ```bash
   export HOSTLINKU_API_KEY=sk-your-api-key
   ```

3. 运行示例：

   ```bash
   bash examples/curl/chat.sh
   node examples/node/messages.mjs
   python examples/python/responses.py
   ```

在命令前加上 `STREAM=1` 即可通过 SSE 流式输出，例如 `STREAM=1 node examples/node/chat.mjs`。

## 目录结构

```text
examples/
  curl/    chat.sh  messages.sh  responses.sh
  node/    chat.mjs messages.mjs responses.mjs        (Node.js >= 18，无依赖)
  python/  chat.py  messages.py  responses.py         (仅标准库)
           sdk_openai.py  sdk_anthropic.py            (官方 SDK，见 requirements.txt)
```

## 配置

| 变量 | 默认值 | 说明 |
|---|---|---|
| `HOSTLINKU_API_KEY` | 无（必填） | 你的 `sk-…` API Key。 |
| `HOSTLINKU_BASE_URL` | `https://api.hostlinku.com` | 仅在测试时修改。 |
| `HOSTLINKU_MODEL` | `gpt-5-5`（chat、responses），`claude-haiku-4-5`（messages） | 公开模型 slug。 |
| `STREAM` | `0` | 设为 `1` 启用 SSE 流式输出。 |

## 注意事项

- 可调用的模型取决于密钥的 Service Mode。可用 `GET /v1/models` 查看；如果默认 slug 对你的密钥不可用，请设置 `HOSTLINKU_MODEL`。
- Messages 示例默认使用的 `claude-haiku-4-5` 在 Economy 密钥下可用。使用 Performance 密钥时，请把 `HOSTLINKU_MODEL` 设置为 `GET /v1/models` 中的 slug（例如 `claude-haiku-5-5`）。
- 官方 SDK 的 Base URL 不同：OpenAI SDK 使用 `https://api.hostlinku.com/v1`，Anthropic SDK 和 Claude Code 使用 `https://api.hostlinku.com`（不带 `/v1`）。
- `/v1/responses` 是无状态的：请在 `input` 中发送完整历史。推理模型会把思考 token 计入 `max_output_tokens`，因此请设置为 256 或更大。
- 非流式的成功响应包含 `hostlinku` 块，内含该请求以 USD 计的费用和延迟；脚本在存在时会打印它。
- 错误格式遵循各协议自身的规范，详见[错误参考](https://docs.hostlinku.com/zh/errors)。

## 已验证

2026-11-18，所有脚本都已使用 Economy 密钥在生产 API 上运行：全部 9 个 curl、Node.js 和 Python 示例（含与不含 `STREAM=1`），以及两个官方 SDK 示例（`openai` 3.55.0、`anthropic` 2.10.0）。响应和流式输出均以 HTTP 200 完成，且输出不为空。这只是某一时间点的检查，并非保证；模型 slug 和可用性可能变化。

## 链接

- 文档：<https://docs.hostlinku.com>
- Console（密钥、账单、日志）：<https://console.hostlinku.com>
- 模型目录与价格：<https://hostlinku.com>

## 许可证

[MIT](LICENSE)。示例按现状提供，不包含任何凭据。
