---
name: morning-checkin
description: Run Roman's morning routine - set today's single priority broken into a chain of concrete micro-steps, note fixed commitments, quick energy check. Designed around his ADHD task-initiation and mid-task focus-drift friction. Use when Roman asks for his morning check-in, morning routine, or invokes /morning-checkin.
---

# Morning check-in

Reference: `docs/daily-rituals.md` for the full design, `docs/roman-operating-guide.md` for the
profile this is built on. Respond in Ukrainian (default language).

Today's note lives at `vault/Daily/YYYY-MM-DD.md` (today's date). If the evening ritual already
pre-seeded a draft priority there yesterday, start from that instead of a blank page.

1. Skim `vault/Inbox.md` "Unprocessed" for anything time-sensitive from overnight — not a full
   triage, just a glance. Full triage happens at the weekly `checkin`.
2. Check `vault/Projects/README.md` Активні for anything due today or this week, **and list every row
   with an "уточнити" deadline too** — see `docs/daily-rituals.md` for why those need surfacing on
   their own, not just date-matched rows. Present them as a list, one item per line with deadline and
   completion criterion (see the presentation note at the top of `Projects/README.md`) — not
   condensed.
3. Ask what the **one** priority for today is. If Roman names several, push him to pick one — "яка
   одна річ зробить сьогодні вдалим днем?"
4. Break that priority into a short chain of concrete micro-steps (~3-5), not just the first one —
   not "попрацювати над X" but actual actions in order ("відкрити файл Y" → "написати перший абзац"
   → "..."). See "Task breakdown" in `docs/daily-rituals.md` for why a chain beats a single first
   step: the stuck point is usually the "що далі?" gap between steps, not only the start.
5. Note any fixed commitments today if not already obvious (meetings, calls).
6. One quick energy/sleep question — light, not an interrogation.
7. Write it into today's `vault/Daily/YYYY-MM-DD.md` under `## Ранок`: one priority, step chain,
   fixed commitments, energy note. Create the file (and folder) if it doesn't exist yet.
8. Commit and push to `main`. If the current session's working branch differs from `main`, push to
   that branch too, to keep them in sync.

Keep the whole exchange short and direct. Give a one-paragraph summary at the end, not a recap of
every step.
