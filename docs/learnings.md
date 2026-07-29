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
inject into a live session. Setup (routine + API token on claude.ai, the iOS Shortcut itself) is on
Roman's side, nothing to build in-repo. Backup considered if this proves unreliable/rate-limited:
Shortcut → GitHub Contents API direct write straight into a new file under `vault/Inbox/`, no Claude
session spun up at all. Promote this to a proper doc once Roman confirms it's actually working.
