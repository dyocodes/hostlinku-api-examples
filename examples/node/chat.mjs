#!/usr/bin/env node
// POST /v1/chat/completions (OpenAI-compatible). Zero dependencies, Node >= 18.
// Set STREAM=1 to stream (SSE).
const apiKey = process.env.HOSTLINKU_API_KEY;
if (!apiKey) {
  console.error("Set HOSTLINKU_API_KEY (see .env.example)");
  process.exit(1);
}
const base = (process.env.HOSTLINKU_BASE_URL ?? "https://api.hostlinku.com").replace(/\/$/, "");
const model = process.env.HOSTLINKU_MODEL ?? "gpt-5-5";
const stream = process.env.STREAM === "1";

const res = await fetch(`${base}/v1/chat/completions`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiKey}`,
    "User-Agent": "hostlinku-api-examples/0.1.0",
  },
  body: JSON.stringify({
    model,
    stream,
    max_tokens: 256,
    messages: [
      { role: "system", content: "You are a concise assistant." },
      { role: "user", content: "Explain what an API gateway is in two sentences." },
    ],
  }),
});

if (!res.ok) {
  console.error(`HTTP ${res.status}: ${await res.text()}`);
  process.exit(1);
}

if (!stream) {
  const data = await res.json();
  console.log(data.choices[0].message.content);
  console.log("usage:", data.usage, "| hostlinku:", data.hostlinku);
} else {
  const decoder = new TextDecoder();
  let buffer = "";
  for await (const chunk of res.body) {
    buffer += decoder.decode(chunk, { stream: true });
    let index;
    while ((index = buffer.indexOf("\n")) >= 0) {
      const line = buffer.slice(0, index).trim();
      buffer = buffer.slice(index + 1);
      if (!line.startsWith("data:")) continue;
      const data = line.slice(5).trim();
      if (data === "[DONE]") continue;
      const delta = JSON.parse(data).choices?.[0]?.delta?.content;
      if (delta) process.stdout.write(delta);
    }
  }
  process.stdout.write("\n");
}
