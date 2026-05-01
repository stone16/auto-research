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
  "rubric": "Enumerate the skills as a table with columns: skill name, originating repo, invocation surface (CLI / function call / agent message / cron), input schema, output schema, state persistence, maintenance signals (last-modified, recent commits, deprecation markers). For duplicates, name all repos that carry a near-equivalent and pick the canonical one with rationale. Penalize answers that list skill names without invocation/contract detail. Require at least 8 skills enumerated; no skill counts unless it has a path reference.",
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
  "rubric": "Enumerate skills with the same table format as Q5. For each, name the brittleness problem it addresses (drift / hallucination / register collapse / factual contamination / language register / cultural fit) and the technique used (template variables / few-shot / critic loop / human review / retrieval grounding). Cite repo:file:line. Penalize answers that ignore brittleness or treat all LLM content generation as equivalent.",
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
  "rubric": "Produce a sequenced plan with at least 6 milestones (Day-1, Week-1, Week-2, Week-4, Week-8, Week-12). For each milestone: scope, dependencies on prior milestones, explicit done criteria, the next-trigger that pulls the following milestone in. Reference the corpus's own evolution (e.g., 0407-prototype → 0408-prototype → getuai-mvp → getuai-2.0) as evidence for the sequence shape. Cross-reference Q1-Q13 for what each milestone delivers. Penalize 'do everything at once' or vague timelines. Demand at least 3 explicit deferrals (X is intentionally not built before Y because Z).",
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
    "source-vertical-cases"
  ]
}
```

### Q15 — I3: Cross-Domain Failure Modes & Anti-Patterns

```json
{
  "id": "q15",
  "question": "What failure modes and anti-patterns recur across multiple domains in the corpus — including the lessons from growth-engine-legacy and the abandoned/deprecated paths in other repos — and for each failure, what is the structural cause, the symptom you would observe early, and the architectural or cognitive prophylactic that the corpus has already converged on?",
  "rubric": "Enumerate at least 8 failure modes. For each: domains affected, structural cause, the early-symptom signal a builder would see in the first weeks, the prophylactic measure (architectural pattern OR cognitive guardrail) and at least 2 repo:file:line evidences (one for the failure occurring, one for the prophylactic being adopted). Special weight on growth-engine-legacy lessons since it is an explicit prior attempt. Penalize listed-but-uncited failure modes — every claim must have an evidence pair.",
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

Judge MUST score each rubric clause INDEPENDENTLY before producing the composite.
Composite score = mean(rubric_clause_scores), NOT a holistic gestalt. Judge MUST emit
the per-clause vector in `judge_feedback.md` so divergence between models can be diagnosed
at the clause level, not only at the question level.

### 6.3 Citation Discipline (Hard Cap)

Every claim that is more specific than a generic noun phrase MUST be linked to one of:
- `source-*.md§<section>` (citing the digest)
- `repo/path/to/file.ext:LINE` (citing the underlying repo directly, for verification)

**Hard cap**: any question whose answer contains >20% uncited claim-volume is capped at
band C (0.69) regardless of other quality. Judge MUST cite the uncited claim count in
feedback.

### 6.4 Anti-Keyword-Gaming Clause

`must_include` is necessary but not sufficient. If a `must_include` term appears in the
KB but is used in a way unrelated to its rubric meaning, judge MUST count it as 0
occurrences. Rubric semantic satisfaction dominates `must_include` count. The
`must_include` field exists to surface gaps, not to be a checklist.

### 6.5 Required_Sources Gate

If any of a question's `required_sources` is not cited at all in the answer, the score
is capped at band B (0.84). Missing two required_sources caps at band C (0.69).
Judge MUST emit which required_sources were uncited.

### 6.6 Cross-Question Consistency

When answers across questions contradict each other (e.g., Q1 architecture contradicts
Q13 shared-foundations decision rule), judge MUST flag the contradiction by question pair
and reduce BOTH question scores by 0.05. Maintain a `consistency_violations` list in
`judge_feedback.md`.

### 6.7 Empirical-Evidence-Required for Cognition Questions

For Q9-Q12 (cognitive-model questions), the rubric demands "worked here / failed here"
pairs. If a stated mental model lacks BOTH a worked-evidence and a failed-evidence
citation, judge MUST mark that model as unsupported and exclude it from the per-clause
mean. A Q9-Q12 answer with zero evidence-paired models is capped at band D (0.49).

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

### 6.10 Anchor Examples (Deferred)

After iteration 1 produces actual KB answers, pick 2 answers per question — one that
should score B (~0.75) and one that should score A (~0.90) — and freeze them as anchor
examples in `runs/growth-engine-from-scratch/judge_calibration.md`. From iteration 2
onward, every judge instance MUST be primed with these anchors before scoring. Anchor
examples convert subjective judgment into ratio-comparison judgment, which is more
reliable across models.

## 7. Run Configuration (Draft)

| Setting                       | Value                                                                                          | Rationale                                                                       |
| ----------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Producer (primary)            | `codex`                                                                                        | Stronger at code-grounded extraction; the source corpus IS code                |
| Judge (primary)               | `claude`                                                                                       | Stronger at structural critique and rubric adherence                            |
| Cross-model validation        | At iterations 5, 15, 30: re-judge with the OTHER model and apply §6.8 disagreement protocol     | Catches rubric drift early                                                      |
| Iteration cap                 | 40                                                                                              | 15-question structure needs ~2x polymarket's 22-iter; 40 leaves room for late refinement |
| `dimension_threshold`         | 0.80                                                                                            | Acceptance band: B/A boundary; matches Polymarket convention                    |
| Layer-iteration grouping      | Iters 1-10 prioritize Q1-Q4 (architecture); 11-20 prioritize Q5-Q8 (skill); 21-30 prioritize Q9-Q12 (cognition); 31-40 prioritize Q13-Q15 (integration) | Avoids 15-way thrash; matches the layer-grouped question order               |
| Source-extraction prerequisite | The 10 `source-*.md` files in §3 must be written before iter-1                                | Auto Research framework requires explicit source set                            |

## 8. Open Ambiguities (Resolve Before Iter-1)

These are the questions Codex's `/review-loop` should weigh in on before run start:

1. **Single 15-Q run vs three sub-runs?** Splitting into Architecture / Skill / Cognition+Integration runs would reduce per-iter context pressure but lose the cross-question consistency signal (§6.6). The current design assumes single run; this is the highest-impact decision left.
2. **"Content Writing" as separate domain?** It is the only domain without its own dedicated repo cluster (overlaps with SEO-poster and openclaw-marketing). Should it fold into SEO/GEO + Social, leaving 3 domains × 3 layers = 9 cells + 3 integration = 12 questions? Defended currently as separate because the cognitive frames (user journey, content portfolio) are distinct.
3. **Required empirical artifacts?** Polymarket required toy calibration results in the KB. The growth analog might be: (a) a generated skill catalog file as KB artifact, (b) a worked Day-1 plan with cited dependencies, (c) a per-domain anti-pattern list. Decide before iter-1 whether KB must produce ≥1 such artifact.
4. **Anchor example sourcing.** §6.10 defers anchor examples until iter-1 output. Alternative: hand-write one anchor per question now, even at low quality, so iter-1's judge has calibration from the first scoring. Trade-off: hand-written anchors might bias the producer toward our writing style.
5. **`growth-engine-legacy` weighting.** Currently it appears in `source-failure-modes.md` only. Should it have its own dedicated source file given §2 says it is a peer source, not the canonical answer?
6. **Producer access pattern.** Should producer be allowed to grep into raw repos during iteration (in addition to the 10 source files), or only into the source files? Allowing raw access enables better grounding but adds a 64-repo surface area to producer's context budget per iteration.

## 9. Definition of Done (For This Design Doc)

- All 15 questions have rubric, must_include, required_sources written (✓)
- Calibration rules cover: anchor table, per-clause scoring, citation discipline, anti-keyword, required_sources gate, cross-question consistency, evidence-required for cognition, inter-judge protocol, model-agnostic language, anchor examples (✓)
- Source set strategy maps every domain + layer to a `source-*.md` file (✓)
- Cross-model peer review by Codex via `/review-loop` complete and divergences resolved (pending)
- Open ambiguities §8 resolved (pending)
- Stometa final approval (pending)

After this design doc is locked, `writing-plans` produces the implementation plan that
covers (a) source-extraction script design, (b) `runs/growth-engine-from-scratch/` init,
(c) iteration kickoff and cross-model validation cadence.
