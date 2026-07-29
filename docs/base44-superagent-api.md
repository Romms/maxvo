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

## Known behavior: one conversation per API key, not per call

Confirmed by direct testing on 2026-07-29 — this is not a misconfiguration on our end, it's how the
API behaves for this key. `POST /conversations` never creates a new conversation; it always returns
the single conversation already bound to this API key's identity (`created_by_id:
6a53ec2ca8ddb9dd9657837f`). Evidence:

- `GET /conversations` returned exactly **one** conversation both before and after ~11 `POST`
  attempts with varying bodies.
- None of the following body params changed the result: `title`, `metadata`, `conversation_type`,
  `user_id`, `external_user_id`, `session_id`, `new: true`, `force_new: true`, `reset: true`. Even a
  deliberately malformed body (`{"messages": "not-an-array"}`) was silently ignored rather than
  rejected — the body doesn't appear to be parsed for conversation-creation purposes at all.
- The `X-Active-Workspace-Id` header (documented for template cloning) had no effect here either.
- A query string `?new=true` had no effect.

So in practice `POST /conversations` behaves as an idempotent "get-or-create the one conversation for
this key" rather than "create a new conversation." There is no known parameter, header, or query
string — documented or guessed — that produces a second conversation for the same key. A Base44
feedback item, ["Superagent Conversation Scoping — App
Isolation"](https://feedback.base44.com/p/superagent-conversation-scoping-app-isolation), requests
exactly this kind of isolation and confirms it isn't solved yet on Base44's side.

**Consequence worth knowing:** the one conversation this key is bound to is not an empty/fresh thread
— it already had `title: "Using Notion Integration"`, `metadata.analytics_channel: "telegram"`, and
549 prior messages before any maxvo test traffic touched it (561 after). That strongly suggests this
key's conversation is shared with an existing Telegram-based integration on the same Superagent —
every message sent through this skill lands in that same real, ongoing thread, not an isolated one.
Decided 2026-07-29: leave this as-is (no separate key/workspace requested) — just documented here so
it's a known property, not a surprise, next time this skill or a debugging session touches it. If
isolation ever becomes necessary, the next thing to try would be provisioning a distinct API key from
the Base44 dashboard (untested — may or may not map to a different `created_by_id`/conversation).

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
