# Contoh API Hostlinku

[![CI](https://github.com/dyocodes/hostlinku-api-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/dyocodes/hostlinku-api-examples/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | **Bahasa Indonesia** | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)

Contoh kecil yang bisa langsung dijalankan untuk memanggil API AI [Hostlinku](https://hostlinku.com) dari **curl**, **Node.js**, dan **Python**. Satu API key dan satu saldo USD berlaku untuk tiga protokol:

| Protokol | Endpoint | Klien umum |
|---|---|---|
| OpenAI Chat Completions | `POST /v1/chat/completions` | SDK OpenAI, LangChain, Cursor, Cline |
| Anthropic Messages | `POST /v1/messages` | SDK Anthropic, Claude Code |
| OpenAI Responses | `POST /v1/responses` | Codex CLI, OpenAI Agents SDK |

Base URL: `https://api.hostlinku.com`. Skrip curl, Node.js, dan Python hanya memakai pustaka standar. Contoh SDK resmi membutuhkan `pip install -r examples/python/requirements.txt`.

## Mulai cepat

1. Masuk ke [Console](https://console.hostlinku.com), isi saldo USD, lalu buat key di **API Keys**. Pilih Service Mode (**Performance**, **Economy**, atau **Dedicated**); mode menentukan model dan harga yang berlaku untuk key tersebut.
2. Ekspor key (jangan pernah di-commit):

   ```bash
   export HOSTLINKU_API_KEY=sk-your-api-key
   ```

3. Jalankan contoh:

   ```bash
   bash examples/curl/chat.sh
   node examples/node/messages.mjs
   python examples/python/responses.py
   ```

Tambahkan `STREAM=1` untuk streaming SSE, misalnya `STREAM=1 node examples/node/chat.mjs`.

## Isi repo

```text
examples/
  curl/    chat.sh  messages.sh  responses.sh
  node/    chat.mjs messages.mjs responses.mjs        (Node.js >= 18, tanpa dependensi)
  python/  chat.py  messages.py  responses.py         (pustaka standar)
           sdk_openai.py  sdk_anthropic.py            (SDK resmi, lihat requirements.txt)
```

## Konfigurasi

| Variabel | Default | Arti |
|---|---|---|
| `HOSTLINKU_API_KEY` | tidak ada (wajib) | API key `sk-…` Anda. |
| `HOSTLINKU_BASE_URL` | `https://api.hostlinku.com` | Ubah hanya untuk pengujian. |
| `HOSTLINKU_MODEL` | `gpt-5-5` (chat, responses), `claude-haiku-4-5` (messages) | Slug model publik. |
| `STREAM` | `0` | `1` mengaktifkan streaming SSE. |

## Perlu diketahui

- Model yang bisa dipanggil bergantung pada Service Mode key. Lihat daftarnya lewat `GET /v1/models`; jika slug default tidak tersedia untuk key Anda, atur `HOSTLINKU_MODEL`.
- Default `claude-haiku-4-5` pada contoh Messages tersedia untuk key Economy. Pada key Performance, atur `HOSTLINKU_MODEL` ke slug dari `GET /v1/models` (misalnya `claude-haiku-5-5`).
- Base URL SDK resmi berbeda: SDK OpenAI memakai `https://api.hostlinku.com/v1`, sedangkan SDK Anthropic dan Claude Code memakai `https://api.hostlinku.com` (tanpa `/v1`).
- `/v1/responses` bersifat stateless: kirim seluruh riwayat di `input`. Model reasoning menghitung token berpikir ke dalam `max_output_tokens`, jadi gunakan 256 atau lebih.
- Respons non-streaming yang sukses memuat blok `hostlinku` berisi biaya request dalam USD dan latensi. Skrip mencetaknya bila ada.
- Format error mengikuti masing-masing protokol; lihat [referensi error](https://docs.hostlinku.com/errors).

## Terverifikasi

Pada 2026-11-18 setiap skrip dijalankan ke API production dengan key Economy: seluruh 9 contoh curl, Node.js, dan Python, dengan dan tanpa `STREAM=1`, ditambah kedua contoh SDK resmi (`openai` 3.55.0, `anthropic` 2.10.0). Respons dan stream selesai dengan HTTP 200 dan keluaran tidak kosong. Ini pengecekan pada satu waktu, bukan jaminan; slug dan ketersediaan model dapat berubah.

## Tautan

- Dokumentasi: <https://docs.hostlinku.com>
- Console (key, billing, log): <https://console.hostlinku.com>
- Katalog model dan harga: <https://hostlinku.com>

## Lisensi

[MIT](LICENSE). Contoh ini disediakan apa adanya dan tidak berisi kredensial.
