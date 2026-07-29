---
name: evening-checkin
description: Run Roman's evening routine - review what happened today, capture what's unfinished without losing it, and set up a low-friction start for tomorrow. Use when Roman asks for his evening check-in, evening routine, end of day review, or invokes /evening-checkin.
---

# Evening check-in

Reference: `docs/daily-rituals.md` for the full design, `docs/roman-operating-guide.md` for the
profile this is built on. Respond in Ukrainian (default language).

Today's note lives at `vault/Daily/YYYY-MM-DD.md` (today's date).

1. Open today's Daily note and find the `## Ранок` priority (if there is no morning entry today,
   just ask what he was aiming for).
2. Ask directly: done, partial, or not done. Push for a real answer, not "ще працюю над цим."
3. Name what actually got finished today, even something small — say it out loud, don't just move
   past it.
4. Anything left open: add it to `vault/Open Loops.md` (if it's still a live commitment) or
   `vault/Inbox.md` (if unclear) — never let it silently disappear.
5. New ideas or urges that came up today but weren't today's priority → `vault/Ideas/` (add a row to
   `README.md` plus a `YYYY-MM-DD - Title.md` detail file), parked. Do not start them tonight.
6. Ask for tomorrow's likely one priority and write it as a draft into tomorrow's
   `vault/Daily/YYYY-MM-DD.md` (`## Ранок`, marked as draft) — this is what removes the morning's
   blank-page problem.
7. One quick fuel-guard question: energy/sleep, and whether he picked up more "crises" than the one
   he planned for (see the guardrails table in the operating guide) — note it, don't lecture.
8. Write everything into today's note under `## Вечір`.
9. Commit and push to `main`. If the current session's working branch differs from `main` (e.g. this
   persistent session's `claude/new-session-uoceqa`), push to that branch too, to keep them in sync.

Keep it short — a checkpoint, not a debrief. One-paragraph summary at the end.
