---
tags: [projects]
date: 2026-08-02
---

# AI Personal Assistant Best Practices — Research Notes

Compiled 2026-08-02, via parallel research across five angles. Not `@`-imported into `CLAUDE.md`:
it's reference material for the comparison below, not something every session needs loaded.

## Порівняння з поточною архітектурою maxvo (2026-08-02)

Що вже покрито добре — і що є справжньою прогалиною, зіставлено джерело за джерелом проти
`CLAUDE.md`, усіх `docs/`, усіх `.claude/skills/*/SKILL.md` і auto-memory системи. Повний список
рекомендацій і пріоритизація — у відповіді Клода в сесії 2026-08-02 (див. чат); тут — короткий
підсумок для майбутніх сесій.

**Вже добре покрито** (не потребує змін): прогресивне розкриття skills (frontmatter опис = what+when,
тіло skillـa лаконічне); розділення capture/organize (Inbox → щотижневий checkin, точно як CODE);
ланцюжок мікрокроків замість одного першого кроку (task breakdown у `daily-rituals.md` — уже прямо
посилається на ADHD-адаптацію GTD); критерій завершення як образ фінішу, а не "зробити X" (Sarah
Ward's "Get Ready·Do·Done", хоч і не усвідомлено звідти); "не тренувати слабку функцію, а змінити
середовище" (Dawson & Guare) — це буквально принцип "complete him, don't correct him" з operating
guide; auto-memory — файлова, git-аудійована, з описом що визначає використання (Letta memory
blocks), оновлюється а не тільки додається (Mem0); voice-capture явно трактує диктовку як контент, не
команди (інстинктивний захист від lethal trifecta); дефолт на один послідовний skill замість рою
підагентів (Cognition's "Don't Build Multi-Agents").

**Реальні прогалини, повторювані у кількох джерелах** (найвищий пріоритет):
1. **Нагадування не "у точці дії"** (Barkley temporal myopia, External Systems for ADHD) — дедлайни й
   "уточнити"-рядки в Активні зринають лише на ранковому/вечірньому чекіні, не в момент і місце дії.
2. **Нуль evals/фідбек-циклу на якість ритуалів** (Hamel Husain, LangChain trajectory evals) — ніщо
   не перевіряє, чи справді ранковий/вечірній чекін чи тріаж працюють добре з часом, окрім разових
   виправлень Романа.
3. **Немає ритуалу перегляду auto-memory** ("Is Agent Memory a Database?" — unregulated growth,
   missing semantic revision) — файли пам'яті ніхто не переглядає і не чистить на регулярній основі.
4. **PARA "Areas" відсутні** — постійні (без дедлайну) відповідальності типу здоров'я
   (`Blood Pressure.md`) не мають формального місця окремо від Projects.

**Менші/новіші можливості:** режим "прорепетирувати важку розмову" перед реальною (OZCHI 2025 diary
study — саме для рядків типу "Зустрітися із П"); перевірка емоційного тертя навколо задачі, не лише
логістики (Brown Model, Emotion cluster); AI body doubling — спільна фокус-сесія в реальному часі
(більший фіча-запит, не просто правка документа).

## Anthropic / Claude Code official

- **[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** —
  Anthropic Engineering (Dec 2024). Draws a hard line between *workflows* (predefined code paths,
  for well-defined repeatable tasks) and *agents* (LLM dynamically directs its own tool use, for
  open-ended tasks). Start with the simplest composition (a single call + retrieval/few-shot) and
  only add agentic complexity when it measurably earns its added latency/cost.
- **[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)**
  — Anthropic Applied AI (Sept 2025). Context is a finite, depleting budget, not a dump site:
  just-in-time retrieval (keep lightweight references, load content only when needed), compaction
  near context limits, structured external note-taking (a persistent notes file) so long tasks
  survive context resets. Sub-agents do focused work in clean context and return condensed
  (~1,000–2,000 token) summaries to the coordinator.
- **[Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)** — CLAUDE.md
  should only include what Claude *can't* infer from reading the code (non-standard commands,
  project-specific gotchas) — ask "would removing this line cause a mistake?" for every line. Use
  domain-specific `skills/` instead of bloating CLAUDE.md for occasional knowledge. Four-phase
  workflow: explore → plan → implement → commit.
- **[Subagents in the SDK](https://code.claude.com/docs/en/agent-sdk/subagents)** — context
  isolation (only the final message returns to the parent), true parallelization, tool restriction
  (e.g. a reviewer subagent given only `Read`/`Grep`). The `description` field is what automatic
  delegation matches against, so it needs to state both what and when.
- **[Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)**
  — progressive disclosure across three token-cost tiers: metadata (~100 tokens, always loaded),
  SKILL.md body (loaded on trigger, target <5k tokens), bundled resources (loaded only if
  referenced). The `description` must state both what the skill does and when to use it.
- **[Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)** — a
  client-side, file-based memory directory read/written across sessions. Documents a concrete
  multi-session pattern: an initializer session sets up a progress log + checklist, every later
  session reads it to resume, and each session ends by updating it — marking work complete only
  after end-to-end verification, not when code is written.
- **[Writing Effective Tools for AI Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)**
  — namespace tools by resource so agents pick the right one among many; return human-readable
  names not opaque IDs; build in pagination/truncation; make error messages actionable. Iterate:
  prototype → realistic eval tasks → measure → let the agent itself propose tool improvements.
- **[Introducing MCP](https://www.anthropic.com/news/model-context-protocol)** — solves the M×N
  integration problem (M assistants × N data sources) with one open client-server protocol. Prefer
  wiring external tools through MCP servers over one-off integrations.
- **[Prompt Engineering Overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)**
  — reach for prompt engineering only after you have clear success criteria and an eval method; not
  every failure is a prompting problem.
- **[Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)**
  — a two-agent harness for work spanning many context windows: a one-time initializer sets up
  progress notes + git baseline; every later session reads progress + recent git log, runs baseline
  tests, picks one incomplete item off a checklist, implements, commits, updates the progress file.
  Warns explicitly against editing/removing tests to fake completion. Descriptive git commits are
  the recovery mechanism when a session goes wrong — directly parallels maxvo's daily-ritual
  loggers.
- **[Bringing Memory to Teams](https://claude.com/blog/memory)** — memory should be user-visible and
  user-editable (view/edit/incognito), scoped so contexts don't bleed into each other, tuned by
  explicit user feedback rather than silently accumulating an opaque store.

## General agent architecture (non-Anthropic)

- **[12-Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/README.md)** — Dex
  Horthy/HumanLayer. Most agents plateau at 70-80% reliability because teams let the LLM own the
  whole loop. Own your prompts/context explicitly; treat tool calls as structured output, not magic;
  keep deterministic code in control of the loop (LLM proposes, code decides); unify business state
  and execution state so progress is just a DB row; design small single-purpose "stateless reducer"
  agents that can be paused/resumed from anywhere (cron, webhook, etc.).
- **[Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)** — Hamel Husain. Three-tier
  eval hierarchy: cheap deterministic unit tests → human + LLM-judge review of real traces (judge
  prompt tuned against human labels, tracked via precision/recall) → A/B in production. Remove
  friction from looking at real traces; do continuous error analysis, don't just write tests once.
- **[Test — LangChain docs](https://docs.langchain.com/oss/python/langchain/test)** — unit tests
  (in-memory fakes) vs. integration tests (real network calls) vs. trajectory evals (checking the
  sequence of actions, not just the final answer). Agentic systems should lean on integration tests
  more than pure unit tests since they chain multiple nondeterministic components.
- **[AI Agent Tool Use Best Practices](https://mlflow.org/articles/ai-agent-tool-use-best-practices-for-practitioners/)**
  — MLflow. Prefer narrow job-specific tools over broad wrappers that hand raw execution power to
  the model; validate input/output against typed schemas; make mutating tools idempotent/retry-safe;
  separate read/write/destructive permission tiers; hard budgets (max steps/tokens/time) after which
  the agent must halt and escalate.
- **[Agents](https://huyenchip.com/2025/01/07/agents.html)** — Chip Huyen. Four planning-failure
  modes: invalid tool calls, invalid parameters, correct-tool-wrong-value, goal failures (a
  plausible plan that doesn't satisfy the real constraint). More tools makes selection *harder*, not
  easier — scope the tool set by ablation, like scoping permissions for a new hire.
- **[Persistence — LangGraph docs](https://docs.langchain.com/oss/python/langgraph/persistence)** —
  a checkpointer snapshots full state after every step keyed by thread ID, so an agent resumes
  exactly where it left off. Default in-memory checkpointer is non-durable; needs a real backend
  beyond local dev, plus an explicit cleanup/retention policy.
- **[Long-Term Memory Architectures for AI Agents](https://redis.io/blog/long-term-memory-architectures-ai-agents/)**
  — Redis. Split memory into semantic (durable facts), episodic (time-indexed past events,
  consolidated into semantic over time), procedural (skills/routines). "Read-before-reasoning,
  write-after-acting" loop; unbounded growth degrades retrieval — deciding what to forget needs an
  explicit policy.
- **[Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents)** — Cognition
  (Devin). Sub-agents running in parallel without seeing each other's full context make silently
  conflicting decisions that compound into unusable results. Default to a single-threaded linear
  agent; if compressing context, use a dedicated compression step, not naive truncation/summarizing.
- **[The Lethal Trifecta for AI Agents](https://simonw.substack.com/p/the-lethal-trifecta-for-ai-agents)**
  — Simon Willison. Private data + untrusted content + external communication, all three together,
  means reliable prompt-injection data exfiltration. Don't rely on "95% effective" filtering —
  architecturally break the trifecta (plan-then-execute, or a dual-LLM pattern).
- **[OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)**
  — prompt injection (direct/indirect via tool results), tool/privilege over-scoping, data
  exfiltration via tool calls, memory poisoning. Sanitize untrusted content before it enters context,
  least-privilege per tool, expiration/size/integrity checks on anything written to persistent
  memory.

## Personal knowledge management + Obsidian/AI

- **[The PARA Method](https://fortelabs.com/blog/para/)** / **[Building a Second Brain (CODE)](https://fortelabs.com/blog/basboverview/)**
  — Tiago Forte. File by actionability (Projects/Areas/Resources/Archives), not topic. CODE
  (Capture → Organize → Distill → Express) explicitly separates capturing from organizing — never
  do both in the same motion, which is what keeps capture frictionless. Named failure mode: the
  "digital junk drawer" — countered by a scheduled, time-boxed weekly review where every new item
  passes a three-question actionability test before the review ends.
- **[Introduction to the Zettelkasten Method](https://zettelkasten.de/introduction/)** — atomicity
  (one idea per note) plus explicit, reasoned links (a link without a stated *why* isn't
  knowledge-building). Always rewrite source material in your own words; verbatim capture doesn't
  count as a note.
- **[What is GTD?](https://gettingthingsdone.com/what-is-gtd/)** / **[the two-minute rule](https://gettingthingsdone.com/2015/04/soaring-with-the-gtd-two-minute-rule/)**
  — David Allen. "Your mind is for having ideas, not holding them" — open loops must live in a
  trusted external system. Every captured item forced through one binary question (actionable or
  not?) before filing. Processing must end in a decision (do/defer/delegate/drop), never in an item
  just sitting there.
- **[obsidian-Smart2Brain](https://github.com/your-papa/obsidian-Smart2Brain)** — vault embedded
  into vectors, chat-with-your-notes RAG, fully offline via Ollama or optional OpenAI.
- **[claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)** — closest existing analog
  to maxvo. Implements the "LLM Wiki" pattern (Karpathy): Claude reads/writes plain markdown
  directly instead of vector search, continuously cross-linking new material and generating
  periodic briefings. Requires reviewing/approving an operation hash before any vault mutation — a
  deliberate guard against silent, un-auditable AI edits.
- **[Obsidian Copilot](https://github.com/logancyang/obsidian-copilot)** — chat UI embedded in
  Obsidian, bring-your-own-LLM, "Vault QA" semantic search mode. The most widely-adopted example of
  the "chat panel next to your notes" style, distinct from claude-obsidian's background-agent style.
- **["Is the GTD System ADHD-Friendly?"](https://workbrighter.co/gtd-adhd/)** — Work Brighter.
  GTD's biggest value for ADHD isn't the full system, it's the next-action breakdown habit ("book
  haircut" → 5 concrete steps) — the same task-chaining logic `docs/daily-rituals.md` already uses.
  Author deliberately rejected the standard two-minute rule (broke focus on the current task) in
  favor of always capture-and-defer.
- **[External Systems for ADHD at Work](https://www.scienceworkshealth.com/post/external-systems-for-adhd-at-work)**
  — ScienceWorks Health. Externalization is a legitimate accommodation, not a workaround to
  "graduate" from. Any external system must be visible, automatic, and present at the exact point of
  performance, or it won't get used.

## Memory & personalization architecture

- **[MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)** — UC Berkeley.
  Treats the context window as constrained RAM; gives the LLM tools to page information between
  in-context "core memory" and out-of-context "archival/recall" stores — the model manages its own
  memory via function calls. Became the design basis for Letta.
- **[Letta memory blocks](https://docs.letta.com/guides/agents/memory-blocks/)** / **[archival memory](https://docs.letta.com/guides/core-concepts/memory/archival-memory)**
  — each memory block has a label + description + value + character limit; the *description* is
  what the agent reads to decide how to use the block — vague descriptions produce misuse. External
  writes fully overwrite a block rather than append (read-modify-write needed). Archival memory is
  the contrasting tier: vector-searchable, queried on demand, for facts too voluminous to pin in
  context.
- **[Cognitive Architectures for Language Agents (CoALA)](https://arxiv.org/abs/2309.02427)** —
  Princeton. Standard taxonomy: working (ephemeral scratchpad), episodic (past decision-cycle
  experience), semantic (durable facts, incrementally built), procedural (how-to knowledge).
  Something belongs in long-term memory only if it has enduring utility for a *future* decision, not
  because it happened.
- **[SOTA RAG & Memory without the database](https://www.nijho.lt/post/file-based-rag-memory/)** —
  Bas Nijholt. One markdown file per fact, explicit ADD/UPDATE/DELETE reconciliation run by the LLM
  (never silent accumulation), deleted facts moved to a `deleted/` folder rather than purged — git
  gives free audit history and `git reset --hard` as an undo button. Switch to a vector DB only for
  high-volume, multi-tenant, or heavy semantic-paraphrase search — not the common single-user case.
- **[Mem0](https://arxiv.org/abs/2504.19413)** — an extraction phase turns a conversation turn into
  a candidate memory, then an update phase compares it against existing similar memories and
  applies add/update/merge/no-op rather than always appending — what keeps a store from growing
  unboundedly with restated or superseded facts.
- **["Is Agent Memory a Database?"](https://arxiv.org/abs/2605.26252)** — Concordia Data Systems
  Lab. Four recurring failure modes: **unregulated growth** (nothing ever removed), **missing
  semantic revision** (contradictions accumulate instead of superseding), **capacity-driven
  forgetting** (things dropped only because storage is full, not because they're stale), **read-only
  retrieval** (fetched but never corrected). Fix: treat memory as a state machine with four
  first-class operators — ingestion, revision, forgetting, retrieval.
- **[Context Rot (Chroma)](https://www.trychroma.com/research/context-rot)** — all 18 tested
  frontier models degrade well before hitting their context limit, tracked by semantic
  similarity/ambiguity and distractor content, not raw token count. Curating what's loaded matters
  more than window size.
- **["Remembering More, Risking More"](https://arxiv.org/html/2605.17830v1)** — Virginia Tech.
  Memory-induced problem behavior grows with accumulated content and exposure length. Detectable at
  the retrieval step before generation — argues for a "check what's about to be recalled" gate.

## ADHD-specific assistive design

- **[Barkley — EF and Self-Regulation in ADHD](https://www.russellbarkley.org/factsheets/ADHD_EF_and_SR.pdf)**
  — Russell Barkley. "Temporal myopia": the ADHD brain over-weights immediate over future
  information, so purely internal/mental task tracking fails structurally. Prescription:
  externalize at the *point of performance* — visible reminders exactly where and when the action
  needs to happen, not just recorded for later recall.
- **[The Brown Model of ADD/ADHD](https://www.brownadhdclinic.com/brown-ef-model-adhd)** — Thomas
  Brown (Yale). Six EF clusters: Activation, Focus, Effort, **Emotion**, Memory, Action — notable
  for treating emotional self-regulation as a core deficit, not a side effect. Task-support systems
  should account for emotional friction around a task, not just logistics.
- **Gawrilow & Gollwitzer (2008), [implementation intentions](https://link.springer.com/article/10.1007/s10608-007-9150-1)**
  — children with ADHD who formed a specific if-then plan ("if X occurs, I will do Y") matched
  non-ADHD performance on a response-inhibition task. Pre-committing to a trigger→action pairing
  measurably improves follow-through, vs. an open-ended intention.
- **[Pauli-Pott, Mann & Becker (2020) meta-analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC8505290/)**
  — across 35 RCTs, ongoing external scaffolding during a task produced a large effect (d=0.95) vs.
  negligible effect from isolated skill-drilling alone (d=0.17). The presence of scaffolding during
  execution is what reduces symptom impact, not upfront training.
- **["The ADHD Body Double"](https://add.org/the-body-double/)** — Linda Anderson/ADDA. Fixed time
  block with another person co-present (not instructing) reliably increases follow-through even
  with zero task-specific interaction. Evidence base is anecdotal/clinical-observation, not RCT.
- **["You Are Not Alone" — AI body doubling in VR](https://arxiv.org/abs/2509.12153)** — both human
  and AI doubling beat solo work on completion speed and perceived focus; some participants
  preferred the AI double for removing social-judgment anxiety while keeping accountability. Design
  implications: a visible shared progress indicator, small milestone/self-talk cues rather than
  silent monitoring.
- **Sarah Ward's "Get Ready · Do · Done" (360 Thinking™)** — targets the future-based-cognition
  deficit directly: build a concrete mental image of the *finished state* first, then work backward
  to what's needed, only then the action steps — rather than starting from step one forward.
- **Dawson & Guare, "Smart but Scattered" (12 Executive Skills)** — for a weak executive skill,
  don't train it directly: modify the environment, modify the task, set an external deadline,
  externalize the target behavior. Starts from "which executive skill is weak here" rather than a
  generic universal workflow.
- **["A little bit of a life raft" (OZCHI 2025)](https://dl.acm.org/doi/10.1145/3764687.3764713)** —
  7-day diary + interview study of 13 adults with ADHD using ChatGPT regularly: appropriated
  specifically for executive-functioning support and communication rehearsal (drafting/practicing a
  hard message before a real conversation), not just task-tracking.
- **[JMIR Preprint #85013 — AI Virtual Assistant for young people with ADHD](https://preprints.jmir.org/preprint/85013/accepted)**
  — co-design study with ADHD users themselves as design partners. The methodological contribution
  (co-design with the actual user population) matters more than the specific prototype.
