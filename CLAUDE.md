# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Roman's personal assistant, built on Claude Code. The repo root itself is a personal Obsidian vault
(`.obsidian/` config lives at the root, not inside `vault/`) — so skills, docs, and this file are all
editable from within Obsidian, not just the notes. `vault/` holds the markdown notes proper; a Python
package (`src/maxvo/`) provides scripts/tooling that operate on that notes folder specifically. The
vault's markdown notes are committed alongside the code that processes them — this is not a
general-purpose library, it's tooling for one specific vault, for one specific person.

## Working with Roman

This is how Claude Code should operate in this repo, not just what it should build. The following
files are imported automatically into every session's context — not just prose pointers, these load
for real, so treat them as part of this file rather than optional reading:

@docs/roman-operating-guide.md
@docs/capture-system.md
@docs/daily-rituals.md

Two standing facts not covered in those docs:

**Default language: Ukrainian.** Respond to Roman in Ukrainian unless he switches languages or asks
for something else.

**Location & timezone: Ukraine, Europe/Kyiv.** Whenever "today"/"now" matters (naming a
`vault/Daily/` note, deciding what "this week" means, timestamping an Inbox entry), compute it in
Kyiv local time — e.g. `TZ=Europe/Kyiv date +%F` — not server/UTC time, which will be a different
calendar day for part of Roman's day. The morning/evening Routines (08:30 / 20:30 Kyiv) are stored as
fixed-UTC cron (`30 5 * * *` / `30 17 * * *`, correct for EEST/UTC+3). Kyiv observes seasonal DST, so
when Ukraine falls back to EET (UTC+2, typically late October) both crons need to shift an hour later
in UTC to keep firing at 08:30/20:30 local — and shift back an hour earlier at the next spring-forward
(typically late March). Check `mcp__Claude_Code_Remote__list_triggers` and adjust with
`update_trigger` around those dates; there's no automatic DST handling.

**Calendars.** Roman's Google Calendar has a dedicated **"Daily Tasks"** calendar (repurposed from an
old "Work" calendar) used only for time-blocked task planning (`plan-day` skill) — never for real
meetings/events, which stay on his primary/Appointments calendars. He also has **"Важливі Дати (+ Дні
народження)"** — dedicated to yearly-recurring events (birthdays, anniversaries): all-day,
`RRULE:FREQ=YEARLY`, a 7-day-before popup reminder is the established default (see the Mark/Ustym
birthday events for the pattern). Resolve calendar IDs via `list_calendars` by name rather than
hardcoding them, in case they're ever recreated.

## Continuous improvement

This assistant is expected to get better at its job over time, not just execute each task in
isolation. When a session surfaces something reusable — a preference of Roman's, a recurring
procedure, a fact about this repo that would've saved time to know upfront — write it down before
the session ends, in the right place rather than the easiest place:

- **Standing rule about Roman or this repo** (applies to every future session regardless of task) →
  edit `CLAUDE.md` directly.
- **Repeatable multi-step procedure** (something worth invoking by name next time) → add or update a
  skill under `.claude/skills/`.
- **Deeper context that would bloat CLAUDE.md if inlined** → its own file under `docs/`, linked from
  CLAUDE.md.
- **Not yet proven, or too narrow to promote yet** → append a dated entry to `docs/learnings.md`.
  Revisit it periodically: once something's come up 2-3 times, promote it to CLAUDE.md or a skill and
  remove the entry.

Keep CLAUDE.md itself lean — when adding to it, check whether something it already says is now
redundant or superseded, and prune rather than let it grow unbounded. Corrections from Roman
("actually, do it this way") are exactly the kind of signal that belongs in one of these places, not
just applied silently in the moment.

**Avoid duplicating data and instructions.** Each fact or procedure should have exactly one canonical
home; everywhere else that needs it should link/reference that file instead of copy-pasting it. Use
`@path/to/file` import syntax in CLAUDE.md for docs that must always be in context (see "Working with
Roman" above) rather than restating their content inline — an import is not a copy, it loads the real
file. Skills reference `docs/` the same way, without restating rituals inline. Before adding something
new, check whether it already lives somewhere — extend or import/link to that instead of writing it
again. If a fact changes, it should only need to change in one place.

## Git workflow

Multiple Claude Code sessions can work on this repo concurrently, each on its own branch — pull
`main` at the start of a session and again before merging back, so conflicting parallel edits (e.g.
two sessions touching the same skill file) surface early instead of at push time. Merge a session's
branch into `main` when its work has reached a stable, finished point (a task/subtask is done, docs
are consistent) — not on a timer or mid-task, since `main` is the shared state every other session
reads. This mirrors how the daily-ritual background loggers already push straight to `main` after
each small, atomic, complete write (see `docs/daily-rituals.md`).

**Pushing to `main` while checked out on a different branch: use `git push origin HEAD:main`, never
`git push origin main`.** A session normally works on its own feature branch, but a local `main` ref
still exists from checkout and goes stale as other sessions push to remote `main` without this
session ever touching it. Plain `git push origin main` pushes *that stale local `main` branch*, not
your current commits — it silently targets the wrong ref and fails as a non-fast-forward rejection
that looks like a real conflict but isn't one. `HEAD:main` sidesteps the stale ref by pushing the
checked-out commit explicitly, regardless of local branch name or how far behind local `main` has
drifted.

## Commands

```bash
pip install -e ".[dev]"   # install package + dev deps (click, python-frontmatter, pytest, ruff)

pytest                    # run all tests
pytest tests/test_vault.py::test_iter_notes_skips_obsidian_dir   # run a single test

ruff check .               # lint

maxvo list                 # list all notes in the vault (paths relative to vault root)
maxvo tags                  # list all unique tags (frontmatter `tags:` + inline #tags) across the vault
```

## Architecture

- `src/maxvo/vault.py` is the only place that knows how to locate and read the vault. All
  scripts should go through `iter_notes()` / `get_vault_path()` rather than walking `vault/`
  directly, so vault location and note-parsing stay consistent.
  - Vault location resolution: `MAXVO_VAULT_PATH` env var if set, otherwise `vault/` at the repo
    root (`DEFAULT_VAULT_DIR` in `vault.py`).
  - `iter_notes()` skips anything under `.obsidian/` and yields a `Note` per `.md` file, parsed
    with `python-frontmatter` (so `note.metadata` is the YAML frontmatter dict and
    `note.content` is the body with frontmatter stripped).
  - `Note.tags` merges frontmatter `tags:` with inline `#tags` scraped from the body via regex
    — use this instead of reading `metadata["tags"]` directly, since notes mix both styles.
- `src/maxvo/cli.py` is a thin `click` CLI (`maxvo` entry point) over `vault.py`. New scripts
  should generally be added as new `@main.command()`s here, built on top of `iter_notes()`.
- Vault subfolders that need an index/root note (e.g. `vault/Ideas/`, `vault/Daily/`) name it
  `README.md`, not a file matching the folder name — keep this consistent for any new ones.
- The Obsidian vault is the repo root, not `vault/` — open the repo root folder in Obsidian.
  `.obsidian/workspace*.json` and `.obsidian/cache` are gitignored (machine-specific UI state);
  `.obsidian/` config and installed plugins are otherwise kept in the repo. `iter_notes()` only
  walks `vault/`, so this is independent of what `maxvo` tooling reads — see `vault.py` above.
