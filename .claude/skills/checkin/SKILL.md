---
name: checkin
description: Run Roman's weekly checkpoint ritual - review last week's commitments, close or consciously kill open loops, and set the one priority for next week. Use when the user asks for a check-in, weekly review, status review, or invokes /checkin.
---

# Weekly checkpoint

Reference: `docs/roman-operating-guide.md` for the full operating guide this ritual comes from, and
`docs/capture-system.md` for how Inbox/Projects fit together.

## Step 0: process the Inbox

Go through `vault/Inbox.md`'s "Unprocessed" section, item by item. For each entry, decide with Roman:

- Clear actionable task/plan → move into `vault/Projects/README.md` Активні, with owner, deadline,
  a concrete completion criterion, and a reminder moment in `Check-in` backed by a `Нагадування`
  calendar event (see `docs/capture-system.md`).
- Interesting but not a commitment yet → move into `vault/Projects/README.md` Ідеї, plus its
  `YYYY-MM-DD - Title.md` detail file.
- Reference/knowledge worth keeping → file into the relevant vault note, or create one.
- No longer relevant → drop it, say so out loud rather than silently deleting.

Move each processed entry to Inbox's "Processed" section, checked off, noting where it went. Don't
skip this step even if the Inbox is short — an unprocessed Inbox is exactly the kind of open loop this
ritual exists to close.

## Then: the three questions

Run exactly three questions, in order, against `vault/Projects/README.md`:

1. **What did we commit to last week?** Read the Активні table — that list is the source of truth,
   not memory. Read it back to Roman as a list, one item per line with deadline and completion
   criterion (see the presentation note at the top of `Projects/README.md`) — not a condensed
   summary. While you're in the table, note any row whose `Check-in` still says "уточнити" — sweep
   those for a reminder moment same as a new row (see below), a few per week is fine, no need to
   clear all of them in one sitting.
2. **What's actually finished vs. still open?** For each active row, ask directly. Finished rows move
   to Завершено with the outcome — also delete that row's `Нагадування` calendar event (find it by
   title match). Rows he wants to abandon move there too, marked dropped, event deleted the same way
   — don't let them linger silently. Anything genuinely still in flight stays in Активні, but push for
   a real answer rather than a vague "still working on it."
3. **What is *the one* priority for next week?** Singular — if he names more than one, ask him to
   pick. Add/update that row in Активні with an owner, deadline, a concrete completion criterion (not
   "make progress on X" — a criterion someone else could check), and a reminder moment in `Check-in`
   backed by a `Нагадування` calendar event.

Also skim Ідеї once: anything become relevant enough to actually commit to? If so, move it to Активні
(with owner/deadline/completion criterion, same as any new commitment) — this is the only "promotion"
an idea gets. Otherwise leave it; someday/maybe doesn't need re-litigating every week.

Also do a light dormancy check on `vault/Areas/README.md`: for each Area, ask "ще актуально? щось
змінилось?" — no deadline pressure, just confirm it's still being maintained or note what changed.
Update the row's "Востаннє перевірено" date, and jot anything noteworthy into that Area's own
`README.md` under "Огляди". This is a lighter pass than Активні — Areas don't get closed or promoted,
just periodically confirmed.

If he pitches something new mid-checkpoint, don't wave it through: "Love it — on the list. Starts when
[current priority] finishes." Add it to На паузі, not Активні.

After the three questions, update `vault/Projects/README.md` directly (Edit tool) and give a
one-paragraph summary: what closed, what's the one priority, what's parked.

Commit and push to `main`. If the current session's working branch differs from `main`, push to that
branch too, to keep them in sync.

Keep the whole thing short — this is a checkpoint, not a planning meeting.
