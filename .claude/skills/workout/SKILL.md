---
name: workout
description: Prepare or log a gym session against Roman's self-directed training program in vault/Areas/Health/Тренування.md - decide today's day (Upper/Lower), pull target weights from the training log, and record what actually happened. Use when Roman asks what today's workout is, heads to or is at the gym, asks to plan/log a training session, or invokes /workout.
---

# Workout: prepare or log a gym session

Roman trains independently now (previously with a coach) — this skill is the planning role a coach
would otherwise play: decide the day, set target weights, track progress, adjust over time. Not
medical advice — see the "Профіль і обмеження" section of the program file for his stated
constraints (disc protrusions, reflux) and respect them every time, not just when first set up.

Source of truth: `vault/Areas/Health/Тренування.md` — profile/constraints, the Upper/Lower exercise
lists, and the session log table at the bottom.

## Before/at the gym: prepare today's session

1. Read the log table's last entry to find the last logged day (Upper or Lower) and alternate — if
   last was Upper, today is Lower, and vice versa. If the log is empty, today is Upper (first day).
2. For each exercise in that day's list, check the log for the most recent entry of that exact
   exercise:
   - No prior entry → calibration: start light, aim for 10-12 reps, note it's a first attempt.
   - Prior entry, felt easy/hit the top of the rep range comfortably → suggest a small increase
     (weight, or +1 rep if the equipment's increment is too coarse).
   - Prior entry, felt hard/didn't complete the range → suggest repeating the same weight.
   Always frame these as suggestions to confirm in the moment, not fixed prescriptions — how it
   actually feels during the set is the real signal, not the log.
3. Present the day's plan as one message: day type, then each exercise with suggested weight/reps —
   short and scannable, like `plan-day`'s proposed-schedule format, not a wall of explanation.

## During/after: log what happened

For each exercise (as he goes, or all at once after): record actual weight × reps into the log table
(newest at the bottom, same row format as existing entries), plus a short note only when there's
something worth keeping (easy/hard, form cue, anything that felt off).

**If something aggravates his back or triggers reflux discomfort** — stop that exercise for the
session, don't push through it, and swap in an alternative respecting the same constraint (torso
staying neutral/horizontal for reflux, no axial-loaded jumping/impact for the disc protrusions).
Note the swap in the log so future sessions route around it too, not just this one.

## What not to do

- Don't diagnose pain or discomfort — flag it, suggest stopping/swapping, and say so plainly; that's
  the extent of it.
- Don't invent a weight/rep count Roman didn't report — ask rather than assume how a set went.
- Don't silently escalate difficulty because "it's been a while" — progression comes from what he
  actually reports each session, not a fixed schedule.

Commit and push to the session's active branch and `main`, as usual for vault files.
