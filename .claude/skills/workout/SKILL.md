---
name: workout
description: Prepare a gym session against Roman's self-directed training program (Full Body A/B, 2-3x/week) and pull target weights from his Hevy workout history. Use when Roman asks what today's workout is, heads to or is at the gym, asks to plan a training session, or invokes /workout.
---

# Workout: prepare a gym session

Roman trains independently now (previously with a coach) — this skill is the planning role a coach
would otherwise play: decide the session, set target weights, adjust over time. Not medical advice —
see `vault/Areas/Health/Тренування.md`'s "Профіль і обмеження" section for his stated constraints
(disc protrusions, reflux) and respect them every time, not just when first set up.

For anything beyond day-of prep — exercise substitutions, form questions, pain/discomfort flags,
reviewing a logged session, or changing the program itself — see the `coach` skill instead.

`vault/Areas/Health/Тренування.md` holds the coaching context (profile, constraints, the Full Body
A/B exercise lists, evidence-based rationale in [[Тренування — дослідження і критика]]) — still the
source Claude reads to design/adjust the program. Actual session history (what got logged, weight ×
reps) lives in **Hevy**, not a vault table — logging happens in the app during the workout, which is
a better in-gym experience than typing sets into chat.

Two routines, "Full Body A" and "Full Body B" — a single combined Full Body session (~75-90 min in
practice) ran long against Roman's ~60 min target, so it's split by exercise selection, not by body
region: **both A and B hit upper push+pull and lower quad+posterior-chain every time**, unlike the
earlier Upper/Lower split, so missing a session doesn't leave a whole body region untrained for a
week. Alternate A → B → A on each session, same alternation logic the old Upper/Lower used.

Hevy's public API has no DELETE endpoint for routines — if a routine needs retiring, either repurpose
it via `PUT` (overwrite with new content) or tell Roman to delete it manually in the app; don't leave
stale placeholder routines lying around as the default move.

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

# Create a routine (one-time setup — "Full Body A" / "Full Body B" from Тренування.md's lists)
# POST requires folder_id (use null); PUT to update an existing routine does NOT accept folder_id.
curl -s -X POST "https://api.hevyapp.com/v1/routines" -H "api-key: $HEVY_API_KEY" \
  -H "Content-Type: application/json" -d '{"routine": {"title": "Full Body A", "folder_id": null, "exercises": [...]}}'

# Custom exercise (when nothing in exercise_templates fits, e.g. tibialis anterior work):
curl -s -X POST "https://api.hevyapp.com/v1/exercise_templates" -H "api-key: $HEVY_API_KEY" \
  -H "Content-Type: application/json" -d '{"exercise": {"title": "...", "muscle_group": "calves", "exercise_type": "bodyweight_reps", "equipment_category": "none"}}'

# List exercise templates (needed to resolve exercise names to the IDs routines/workouts require)
curl -s "https://api.hevyapp.com/v1/exercise_templates" -H "api-key: $HEVY_API_KEY"
```

Full API reference: `https://api.hevyapp.com/docs/`. If "Full Body A"/"Full Body B" don't exist yet in
Hevy (first time this skill runs with a working key), create them once via `POST /v1/routines` before
doing anything else. Supersets use a shared `superset_id` (integer) across the paired exercises.

## Prepare today's session

1. `GET /v1/workouts` (most recent page) to find which routine (A or B — inferred from which
   exercises appear) was logged last, and alternate. No workouts yet → today is A.
2. For each exercise in that session's list, look at its most recent occurrence across recent workouts:
   - No prior entry anywhere → calibration: start light, aim for 10-12 reps, note it's a first
     attempt.
   - Prior entry, felt easy/hit the top of the rep range comfortably → suggest a small increase
     (weight, or +1 rep if the equipment's increment is too coarse).
   - Prior entry, felt hard/didn't complete the range → suggest repeating the same weight.
   Always frame these as suggestions to confirm in the moment, not fixed prescriptions — how it
   actually feels during the set is the real signal, not the history.
3. Present the session plan as one message: which session (A or B), then each exercise (grouped by
   superset pair where relevant) with suggested weight/reps — short and scannable, like `plan-day`'s
   proposed-schedule format, not a wall of explanation.
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
