#!/usr/bin/env node
// POST /v1/responses (OpenAI Responses-compatible, stateless). Zero dependencies, Node >= 18.
// Set STREAM=1 to stream (SSE).
// Reasoning models count thinking tokens toward max_output_tokens: keep it >= 256.
const apiKey = process.env.HOSTLINKU_API_KEY;
if (!apiKey) {
  console.error("Set HOSTLINKU_API_KEY (see .env.example)");
  process.exit(1);
}
const base = (process.env.HOSTLINKU_BASE_URL ?? "https://api.hostlinku.com").replace(/\/$/, "");
const model = process.env.HOSTLINKU_MODEL ?? "gpt-5-5";
const stream = process.env.STREAM === "1";

const res = await fetch(`${base}/v1/responses`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiKey}`,
    "User-Agent": "hostlinku-api-examples/0.1.0",
  },
  body: JSON.stringify({
    model,
    stream,
    max_output_tokens: 256,
    instructions: "Answer briefly.",
    input: "What is an API gateway?",
  }),
});

if (!res.ok) {
  console.error(`HTTP ${res.status}: ${await res.text()}`);
  process.exit(1);
}

if (!stream) {
  const data = await res.json();
  const message = data.output.find((item) => item.type === "message");
  console.log(message?.content?.find((part) => part.type === "output_text")?.text ?? `(status: ${data.status})`);
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
      if (event.type === "response.output_text.delta") process.stdout.write(event.delta);
      if (event.type === "error") {
        console.error(`\nstream error: ${JSON.stringify(event)}`);
        process.exit(1);
      }
    }
  }
  process.stdout.write("\n");
}
