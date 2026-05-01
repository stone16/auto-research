# Auto Research Run Design — Growth Engine From Scratch

**Date**: 2026-05-01
**Status**: Draft (pending cross-model peer review by Codex via `/review-loop`)
**Run path (target)**: `runs/growth-engine-from-scratch/` (initialized after design lock)
**Source corpus**: `~/dev/getuai/` (~64 repos, ~985 skill files)

---

## 1. Goal

Synthesize, from the ~64 repositories under `~/dev/getuai/`, a from-scratch playbook for
building a growth engine: the architecture (how the system is wired), the reusable skills
(what units of work exist, how they are invoked and maintained), and the practitioner
cognitive models (what mental frames the people who built these repos applied).

The deliverable is a `knowledge_base.md` that gives a small team starting Day 1 a
defensible build sequence and decision frame across four growth domains — SEO/GEO, Content
Writing, Ads management, and Social media — plus the cross-cutting infrastructure and
failure-mode discipline that ties them together.

This is not a code-generation run. It is a research-and-synthesis run whose output guides
later code work.

## 2. Non-Goals

- Code-from-scratch implementation. The KB is design knowledge, not code.
- Coverage of repos outside `~/dev/getuai/`.
- Treating any single existing project (including `getuai/growth-engine` and
  `getuai/growth-engine-legacy`) as the canonical answer. They are peer evidence among 64.
- Generic growth-marketing advice not grounded in the corpus.
- Live experimentation. The corpus IS the empirical evidence; this run does not run
  campaigns or A/B tests.

## 3. Source Set Strategy

The corpus has ~985 skill `.md` files plus thousands of source files. It cannot be loaded
into context directly. Pre-extract into 10 curated `source-*.md` files placed under
`runs/growth-engine-from-scratch/sources/`. Each file is a structured digest, not a raw
dump — it must contain enough verbatim references (file paths, function names, prompt
templates, schema definitions) for the producer to ground claims to specific repo
locations during iteration.

| Source file                          | Primary repos to extract from                                                                                                                                    | Section types to capture                                                                                                  |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `source-seo-geo.md`                  | `geo-aeo`, `geo-seo-v2`, `geowriter`, `getuai-seo`, `rankgale`, `rankncompare`, `rankncompare_v2`, `seo-poster`                                                   | Architecture diagrams from READMEs, ranking-data ingestion, GEO-specific patterns, content publishing flow                |
| `source-content-writing.md`          | `geowriter`, `seo-poster`, `getuai-email-2.0`; content-touching parts of `openclaw-marketing`, `OpenBox-Marketing`, `Vibe-marketing`, `LLMRush`                   | Prompt templates, voice/tone systems, multi-lingual handling, draft-edit-publish stages, human-review insertion points    |
| `source-ads.md`                      | `getuai-ads`, `getuai-ads-attribution`, `getuai-ads-attribution-sdk`, `getuai-ads-data`, `getuai-ads-sdk`, `getu_ads_v2`, `attribution_v2`, `Fast-Attribution`, `ads-library`, `facebook-ads-library-api-demo` | Campaign feed schemas, bidding logic, attribution models, anomaly detection, budget pacing                                |
| `source-social.md`                   | `reddit-scount`, `x-api-credit-monitor`, `youtube-api-demo`; social-touching parts of `openclaw-marketing`                                                        | Listening pipelines, posting schedulers, multi-platform abstractions, rate-limit handling, engagement loops               |
| `source-shared-infra.md`             | `getuai-api`, `getuai-console`, `getuai-ui`, `getuai-auth-center`, `getuai-mvp`, `getuai-plugin`, `Pi`, `Visionary`, `clawcloud`, `cloud-claw-k`, `valuecell`, `project-base`, `optiminds-org-config`, `optiminds-repo-template` | Identity, data models, queue/scheduler, observability, LLM gateway, deployment pattern, repo-template conventions          |
| `source-skills-catalog.md`           | All repos' `skills/`, `.claude/skills/`, `.cursor/skills/`, `.agents/skills/` directories                                                                          | Structured table per skill: path, frontmatter (name/description), invocation surface, maintenance signals (last-modified, recent commits) |
| `source-cognitive-models.md`         | All repos' `CLAUDE.md`, `AGENTS.md`, `README.md`, top-level `docs/`                                                                                                | Verbatim "hard rules", do/don't lists, decision criteria, sequencing prescriptions, mental models stated in prose         |
| `source-failure-modes.md`            | `growth-engine-legacy`, deprecated paths, abandoned branches, `legacy/`, `archive/` subdirs, `_old` files; commit messages mentioning "revert", "abandon", "deprecate" | Each failure: symptom, repo evidence (file:line + commit hash), root cause if stated, what replaced it                    |
| `source-vertical-cases.md`           | `lawyer_marketing`, `lawyer_finder`, `law-intake`, `cuilawgroup`; case-study writeups in `docs/`                                                                  | Domain-specific instantiations: how the generic patterns adapt to one vertical (legal), what was added/removed             |
| `source-platform-prototypes.md`      | `0407-prototype`, `0408-prototype`, `getuai-2.0`, `getuai-mvp`, `gmi-prototype`, `getuai-comp-analysis-demo`, `getuai-competitor-analysis`                          | In-flight design choices, what was tried in v0/v1/v2, naming/structure evolution, stated rationale                         |

Extraction is a separate workstream that happens before the run starts (likely via a
`scripts/extract-sources.py` driven by `harness-engineering-skills:harness-generator` or
manually). The benchmark and run config in this doc assume those 10 source files exist.

## 4. Benchmark Structure

3 layers (Architecture, Skill, Cognition) × 4 domains (SEO/GEO, Content, Ads, Social) =
12 cells, plus 3 integration questions for cross-domain synthesis = 15 total.

Question order is by **layer first, then domain** (A1-A4 → S1-S4 → C1-C4 → I1-I3). This
lets each iteration of the producer focus on one layer (architecture today, skills tomorrow,
cognition the day after), keeping the KB internally coherent rather than chasing 15
independent dimensions per round.

| #   | Cell    | Domain          | Layer        |
| --- | ------- | --------------- | ------------ |
| Q1  | A1      | SEO/GEO         | Architecture |
| Q2  | A2      | Content Writing | Architecture |
| Q3  | A3      | Ads             | Architecture |
| Q4  | A4      | Social          | Architecture |
| Q5  | S1      | SEO/GEO         | Skill        |
| Q6  | S2      | Content Writing | Skill        |
| Q7  | S3      | Ads             | Skill        |
| Q8  | S4      | Social          | Skill        |
| Q9  | C1      | SEO/GEO         | Cognition    |
| Q10 | C2      | Content Writing | Cognition    |
| Q11 | C3      | Ads             | Cognition    |
| Q12 | C4      | Social          | Cognition    |
| Q13 | I1      | (cross)         | Shared infra |
| Q14 | I2      | (cross)         | Build sequence |
| Q15 | I3      | (cross)         | Failure modes |

## 5. Benchmark Questions

Format mirrors the framework's `benchmark.json` schema (`id`, `question`, `rubric`,
`must_include`, `required_sources`).

### Q1 — A1: SEO/GEO Architecture

```json
{
  "id": "q1",
  "question": "Reading across the SEO/GEO repos in getuai/, what from-scratch architecture for a SEO/GEO subsystem emerges as the converged pattern — components, data stores, external dependencies, and human-in-loop control points — and where do these repos disagree about that pattern?",
  "rubric": "Specify the components (crawler, ranking sensor, content store, generator, publisher, evaluator) and their data flow with explicit interfaces. Name external dependencies (search APIs, LLM providers, CMS) and their failure handling. Identify human-in-loop control points (approval, override, kill-switch). For every architectural claim, cite at least one repo:file:line. Where repos disagree (e.g., one uses pull-based ranking checks, another push-based webhooks), name both repos and state the trade-off. Penalize answers that describe an aspirational design not actually present in code.",
  "rubric_criteria": [
    {"id": "q1.r1", "weight": 1.0, "criterion": "Components (crawler, ranking sensor, content store, generator, publisher, evaluator) named AND data flow specified with explicit interfaces"},
    {"id": "q1.r2", "weight": 1.0, "criterion": "External dependencies (search APIs, LLM providers, CMS) named with explicit failure handling per dependency"},
    {"id": "q1.r3", "weight": 1.0, "criterion": "Human-in-loop control points (approval, override, kill-switch) identified with repo evidence"},
    {"id": "q1.r4", "weight": 1.0, "criterion": "Every architectural claim cites at least one repo:file:line"},
    {"id": "q1.r5", "weight": 1.0, "criterion": "Where repos disagree, both repos named AND the trade-off stated"}
  ],
  "penalty_criteria": [
    {"id": "q1.p1", "deduction": 0.15, "trigger": "Any architectural claim is aspirational rather than present-in-code (uncitable to a real implementation)"}
  ],
  "must_include": [
    "components",
    "data flow",
    "external dependencies",
    "ranking signal source",
    "content store",
    "human-in-loop",
    "kill-switch",
    "convergence",
    "disagreement",
    "file:line"
  ],
  "required_sources": [
    "source-seo-geo",
    "source-shared-infra"
  ]
}
```

### Q2 — A2: Content Writing Architecture

```json
{
  "id": "q2",
  "question": "From the corpus, what is the from-scratch architecture of a Content Writing subsystem — the stages from ideation through publish, the role of LLMs at each stage, and the human-review insertion points — and which choices in this architecture are load-bearing versus stylistic?",
  "rubric": "Walk the pipeline: ideation, outline, draft, edit, publish, post-publish iteration. For each stage, name LLM role (none / generator / critic / orchestrator), input contract, output contract, and the human-review hook if any. Distinguish load-bearing choices (those whose change breaks correctness, e.g. mandatory style-guide injection) from stylistic ones (e.g. which template format). Cite repo:file:line for each pipeline component. Penalize generic 'agent writes blog post' answers without stage-by-stage decomposition.",
  "rubric_criteria": [
    {"id": "q2.r1", "weight": 1.0, "criterion": "Pipeline stages (ideation, outline, draft, edit, publish, post-publish) walked with input/output contracts per stage"},
    {"id": "q2.r2", "weight": 1.0, "criterion": "LLM role per stage named (none / generator / critic / orchestrator) with repo evidence"},
    {"id": "q2.r3", "weight": 1.0, "criterion": "Human-review hooks identified with specific repo evidence per hook"},
    {"id": "q2.r4", "weight": 1.0, "criterion": "Load-bearing vs stylistic choices distinguished with reasoning, with at least 2 examples on each side"},
    {"id": "q2.r5", "weight": 1.0, "criterion": "Every pipeline component cites repo:file:line"}
  ],
  "penalty_criteria": [
    {"id": "q2.p1", "deduction": 0.15, "trigger": "Generic 'agent writes blog post' framing without stage-by-stage decomposition"}
  ],
  "must_include": [
    "ideation",
    "outline",
    "draft",
    "edit",
    "publish",
    "LLM role",
    "human review point",
    "style guide injection",
    "load-bearing",
    "file:line"
  ],
  "required_sources": [
    "source-content-writing",
    "source-shared-infra"
  ]
}
```

### Q3 — A3: Ads Architecture

```json
{
  "id": "q3",
  "question": "What from-scratch architecture for an Ads management subsystem emerges from the getuai/getuai-ads* and attribution repos — the closed loop of campaign feed → bidding → reporting → attribution → optimization — and how are the boundaries between platform-API integration and platform-agnostic logic drawn?",
  "rubric": "Specify the closed loop end-to-end. Name the data model for campaigns, ad groups, creatives, conversions. Describe bidding strategy implementation, attribution model implementation, anomaly detection. State explicitly where platform-specific code lives (e.g. Google Ads vs Facebook Ads) versus where shared business logic sits. Cite repo:file:line for each boundary. Penalize answers that conflate the closed-loop with platform SDKs without naming the abstraction layer.",
  "rubric_criteria": [
    {"id": "q3.r1", "weight": 1.0, "criterion": "Closed loop (campaign feed → bidding → reporting → attribution → optimization) specified end-to-end with data flows"},
    {"id": "q3.r2", "weight": 1.0, "criterion": "Data model for campaigns, ad groups, creatives, conversions explicitly named with field-level detail"},
    {"id": "q3.r3", "weight": 1.0, "criterion": "Bidding strategy, attribution model, anomaly detection implementations cited"},
    {"id": "q3.r4", "weight": 1.0, "criterion": "Platform-specific code vs platform-agnostic logic boundary explicitly drawn with file:line"},
    {"id": "q3.r5", "weight": 1.0, "criterion": "Every architectural claim cites repo:file:line"}
  ],
  "penalty_criteria": [
    {"id": "q3.p1", "deduction": 0.15, "trigger": "Conflating the closed loop with platform SDKs without naming the abstraction layer"}
  ],
  "must_include": [
    "campaign feed",
    "bidding",
    "reporting",
    "attribution model",
    "conversion event",
    "budget pacing",
    "anomaly detection",
    "platform-agnostic boundary",
    "data model",
    "file:line"
  ],
  "required_sources": [
    "source-ads",
    "source-shared-infra"
  ]
}
```

### Q4 — A4: Social Architecture

```json
{
  "id": "q4",
  "question": "From reddit-scount, x-api-credit-monitor, youtube-api-demo and the social-touching parts of openclaw-marketing, what from-scratch architecture for a Social media subsystem emerges — covering listen, post, schedule, engage, monitor — and what unifying abstraction (if any) lets one engine speak to multiple platforms without an N×M explosion?",
  "rubric": "Decompose into the listen / post / schedule / engage / monitor surfaces. Name the multi-platform abstraction (or admit none exists in the corpus, with evidence). Specify rate-limit and credit accounting (x-api-credit-monitor is a strong signal here). Specify content-moderation insertion point. Cite repo:file:line. Penalize answers that assume a unified abstraction without finding it in code; an honest 'corpus uses N adapters with no shared abstraction' is worth more than a fictitious clean design.",
  "rubric_criteria": [
    {"id": "q4.r1", "weight": 1.0, "criterion": "All five surfaces (listen, post, schedule, engage, monitor) decomposed with per-surface contracts"},
    {"id": "q4.r2", "weight": 1.0, "criterion": "Multi-platform abstraction named OR honest 'no shared abstraction' verdict given with corpus evidence"},
    {"id": "q4.r3", "weight": 1.0, "criterion": "Rate-limit and credit accounting cited (x-api-credit-monitor or equivalent)"},
    {"id": "q4.r4", "weight": 1.0, "criterion": "Content moderation insertion point identified with repo evidence"},
    {"id": "q4.r5", "weight": 1.0, "criterion": "Every architectural claim cites repo:file:line"}
  ],
  "penalty_criteria": [
    {"id": "q4.p1", "deduction": 0.15, "trigger": "Assumed unified abstraction without finding it in code"}
  ],
  "must_include": [
    "listen",
    "post",
    "schedule",
    "engage",
    "monitor",
    "multi-platform abstraction",
    "rate limit",
    "credit accounting",
    "content moderation",
    "file:line"
  ],
  "required_sources": [
    "source-social",
    "source-shared-infra"
  ]
}
```

### Q5 — S1: SEO/GEO Skills

```json
{
  "id": "q5",
  "question": "What are the reusable skills in the SEO/GEO domain across the corpus — for each: what it does, how it is invoked, what parameters and output contract it enforces, what state it persists, and how it is maintained (versioning, dependencies, retries) — and which skills are duplicated across repos versus genuinely unique?",
  "rubric": "Enumerate the skills as a table with the 8-column contract from §8.3: skill_name, originating_repo, path_reference (the directory or file path under ~/dev/getuai/<repo>/... where the skill lives, with optional :LINE), invocation_surface (CLI / function call / agent message / cron), input_schema, output_schema, state_persistence, maintenance_signals (last-modified, recent commits, deprecation markers). For duplicates, name all repos that carry a near-equivalent and pick the canonical one with rationale. Penalize answers that list skill names without invocation/contract detail. Require at least 8 skills enumerated; no skill counts unless it has a path_reference that resolves under the corpus.",
  "rubric_criteria": [
    {"id": "q5.r1", "weight": 1.0, "criterion": "≥8 skills enumerated as a table with all 8 columns (skill_name, originating_repo, path_reference, invocation_surface, input_schema, output_schema, state_persistence, maintenance_signals) per the §8.3 contract"},
    {"id": "q5.r2", "weight": 1.0, "criterion": "Duplicates identified across repos with canonical pick + rationale"},
    {"id": "q5.r3", "weight": 1.0, "criterion": "Maintenance signals populated (last-modified, recent commits, deprecation markers), not stubbed"},
    {"id": "q5.r4", "weight": 1.0, "criterion": "Each skill row's path_reference resolves under ~/dev/getuai/<repo>/... (this is row identity, not a §6.3 citation; supporting claims in the row follow §6.3 per §6.2.1)"}
  ],
  "penalty_criteria": [
    {"id": "q5.p1", "deduction": 0.20, "trigger": "<8 skills enumerated OR skills listed without invocation/contract detail OR rows missing path reference"}
  ],
  "must_include": [
    "skill name",
    "invocation surface",
    "input schema",
    "output schema",
    "state persistence",
    "version",
    "deprecation",
    "duplicate",
    "canonical",
    "file:line"
  ],
  "required_sources": [
    "source-seo-geo",
    "source-skills-catalog"
  ]
}
```

### Q6 — S2: Content Writing Skills

```json
{
  "id": "q6",
  "question": "What are the reusable Content Writing skills in the corpus — prompt templates, voice/tone systems, multi-lingual handlers, image+text composers, evaluation rubrics — and how do these skills handle the brittleness problems unique to LLM-driven content (drift, hallucination, register collapse)?",
  "rubric": "Enumerate skills with the same 8-column table format as Q5 (§8.3 contract: skill_name, originating_repo, path_reference, invocation_surface, input_schema, output_schema, state_persistence, maintenance_signals). For each skill, name the brittleness problem it addresses (drift / hallucination / register collapse / factual contamination / language register / cultural fit) and the technique used (template variables / few-shot / critic loop / human review / retrieval grounding). Supporting claims (brittleness, technique) are cited per §6.3 / §6.2.1. Penalize answers that ignore brittleness or treat all LLM content generation as equivalent.",
  "rubric_criteria": [
    {"id": "q6.r1", "weight": 1.0, "criterion": "Skills enumerated as a table with all 8 columns per §8.3 contract (same as Q5)"},
    {"id": "q6.r2", "weight": 1.0, "criterion": "Each skill names the brittleness problem it addresses (drift / hallucination / register collapse / contamination / language register / cultural fit)"},
    {"id": "q6.r3", "weight": 1.0, "criterion": "Each skill names the mitigation technique (template variables / few-shot / critic loop / human review / retrieval grounding)"},
    {"id": "q6.r4", "weight": 1.0, "criterion": "Each skill row's path_reference resolves under ~/dev/getuai/; supporting brittleness/technique claims cite per §6.3 / §6.2.1"}
  ],
  "penalty_criteria": [
    {"id": "q6.p1", "deduction": 0.15, "trigger": "Treats LLM content generation as monolithic / ignores the brittleness dimension"}
  ],
  "must_include": [
    "prompt template",
    "voice and tone",
    "multi-lingual",
    "image and text",
    "evaluation rubric",
    "drift",
    "hallucination",
    "register",
    "retrieval grounding",
    "file:line"
  ],
  "required_sources": [
    "source-content-writing",
    "source-skills-catalog"
  ]
}
```

### Q7 — S3: Ads Skills

```json
{
  "id": "q7",
  "question": "What are the reusable Ads skills in the corpus — keyword analysis, bid strategy, creative generation, budget allocation, anomaly detection, A/B test orchestration — and which are explicitly platform-bound versus platform-agnostic, with the contract for the platform abstraction?",
  "rubric": "Enumerate skills. For each: platform-bound (which platform) vs platform-agnostic, abstraction contract if agnostic, dependence on attribution data, kill criteria embedded. Show repo:file:line evidence per skill. Penalize 'this skill exists for Google Ads' without invocation and contract detail.",
  "rubric_criteria": [
    {"id": "q7.r1", "weight": 1.0, "criterion": "Skills enumerated with table format covering keyword analysis, bid strategy, creative generation, budget allocation, anomaly detection, A/B test"},
    {"id": "q7.r2", "weight": 1.0, "criterion": "Platform-bound vs platform-agnostic explicitly tagged per skill"},
    {"id": "q7.r3", "weight": 1.0, "criterion": "Abstraction contract specified for platform-agnostic skills (interface and parameters)"},
    {"id": "q7.r4", "weight": 1.0, "criterion": "Kill criteria embedded per skill where applicable, with repo:file:line evidence"}
  ],
  "penalty_criteria": [
    {"id": "q7.p1", "deduction": 0.15, "trigger": "Skill listed without invocation/contract detail or platform classification"}
  ],
  "must_include": [
    "keyword analysis",
    "bid strategy",
    "creative generation",
    "budget allocation",
    "anomaly detection",
    "A/B test",
    "platform-bound",
    "platform-agnostic abstraction",
    "kill criteria",
    "file:line"
  ],
  "required_sources": [
    "source-ads",
    "source-skills-catalog"
  ]
}
```

### Q8 — S4: Social Skills

```json
{
  "id": "q8",
  "question": "What are the reusable Social skills — listening (topic / sentiment / mention), topic selection, multi-platform rewrite, scheduling, reply, sentiment classification — and how do they encode the platform-specific differences in tone, length, and engagement pattern without forking per platform?",
  "rubric": "Enumerate skills. For each: cross-platform versus per-platform, the parameterization that captures platform difference (max length, hashtag policy, mention semantics, image/video requirement), and the failure mode when the platform changes its API or rules. Cite repo:file:line. Penalize answers that pretend platforms are interchangeable.",
  "rubric_criteria": [
    {"id": "q8.r1", "weight": 1.0, "criterion": "Skills enumerated covering listening, topic selection, multi-platform rewrite, scheduling, reply, sentiment"},
    {"id": "q8.r2", "weight": 1.0, "criterion": "Cross-platform vs per-platform tagged per skill"},
    {"id": "q8.r3", "weight": 1.0, "criterion": "Parameterization captures platform difference (max length, hashtag policy, mention semantics, image/video requirement)"},
    {"id": "q8.r4", "weight": 1.0, "criterion": "Failure mode for each skill when the platform changes API or rules cited from repo evidence"}
  ],
  "penalty_criteria": [
    {"id": "q8.p1", "deduction": 0.15, "trigger": "Pretends platforms are interchangeable / lacks platform-difference parameterization"}
  ],
  "must_include": [
    "listening",
    "topic selection",
    "multi-platform rewrite",
    "scheduling",
    "reply",
    "sentiment",
    "platform difference",
    "parameterization",
    "API change failure",
    "file:line"
  ],
  "required_sources": [
    "source-social",
    "source-skills-catalog"
  ]
}
```

### Q9 — C1: SEO/GEO Cognitive Models

```json
{
  "id": "q9",
  "question": "What mental models do the SEO/GEO practitioners in the corpus apply when making decisions — topical authority, E-E-A-T, the GEO-vs-SEO pivot, intent mapping, content velocity vs depth — and where do these models prove right or wrong as evidenced by the repos?",
  "rubric": "Name each mental model explicitly. For each model: the canonical decision it shapes, the trigger conditions that invoke it, and at least one 'this model worked here' repo:file:line evidence AND one 'this model failed here' repo:file:line evidence (or commit message admitting failure). Identify at least 2 anti-patterns the corpus reveals. Penalize generic SEO advice not grounded in repo evidence; demand the model-evidence pairing.",
  "rubric_criteria": [
    {"id": "q9.r1", "weight": 1.0, "criterion": "≥3 mental models named explicitly (e.g., topical authority, E-E-A-T, GEO vs SEO pivot, intent mapping, content velocity vs depth)"},
    {"id": "q9.r2", "weight": 1.0, "criterion": "Each model has trigger conditions stated"},
    {"id": "q9.r3", "weight": 1.0, "criterion": "Each model has ≥1 'worked here' repo:file:line evidence (per §6.7, models without paired evidence score 0.0 in this clause)"},
    {"id": "q9.r4", "weight": 1.0, "criterion": "Each model has ≥1 'failed here' repo:file:line evidence (or commit message admitting failure)"},
    {"id": "q9.r5", "weight": 1.0, "criterion": "≥2 anti-patterns identified with corpus evidence"}
  ],
  "penalty_criteria": [
    {"id": "q9.p1", "deduction": 0.20, "trigger": "Generic SEO advice not grounded in repo evidence; reciting industry slogans"}
  ],
  "must_include": [
    "topical authority",
    "E-E-A-T",
    "GEO vs SEO",
    "intent mapping",
    "content velocity",
    "anti-pattern",
    "worked here",
    "failed here",
    "trigger condition",
    "file:line"
  ],
  "required_sources": [
    "source-seo-geo",
    "source-cognitive-models",
    "source-failure-modes"
  ]
}
```

### Q10 — C2: Content Writing Cognitive Models

```json
{
  "id": "q10",
  "question": "What cognitive frames do the content practitioners apply — user journey mapping, content portfolio theory, distribution-over-production, ROI time windows, brand voice as forcing function — and how do those frames shape the architecture and skill choices already documented in Q2 and Q6?",
  "rubric": "Name each cognitive frame, its decision-shaping role, and at least one 'worked' / 'failed' repo evidence pairing. Explicitly link each frame to a Q2 architecture choice or a Q6 skill choice (cross-question hook). Identify at least 2 anti-patterns. Penalize answers that treat content as a craft question rather than a system question.",
  "rubric_criteria": [
    {"id": "q10.r1", "weight": 1.0, "criterion": "≥3 cognitive frames named (e.g., user journey, content portfolio, distribution-over-production, ROI window, brand voice as forcing function)"},
    {"id": "q10.r2", "weight": 1.0, "criterion": "Each frame has its decision-shaping role explicitly stated"},
    {"id": "q10.r3", "weight": 1.0, "criterion": "Each frame has worked + failed repo evidence pairing (per §6.7, frames without paired evidence score 0.0 in this clause)"},
    {"id": "q10.r4", "weight": 1.0, "criterion": "Each frame is explicitly linked to a Q2 architecture choice OR a Q6 skill choice (cross-question hook)"},
    {"id": "q10.r5", "weight": 1.0, "criterion": "≥2 anti-patterns identified with corpus evidence"}
  ],
  "penalty_criteria": [
    {"id": "q10.p1", "deduction": 0.15, "trigger": "Treats content as craft rather than system; no Q2/Q6 cross-references"}
  ],
  "must_include": [
    "user journey",
    "content portfolio",
    "distribution over production",
    "ROI window",
    "brand voice",
    "anti-pattern",
    "worked here",
    "failed here",
    "links to Q2",
    "links to Q6"
  ],
  "required_sources": [
    "source-content-writing",
    "source-cognitive-models",
    "source-failure-modes"
  ]
}
```

### Q11 — C3: Ads Cognitive Models

```json
{
  "id": "q11",
  "question": "What mental models do the ads practitioners apply — LTV/CAC discipline, pacing logic, creative fatigue curves, attribution paradox, kill-vs-double-down criteria — and how do they survive contact with the realities of platform algorithm changes and attribution windows?",
  "rubric": "Name each model, the decision it shapes, the conditions where it holds, and the conditions where it breaks (with repo evidence). Provide at least 2 'this model survived a platform change here' or 'broke here' pairings. Demand explicit kill-vs-scale criteria. Penalize answers that recite ads-buyer slogans without naming the breakage conditions in the corpus.",
  "rubric_criteria": [
    {"id": "q11.r1", "weight": 1.0, "criterion": "≥3 mental models named (e.g., LTV/CAC, pacing, creative fatigue, attribution paradox, kill-vs-double-down)"},
    {"id": "q11.r2", "weight": 1.0, "criterion": "Each model has both holding-conditions AND breaking-conditions named, each with repo evidence (per §6.7, models without paired evidence score 0.0)"},
    {"id": "q11.r3", "weight": 1.0, "criterion": "≥2 'survived a platform change' or 'broke under platform change' pairings provided"},
    {"id": "q11.r4", "weight": 1.0, "criterion": "Explicit kill-vs-scale criteria stated, citable to a repo's actual decision logic"},
    {"id": "q11.r5", "weight": 1.0, "criterion": "≥2 anti-patterns identified with corpus evidence"}
  ],
  "penalty_criteria": [
    {"id": "q11.p1", "deduction": 0.15, "trigger": "Recites ads-buyer slogans without naming breakage conditions in the corpus"}
  ],
  "must_include": [
    "LTV CAC",
    "pacing",
    "creative fatigue",
    "attribution paradox",
    "kill criteria",
    "scale criteria",
    "platform change",
    "anti-pattern",
    "worked here",
    "failed here"
  ],
  "required_sources": [
    "source-ads",
    "source-cognitive-models",
    "source-failure-modes"
  ]
}
```

### Q12 — C4: Social Cognitive Models

```json
{
  "id": "q12",
  "question": "What cognitive models do the social practitioners apply — platform-as-game-theory, algorithm preference modeling, community-fit-before-brand-voice, viral mechanics, the costs of automation visibility — and which of these models are validated, contested, or debunked by the corpus's actual outcomes?",
  "rubric": "Name each model, its decision-shaping role, supporting and contradicting repo evidence. Specifically address the automation visibility cost (when audiences detect AI-generated posts and disengage) with at least one repo example. Identify 2+ anti-patterns. Penalize 'platform best practices' answers without per-platform repo evidence.",
  "rubric_criteria": [
    {"id": "q12.r1", "weight": 1.0, "criterion": "≥3 cognitive models named (e.g., platform game theory, algorithm preference modeling, community fit, viral mechanics, automation visibility cost)"},
    {"id": "q12.r2", "weight": 1.0, "criterion": "Each model has supporting + contradicting repo evidence (per §6.7, models without paired evidence score 0.0)"},
    {"id": "q12.r3", "weight": 1.0, "criterion": "Automation visibility cost addressed specifically with ≥1 repo example"},
    {"id": "q12.r4", "weight": 1.0, "criterion": "Per-platform repo evidence provided (not generic platform-best-practices)"},
    {"id": "q12.r5", "weight": 1.0, "criterion": "≥2 anti-patterns identified with corpus evidence"}
  ],
  "penalty_criteria": [
    {"id": "q12.p1", "deduction": 0.15, "trigger": "Generic 'platform best practices' answer without per-platform repo evidence"}
  ],
  "must_include": [
    "platform game theory",
    "algorithm preference",
    "community fit",
    "brand voice",
    "viral mechanics",
    "automation visibility",
    "anti-pattern",
    "worked here",
    "failed here",
    "platform difference"
  ],
  "required_sources": [
    "source-social",
    "source-cognitive-models",
    "source-failure-modes"
  ]
}
```

### Q13 — I1: Shared Foundations

```json
{
  "id": "q13",
  "question": "Across the four domains, what infrastructure must be shared (identity, data lake, task queue, observability, LLM gateway, human-in-loop console, secrets and credentials, repo-template conventions) and what must be domain-isolated, and what is the criterion that decides which side of that line a new component belongs on?",
  "rubric": "List the shared foundations with the corpus evidence for each (at least 2 repos showing convergent pattern). For each foundation, name the contract (interface, schema, version policy). Provide an explicit decision rule: when does a new component belong in the shared layer vs in a domain-specific repo? Penalize answers that handwave 'platform stuff is shared' without naming the contract.",
  "rubric_criteria": [
    {"id": "q13.r1", "weight": 1.0, "criterion": "≥6 shared foundations listed (identity, data lake, task queue, observability, LLM gateway, human-in-loop console, secrets, repo-template)"},
    {"id": "q13.r2", "weight": 1.0, "criterion": "Each foundation has corpus evidence from ≥2 repos showing convergent pattern"},
    {"id": "q13.r3", "weight": 1.0, "criterion": "Each foundation has contract specified (interface, schema, version policy)"},
    {"id": "q13.r4", "weight": 1.0, "criterion": "Domain-isolated components also enumerated with rationale"},
    {"id": "q13.r5", "weight": 1.0, "criterion": "Explicit decision rule stated for 'new component → shared layer vs domain-specific'"}
  ],
  "penalty_criteria": [
    {"id": "q13.p1", "deduction": 0.15, "trigger": "Handwaves 'platform stuff is shared' without naming the contract"}
  ],
  "must_include": [
    "identity",
    "data lake",
    "task queue",
    "observability",
    "LLM gateway",
    "human-in-loop console",
    "secrets",
    "repo template",
    "domain-isolated",
    "decision rule"
  ],
  "required_sources": [
    "source-shared-infra",
    "source-skills-catalog",
    "source-platform-prototypes"
  ]
}
```

### Q14 — I2: Build Sequence (Day-1 → Month-3)

```json
{
  "id": "q14",
  "question": "If a small team starts on Day 1 with the goal of running a growth engine across the four domains in three months, what is the minimum-viable build sequence — what is built first, what is deferred, what triggers introducing each next subsystem, and what is the explicit decision rule for declaring a milestone done — grounded in evidence from the corpus's own evolution (prototypes → MVP → product)?",
  "rubric": "Produce a sequenced plan with at least 6 milestones (Day-1, Week-1, Week-2, Week-4, Week-8, Week-12). For each milestone: scope, dependencies on prior milestones, explicit done criteria, the next-trigger that pulls the following milestone in. Reference the corpus's own evolution (e.g., 0407-prototype → 0408-prototype → getuai-mvp → getuai-2.0) as evidence for the sequence shape. Cross-reference Q1-Q13 for what each milestone delivers AND fold in skill-delivery milestones (Q5-Q8 evidence) and failure-informed deferrals (Q15 evidence). Penalize 'do everything at once' or vague timelines. Demand at least 3 explicit deferrals (X is intentionally not built before Y because Z).",
  "rubric_criteria": [
    {"id": "q14.r1", "weight": 1.0, "criterion": "≥6 milestones (Day-1, Week-1, Week-2, Week-4, Week-8, Week-12) defined"},
    {"id": "q14.r2", "weight": 1.0, "criterion": "Each milestone has scope + dependencies + done criteria + next-trigger"},
    {"id": "q14.r3", "weight": 1.0, "criterion": "References the corpus's evolution (0407-prototype → 0408-prototype → getuai-mvp → getuai-2.0 or equivalent) as evidence for sequence shape"},
    {"id": "q14.r4", "weight": 1.0, "criterion": "Cross-references Q1-Q13 for what each milestone delivers; specifically includes skill-delivery milestones (Q5-Q8 evidence) and failure-informed deferrals (Q15 evidence)"},
    {"id": "q14.r5", "weight": 1.0, "criterion": "≥3 explicit deferrals stated (X is intentionally not built before Y because Z), each citable"}
  ],
  "penalty_criteria": [
    {"id": "q14.p1", "deduction": 0.20, "trigger": "'Do everything at once' or vague timelines / no deferral discipline"}
  ],
  "must_include": [
    "Day-1",
    "Week-1",
    "Week-4",
    "Month-3",
    "milestone done criteria",
    "next-trigger",
    "deferral",
    "minimum viable",
    "evidence from corpus evolution",
    "cross-reference"
  ],
  "required_sources": [
    "source-seo-geo",
    "source-content-writing",
    "source-ads",
    "source-social",
    "source-shared-infra",
    "source-platform-prototypes",
    "source-cognitive-models",
    "source-vertical-cases",
    "source-skills-catalog",
    "source-failure-modes"
  ]
}
```

### Q15 — I3: Cross-Domain Failure Modes & Anti-Patterns

```json
{
  "id": "q15",
  "question": "What failure modes and anti-patterns recur across multiple domains in the corpus — including the lessons from growth-engine-legacy and the abandoned/deprecated paths in other repos — and for each failure, what is the structural cause, the symptom you would observe early, and the architectural or cognitive prophylactic that the corpus has already converged on?",
  "rubric": "Enumerate at least 8 failure modes. For each: affected domains (named explicitly), structural cause, early-symptom signal a builder would see in the first weeks, prophylactic measure (architectural pattern OR cognitive guardrail). Evidence requirements: (a) ≥1 failure-occurrence repo:file:line citation per affected domain (a failure mode claimed cross-domain across N domains needs ≥N failure-occurrence citations across those N domains — single-domain evidence does NOT qualify a cross-domain claim and is scored 0); (b) ≥1 prophylactic-adoption repo:file:line citation. Special weight on growth-engine-legacy lessons since it is an explicit prior attempt. Penalize listed-but-uncited failure modes — every claim must have evidence per the per-domain rule.",
  "rubric_criteria": [
    {"id": "q15.r1", "weight": 1.0, "criterion": "≥8 failure modes enumerated"},
    {"id": "q15.r2", "weight": 1.0, "criterion": "Each mode has structural cause + early-symptom signal + prophylactic stated"},
    {"id": "q15.r3", "weight": 1.5, "criterion": "For each cross-domain claim, ≥1 failure-occurrence citation PER affected domain (cross-domain claims with single-domain evidence are scored 0 in this clause); per-domain evidence count must equal or exceed the number of domains claimed"},
    {"id": "q15.r4", "weight": 1.0, "criterion": "≥1 prophylactic-adoption citation per failure mode"},
    {"id": "q15.r5", "weight": 1.0, "criterion": "≥3 modes derived from growth-engine-legacy lessons, tagged with origin"}
  ],
  "penalty_criteria": [
    {"id": "q15.p1", "deduction": 0.25, "trigger": "Failure mode listed without evidence pair OR cross-domain claim with single-domain evidence (these are also scored 0 in q15.r3)"}
  ],
  "must_include": [
    "structural cause",
    "early symptom",
    "prophylactic",
    "growth-engine-legacy",
    "abandoned",
    "deprecated",
    "recurrence count",
    "evidence pair",
    "cross-domain",
    "file:line"
  ],
  "required_sources": [
    "source-failure-modes",
    "source-cognitive-models",
    "source-platform-prototypes"
  ]
}
```

## 6. Cross-Model Calibration Rules

These rules govern how a judge model scores a knowledge_base.md against the 15 questions
above. They are deliberately model-agnostic so that running judge=claude or judge=codex
or judge=gemini against the same KB produces scores that agree within a tolerance.

### 6.1 Score Anchor Table

The judge MUST place each per-question score in one of these bands and state which band
applied:

| Band | Score | Criteria (ALL must hold)                                                                                                      |
| ---- | ----- | ----------------------------------------------------------------------------------------------------------------------------- |
| S    | 0.95-1.00 | Every rubric item satisfied; ≥1 file:line citation per `must_include` concept; zero uncited claims; cross-question hooks present where required |
| A    | 0.85-0.94 | All rubric items satisfied; `must_include` coverage ≥80% with citations; ≤1 weak rubric item                                  |
| B    | 0.70-0.84 | All required_sources cited; `must_include` coverage ≥60%; 1-2 rubric items underdeveloped but addressed                       |
| C    | 0.50-0.69 | Question addressed but with major rubric gaps OR missing required_sources OR uncited claims >20% of body                      |
| D    | 0.30-0.49 | Off-target / generic / few citations; producer wrote about the domain, not the question                                       |
| F    | 0.00-0.29 | Hallucinated, contradicts source evidence, or not addressed                                                                   |

### 6.2 Per-Criterion Sub-Scoring Before Composite

Each question in §5 carries TWO scoring fields:

- `rubric_criteria` — a list of objects `{id, weight, criterion}` with stable IDs
  (`q<N>.r<M>`). The judge MUST score each criterion INDEPENDENTLY in `[0.0, 1.0]`.
- `penalty_criteria` — a list of objects `{id, deduction, trigger}` with stable IDs
  (`q<N>.p<M>`). Each triggered penalty deducts its `deduction` from the composite.

Composite score = `weighted_mean(rubric_criteria scores, weights) − sum(triggered penalties)`,
clamped to `[0.0, 1.0]` and then capped per §6.1, §6.3, §6.5, §6.7 as applicable.

Judge MUST emit the per-criterion score vector keyed by criterion id in
`judge_feedback.md` (e.g., `q1.r1: 0.85; q1.r2: 0.90; q1.p1: triggered`). This is what
makes cross-model divergence diagnosable at the clause level rather than the question
level. The composite alone is not enough.

Holistic gestalt scoring is forbidden.

### 6.2.1 Citation Form in Rubric Criteria

Where a `rubric_criteria` entry uses phrasing like "cites file:line",
"cites repo:file:line", or "every claim cites file:line", it means **"cites a
§6.3-valid citation appropriate to the score band being claimed"**:

- For S-band targets: direct `repo/path:LINE` is required per §6.3
  (digest-only citations do not qualify for S band).
- For B/A-band targets: transitively-backed digest citations
  (`source-*.md§<section>` whose section contains underlying file:line) satisfy
  the criterion. Direct file:line is preferred but not required for B/A.

All rubric criteria follow this rule. There are NO exceptions where the
criterion demands stricter form than §6.3.

Two specific question-type notes (these are NOT exceptions to §6.3 — they are
clarifications about WHAT is being verified, not about citation form):

(a) **Q5/Q6/Q7/Q8 skill-catalog rows**: each row carries a structural
    `path_reference` column (per §8.3 column contract). The `path_reference`
    is the row's identity (the directory or file path under
    `~/dev/getuai/<repo>/...` where the skill lives), not a citation. Artifact
    criterion `a1.c3` (§6.11) checks that the path resolves under the corpus.
    The CITATIONS supporting other claims in the row body still follow §6.3.

(b) **Q9/Q10/Q11/Q12 cognition worked-here / failed-here pairs**: the criterion
    is verifiability — the evidence MUST point to a specific code or commit
    location (so a generic "this worked" without locatable evidence is
    unsupported per §6.7). The CITATION FORM follows §6.3: direct file:line
    OR transitively-backed digest is acceptable.

Judges who interpret any rubric criterion as demanding stricter citation form
than §6.3 are wrong; §6.3 governs the floor, and this §6.2.1 maps criterion
phrasing to that floor.

### 6.3 Citation Discipline (Hard Cap)

Every claim that is more specific than a generic noun phrase MUST be linked to a citation.
Citations are tiered:

- **Strong (`repo/path/to/file.ext:LINE`)** — direct repo evidence. Always sufficient.
- **Acceptable for B/A bands (`source-*.md§<section>`)** — digest-section citation,
  ONLY when that digest section itself contains underlying `repo/path/to/file.ext:LINE`
  evidence transitively (verifiable by opening the digest section). A digest-only
  citation pointing to a digest section that lacks transitive `file:line` evidence is
  treated as UNCITED.
- **Required for S band per `must_include` concept** — at least one direct
  `repo/path/to/file.ext:LINE` citation. Digest-only citation does not qualify for S band.

**Hard cap**: any question whose answer contains >20% uncited claim-volume is capped at
band C (0.69) regardless of other quality. Judge MUST cite the uncited claim count and
the count of digest-only citations whose underlying section lacks `file:line` evidence in
feedback.

### 6.4 Anti-Keyword-Gaming Clause

`must_include` is necessary but not sufficient. If a `must_include` term appears in the
KB but is used in a way unrelated to its rubric meaning, judge MUST count it as 0
occurrences. Rubric semantic satisfaction dominates `must_include` count. The
`must_include` field exists to surface gaps, not to be a checklist.

### 6.5 Required_Sources Gate

If a question's `required_sources` are missing from the answer:

- **1 missing** → score capped at band C (0.69).
- **2+ missing** → score capped at band D (0.49).

This makes B band's "all required_sources cited" criterion a hard requirement,
consistent with §6.1 anchor table. Judge MUST emit which required_sources were
uncited and the resulting cap.

### 6.6 Cross-Question Consistency

When answers across questions contradict each other (e.g., Q1 architecture contradicts
Q13 shared-foundations decision rule), judge MUST flag the contradiction by question pair
and reduce BOTH question scores by 0.05. Maintain a `consistency_violations` list in
`judge_feedback.md`.

### 6.7 Empirical-Evidence-Required for Cognition Questions

For Q9-Q12 (cognitive-model questions), the rubric demands "worked here / failed here"
pairs. If a stated mental model lacks BOTH a worked-evidence and a failed-evidence
citation, judge MUST score that model's slot as `0.0` in the per-clause mean (NOT exclude
it from the denominator — exclusion would let a producer pad with unevidenced models
without score consequence). Each unsupported model contributes `0.0`; supported models
contribute their per-clause score.

Additional caps:
- ≥1 unsupported model present: per-question score capped at band B (0.84).
- 0 evidence-paired models: capped at band D (0.49).
- All named models supported: no cap from this rule.

### 6.8 Inter-Judge Disagreement Protocol

When the same KB is scored by two judge models (the cross-model evaluation flow):

- Compute per-question score deltas.
- If any single question delta > 0.15 → flag for human review; do not auto-pick.
- If aggregate (mean across 15) delta > 0.10 → flag for human review.
- Otherwise, take the mean of the two models' scores as the canonical score.
- The flagged divergences are the most informative signal of rubric ambiguity — they
  drive the next iteration's rubric refinement, not the next iteration of the KB.

### 6.9 Model-Agnostic Rubric Language

Rubrics MUST avoid model-specific reasoning instructions (no "think step by step", no
"as a careful reviewer", no "consider that you are an expert in X"). Rubrics MUST use
objective verifiable criteria (counts, presence/absence of cited evidence, structural
features). When this design doc is reviewed by Codex via `/review-loop`, one explicit
review focus is whether any rubric language tilts toward Claude-style or Codex-style
reasoning patterns.

### 6.10 Anchor Examples (Required Before Iter-1)

Per §8.4, provisional anchors (one B-band ≈0.75, one A-band ≈0.90, per question)
are hand-written BEFORE iter-1 starts and stored in
`runs/growth-engine-from-scratch/judge_calibration.md`, marked PROVISIONAL.
They are judge-side only — producer is NOT shown them.

**Anchor crystallization (progressive replacement)**. Auto Research produces
ONE KB answer per question per iteration, so anchors crystallize gradually
as iterations supply real material. The protocol:

1. **After iter-1**: For each question, score iter-1's answer. Replace the
   provisional anchor on whichever band the iter-1 answer scored closest to
   (e.g., if iter-1 Q3 scored 0.78 ≈ B band, replace the provisional B
   anchor for Q3 with iter-1's Q3 answer). The OTHER band's provisional
   anchor remains in use.
2. **After iter-2 onward**: Each new kept iteration produces an answer per
   question. If that answer falls closer to the band whose anchor is still
   provisional AND scores within ±0.07 of that target band centroid (B≈0.75,
   A≈0.90), replace that provisional anchor with the new answer. Otherwise
   leave the provisional anchor in place.
3. **Mixed-anchor period**: From iter-2 until both bands have a real anchor
   for a given question, the judge uses the question's mix of real and
   provisional anchors. Judge feedback flags which anchors are still
   provisional so subsequent iterations are aware of remaining calibration
   gap.
4. **Full crystallization**: A question's anchors are fully real once both
   bands have been observed and replaced. Across the run, expect most
   questions to fully crystallize by iter-5 to iter-10 (architecture-layer
   questions earlier, integration-layer questions later).

Optional acceleration: at iter-1, the harness MAY run a multi-sample
calibration pass (the same prompt with two different temperature or
sampling settings) to generate two candidate answers per question, scoring
both. This produces real B and A anchors immediately for many questions,
at the cost of doubled iter-1 producer compute. Whether to enable this is
a run-config decision in §7; default is OFF (single-sample iter-1 with
progressive replacement).

Provisional anchors are coarse and serve only to prevent uncalibrated iter-1
scoring; real anchors take over as soon as the protocol above produces
them. Anchor examples convert subjective judgment into ratio-comparison
judgment, which is more reliable across models.

### 6.11 Artifact Criteria (Embedded-Table Scoring)

The three structured tables embedded in KB (per §8.3) are evaluated by these
criteria, with deductions applied to the named questions' composite scores.
Stable IDs `a<N>.c<M>` are used for cross-model diagnostic.

| ID     | Artifact         | Affected Q's       | Criterion                                                                                  | Per-Q Deduction | Trigger                                                  |
| ------ | ---------------- | ------------------ | ------------------------------------------------------------------------------------------ | --------------- | -------------------------------------------------------- |
| a1.c1  | skill-catalog    | Q5, Q6, Q7, Q8     | Each domain's quadrant has ≥8 rows                                                         | 0.10            | Quadrant for this domain has <8 rows                     |
| a1.c2  | skill-catalog    | Q5, Q6, Q7, Q8     | Every row has all 8 columns populated (no `—`, no empty cells)                             | 0.10            | Any row in this domain's quadrant has missing column     |
| a1.c3  | skill-catalog    | Q5, Q6, Q7, Q8     | Every row's `originating_repo` and path reference resolves under `~/dev/getuai/`           | 0.10            | Any row cites a path outside the corpus or unresolvable  |
| a2.c1  | build-sequence   | Q14                | Table has ≥6 milestone rows                                                                | 0.20            | <6 rows                                                  |
| a2.c2  | build-sequence   | Q14                | Every row has all 6 columns populated                                                      | 0.10            | Any row missing a column                                 |
| a2.c3  | build-sequence   | Q14                | `corpus_evidence` column cites at least one repo per milestone                             | 0.10            | Any milestone with empty or generic `corpus_evidence`    |
| a3.c1  | failure-modes    | Q15                | Table has ≥8 mode rows                                                                     | 0.20            | <8 rows                                                  |
| a3.c2  | failure-modes    | Q15                | Every row has all 7 columns populated                                                      | 0.10            | Any row missing a column                                 |
| a3.c3  | failure-modes    | Q15                | `failure_evidence_per_domain` column populated per affected domain (per §15 r3 contract)   | 0.15            | Any cross-domain claim missing per-domain evidence       |

Composite formula (extending §6.2):

```
composite_q = clamp_0_1( weighted_mean(rubric_criteria_q) − sum(triggered penalty_criteria_q) − sum(triggered artifact_criteria for q) )
```

Then apply caps from §6.1 / §6.3 / §6.5 / §6.7 in that order.

Judge MUST emit triggered artifact criteria with their stable IDs (`a1.c1`,
`a2.c1`, etc.) in `judge_feedback.md` for each affected question. An artifact
deduction triggered for a question affects only that question's composite, not
others.

## 7. Run Configuration (Draft)

| Setting                       | Value                                                                                          | Rationale                                                                       |
| ----------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Producer (primary)            | `codex`                                                                                        | Stronger at code-grounded extraction; the source corpus IS code                |
| Judge (primary)               | `claude`                                                                                       | Stronger at structural critique and rubric adherence                            |
| Cross-model validation        | Required at: (a) iter-1 anchor crystallization (before iter-2); (b) every first-time `dimension_threshold` crossing per question (the OTHER model must confirm; if delta >0.15, score regresses below threshold until disagreement resolves); (c) iters 5, 15, 30 full-cross-model with §6.8 protocol; (d) final iteration / termination — independent fresh-session judge from BOTH models, consensus required for run completion | Final ratchet must not be single-model; threshold crossings must not be silent |
| Iteration cap                 | 40                                                                                              | 15-question structure needs ~2x polymarket's 22-iter; 40 leaves room for late refinement |
| `dimension_threshold`         | 0.80                                                                                            | Acceptance band: B/A boundary; matches Polymarket convention                    |
| Layer-iteration grouping      | Iters 1-10 prioritize Q1-Q4 (architecture); 11-20 prioritize Q5-Q8 (skill); 21-30 prioritize Q9-Q12 (cognition); 31-40 prioritize Q13-Q15 (integration) | Avoids 15-way thrash; matches the layer-grouped question order               |
| Source-extraction prerequisite | The 10 `source-*.md` files in §3 must be written before iter-1                                | Auto Research framework requires explicit source set                            |
| Iter-1 multi-sample calibration | OFF by default. If enabled (per §6.10): record `iter1_sample_count` (≥2) and the sampling/temperature settings used per sample | Anchor crystallization is faster but doubles iter-1 producer compute; if changed mid-run, the anchor protocol becomes non-replicable so the setting is locked at run start |

## 8. Resolved Decisions and Acknowledged Choices

Codex's `/review-loop` flagged that 4 of these 6 items affect the scoring contract and
must be resolved before iter-1, not deferred. Resolved here. The remaining 2 are
acknowledged design choices recorded so judges and producers know the contract.

### 8.1 Single 15-Q run vs three sub-runs — RESOLVED: single 15-Q run

A single 15-question run is mandatory. Splitting into Architecture / Skill /
Cognition+Integration sub-runs would prevent §6.6 (cross-question consistency)
from being enforceable across domain layers, defeating the design's central
goal of producing one coherent KB instead of three disconnected slices. The
~40-iteration cost is the price of this coherence.

### 8.2 "Content Writing" as separate domain — DECISION: keep as separate

Content Writing remains a separate domain alongside SEO/GEO, Ads, Social.
Rationale: its cognitive frames (user journey, content portfolio theory,
distribution-over-production) are distinct enough from the other three to
warrant independent extraction. The lower repo-density (it shares files with
SEO/GEO and Social) is a sourcing challenge, not a reason to fold the
cognitive layer.

### 8.3 Required empirical artifacts in KB — RESOLVED: three structured tables embedded in KB

The KB MUST embed three structured tables INSIDE `knowledge_base.md` itself,
as part of the answers to specific questions. **The KB remains the single
ratcheted deliverable; artifact tables are KB content, not parallel files.**

Embedded table contracts (these are the source of truth — judge scores them):

- **skill-catalog table**: split across answers to Q5/Q6/Q7/Q8 (one quadrant
  per domain). Columns: `skill_name | originating_repo | path_reference |
  invocation_surface | input_schema | output_schema | state_persistence |
  maintenance_signals`. Total ≥32 rows across the 4 domains (≥8 per domain).
  The `path_reference` column is the skill's row identity (the directory or
  file path under `~/dev/getuai/<repo>/...` where the skill lives), with
  optional `:LINE`. It is verified by artifact criterion `a1.c3`.
- **build-sequence table**: embedded in the Q14 answer. Columns: `milestone |
  scope | dependencies | done_criteria | next_trigger | corpus_evidence`. ≥6 rows.
- **failure-modes table**: embedded in the Q15 answer. Columns: `failure_id |
  affected_domains | structural_cause | early_symptom | prophylactic |
  failure_evidence_per_domain | prophylactic_evidence`. ≥8 rows.

Optional convenience exports (NOT scored, NOT ratcheted):

- `runs/growth-engine-from-scratch/artifacts/skill-catalog.md` — concatenation of
  the 4 quadrants from KB.
- `runs/growth-engine-from-scratch/artifacts/build-sequence.md` — copy of Q14 table.
- `runs/growth-engine-from-scratch/artifacts/failure-modes.md` — copy of Q15 table.

Producer MAY emit these for human consumption; the run loop does NOT track their
state. The framework's iteration ratchet operates on `knowledge_base.md` alone.

These embedded tables serve the same purpose as Polymarket's toy calibration
results: they force the producer to traverse the corpus rather than reason in
the abstract. Judge applies §6.11 artifact criteria to these embedded tables.

### 8.4 Anchor example sourcing — RESOLVED: provisional anchors before iter-1

Provisional anchor examples (one B-band ≈ 0.75, one A-band ≈ 0.90, per question)
MUST be hand-written before iter-1 starts and stored in
`runs/growth-engine-from-scratch/judge_calibration.md`. They are explicitly marked
PROVISIONAL and serve only to anchor the score bands during iter-1 when no real
iteration output exists.

After iter-1 produces actual KB content, anchors crystallize PROGRESSIVELY (per
§6.10's protocol): each kept iteration replaces ONE provisional anchor at a time
(the one whose band the iteration's answer falls closest to). Both bands per
question typically become real by iter-5 to iter-10. Optional multi-sample iter-1
acceleration is documented in §6.10 (default OFF).

Producer is NOT shown the anchors. They are judge-side only. This prevents the
producer-bias-toward-anchor-style risk from §6.10's earlier "deferred" stance.

### 8.5 `growth-engine-legacy` weighting — DECISION: stays in source-failure-modes

`growth-engine-legacy` does not get its own source file. It is the strongest single
contributor to `source-failure-modes.md` and is treated as such; the extraction process
tags every entry derived from it with `origin: growth-engine-legacy` so judges can
verify §2 (this run is not canonical to growth-engine-legacy) is honored. If extraction
reveals growth-engine-legacy material that is NOT failure-mode evidence (e.g., genuine
successful patterns abandoned for non-quality reasons), that material moves to the
appropriate domain source file with the same origin tag.

### 8.6 Producer access pattern — RESOLVED: digest-only with supervisor-side enforcement

Producer reads from the 10 `source-*.md` digest files for bulk reasoning.
Direct repo access is permitted ONLY for point verification — verifying a
quoted line, function name, or schema field that the digest references but
does not reproduce verbatim.

Enforcement is environment-side, NOT producer-self-reported and NOT just
tool-level interception (a producer with shell access can read files via
arbitrary commands — `python -c 'open(p).read()'`, `node`, `ruby`, custom
scripts — that no application-layer interceptor can fully cover):

1. **OS-level filesystem sandbox is mandatory.** The producer process MUST run
   inside a container or sandbox where the only readable paths are:
   - `runs/growth-engine-from-scratch/sources/*.md` (the 10 digests) — full read
   - `runs/growth-engine-from-scratch/iter-*/` workspace — full read/write
   - Raw `~/dev/getuai/` repos — accessible ONLY through a specific
     allowlisted "point-verify" tool (see step 2). All other paths in the
     filesystem are unreadable.

   Free-form shell access that can call interpreters with arbitrary file
   reads is disabled. If the harness cannot enforce this, the run does not
   start (§9 acceptance criterion).

   **Network and tool-channel sandboxing (equally mandatory).** The OS sandbox
   alone is not enough — a producer with network access can fetch repo content
   from GitHub, mirrors, or any URL; an MCP/connector tool with repo capability
   can read content via a side channel. So:
   - **Network egress** from the producer process MUST be disabled, OR routed
     through a logged proxy that applies the same digest-ref discipline as
     point-verify (raw fetch without `--digest-ref` rejected).
   - **MCP tools / connectors** are allowlisted explicitly. Repo-capable
     connectors (GitHub MCP, Linear MCP with attachment access, generic
     web-fetch tools) are DISABLED for the producer process unless they go
     through the point-verify policy.
   - LLM gateway calls (the producer's own model invocations) are exempt from
     this rule but their tool-call arguments are inspected by the harness for
     network or repo-fetching attempts.

2. **Allowlisted point-verify tool.** A single tool (e.g.,
   `pv read --digest-ref <id> <path>:<line-range>`) is the producer's only
   way to read raw repos. The tool:
   - Requires an explicit `--digest-ref` argument naming the digest section
     whose claim the read is verifying.
   - Records every invocation to
     `runs/growth-engine-from-scratch/artifacts/iteration-N/raw-access-log.md`
     (timestamp, file path, line range, digest-ref) BEFORE returning the
     content.
   - Rejects calls without `--digest-ref`.

   **Digest reads are also logged** to a separate
   `runs/growth-engine-from-scratch/artifacts/iteration-N/digest-access-log.md`
   (timestamp, source-*.md path, line range read). The producer's digest reads
   go through the same tool wrapper as raw reads but with a `--digest <name>`
   flag instead of `--digest-ref`. Logging digest reads is what makes the §8.6
   step 4 (b) audit ("file:line referenced inside an accessed digest section")
   verifiable — the auditor can check whether the cited digest section was
   actually read this iteration.

3. **Judge audit (post-iteration).** Judge inspects both access logs:
   - Any `raw-access-log.md` entry without a `--digest-ref` is impossible by
     step 2's contract; if such an entry exists, the harness is broken — flag
     for human.
   - The number of raw reads should be small relative to digest reads
     (rule of thumb: raw reads <10% of total reads). Suspicious bulk patterns
     flagged.
   - An empty `raw-access-log.md` is acceptable IF the KB contains zero
     `tier: file:line` citations whose evidence is not transitively in
     accessed digests (i.e., the producer's work was fully digest-driven and
     did not need raw verification).
   - An empty `digest-access-log.md` is always a hard reject — a producer
     that read no digest cannot have grounded any claim.

4. **Citation provenance audit (cross-check).** Producer self-marks every
   citation in KB with its tier (`tier: digest` or `tier: file:line`). Judge
   spot-checks 5 random citations per question:
   - For `tier: digest` → verify (i) the digest section exists, (ii) the
     section contains the cited claim, AND (iii) the section transitively
     contains underlying `repo/path:LINE` evidence supporting the claim
     (per §6.3 — a digest citation is valid ONLY when transitively backed
     by file:line). If (iii) fails, count the citation as UNCITED and apply
     the §6.3 hard cap.
   - For `tier: file:line` → verify EITHER (a) the raw file:line appears in
     `raw-access-log.md`, OR (b) the file:line is quoted/referenced inside a
     digest section that appears in `digest-access-log.md` (i.e., the
     producer copied the file:line evidence from a digest they actually
     accessed). Both are valid citation paths under §6.3 — only neither is
     invalid.

   Mismatches (citation cannot be backed by the digest content's transitive
   file:line, or by either access log) reject the iteration.

This makes §8.6 enforceable from the environment, not contingent on producer
honesty. The OS-level sandbox + allowlisted point-verify tool together are a
hard prerequisite for run start (acceptance criterion in §9). Tool-level
interception alone is insufficient and is explicitly NOT what this spec
requires.

## 9. Definition of Done (For This Design Doc)

- All 15 questions have rubric, rubric_criteria (with stable IDs), penalty_criteria, must_include, required_sources written (✓)
- Calibration rules cover: anchor table, structured per-criterion scoring, citation tier system, anti-keyword, required_sources gate (caps consistent with anchor bands), cross-question consistency, evidence-required for cognition (score 0 not exclude), inter-judge protocol, model-agnostic language, provisional anchors before iter-1 (✓)
- Source set strategy maps every domain + layer to a `source-*.md` file; all 10 source files referenced by ≥1 question (✓)
- Cross-model peer review by Codex via `/review-loop` Round 1: 8 findings (1 critical, 7 major), all accepted and applied (✓)
- Cross-model peer review Round 2: 5 second-order findings (all major) — §6.10 contradiction with §8.4, §6.3 vs rubric criteria citation form, missing artifact scoring criteria, KB-vs-artifact deliverable conflict, supervisor-side enforcement — all accepted and applied (✓)
- Cross-model peer review Round 3: 4 findings (all major) — §6.2.1 self-contradiction, missing path_reference column, tool-level interception inadequate, access-log audit too strict for digest-sourced citations — all accepted and applied (✓)
- Cross-model peer review Round 4: 4 findings (all major) — Q5/Q6 still 7-column, digest reads not logged, sandbox missed network/MCP, digest-tier audit dropped transitive evidence check — all accepted and applied (✓)
- Cross-model peer review Round 5 (resumed session): CONSENSUS (✓)
- Cross-model peer review fresh-final pass (independent session per Documentation/Protocol Scope rule): 1 finding (f22, anchor replacement protocol not operationally satisfiable — §6.10/§8.4 said "two real iter-1 answers per question" but Auto Research produces one answer per iteration). Fixed in §6.10 with progressive replacement protocol + optional multi-sample acceleration, mirrored in §8.4 (✓)
- Open ambiguities §8 resolved: §8.1 single run, §8.2 keep CW, §8.3 three tables embedded in KB (8-column skill-catalog), §8.4 provisional anchors with progressive crystallization, §8.5 GE-legacy in failure-modes, §8.6 OS-level sandbox + network/MCP sandbox + allowlisted point-verify tool with split access logs (✓)
- Cross-model peer review re-confirmation: f23 (§7 missing multi-sample row) accepted and applied; codex fresh-final-3 returned CONSENSUS Approved (✓)
- Stometa final approval (pending)

After this design doc is locked, `writing-plans` produces the implementation plan that
covers (a) source-extraction script design, (b) `runs/growth-engine-from-scratch/` init,
(c) iteration kickoff and cross-model validation cadence.
