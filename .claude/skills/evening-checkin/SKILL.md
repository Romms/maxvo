---
name: evening-checkin
description: Run Roman's evening routine - review what happened today, capture what's unfinished without losing it, and set up a low-friction start for tomorrow. Use when Roman asks for his evening check-in, evening routine, end of day review, or invokes /evening-checkin.
---

# Evening check-in

Reference: `docs/daily-rituals.md` for the full design, `docs/roman-operating-guide.md` for the
profile this is built on. Respond in Ukrainian (default language).

Today's note lives at `vault/Daily/YYYY-MM-DD.md` (today's date).

1. Open today's Daily note and find the `## Ранок` priority (if there is no morning entry today,
   just ask what he was aiming for). Also check `vault/Projects/README.md` Активні for anything dated
   today — list it as its own line with deadline and completion criterion (see the presentation note
   at the top of `Projects/README.md`), not condensed into one sentence.
2. Ask directly, per item: done, partial, or not done. Push for a real answer, not "ще працюю над
   цим."
3. Name what actually got finished today, even something small — say it out loud, don't just move
   past it.
4. Anything left open: add it to `vault/Projects/README.md` Активні (if it's still a live commitment
   — ask when to remind and write it into `Check-in` plus a `Reminders` calendar event, per
   `docs/capture-system.md`) or `vault/Inbox.md` (if unclear) — never let it silently disappear.
5. New ideas or urges that came up today but weren't today's priority → `vault/Projects/README.md`
   Ідеї (add a row plus a `YYYY-MM-DD - Title.md` detail file), parked. Do not start them tonight.
6. **Before asking, remind him what he's actually choosing from** — open Активні rows relevant to
   tomorrow, anything left open from today (step 4), ideas parked today (step 5). Don't ask "what's
   tomorrow's priority" cold; his Discipline/Arranger aren't the strength that would otherwise
   surface this list from memory (`docs/roman-operating-guide.md`) — surfacing it is this skill's
   job, same principle `morning-checkin` already applies before its own priority question. Then ask
   for tomorrow's likely one priority and write it as a draft into tomorrow's
   `vault/Daily/YYYY-MM-DD.md` (`## Ранок`, marked as draft) — this is what removes the morning's
   blank-page problem.
7. One quick fuel-guard question: energy/sleep, and whether he picked up more "crises" than the one
   he planned for (see the guardrails table in the operating guide) — note it, don't lecture.
   **While the headache diary is running** (see below), attach the day's diary line to this same
   question instead of asking separately — was there a head episode today (біль, дзвін, "під
   водою")? If yes, capture it per the structure in
   `vault/Areas/Health/Головний біль — щоденник спостережень.md`. **If no — still write one short
   line for the day** (sleep, coffee, training, "болю не було"). That "no pain" line is the part
   that's easiest to skip and the whole reason the diary works: without baseline days there's
   nothing to compare a trigger against. The evening is where it belongs, since the day is done.
8. Write everything into today's note under `## Вечір`.
9. Commit and push to `main`. If the current session's working branch differs from `main`, push to
   that branch too, to keep them in sync.
10. Send a short proactive Telegram summary (what got done today + tomorrow's priority) — see
    "Telegram" in `CLAUDE.md` for the curl pattern and chat_id. This is a notification, not a
    substitute for the conversation above; skip silently (don't block or retry hard) if the curl
    fails, just note the failure inline rather than treating the check-in itself as incomplete.

Keep it short — a checkpoint, not a debrief. One-paragraph summary at the end.

## Headache diary (тимчасово, до візиту до лікаря)

Active from 15.08.2026 until Roman's doctor visit (Активні row "Звернутися до лікаря щодо головного
болю", орієнтир — початок вересня). This is a **temporary** addition to the ritual, not a permanent
step: when the row moves to Завершено, delete this section and the clause in step 7 rather than
leaving them to run indefinitely. The diary itself, including what to record and why days without
pain matter, lives in `vault/Areas/Health/Головний біль — щоденник спостережень.md` — read it there,
don't duplicate the field list into this skill.
