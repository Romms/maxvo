---
tags: [projects]
date: 2026-08-02
---

# AI Personal Assistant Best Practices — Research Notes

Compiled 2026-08-02, via parallel research across five angles; refreshed 2026-08-03 with a targeted
second pass per category (see below). Not `@`-imported into `CLAUDE.md`: it's reference material for
the comparison below, not something every session needs loaded.

## Порівняння з поточною архітектурою maxvo (2026-08-02, оновлено 2026-08-03)

Що вже покрито добре — і що є справжньою прогалиною, зіставлено джерело за джерелом проти
`CLAUDE.md`, усіх `docs/`, усіх `.claude/skills/*/SKILL.md` і auto-memory системи.

**Вже добре покрито** (не потребує змін): прогресивне розкриття skills (frontmatter опис = what+when,
тіло skillـa лаконічне); розділення capture/organize (Inbox → щотижневий checkin, точно як CODE);
ланцюжок мікрокроків замість одного першого кроку (task breakdown у `daily-rituals.md` — уже прямо
посилається на ADHD-адаптацію GTD); критерій завершення як образ фінішу, а не "зробити X" (Sarah
Ward's "Get Ready·Do·Done", хоч і не усвідомлено звідти); "не тренувати слабку функцію, а змінити
середовище" (Dawson & Guare) — це буквально принцип "complete him, don't correct him" з operating
guide; auto-memory — файлова, git-аудійована, з описом що визначає використання (Letta memory
blocks), оновлюється а не тільки додається (Mem0); voice-capture явно трактує диктовку як контент, не
команди (інстинктивний захист від lethal trifecta); дефолт на один послідовний skill замість рою
підагентів (Cognition's "Don't Build Multi-Agents"); усі 8 skills тепер англійською в інструкційній
прозі (українські репліки для Романа й vault-термінологія — Активні/Ідеї/Check-in тощо — без змін) —
консистентність, порушена наполовину перекладеним станом, усунена 2026-08-03.

**Зроблено / у процесі**:
1. **Нагадування в точці дії** (обрано першим 2026-08-02) — правило описано в `docs/capture-system.md`
   і 5 skills (checkin/evening-checkin/work-assistant/unstuck/voice-capture). Лишилось: створити
   календар `Нагадування`, backfill 13 існуючих рядків — станеться при першому запуску skill із
   доступом до Google Calendar (див. Активні рядок).
2. **PARA "Areas"** (обрано другим 2026-08-03) — реалізовано: `vault/Areas/README.md` (індекс) +
   `vault/Areas/Health/` (перший Area, `Blood Pressure.md` перенесено з кореня vault), dormancy-
   check доданий у щотижневий `checkin`. Готово повністю, без залежності від зовнішніх інструментів.

**Досі відкриті прогалини — тепер із конкретним дизайном, не просто назвою** (після цілеспрямованого
повторного дослідження 2026-08-03, по кожній зокрема, а не загального повторного пошуку). Роман ще
не обирав, яку з цих двох брати третьою:

1. **Evals/фідбек-цикл на якість ритуалів** — конкретний план тепер є: невеликий eval-файл на кожен
   skill (10-20 кейсів, зібраних із реальних виправлень Романа — explicit invocation + implicit
   trigger + negative control), спочатку детермінований trace-check, rubric лише за потреби (OpenAI
   "Testing Agent Skills Systematically"; Claude skill-creator's Eval-режим). Дешевий субститут
   постійного моніторингу: "прочитати N останніх Daily notes щотижня" + рахувати override/correction
   rate Романа як безкоштовний сигнал (Anthropic "Demystifying Evals" — capability vs regression
   evals, grade outcome окремо від transcript).
2. **Ритуал перегляду auto-memory** — конкретний паттерн тепер є: не редагувати memory-файли на
   місці, а раз на тиждень/два генерувати пропоновану консолідовану версію окремо для затвердження
   (Claude's Dreams-паттерн: read store + recent transcripts → new separate output, input store не
   чіпається); при суперечності — always supersede, never delete (0Latency contradiction-detection);
   архівувати, якщо пам'ять 30+ днів не використовувалась (AI Agent Memory Design Guide);
   найважливіше застереження — не довіряти самій моделі самостійно позначати застарілість (STALE
   benchmark: frontier LLMs ловлять implicit conflict лише ~55% випадків), тому перевірка має бути
   окремим детермінованим кроком, а не "запитати Клода чи щось застаріло".

**Менші/новіші можливості — тепер із конкретнішою структурою**:
1. **AI body doubling** — головна небезпека виявлена дослідженням: уникати gamification/рахунку/
   стріків (учасники досліджень явно боялись over-reliance на систему) — сесія відкривається
   завданням + рівнем енергії, лишається тихою/амбієнтною під час роботи (переривати лише короткою
   афірмацією чи fatigue-нагадуванням за поведінковим порогом — неактивність, "кружляння" між
   задачами — не за фіксованим інтервалом), закривається рефлексією ("що здивувало в цій сесії"), не
   оцінкою.
2. **Прорепетирувати важку розмову** — конкретна структура тепер є: визначити мету спершу (коучинг
   нової техніки vs. практика відомої — по-різному, чи має AI підказувати), налаштувати опір
   "співрозмовника" явно ("не роби це легким для мене" — інакше кооперативний strawman вбиває сенс
   вправи), репетирувати саме гілку невдачі ("як це може піти не так"), і закрити цикл після реальної
   розмови — що насправді сталось.

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
- **[Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)**
  — Anthropic Engineering (Jan 2026). Separate **capability evals** (low pass rate, "what can it
  do") from **regression evals** (should sit ~100%, "did it stop doing what it used to") — mature
  capability evals graduate into regression suites over time. Grade **outcome** (actual end-state)
  separately from the transcript; use **pass^k** (all k trials succeed), not pass@k, when judging
  user-facing reliability.
- **[Test, measure, and refine Agent Skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)**
  — Claude blog (Mar 2026). skill-creator's Create/Eval/Improve/Benchmark modes: verifiable
  assertions per task prompt, with-skill vs. baseline runs graded by a sub-agent, pass-rate/tokens/
  time tracked per iteration. For subjective/workflow-style skills, falls back to human qualitative
  review instead of forcing brittle assertions.
- **[Memory for Claude Managed Agents](https://claude.com/blog/claude-managed-agents-memory)** —
  (Apr 2026, public beta). File-based memory with per-write audit logs (which agent/session wrote
  what) and the ability to roll back to an earlier version or redact specific content.
- **[Dreams](https://platform.claude.com/docs/en/managed-agents/dreams)** — research preview
  (~May 2026). A scheduled/on-demand job reads the memory store plus recent transcripts and produces
  a *new, separate* output store — duplicates merged, stale/contradicted entries replaced, new
  insights surfaced — while never modifying the input store in place, so the result can be reviewed
  and discarded if bad.

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
- **["Learning Personalized Agents from Human Feedback"](https://arxiv.org/html/2602.16173v1)** — a
  3-step loop: pre-action clarification → ground the action in memory-stored preferences →
  post-action correction updates memory when a preference drifted. The third step is usually the
  missing piece — a correction should routinely get written back to memory, not just applied once.
- **[Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)**
  — OpenAI. Per-skill sets of 10-20 prompts (explicit invocation + implicit trigger + negative
  control), deterministic trace-check first, rubric grading second, grown from real failures rather
  than predicted upfront — small enough to run without a product-scale eval pipeline.
- **["Always-On Agents" survey](https://arxiv.org/pdf/2606.30306)** — reframes persistent-state
  agents around a full lifecycle (write/validate/organize/retrieve/act/update/**forget/audit/
  rollback**) across 6 dimensions; explicitly calls out that the field over-indexes on accumulation/
  retrieval and under-indexes on governing/forgetting/rollback.
- Cross-session continuity benchmarks (**π-Bench**, arxiv.org/abs/2605.14678; **PAUSE**,
  arxiv.org/html/2607.27354v1; **LifeSide**, arxiv.org/pdf/2606.04660) — all stress whether an agent
  *proactively* surfaces stored state rather than waiting to be asked, over multi-month timelines —
  confirms morning-checkin's "surface uncertain-deadline rows unasked" instinct is the right kind of
  metric, even without off-the-shelf single-user tooling to benchmark against.

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
- **["The PARA Method" — Forte Labs](https://fortelabs.com/blog/para/)**, revisited — Areas are
  "important parts of your work and life that require ongoing attention," no completion state,
  contrasted with Projects (short-term, defined goal + deadline); the personal-life example list
  explicitly names Health, Finances, Kids, Car, Home as Areas.
- **["How to Use PARA in an AI Second Brain"](https://www.iwoszapar.com/p/para-method-ai-second-brain)**
  — for an AI-managed vault specifically: Areas hold facts/standards (reference, current state)
  while Projects hold goal+deadline+open decisions; an Area needs a **dormancy check** instead of a
  deadline as its review trigger.
- **["How to Build an AI Second Brain That Evolves Over Time"](https://www.mindstudio.ai/blog/ai-second-brain-claude-code-obsidian-architecture)**
  — MindStudio. Recommends a daily lightweight heartbeat (5-10 min) plus a weekly deep review
  (30-60 min) as two distinct loops — maxvo's morning/evening rituals + weekly `checkin` already are
  this split.
- **Obsidian's official CLI (v1.12, Feb 2026) + [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)**
  — Obsidian's own team now ships first-party Claude-Code/Codex agent skills (`obsidian-bases`,
  `obsidian-cli`, `defuddle` for web-capture-to-markdown) — worth a look for `vault/Projects/
  README.md`'s hand-rolled table and for the Inbox capture pipeline.

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
- **[AI Agent Memory Design Guide](https://hidekazu-konishi.com/entry/ai_agent_memory_design_guide.html)**
  — a concrete decay formula (similarity × recency-half-life × reinforcement × confidence) and a
  cadence: weekly/bi-weekly review for personal assistants with no external event hooks; archive
  once a memory sits below threshold 30+ days unretrieved.
- **[How to evaluate agent memory](https://labelstud.io/learningcenter/how-to-evaluate-agent-memory/)**
  — automated regression checks on every memory-architecture change, plus human trace review on a
  fixed weekly-or-per-release cadence, targeted at the hardest 5-10% of traces (conflict resolution,
  drifted preferences) rather than the whole store.
- **[Memory eviction and forgetting in AI agents](https://mem0.ai/blog/memory-eviction-and-forgetting-in-ai-agents)**
  — Mem0. Passive TTL/decay handles bulk noise automatically; active reconciliation happens at write
  time (new fact compared against top-k similar existing memories before committing); manual review
  triggers specifically on new contradictions or storage thresholds, not a fixed clock.
- **[STALE benchmark](https://arxiv.org/abs/2605.06527)** — names "Implicit Conflict" (new evidence
  invalidates an old memory without explicit negation) and finds frontier LLMs self-catch it only
  ~55% of the time — don't trust a model to self-flag its own memory as stale.
- **[Contradiction-detection workflow — 0Latency](https://0latency.ai/blog/contradiction-detection.html)**
  — semantic-similarity+polarity check, entity-attribute conflict tracking, temporal windowing (so
  two facts months apart aren't falsely flagged); resolution should always **supersede, never
  delete**.
- **["Don't Ask the LLM to Track Freshness"](https://arxiv.org/abs/2606.01435)** — a deterministic
  recency-field `max()` aggregation at retrieval time beats LLM-judged freshness — the failure point
  is assembly, not storage.

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
- **["Toward Neurodivergent-Aware Productivity"](https://arxiv.org/html/2507.06864)** — nudges fire
  off *behavioral thresholds* (tab-churn, inactivity, failed re-entry into a task), not a fixed
  Pomodoro-style interval; AI stays ambient/silent by default, breaking silence only for a short
  affirmation or fatigue nudge. Explicitly never a "performance ledger" — no ranking/streaks/
  gamification, since users specifically feared over-reliance on the system.
- **["Not Just Me and My To-Do List"](https://arxiv.org/html/2603.17258v1)** — CHI 2026. A focus
  session opens with task + energy-level, stays low-friction during, and closes with a narrative
  reflection ("what surprised you about this session?") rather than a score — "a companion, not a
  manager."
- **OpenClaw's shipped "ADHD Body Doubling" skill** (clawbot.ai) — a working reference
  implementation: micro-step protocols, frequent check-ins, a named "dopamine reset" mechanic,
  session history tracking.
- **[Rehearsable.ai design notes](https://rehearsable.ai/blog/ten-tips-for-creating-ai-role-play-scenarios)**
  — decide purpose first (coach a new technique vs. practice a known one changes whether the AI
  should interject); configure the simulated counterpart's resistance explicitly ("push back the way
  you think they would, don't make it easy for me") — a cooperative-strawman AI defeats the point.
  Rehearse the failure branch specifically ("what's the most likely way this goes badly"), and close
  the loop afterward by describing what actually happened.
- **["Scaffolding Metacognition with GenAI"](https://arxiv.org/html/2602.09381v1)** — CHI 2026. Core
  principle: "promote reflection, not automation" — full task outsourcing erodes metacognitive
  skill; also recommends normalizing incompletion *during planning itself* to preempt anxiety about
  not finishing.
