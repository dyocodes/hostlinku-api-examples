# Hostlinku API サンプル

[![CI](https://github.com/dyocodes/hostlinku-api-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/dyocodes/hostlinku-api-examples/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | [Bahasa Indonesia](README.id.md) | **日本語** | [简体中文](README.zh-CN.md)

[Hostlinku](https://hostlinku.com) の AI API を **curl**、**Node.js**、**Python** から呼び出す、そのまま実行できる小さなサンプル集です。1 つの API キーと 1 つの USD 残高で、3 つのプロトコルを利用できます。

| プロトコル | エンドポイント | 主なクライアント |
|---|---|---|
| OpenAI Chat Completions | `POST /v1/chat/completions` | OpenAI SDK、LangChain、Cursor、Cline |
| Anthropic Messages | `POST /v1/messages` | Anthropic SDK、Claude Code |
| OpenAI Responses | `POST /v1/responses` | Codex CLI、OpenAI Agents SDK |

ベース URL: `https://api.hostlinku.com`。curl、Node.js、Python のスクリプトは標準ライブラリのみを使用します。公式 SDK のサンプルには `pip install -r examples/python/requirements.txt` が必要です。

## クイックスタート

1. [Console](https://console.hostlinku.com) にサインインし、USD 残高をチャージして、**API Keys** でキーを作成します。Service Mode（**Performance**、**Economy**、**Dedicated**）を選びます。モードによって、そのキーで使えるモデルと料金が決まります。
2. キーを環境変数に設定します（コミットしないでください）。

   ```bash
   export HOSTLINKU_API_KEY=sk-your-api-key
   ```

3. サンプルを実行します。

   ```bash
   bash examples/curl/chat.sh
   node examples/node/messages.mjs
   python examples/python/responses.py
   ```

`STREAM=1` を付けると SSE でストリーミングします。例: `STREAM=1 node examples/node/chat.mjs`

## 構成

```text
examples/
  curl/    chat.sh  messages.sh  responses.sh
  node/    chat.mjs messages.mjs responses.mjs        (Node.js >= 18、依存なし)
  python/  chat.py  messages.py  responses.py         (標準ライブラリのみ)
           sdk_openai.py  sdk_anthropic.py            (公式 SDK、requirements.txt 参照)
```

## 設定

| 変数 | デフォルト | 説明 |
|---|---|---|
| `HOSTLINKU_API_KEY` | なし（必須） | `sk-…` 形式の API キー。 |
| `HOSTLINKU_BASE_URL` | `https://api.hostlinku.com` | テスト時のみ変更してください。 |
| `HOSTLINKU_MODEL` | `gpt-5-5`（chat、responses）、`claude-haiku-4-5`（messages） | 公開モデル slug。 |
| `STREAM` | `0` | `1` で SSE ストリーミングを有効にします。 |

## 注意点

- 呼び出せるモデルはキーの Service Mode によって異なります。`GET /v1/models` で確認でき、デフォルトの slug が使えない場合は `HOSTLINKU_MODEL` を設定してください。
- Messages のサンプルが使うデフォルトの `claude-haiku-4-5` は Economy キーで利用できます。Performance キーでは、`GET /v1/models` の slug（例: `claude-haiku-5-5`）を `HOSTLINKU_MODEL` に設定してください。
- 公式 SDK のベース URL は異なります。OpenAI SDK は `https://api.hostlinku.com/v1`、Anthropic SDK と Claude Code は `https://api.hostlinku.com`（`/v1` なし）です。
- `/v1/responses` はステートレスです。履歴全体を `input` に含めてください。推論モデルは思考トークンも `max_output_tokens` に含めるため、256 以上を指定してください。
- ストリーミングでない成功レスポンスには、リクエストの USD コストとレイテンシを含む `hostlinku` ブロックが付きます。スクリプトは存在する場合に表示します。
- エラーは各プロトコルの形式に従います。詳しくは[エラーリファレンス](https://docs.hostlinku.com/ja/errors)を参照してください。

## 動作確認

2026-11-18 に、すべてのスクリプトを Economy キーで本番 API に対して実行しました。curl、Node.js、Python の 9 個のサンプルすべて（`STREAM=1` あり・なし）と、公式 SDK の 2 つのサンプル（`openai` 3.55.0、`anthropic` 2.10.0）です。レスポンスとストリームは HTTP 200 で完了し、出力は空ではありませんでした。これは特定時点の確認であり保証ではありません。モデルの slug や提供状況は変わることがあります。

## リンク

- ドキュメント: <https://docs.hostlinku.com>
- Console（キー、請求、ログ）: <https://console.hostlinku.com>
- モデルカタログと料金: <https://hostlinku.com>

## ライセンス

[MIT](LICENSE)。このサンプルは現状のまま提供され、認証情報は含まれていません。
