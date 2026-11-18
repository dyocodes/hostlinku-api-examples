#!/usr/bin/env node
// POST /v1/messages (Anthropic Messages-compatible). Zero dependencies, Node >= 18.
// Set STREAM=1 to stream (SSE).
const apiKey = process.env.HOSTLINKU_API_KEY;
if (!apiKey) {
  console.error("Set HOSTLINKU_API_KEY (see .env.example)");
  process.exit(1);
}
const base = (process.env.HOSTLINKU_BASE_URL ?? "https://api.hostlinku.com").replace(/\/$/, "");
const model = process.env.HOSTLINKU_MODEL ?? "claude-haiku-4-5";
const stream = process.env.STREAM === "1";

const res = await fetch(`${base}/v1/messages`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": apiKey,
    "anthropic-version": "2023-06-01",
    "User-Agent": "hostlinku-api-examples/0.1.0",
  },
  body: JSON.stringify({
    model,
    stream,
    max_tokens: 256,
    messages: [{ role: "user", content: "Explain what an API gateway is in two sentences." }],
  }),
});

if (!res.ok) {
  console.error(`HTTP ${res.status}: ${await res.text()}`);
  process.exit(1);
}

if (!stream) {
  const data = await res.json();
  console.log(data.content.find((block) => block.type === "text")?.text);
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
      const event = JSON.parse(line.slice(5).trim());
      if (event.type === "content_block_delta" && event.delta?.type === "text_delta") {
        process.stdout.write(event.delta.text);
      }
      if (event.type === "error") {
        console.error(`\nstream error: ${JSON.stringify(event.error)}`);
        process.exit(1);
      }
    }
  }
  process.stdout.write("\n");
}
