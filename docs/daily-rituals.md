# Daily rituals: morning/evening check-ins and background logging

Two lightweight daily check-in rituals, plus continuous background logging throughout the day, on
top of the weekly `checkin` and the `capture-system.md` Inbox. Designed for Roman's ADHD (combined
type) specifically — see `docs/roman-operating-guide.md` for the full profile this is built on.

Why daily, on top of weekly: the weekly checkpoint sets the one priority for the week, but ADHD task
initiation is a day-by-day (often hour-by-hour) problem. The daily rituals exist to make starting
easier, not to add more planning overhead.

**Never ask him to pick/name something cold — remind him what he's choosing from first.** Roman said
this explicitly (07.08): "коли питаєш за щось - нагадуй про всі речі які я планував!" His
Discipline/Arranger aren't the strength that would otherwise surface a list of open items from memory
(`docs/roman-operating-guide.md`) — that surfacing is this assistant's job, not something to leave to
him. `morning-checkin` already does this before its priority question (step 3 lists Активні
due-dates/"уточнити" rows before step 4 asks); `evening-checkin` does the same before its
tomorrow's-priority question. Apply the same pattern anywhere a checkin (daily or weekly) asks him to
choose or decide — surface the relevant open items/options first, don't ask blank.

## Where it lives

Each day gets one note: `vault/Daily/YYYY-MM-DD.md`, with a `## Ранок` section written by the
morning ritual, a `## Протягом дня` section updated continuously in the background, and a `## Вечір`
section written by the evening one. The evening ritual pre-seeds the next day's note with a draft
priority, so the morning ritual starts from something already decided instead of a blank page —
reducing the number of decisions Roman has to make before he's even started the day.

## Morning: `morning-checkin` skill

Point of the morning ritual: turn "what should I do today" into "what's the first 5-minute action,"
because starting is the hard part with ADHD, not knowing what to do in the abstract.

1. Quick skim of `vault/Inbox.md` for anything urgent from overnight — not a full triage, just a
   glance.
2. Check `vault/Projects/README.md` Активні for anything due today/this week — **and separately list
   every row with an "уточнити" (unclear) deadline**. Those never match a date filter, so they
   silently never come up again once created unless something explicitly re-surfaces them; don't let
   "no deadline yet" become "never mentioned again." Surfacing them isn't the same as resolving them
   — just make sure Roman sees the list.
3. Ask for **one** priority for today — if Roman names several, push him to pick one.
4. Break that priority into a short chain of concrete micro-steps (roughly 3-5), not just the first
   one. See "Task breakdown" below for why — the same first-step logic applies at every step, not
   only the start.
5. Note any fixed commitments (meetings etc.) if not already obvious.
6. One quick energy/sleep question — fuel-guard, not an interrogation.
7. Write it all into today's Daily note, give a short direct summary back.

### Task breakdown: why a chain, not just a first step

Breaking a task into micro-steps helps ADHD focus for the whole task, not just getting started: each
step should be concrete enough to require no further decision to execute. The failure point usually
isn't the beginning — it's the "what's next?" gap between steps, where attention drifts, focus
switches to something else, or procrastination creeps back in. A pre-decided chain of small steps
removes that gap at every transition, not just the first one, and each completed step gives a small
sense of progress that carries momentum into the next. Apply this whenever breaking down a task for
Roman — morning-checkin, `plan-day` time blocks, or mid-conversation when he's stuck mid-task — not
only when a task is starting from zero.

## Evening: `evening-checkin` skill

Point of the evening ritual: close the day's loop explicitly (ADHD motivation needs the win named,
not just moved past), make sure nothing unfinished silently vanishes, and remove friction from
tomorrow's start.

1. Pull up today's Daily note — what was the morning's one priority?
2. Ask directly: done / partial / not done. No vague answers.
3. Name what actually got finished today, even if small — say it out loud.
4. Anything left open goes to `vault/Inbox.md` or `vault/Projects/README.md` Активні, never silently
   dropped.
5. New ideas/urges from today that weren't today's priority → `vault/Projects/README.md` Ідеї,
   parked, not chased tonight.
6. Ask for tomorrow's likely one priority and write it into tomorrow's Daily note in advance.
7. One quick fuel-guard check: energy, and whether he picked up more "crises" than planned (see the
   guardrails table in the operating guide).

Both rituals stay short by design — a checkpoint, not a planning meeting. If either starts running
long, that's a signal to trim it, not to push through.

## During the day: background logging

Beyond what Roman explicitly shares (that's the Inbox's job, see `capture-system.md`), notable things
that happen while working together — a decision made, something finished, important context
surfaced, a plan changing — get logged into today's `## Протягом дня` section as they happen, not
reconstructed later from memory at the evening check-in.

**This is a side-effect, not the main task**: don't stop and do the write yourself in the middle of
whatever else is happening. Instead, dispatch it to a separate background agent (`Agent` tool,
`run_in_background: true`, `isolation: "worktree"` so it doesn't collide with whatever the main
session's working tree is doing) so the actual work continues without waiting on a
read-edit-commit-push cycle. Each logging agent:

1. Determines today's date in Kyiv time (`TZ=Europe/Kyiv date +%F`).
2. Opens (or creates) `vault/Daily/<date>.md` and appends one short bullet under `## Протягом дня` —
   a timestamp and one sentence, not a transcript of the conversation.
3. Commits and pushes to both the active session branch and `main` — push `main` with
   `git push origin HEAD:main` (not `git push origin main`; see "Git workflow" in `CLAUDE.md` for why
   the plain form targets the wrong ref). If the push is rejected because another logging agent
   pushed in the meantime, `git pull --rebase` once and retry; don't loop beyond one retry.

Don't report back to Roman on every individual log write — it's background bookkeeping, not a
conversation turn. Only surface it if a write genuinely fails after the retry.

## Automation

Both fire automatically via Claude Code Remote Routines, bound to this persistent session (not a
fresh session each time — repo state, branch, and prior context need to already be there):

- `trig_01UQ25fk2iGao4W12RqH1suN` — morning, `30 5 * * *` UTC (08:30 Europe/Kyiv, EEST/UTC+3)
- `trig_01SwrqTt9eQurjKMCtbJqrrS` — evening, `30 17 * * *` UTC (20:30 Europe/Kyiv, EEST/UTC+3)

These are fixed-UTC cron, so they don't auto-adjust for Kyiv's seasonal DST switch — see "Location &
timezone" in `CLAUDE.md` for when/how to shift them. Each firing's prompt tells Claude to run the
relevant skill and then commit + push to both the active session branch and `main`, so the vault
notes end up on the remote without Roman needing to ask.
