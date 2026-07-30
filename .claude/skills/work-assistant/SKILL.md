---
name: work-assistant
description: Contact Roman's work assistant (Base44 Superagent, used for his Engineering Lead role in Strategy & Growth at Universe Group) to delegate a work task or check on one. Use ONLY when Roman explicitly asks to contact, ask, or delegate to his "робочий асистент" / work assistant / Base44 agent — never automatically, and never as part of the morning/evening/checkin rituals unless he says so this time.
---

# Base44 work assistant

Roman's day-job assistant, built on Base44 Superagents (agent id `6a53ec2ca8ddb9dd9657837e`). This is
an experimental link between the two assistants — reach out to it only when Roman explicitly asks in
the moment (e.g. "запитай робочого асистента...", "передай це Base44...", "зв'яжись з роб. асистентом").
Don't wire it into any standing ritual on your own initiative.

## Setup (one-time, not done automatically)

Calls need the `BASE44_API_KEY` environment variable. It must be set at the **assistant runtime
environment** level (outside this repo) — this repo's container is rebuilt fresh from git each
session, so a key committed to a file here would either leak into git history or vanish on the next
session. It should never be written into any file inside this repo.

If `BASE44_API_KEY` isn't set when this skill is invoked, tell Roman and stop — don't ask him to paste
the raw key into chat again (it's a secret and chat history isn't a safe place for it). Point him to:
the relevant assistant environment settings → environment variables → add `BASE44_API_KEY`.

## Calling the agent

Base URL: `https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e`

```bash
# 1. Create a conversation (once per topic/exchange with the assistant)
curl -s -X POST "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/conversations" \
  -H "api_key: $BASE44_API_KEY" -H "Content-Type: application/json" -d '{}'

# 2. Send Roman's message (reuse the conversation_id from step 1 for follow-ups)
curl -s -X POST "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/conversations/{conversation_id}/messages" \
  -H "api_key: $BASE44_API_KEY" -H "Content-Type: application/json" \
  -d '{"role":"user","content":"<message>"}'

# 3. Read the reply
curl -s "https://app.base44.com/api/agents/6a53ec2ca8ddb9dd9657837e/conversations/{conversation_id}" \
  -H "api_key: $BASE44_API_KEY"
```

In practice `POST /conversations` always returns the same single conversation for this API key —
confirmed by testing, not just observed once — so there's no way to start an isolated thread per
topic; every call lands in the same ongoing conversation (which is also shared with an existing
Telegram integration on this Superagent). See `docs/base44-superagent-api.md` for the full writeup
and other endpoints (memory, webhooks, template cloning) not used by this skill today.

## What to do with the result

Report the assistant's reply back to Roman directly, in Ukrainian. If the exchange surfaces a new work
task or commitment worth tracking, follow the normal capture flow (`docs/capture-system.md`): clearly
actionable items go straight to `vault/Open Loops.md` Active (with owner/deadline/completion
criterion) or `vault/Ideas/` (add a row to `README.md` plus a `YYYY-MM-DD - Title.md` detail file) if
explicitly not a commitment; anything ambiguous goes to `vault/Inbox.md` Unprocessed for the weekly
triage.

Never print, log, or write the raw `BASE44_API_KEY` value anywhere, including into vault notes.
