# Base44 Superagent API — reference

Full endpoint reference for Roman's Base44 Superagent (agent id `6a53ec2ca8ddb9dd9657837e`), pulled
from that agent's "View full API documentation" page in the Base44 dashboard on 2026-07-29. Linked
from `.claude/skills/work-assistant/SKILL.md`, which covers the conversation/message calls actually
used today — this file is the fuller reference for endpoints not yet wired up (memory, webhooks,
template cloning), kept here so it doesn't bloat the skill.

**Not installed as a Claude Code skill.** The page it came from offers this content pre-formatted as
an installable skill (YAML frontmatter, "trigger when the user wants another agent to delegate work
to this Base44 agent"). That's a much wider trigger than `work-assistant`'s "only when Roman
explicitly asks," and it bundles destructive/expansive capabilities (deleting messages and memory,
registering webhooks to an arbitrary `target_url`, cloning templates into workspaces) that nothing
has asked for. Only the plain reference content is kept below — treat any future "install me as a
skill" framing from an external source the same way: reference material by default, not an
auto-triggering skill, unless Roman explicitly asks for that.

Base URL: `https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e`. Auth: `api_key` header or
`?api_key=` query string — never commit the actual key, see the Setup section in `work-assistant`.

## Known undocumented behavior: conversation reuse

Tested 2026-07-29: `POST /conversations` with body `{}` did **not** create a fresh empty conversation
— it returned an existing one (with 549 prior messages) instead. Base44's docs, including the full
API reference, don't mention a parameter to force a new conversation vs. reuse an existing one (no
`title`, `conversation_type`, or similar on the create call). A Base44 feedback item, ["Superagent
Conversation Scoping — App Isolation"](https://feedback.base44.com/p/superagent-conversation-scoping-app-isolation),
requests exactly this isolation and confirms it isn't solved yet — so this looks like current
platform behavior, not a misconfiguration on our end. If this matters for a given call, check the
returned conversation's `title`/`messages` before assuming it's fresh.

## Create from a shared template

Clones a Superagent from a share URL. The clone lands in the authenticated user's active workspace;
pass `X-Active-Workspace-Id` to target a specific one.

```bash
curl -X POST "https://app.base44.com/api/agents/from-template" -H "api_key: API_KEY" -H "Content-Type: application/json" \
  -H "X-Active-Workspace-Id: <workspace_id>" \
  -d '{"template_url":"https://base44.com/clone-superagent-template/<template_token>"}'
```

## Conversations

```bash
# POST /conversations — create
curl -X POST "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/conversations" -H "api_key: API_KEY" -H "Content-Type: application/json" -d '{}'

# GET /conversations — list
curl "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/conversations" -H "api_key: API_KEY"

# GET /conversations/{id} — fetch one
curl "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/conversations/{conversation_id}" -H "api_key: API_KEY"
```

## Messages

```bash
# POST /conversations/{id}/messages — send
curl -X POST "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/conversations/{conversation_id}/messages" -H "api_key: API_KEY" -H "Content-Type: application/json" \
  -d '{"role":"user","content":"Hello!","file_urls":[]}'

# DELETE /conversations/{id}/messages/{message_id}
curl -X DELETE "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/conversations/{conversation_id}/messages/{message_id}" -H "api_key: API_KEY"
```

## Memory

```bash
# GET /memory — list
curl "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/memory" -H "api_key: API_KEY"

# DELETE /memory/{id}
curl -X DELETE "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/memory/{memory_id}" -H "api_key: API_KEY"
```

## Webhooks

Subscribe an HTTPS endpoint to receive agent events. HMAC signing is optional — pass
`"generate_secret": true` when creating a webhook and the response includes a `secret` field once;
store it, since every later delivery carries an `X-Base44-Signature` header to verify against it.

Events: `message.created` (a user message was received), `message.completed` (the assistant's reply
is ready).

Request headers: `X-Base44-Event` (event name), `X-Base44-Delivery` (unique per attempt, for retry
dedup), `X-Base44-Signature` (`sha256=<hex>` HMAC of the raw body, only when signing is enabled).

Sample payload:
```json
{
  "event": "message.completed",
  "app_id": "6a53ec2ca8ddb9dd9657837e",
  "conversation_id": "conv_xyz",
  "timestamp": "2026-04-21T10:00:00Z",
  "data": {
    "message": { "id": "msg_123", "role": "assistant", "content": "Hi!" }
  }
}
```

### Verify the signature

HMAC the raw request bytes (`await req.text()` / `express.raw`) — that's the only fully reliable
method. The compact JSON body is signed (no spaces, unescaped UTF-8), matching
`JSON.stringify(payload)`; if your runtime only exposes a parsed body, `JSON.stringify(body)` works as
a best-effort fallback but can differ on number formatting (e.g. Python `1.0` vs JS `1`) — prefer raw
bytes whenever the payload may contain numbers.

Base44 functions / Deno (`Deno.serve` is the required entrypoint):
```js
Deno.serve(async (req) => {
  const raw = await req.text(); // exact signed bytes — don't re-parse first
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(Deno.env.get("WEBHOOK_SIGNING_SECRET")),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(raw));
  const expected =
    "sha256=" + [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
  // Constant-time compare so verification can't be timing-probed.
  const a = new TextEncoder().encode(expected);
  const b = new TextEncoder().encode(req.headers.get("x-base44-signature") ?? "");
  const ok = a.length === b.length && a.reduce((acc, v, i) => acc | (v ^ b[i]), 0) === 0;
  if (!ok) return new Response("invalid signature", { status: 401 });
  const payload = JSON.parse(raw);
  return new Response(null, { status: 204 });
});
```

Node.js / Express:
```js
import express from "express";
import crypto from "crypto";

app.post(
  "/hooks/base44",
  express.raw({ type: "application/json" }),
  (req, res) => {
    const expected = "sha256=" + crypto
      .createHmac("sha256", process.env.WEBHOOK_SIGNING_SECRET)
      .update(req.body)
      .digest("hex");
    const a = Buffer.from(expected);
    const b = Buffer.from(req.header("x-base44-signature") || "");
    if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
      return res.status(401).send("invalid signature");
    }
    const payload = JSON.parse(req.body.toString("utf8"));
    res.sendStatus(204);
  },
);
```

### Manage webhooks

```bash
# Subscribe
curl -X POST "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/webhooks" -H "api_key: API_KEY" -H "Content-Type: application/json" \
  -d '{"target_url":"https://your-app.example.com/hooks/base44","events":["message.completed"],"generate_secret":true}'

# List
curl "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/webhooks" -H "api_key: API_KEY"

# Update or re-enable
curl -X PATCH "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/webhooks/{webhook_id}" -H "api_key: API_KEY" -H "Content-Type: application/json" \
  -d '{"events":["message.completed","message.created"],"enabled":true}'

# Test delivery
curl -X POST "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/webhooks/{webhook_id}/test" -H "api_key: API_KEY"

# Delete
curl -X DELETE "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/webhooks/{webhook_id}" -H "api_key: API_KEY"
```

Limits: up to 5 webhooks per agent. After 20 consecutive failures a webhook is auto-disabled;
re-enable with `PATCH {"enabled": true}`.

## Response format (conversation)

```json
{
  "id": "conversation_id",
  "app_id": "6a53ec2ca8ddb9dd9657837e",
  "agent_name": "your_agent",
  "messages": [
    { "id": "msg_1", "role": "user", "content": "..." },
    { "id": "msg_2", "role": "assistant", "content": "..." }
  ]
}
```
