---
name: plan-day
description: Time-block today's (or a named day's) tasks into Roman's dedicated "Daily Tasks" Google Calendar - brain dump, prioritize/size, then fill the calendar around fixed commitments with realistic buffers. Also re-plans the rest of the day if something runs over. Use when Roman asks to plan his day, block out his day, "розплануй день", "заповни календар задачами", or invokes /plan-day. Do NOT use this for the lightweight morning-checkin ritual (single priority + first step) unless he explicitly asks for the fuller planning session this time.
---

# Day planning: brain dump → priority → calendar blocks

Roman's own method (short list → priority per item → add to calendar one by one until the day fills
up), combined with evidence-based adjustments: time blocking works especially well for ADHD because
it does prioritization once instead of re-deciding all day, but naive time blocking fails without
buffer time — ADHD time-estimates run optimistic, so blocks need slack built in.

## Calendar

Task blocks go on a separate **"Daily Tasks"** calendar, not the primary/Appointments one — so they
don't mix with real meetings. Use the hardcoded `calendarId` from `CLAUDE.md` "Calendars". If a call
against it fails (calendar recreated), re-resolve via `list_calendars` by name and update the ID
there.

## Step 1: brain dump

Gather the day's task list:
- Ask directly: "які задачі на сьогодні?"
- Pull in from `vault/Projects/README.md` Активні anything due today/this week
- Skim `vault/Inbox.md` Unprocessed for anything that looks like today's task
- Also ask about today's three meals — сніданок/обід/вечеря — specifically because meals are exactly
  the kind of routine that hyperfocus makes invisible (nothing forces them onto the radar the way a
  deadline does). For each: готувати / замовити / піти кудись — this determines both duration and
  prep steps (готувати needs a check "чи є всі продукти" and a shopping step if not, plus cooking
  time; замовити needs a decide+order step plus wait+eat time; піти кудись needs travel time both
  ways plus eating time, and is an anchor like a fixed meeting rather than a movable block). From here
  on treat each meal like any other task on the list — size it, block it, break it into steps if
  needed — not a lesser, easy-to-drop item. If a meal choice raises a real nutrition/hydration
  question (what to eat, reflux timing, etc.) — see the `nutrition` skill, don't re-derive its
  guidance here.

Just gather the list, briefly — don't discuss or prioritize at this step.

## Step 2: priority and size

For each task — a priority and a rough size (T-shirt: small ~15-20 min / medium ~30-45 min / large
~60-90 min).

If there are too many tasks for one day (roughly >9, or the estimates clearly don't fit the work
window) — don't silently cut the list. Say so out loud and apply a soft limit: 1-3-5 (1 large + 3
medium + 5 small) or Ivy Lee (no more than 6, strict priority order, the next one doesn't start until
the previous is closed). One question: "Це забагато для сьогодні. Що з цього реально мусить бути
зроблено сьогодні?" — the rest goes to `vault/Projects/README.md` Активні (not lost, just not today).

## Step 3: fixed meetings, and wind-down

`list_events` on Roman's real calendars (primary `rommssh@gmail.com`, `Appointments`) for the target
day — not "Daily Tasks", that one's task blocks only. Meetings are anchors — task blocks get built
around them, not on top of them.

If the day's working window isn't obvious — ask ("з якої до якої сьогодні працюємо?"), otherwise
propose a default of 09:00–19:00 and say so out loud rather than silently assuming.

Also block an **evening wind-down anchor** — working backward from a target "ready to sleep" time
(default ~23:30, confirm it's still right rather than assuming) minus however long wind-down itself
needs (ask; don't invent a duration). This is Sarah Ward's "picture the finished state, then work
backward" applied to the end of the day, and it's the fuel-guard half of `plan-day` — recovery doesn't
happen on its own (see `docs/roman-operating-guide.md`), so it needs the same anchor treatment as a
meeting, not just a hope that the day winds down naturally.

## Step 4: filling the calendar

In order, by priority:
- Block duration = size estimate + ~25% buffer (correction for ADHD time-underestimation)
- 10-15 min between blocks for switching — not back-to-back
- Route around fixed meetings, don't overlap them

Before actually creating events — show Roman the proposed schedule in one message (time → task, in
order), giving him a chance to quickly adjust order/duration. Only after that, create events via
`create_event` on "Daily Tasks" (`summary` = short task name), each with a popup reminder override at
0 minutes before — fires right at the moment the block starts, same point-of-performance principle as
the `Reminders` calendar (`docs/capture-system.md`), so "what am I on right now" doesn't require
actively checking the calendar.

For medium/large tasks — break it into a short chain of concrete steps (as in morning-checkin, see
"Task breakdown" in `docs/daily-rituals.md`) and put it in the event's `description`, not just the
title. Same goal: don't let him get stuck on "what's next" mid-block.

## During the day: replan

When Roman says something like "затягнулось", "переплануй решту дня", "не встигаю" — without long
questioning: check the current time and which "Daily Tasks" blocks are still ahead today, briefly ask
what's still relevant about the current task, and shift the remaining blocks from (current time +
buffer) in the same priority order. Update existing events (`update_event`), don't create duplicates.

## After the day

End-of-day is `evening-checkin`'s job (`vault/Daily/YYYY-MM-DD.md` `## Вечір`) — don't duplicate that
here. If something fell off the day entirely after a replan — it goes to `vault/Projects/README.md`
Активні or `vault/Inbox.md` as usual, never silently lost.
