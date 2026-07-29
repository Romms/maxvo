---
name: checkin
description: Run Roman's weekly checkpoint ritual - review last week's commitments, close or consciously kill open loops, and set the one priority for next week. Use when the user asks for a check-in, weekly review, status review, or invokes /checkin.
---

# Weekly checkpoint

Reference: `docs/roman-operating-guide.md` for the full operating guide this ritual comes from, and
`docs/capture-system.md` for how Inbox/Ideas/Open Loops fit together.

## Step 0: process the Inbox

Go through `vault/Inbox.md`'s "Unprocessed" section, item by item. For each entry, decide with Roman:

- Clear actionable task/plan → move into `vault/Open Loops.md` Active, with owner, deadline, and a
  concrete completion criterion.
- Interesting but not a commitment yet → move into `vault/Ideas/`: add a row to `Ideas.md` and
  create its `YYYY-MM-DD - Title.md` detail file.
- Reference/knowledge worth keeping → file into the relevant vault note, or create one.
- No longer relevant → drop it, say so out loud rather than silently deleting.

Move each processed entry to Inbox's "Processed" section, checked off, noting where it went. Don't
skip this step even if the Inbox is short — an unprocessed Inbox is exactly the kind of open loop this
ritual exists to close.

## Then: the three questions

Run exactly three questions, in order, against `vault/Open Loops.md`:

1. **What did we commit to last week?** Read the Active table in `vault/Open Loops.md` — that list is
   the source of truth, not memory. Read it back to Roman.
2. **What's actually finished vs. still open?** For each active row, ask directly. Finished rows move
   to "Recently closed" with the outcome. Rows he wants to abandon move there too, marked dropped —
   don't let them linger silently. Anything genuinely still in flight stays in Active, but push for a
   real answer rather than a vague "still working on it."
3. **What is *the one* priority for next week?** Singular — if he names more than one, ask him to pick.
   Add/update that row in Active with an owner, deadline, and a concrete completion criterion (not
   "make progress on X" — a criterion someone else could check).

If he pitches something new mid-checkpoint, don't wave it through: "Love it — on the list. Starts when
[current priority] finishes." Add it to the Parked table, not Active.

After the three questions, update `vault/Open Loops.md` directly (Edit tool) and give a one-paragraph
summary: what closed, what's the one priority, what's parked.

Keep the whole thing short — this is a checkpoint, not a planning meeting.
