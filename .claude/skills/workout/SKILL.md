---
name: workout
description: Prepare a gym session against Roman's self-directed training program (Full Body, 2-3x/week) and pull target weights from his Hevy workout history. Use when Roman asks what today's workout is, heads to or is at the gym, asks to plan a training session, or invokes /workout.
---

# Workout: prepare a gym session

Roman trains independently now (previously with a coach) — this skill is the planning role a coach
would otherwise play: set target weights, adjust over time. Not medical advice — see
`vault/Areas/Health/Тренування.md`'s "Профіль і обмеження" section for his stated constraints (disc
protrusions, reflux) and respect them every time, not just when first set up.

`vault/Areas/Health/Тренування.md` holds the coaching context (profile, constraints, the Full Body
exercise list, evidence-based rationale in [[Тренування — дослідження і критика]]) — still the source
Claude reads to design/adjust the program. Actual session history (what got logged, weight × reps)
lives in **Hevy**, not a vault table — logging happens in the app during the workout, which is a
better in-gym experience than typing sets into chat.

Single routine ("Full Body"), same session every time — no day-type decision needed, unlike the
earlier Upper/Lower split. Roman's old "Lower" routine is renamed "АРХІВ (не використовувати)" with a
placeholder exercise, since the Hevy public API has no DELETE endpoint for routines — safe to ignore,
he can delete it manually in the app if it bothers him.

## Setup (one-time, not done automatically)

Calls need the `HEVY_API_KEY` environment variable (requires an active Hevy Pro subscription — that's
Roman's side, not something this skill can set up). It must be set at the **Claude Code Remote
environment** level (outside this repo), same as `BASE44_API_KEY` (see `work-assistant/SKILL.md`) —
this repo's container is rebuilt fresh from git each session, so a key committed to a file here would
either leak into git history or vanish on the next session. Never write it into any file in this repo.

If `HEVY_API_KEY` isn't set when this skill is invoked, tell Roman and stop — don't ask him to paste
the raw key into chat (it's a secret, chat history isn't a safe place for it). Point him to:
`hevy.com/settings?developer` → generate a key → Claude Code environment settings → this environment
→ environment variables → add `HEVY_API_KEY`.

Base URL: `https://api.hevyapp.com/v1`. Every call needs the header `api-key: $HEVY_API_KEY`.

```bash
# List recent workouts (paginated - page/pageSize params)
curl -s "https://api.hevyapp.com/v1/workouts?page=1&pageSize=10" -H "api-key: $HEVY_API_KEY"

# Create a routine (one-time setup — "Full Body" from Тренування.md's exercise list)
curl -s -X POST "https://api.hevyapp.com/v1/routines" -H "api-key: $HEVY_API_KEY" \
  -H "Content-Type: application/json" -d '{"routine": {"title": "Full Body", "exercises": [...]}}'
# To update an existing routine instead of creating a duplicate: PUT /v1/routines/{id} (same body
# shape, no folder_id field on PUT). There is no DELETE endpoint for routines in this API.

# List exercise templates (needed to resolve exercise names to the IDs routines/workouts require)
curl -s "https://api.hevyapp.com/v1/exercise_templates" -H "api-key: $HEVY_API_KEY"
```

Full API reference: `https://api.hevyapp.com/docs/`. If the "Full Body" routine doesn't exist yet in
Hevy (first time this skill runs with a working key), create it once via `POST /v1/routines` before
doing anything else. Supersets use a shared `superset_id` (integer) across the paired exercises.

## Prepare today's session

1. `GET /v1/workouts` (most recent page) to see the last logged session's exercises and weights.
2. For each exercise in the Full Body list, look at its most recent occurrence across recent workouts:
   - No prior entry anywhere → calibration: start light, aim for 10-12 reps, note it's a first
     attempt.
   - Prior entry, felt easy/hit the top of the rep range comfortably → suggest a small increase
     (weight, or +1 rep if the equipment's increment is too coarse).
   - Prior entry, felt hard/didn't complete the range → suggest repeating the same weight.
   Always frame these as suggestions to confirm in the moment, not fixed prescriptions — how it
   actually feels during the set is the real signal, not the history.
3. Present the session plan as one message: each exercise (grouped by superset pair where relevant)
   with suggested weight/reps — short and scannable, like `plan-day`'s proposed-schedule format, not
   a wall of explanation.
4. Tell Roman to log the actual session in the Hevy app as he goes — this skill doesn't write
   workouts back for him mid-session, it prepares what to aim for.

**If something aggravates his back or triggers reflux discomfort** — tell him to stop that exercise
for the session and swap in an alternative respecting the same constraint (torso staying
neutral/horizontal for reflux, no axial-loaded jumping/impact for the disc protrusions), and note the
swap in `vault/Areas/Health/Тренування.md`'s exercise list so future sessions route around it too.

## What not to do

- Don't diagnose pain or discomfort — flag it, suggest stopping/swapping, and say so plainly; that's
  the extent of it.
- Don't invent a weight/rep count Roman didn't report — ask rather than assume how a set went, if it's
  not yet reflected in Hevy.
- Don't silently escalate difficulty because "it's been a while" — progression comes from what
  actually got logged, not a fixed schedule.
- Never print, log, or write the raw `HEVY_API_KEY` value anywhere, including into vault notes.
