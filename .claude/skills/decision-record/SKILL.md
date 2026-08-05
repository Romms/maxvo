---
name: decision-record
description: Research a choice using authoritative, current sources and record it - context, alternatives, sources, and consequences - with a status (accepted/superseded/deprecated) that gets updated rather than silently rewritten when new information arrives. For any of Roman's life/projects (an app or tool choice, a program or routine design, a purchase, how to structure something) - explicitly not limited to code or engineering. Use when comparing options worth getting right, or when asked "why did we choose X" / "what did we decide about Y".
---

# Decision record: research it, cite it, keep it correctable

This is **evidence-based practice** (the clinical-decision model — best available evidence +
practitioner judgment + the individual's specific context — applied to Roman's life instead of
medicine), structurally borrowing the software "Architecture Decision Record" (ADR) pattern (context
→ decision → alternatives → consequences, with a status lifecycle instead of overwriting history).
The three EBP pillars map directly onto the format below: **Джерела** is the evidence, **Рішення**
is the practitioner's synthesis of it (not just a source dump), **Контекст** is what makes it
Roman's specific case rather than generic best practice. The lifecycle (`superseded by`) is EBP's
defining trait, not an afterthought — a decision is explicitly expected to update when better
evidence shows up, unlike "we've always done it this way."

This formalizes what already happened ad hoc for `2026-08-03 - WHOOP integration` and
`2026-08-02 - AI assistant best practices`: research with real sources, write down why, let it be
superseded later instead of quietly edited.

## When to use

- Comparing real options for something worth getting right — an app/tool (e.g. Hevy vs Strong), a
  program/routine design (a workout split, a self-hosting approach), a purchase, how to structure a
  system (one Railway project vs many).
- Roman asks "чому ми обрали X" / "що ми вирішили про Y" — read the existing record instead of
  reconstructing it from memory.
- **Not** for trivial or easily-reversible-in-a-minute choices — same "don't record trivial
  decisions" rule the software ADR pattern already follows.

## Detecting a decision moment

Same as the software version — suggest recording, don't auto-create without confirmation:

- Explicit: "давай оберемо X", "вирішили, що...", "запиши це рішення"
- Implicit: comparing two or more real options and reaching a conclusion, choosing an approach
  after weighing trade-offs, picking a structure/pattern for something ongoing

## Researching

- Prefer primary/official sources (vendor docs, the API's own reference, the maker's own
  statements) over aggregator blog posts and secondhand summaries — same instinct already applied
  in this repo (WHOOP's official API over a reverse-engineered one; an app's own developer docs
  over a comparison-site's paraphrase of them).
- Note recency for anything that can go stale (pricing, feature availability, API behavior,
  current best practice) — a source being right when written doesn't mean it's right now; say when
  it was published or checked.
- Cross-check anything consequential against at least two independent sources when feasible — one
  source's claim is a lead, not a fact, until confirmed elsewhere.
- Record enough about *each* source for a future reader to judge how much to trust it — not just a
  bare link, but what it actually supports and how authoritative it is.

## Where it lives

Inside the relevant project's own detail file in `vault/Projects/` (`YYYY-MM-DD - Title.md`) — not
a separate `docs/adr/`-style directory (`docs/` is for repo/tooling documentation, not project
content — see `vault/Projects/README.md`'s own intro on this). If the project doesn't have a detail
file yet, create one exactly like any other project detail file, linked from its `Projects/README.md`
row.

A project that accumulates several decisions over its life (WHOOP integration already had five) just
gets several `## Рішення: ...` sections in that same file, not five separate files.

## Format

```markdown
## Рішення: [Назва]

**Дата**: YYYY-MM-DD
**Статус**: proposed | accepted | deprecated | superseded by [[link до нового рішення]]

### Контекст
[Що спонукало це рішення — 2-5 речень, без есе]

### Рішення
[Що вирішено — 1-3 речення, чітко]

### Альтернативи
- **Варіант A** — плюси / мінуси / чому ні
- **Варіант B** — плюси / мінуси / чому ні

### Джерела
- [Назва](url) — що саме підтверджує, наскільки авторитетне, коли перевірено
- ...

### Наслідки
- Плюси: ...
- Мінуси/ризики: ...

### Коли переглянути
[Конкретна подія чи дата, не "colись". Якщо є конкретна дата — це також звичайний рядок Активні з
нагадуванням (`docs/capture-system.md`), не окремий механізм.]
```

## Lifecycle

Same states as the software ADR pattern: `proposed → accepted → deprecated | superseded by
[[...]]`. When new information contradicts an accepted decision — don't edit the old section to
pretend it always said the new thing. Add a new `## Рішення` section (or update the status line to
`superseded by`) and link the two, so the reasoning trail survives. This is the actual mechanism for
"correct it when something is refuted" — the record shows both what was believed and why it
changed, not just the final state.

## What not to do

- Don't record trivial or easily-reversible choices — if changing your mind costs nothing, it
  doesn't need a paper trail.
- Don't cite a source without saying what it actually supports — "found via search" isn't a
  citation.
- Don't silently overwrite a prior decision's text — supersede it, keep both visible.
- Don't invent a "коли переглянути" trigger Roman didn't give — ask, or leave it honestly open if
  it's genuinely not known yet (same "критерій ще не визначено" honesty rule as completion
  criteria in `docs/capture-system.md`).
