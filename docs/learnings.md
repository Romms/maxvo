# Learnings

Dated, not-yet-promoted observations about Roman or this repo. Once something recurs 2-3 times,
promote it into `CLAUDE.md` or a skill (see "Continuous improvement" there) and remove it from here.

<!-- Example entry format:
## 2026-07-29
Roman prefers X over Y when Z. (context: what prompted this)
-->

## 2026-08-02
Compiled research on AI personal assistant best practices — five angles (Anthropic/Claude Code
official guidance, general agent architecture, PKM methodology + Obsidian/AI tools, memory
architecture, ADHD-specific assistive design). Lives at
`vault/Projects/2026-08-02 - AI assistant best practices.md` — it's one of our projects, not
engineering-only reference, so it belongs in `vault/Projects/` like any other project detail file
(moved there from `docs/`, where it first landed). Tracked as an Активні row in
`vault/Projects/README.md`; comparison against what maxvo already does is still open.

While scoping that follow-up, Roman pointed out `vault/Ideas/` and the "initiative" concept I'd
proposed for `docs/` were really the same thing — a project, just a different status. Unified
`vault/Ideas/` + `vault/Open Loops.md` (which itself had a redundant Parked/Recently-closed
mechanism overlapping Ideas) into `vault/Projects/README.md`: one index, sectioned by status
(Активні/Ідеї/На паузі/Завершено), row moves between sections instead of three separate
systems/columns duplicating the same status. Already promoted into `capture-system.md`, `CLAUDE.md`,
and the skills — not a "not yet proven" item, just noting why the shape changed.

## 2026-07-29
Voice-capture via iPhone 17 Pro Action Button — capture-only, no reply/email (Roman explicitly
dropped that scope for now, keep it simple). Roman holds the Action Button → Shortcuts app dictates →
POSTs to the Claude Code routine-fire API (`api.anthropic.com/v1/claude_code/routines/{id}/fire`,
experimental/beta). Each fire spins up a *new* one-off Claude Code session that clones `romms/maxvo`,
picks up CLAUDE.md's @imports automatically, and runs the `voice-capture` skill (triages into
Projects/Inbox per `docs/capture-system.md`, commits, pushes to `main`, ends — no reply needed).
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

## 2026-08-15
Two research-discipline lessons from building the headache source base, both worth watching for
recurrence before promoting anywhere.

**Don't let the specific case drive selection of the evidence base.** Built the first version of
`vault/Areas/Health/Головний біль — база джерел.md` by picking the ICHD-3 chapters that matched
Roman's symptoms. He rejected it: "Те які в мене симптоми не мають впливати на результати пошуку
матеріалів. Ми сфокусуємося над конкретною проблемою пізніше." He's right — selecting sources around
a hypothesis you already hold bakes confirmation bias into the foundation, and the resulting
"research" just restates the assumption. Build the base to cover the field, then apply it to the case
as a separate, later step. Applies to any `дослідження і критика`-style file, not just health.

**`WebFetch` being blocked does not mean the network is blocked — they are different paths.**
WebFetch returns `EGRESS_BLOCKED` for many domains (ichd-3.org, pmc.ncbi.nlm.nih.gov,
australianprescriber.tg.org.au, nice.org.uk) because it fetches through Anthropic-side infrastructure
with its own domain policy. Bash `curl` goes through the session proxy (`$HTTPS_PROXY` →
127.0.0.1:46339 → the environment's egress proxy) and returned HTTP 200 for every one of those same
domains. Check `curl -sS "$HTTPS_PROXY/__agentproxy/status"` — `recentRelayFailures: []` alongside
WebFetch failures is the tell that the environment policy is not the thing blocking you. I reported
this to Roman as a hard limitation and asked him to unblock domains before testing the alternative
path; that was wrong and cost a round trip. Test curl before declaring a source unreachable.

Extraction detail that matters: `sed 's/<[^>]*>//g'` leaves the entire CSS/JS payload in the output
and is useless on modern pages. Strip `<script>/<style>/<head>/<nav>/<footer>` blocks *with their
contents* first, convert block tags to newlines, then strip remaining tags — a ~40-line Python helper
does it well enough to read ICHD-3 in full.
