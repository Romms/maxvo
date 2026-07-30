# Capture system: Inbox → Ideas / Open Loops

Roman periodically shares raw thoughts, ideas, plans, and tasks in conversation — not through a
structured form. This is the system for what happens to that input, designed around his profile:
Woo/Input/Activator generate raw material fast, Discipline/Arranger/Maximizer (organizing, filing,
finishing) are weak. The assistant owns the filing, not him — see `docs/roman-operating-guide.md`.

## The three files

- **`vault/Inbox.md`** — raw, unfiltered capture log. Every thought, idea, plan, or task Roman shares
  gets written here immediately, verbatim or close to it, with a date. No judgment about where it
  "really" belongs at capture time — the point is nothing gets lost between the conversation and the
  vault.
- **`vault/Ideas/`** — someday/maybe backlog. `README.md` is the index (one line per idea: short
  description, date, status, link); each idea's full detail lives in its own
  `YYYY-MM-DD - Title.md` file next to it, so browsing the backlog doesn't pull in detail for ideas
  that aren't currently relevant. Only open the detail file when the idea is actually being acted on.
- **`vault/Open Loops.md`** — active commitments with an owner, deadline, and completion criterion.
  Existing ritual from the operating guide; unchanged by this system.

## When the assistant should act

**Capture immediately, always.** The moment Roman shares something worth remembering mid-conversation
— not just when he explicitly says "remember this" — append it to `vault/Inbox.md` under
"Unprocessed." This is a background action alongside whatever else is happening in the conversation,
not something that needs to interrupt the main thread of work.

**Triage on the spot when the category is obvious**, instead of parking it in the Inbox and
double-handling it later:

- A clearly actionable task or plan with a specific outcome → straight into `vault/Open Loops.md`
  Active. Ask for a deadline/completion criterion if Roman didn't give one — don't invent one
  silently.
- A clearly non-actionable idea/musing he's explicit isn't a commitment → straight into
  `vault/Ideas/`: add a row to `README.md` and create its `YYYY-MM-DD - Title.md` detail file.

**Everything ambiguous stays in the Inbox** and gets triaged during the weekly `checkin` skill (see
its "Step 0"), rather than the assistant guessing.

## Why this shape

This mirrors the "finish before you start" and "own the last 20%" rules from the operating guide:
capture is zero-friction so Roman's fast-generating themes aren't taxed with filing, but nothing
accumulates unprocessed indefinitely — the weekly ritual forces a real decision on every open item
instead of letting the Inbox become its own silent backlog.
