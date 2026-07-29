# Learnings

Dated, not-yet-promoted observations about Roman or this repo. Once something recurs 2-3 times,
promote it into `CLAUDE.md` or a skill (see "Continuous improvement" there) and remove it from here.

<!-- Example entry format:
## 2026-07-29
Roman prefers X over Y when Z. (context: what prompted this)
-->

## 2026-07-29
Voice-capture via iPhone 17 Pro Action Button — capture-only, no reply/email (Roman explicitly
dropped that scope for now, keep it simple). Roman holds the Action Button → Shortcuts app dictates →
POSTs to the Claude Code routine-fire API (`api.anthropic.com/v1/claude_code/routines/{id}/fire`,
experimental/beta). Each fire spins up a *new* one-off Claude Code session that clones `romms/maxvo`,
picks up CLAUDE.md's @imports automatically, and runs the `voice-capture` skill (triages into Open
Loops/Ideas/Inbox per `docs/capture-system.md`, commits, pushes to `main`, ends — no reply needed).
Routine: `trig_01Fk4eZ6dxj6DgeH6e5JegQi` ("Голосова нотатка (Action Button)"), poke-only, prompt is
just "run skill voice-capture" (routine prompts for all three voice/daily routines now just invoke a
skill instead of duplicating the ritual steps inline — single source of truth in the repo).

`create_trigger` (MCP tool) can create the routine itself but can't attach an API trigger/token or
MCP connectors — those are web-UI-only (claude.ai/code/routines → edit). Roman added the API trigger
already (confirmed via `api_token_hint`). Remaining on his side: enable "Allow unrestricted branch
pushes" for `romms/maxvo` under the routine's Permissions tab — without it, fired sessions likely can
only push `claude/`-prefixed branches, not `main` directly (a placeholder branch name
`claude/determined-archimedes` already showed up in the trigger config, unconfirmed whether from an
actual run or just reserved). Then build/finish the iOS Shortcut and test end-to-end. As of this
note, no confirmed successful run yet (no new commit on `main`, no verified branch). Promote to a
proper doc once confirmed working.
