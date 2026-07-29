# Learnings

Dated, not-yet-promoted observations about Roman or this repo. Once something recurs 2-3 times,
promote it into `CLAUDE.md` or a skill (see "Continuous improvement" there) and remove it from here.

<!-- Example entry format:
## 2026-07-29
Roman prefers X over Y when Z. (context: what prompted this)
-->

## 2026-07-29
Planned (not yet built): voice-capture via iPhone 17 Pro Action Button. Roman holds the button →
Shortcuts app dictates → POSTs to the Claude Code routine-fire API
(`api.anthropic.com/v1/claude_code/routines/{id}/fire`, experimental/beta). Each fire spins up a
*new* one-off Claude Code session (not this one) that clones `romms/maxvo`, picks up CLAUDE.md's
@imports automatically, and applies the normal capture-system triage (Open Loops if clearly
actionable / Ideas if clearly not / Inbox if ambiguous) before committing and pushing to `main`.
Roman confirmed he doesn't need the capture to land in this specific ongoing conversation — new or
disconnected sessions per capture are fine, which is what made this option viable over trying to
inject into a live session. Backup considered if this proves unreliable/rate-limited: Shortcut →
GitHub Contents API direct write straight into a new file under `vault/Inbox/`, no Claude session
spun up at all. Promote this to a proper doc once Roman confirms it's actually working.

Update: the routine itself is created — `trig_01Fk4eZ6dxj6DgeH6e5JegQi` ("Голосова нотатка (Action
Button)"), poke-only (no schedule), `create_new_session_on_fire: true`, prompt already has the full
triage instructions. `create_trigger` (MCP tool) has no way to attach an "API" trigger / generate a
bearer token — that's only available from the claude.ai/code/routines web UI ("Add another trigger →
API → Generate token"). Roman added the API trigger (confirmed via `api_token_hint` on the trigger).

Update: `create_trigger` also attaches zero MCP connectors by default (explicit warning on creation)
— unlike routines created from the web UI, which include all connected connectors automatically.
Fixed by editing the prompt (via `update_trigger`, which I *can* call) to add a step: after filing
the capture, email a short summary to rommssh@gmail.com via Gmail, so Roman can hear it read aloud
via iOS "Announce Notifications" on Mail — an approximation of a spoken reply, since the public
`/fire` API has no synchronous reply and no documented way to poll a fired session's output. Roman
still needs to, on his side: (1) add the Gmail connector to this specific routine via
claude.ai/code/routines → edit → Connectors tab (has none currently), (2) enable "Allow unrestricted
branch pushes" for `romms/maxvo` under the routine's Permissions tab, or fired sessions can likely
only push `claude/`-prefixed branches, not `main` directly, (3) enable iOS Announce Notifications for
Mail, reliability unverified (works best with AirPods per general iOS behavior, not confirmed for
this specific setup), (4) build/finish the iOS Shortcut itself and test it. As of this note, no
routine run has happened yet (no new commit on `main`, no stray `claude/` branch) — still unverified
end-to-end. Promote to a proper doc once confirmed working.
