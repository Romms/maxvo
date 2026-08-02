# Capture system: Inbox → Projects

Roman periodically shares raw thoughts, ideas, plans, and tasks in conversation — not through a
structured form. This is the system for what happens to that input, designed around his profile:
Woo/Input/Activator generate raw material fast, Discipline/Arranger/Maximizer (organizing, filing,
finishing) are weak. The assistant owns the filing, not him — see `docs/roman-operating-guide.md`.

## The two files

- **`vault/Inbox.md`** — raw, unfiltered capture log. Every thought, idea, plan, or task Roman shares
  gets written here immediately, verbatim or close to it, with a date. No judgment about where it
  "really" belongs at capture time — the point is nothing gets lost between the conversation and the
  vault.
- **`vault/Projects/`** — every project Roman is tracking, at any stage, as one row in
  `README.md` sectioned by status: **Активні** (committed, with an owner/deadline/completion
  criterion — the existing "open loops" ritual from the operating guide), **Ідеї** (someday/maybe,
  not yet a commitment), **На паузі** (parked mid-work, not killed), **Завершено** (closed, with an
  outcome). A project's full detail — when it needs one — lives in its own `YYYY-MM-DD - Title.md`
  file (or `YYYY-MM-DD - Title/` folder, for something with multiple supporting documents) next to
  the index, linked from the row's Деталі column, so browsing the index doesn't pull in detail for
  projects that aren't currently relevant. Only open the detail file when a project is actually being
  acted on. Moving a row between sections (e.g. Ідеї → Активні when something gets committed to) is
  the entire status-change mechanic — see `vault/Projects/README.md` itself for the presentation and
  inline-steps rules.

## When Claude Code should act

**Capture immediately, always.** The moment Roman shares something worth remembering mid-conversation
— not just when he explicitly says "remember this" — append it to `vault/Inbox.md` under
"Unprocessed." This is a background action alongside whatever else is happening in the conversation,
not something that needs to interrupt the main thread of work.

**Triage on the spot when the category is obvious**, instead of parking it in the Inbox and
double-handling it later:

- A clearly actionable task or plan with a specific outcome → straight into `vault/Projects/README.md`
  Активні. Ask for a deadline/completion criterion if Roman didn't give one — don't invent one
  silently.
- A clearly non-actionable idea/musing he's explicit isn't a commitment → straight into
  `vault/Projects/README.md` Ідеї, plus its `YYYY-MM-DD - Title.md` detail file.

**Everything ambiguous stays in the Inbox** and gets triaged during the weekly `checkin` skill (see
its "Step 0"), rather than Claude guessing.

**Future commitments need their prep steps captured too, not just the commitment itself.** Roman
procrastinates on things unless they're broken into small, concrete steps — and for a
future-dated plan, some of those steps are things to prepare *in advance*, not on the day itself.
"Піти в зал у понеділок" rarely happens on its own; it happens if "купити абонемент," "зібрати
спортивний одяг," "домовитися з тренером," or even just "поставити нагадування" got done
beforehand. When a new Активні row is a future commitment (not something to do right now), ask what
needs to happen beforehand to make it actually happen — don't invent the list, ask Roman — and add
each answer as its own row with a deadline earlier than the commitment itself. This is
the same principle as the "Task breakdown" chain in `docs/daily-rituals.md`, applied to preparation
for a future event instead of execution of today's priority.

**Every new Активні row needs a point-of-performance reminder, not just a deadline.** A deadline
sitting in the table doesn't reach Roman unless he happens to run a check-in that day — see
`vault/Projects/README.md`'s `Check-in` column, which exists for exactly this but was never wired to
anything until now. Whenever a new Активні row is created — or an existing one still shows "уточнити"
in `Check-in`, which `checkin`'s weekly pass sweeps for — ask Roman when he wants to be reminded: a
concrete date+time, decoupled from whether the row's own deadline is concrete yet (an "уточнити
дедлайн" task can still get a real reminder moment). If he only gives a day-part ("ввечері"), ask a
quick follow-up for a rough time rather than inventing one — same rule as a missing deadline. Write
the answer into `Check-in`, then create a matching event on the **`Нагадування`** Google Calendar (see
`CLAUDE.md` "Calendars"): start = that moment, ~15 min duration, popup reminder override at 0 minutes
before (fires right at the moment, not in advance — that's the point), title = short task name,
description = the row's full text. When the row later moves out of Активні (Завершено, or dropped),
find and delete that event by title match on `Нагадування` — don't persist event IDs into the
human-facing table. `voice-capture` is the one exception: it's one-shot with no reply, so it can't
ask — if the dictation states a concrete moment, use it as `Check-in` and create the event as normal;
otherwise leave `Check-in` as "уточнити" for the next `checkin` backfill pass, same interactive-vs-
one-shot line the late-night-date rule below already draws.

**Completion criteria need to be verifiable, not tautological.** The test: could someone with no
context read only the criterion and answer yes/no about whether it's done? A criterion that just
restates the task with "done" tacked on fails this test and is worthless — Roman named the exact
failure pattern to avoid: "задача: зробити щось, критерій: щось зроблено." That's not a check, it's
an echo.

- Bad (process, not outcome): "Попрацювати над X," "Розібратися з Х," "Подумати про Y" — describes an
  activity, not a state that can be confirmed afterward.
- Good (observable, specific): "Рюкзак відправлено," "Готівку знято," "MCP налаштовано, події
  створюються без permission prompt" (names the actual observable behavior, not just "installed"),
  "Довідка написана й показана Роману" (two parts — catches the gap where something gets written but
  never actually shown to him).
- Watch for the trap of a criterion that only captures the first step, not the real finish — e.g.
  "написати Руслану" sounds done the moment a message is sent, but what actually matters is "Руслан
  підтвердив, що задача розблокована." Ask what changes in the world when this is *actually* over,
  not just when Roman's part of it is done.
- For a trigger → result shaped task, Given-When-Then works well: Given [context], When [action],
  Then [one specific, observable result] — "Then it works" is not a criterion, "Then X" (a concrete,
  checkable fact) is.
- For a task with several independent conditions, a checklist works better than a single sentence
  (the Obsidian-mobile item is the existing example: plugin installed *and* configured *and*
  auto-pushing).
- If Roman doesn't have enough detail yet to write a real criterion, don't force one — write "критерій
  ще не визначено" plus what's missing to define it, and revisit once that detail exists. A fake
  criterion is worse than an honest placeholder.

**Relative dates said late at night are ambiguous — don't resolve them confidently.** "Завтра"
("tomorrow") said at, say, 01:37 could mean the calendar day that just started a little while ago
(a few hours away) or the one after it (once he's actually slept) — Roman himself may not be
distinguishing the two in the moment. Roughly midnight–06:00 Kyiv is the risk window. In an
interactive skill (`checkin`, `morning-checkin`, `evening-checkin`), just ask him which he means —
cheap to resolve on the spot. In a one-shot skill with no back-and-forth (`voice-capture`), don't
guess: record the relative word as said plus the capture timestamp, and flag the date explicitly as
needing confirmation (e.g. "'завтра' сказано о 01:37 — може бути пт 31.07 чи сб 01.08, уточнити")
instead of writing a single resolved date as if it were certain.

## Why this shape

This mirrors the "finish before you start" and "own the last 20%" rules from the operating guide:
capture is zero-friction so Roman's fast-generating themes aren't taxed with filing, but nothing
accumulates unprocessed indefinitely — the weekly ritual forces a real decision on every open item
instead of letting the Inbox become its own silent backlog.
