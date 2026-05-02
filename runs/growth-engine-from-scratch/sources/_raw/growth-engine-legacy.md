# Repo: growth-engine-legacy

## CLAUDE.md
```markdown
# Growth Engine

@AGENTS.md

## Architecture

Growth Core (single backend) + Engines (plug-in domain modules). Browser → Core only. Start with `docs/migration/README.md`; use `docs/series/11_growth_core_phase1_tech_spec.md` as deeper Phase 1 reference.

## Current structure

Architecture and migration docs live under `docs/`; start at `docs/INDEX.md`.
The repository also contains an existing SEO/GEO engine tree at
`engines/geo-seo/`. The Growth Core runtime tree (`core/`) has not been created
yet.

## Target structure

`core/` (identity, credentials, ledgers, observability, core_sdk) + `engines/<name>/` + `docs/`

## Rules

Full rules: `AGENTS.md` (loaded above). Operating constraints:

- Migration architecture changes should update `docs/migration/` before runtime
  code changes
- Engine names are provisional — don't lock new names in specs
- Restate goal + target before multi-file edits

```

## AGENTS.md
```markdown
# AGENTS.md

Repo-wide rules. Loaded by Claude Code (via `@AGENTS.md` in `CLAUDE.md`), Codex CLI, Cursor, Aider, Continue.

## Architecture

Growth Engine = Growth Core (single backend) + Engines (plug-in domain modules).

- Browser talks to Core only.
- Engines never see raw Logto tokens.
  - In-process engines (default for new engines) receive a `RequestContext` constructed by Core in the same process.
  - Remote engines (existing services like SEO/GEO) receive a Core-signed internal context envelope and verify it.
- Core owns all platform facts (identity, tenancy, credentials, runs, artifacts, actions, schedules, observability). Engines own domain logic only.
- Engine deployment mode is per-engine: in-process module under Core by default; remote service when justified (existing service, different language stack, hard isolation requirement). See [`docs/adr/0001-engine-deployment-mode.md`](docs/adr/0001-engine-deployment-mode.md).

## Current structure

Architecture and migration docs live under `docs/`; navigation starts at
`docs/INDEX.md`. The repository also contains an existing SEO/GEO engine tree at
`engines/geo-seo/`. The Growth Core runtime tree (`core/`) has not been created
yet and should be introduced only through the migration plan.

## Target structure (Phase 1+)

```
growth-engine/
├── core/                        Core platform service (single deployable)
│   ├── identity/                Logto verify, user/org sync, role/flag evaluator
│   ├── runs/                    workflow_runs, engine_runs, run_events ledgers
│   ├── credentials/             credential records and lease issuer
│   ├── schedules/               workflow_schedules and poller
│   ├── observability/           Sentry/Langfuse helpers, run-event redactor
│   ├── core_sdk/                transport abstraction (in-process + signed-http)
│   └── engines/<name>/          in-process engine modules (default for new engines)
├── engines/<name>/              remote engine services (existing SEO/GEO; new engines that opt remote)
└── docs/                        specs, ADRs, runbooks, FUTURE_SCOPE
```

The `core/engines/` and `engines/` split encodes the deployment-mode choice from
ADR-0001: `core/engines/<name>/` is in-process under Core, `engines/<name>/` is a
separate deployable.

## Moat-binding rules

| # | Rule | Source | Breaks if violated |
|---|---|---|---|
| 1 | Core is the only browser-facing surface; engines never receive raw Logto tokens. The trust boundary is logical — applies to in-process modules and remote services equally | series/11 §6, series/12 §2; ADR-0001 | identity stitching |
| 2 | Platform facts written through `core_sdk` (`workflow_runs`, `engine_runs`, `run_events`, `growth_artifacts`, `action_ledger`) | series/11 §2 | attribution graph; audit trail |
| 3 | Credentials never leave Core; engines get scoped, time-bound leases | series/11 §7, series/12 §4.1 | credential rotation |
| 4 | Sentry + Langfuse + run-event log via `core/observability` only | series/11 §11 | trace correlation |
| 5 | Industry adaptation = domain packs, not `if industry == "..."`; generic labels (`SaaS`, `legal`, `e-commerce`) forbidden — require product-vertical specificity | series/12 §1; Stometa 2026-04-28 | scaling to N industries |
| 6 | Schedules registered in Core in Phase 1; engines do NOT run own cron loops | series/11 §4.1, series/12 §2 | Phase 2 Temporal migration |

## Established rules

- Branches: `feat/`, `fix/`, `docs/`, `refactor/` — never push to `main`
- Commits: Conventional Commits; no `Co-Authored-By`; atomic (one concern per commit)
- No secrets in git; if leaked, rotate FIRST then clean history
- No `--no-verify`, no force-push to shared branches, no `--amend` on pushed commits without permission
- No PII in logs; observability helpers must redact before write
- Doc-first for non-trivial changes — needs `docs/series/` or `docs/adr/` paper trail before code lands
- PR descriptions: Summary + Why + Out of scope + Validation

## Hard Rules

Extend the **Moat-binding rules** and **Established rules** above. Apply every task.

**Cite file:line for any code claim.** "Core verifies tenant scoping" is not evidence; `core/identity/verify.py:88` is. If you cannot cite, you have not verified — say so.

**Never fabricate command output.** Run `pytest`, run the migration, run `curl`. Paste the real output. Inferred output is fiction — discard it. If you cannot run a command (no env, no perms), say so explicitly.

**Restate before multi-file edits.** Restate the goal, target directory, and deliverable in one sentence each. If you cannot, ask one clarifying question — do not proceed on assumed scope.

**Challenge before endorsing.** In architecture discussions, surface counterpoints first. Name the constraint that rules out alternatives. If you cannot name one, you have made a guess — not a recommendation.

## Writing Discipline

Principles in this AGENTS.md and in `docs/series/`, `docs/adr/` use **imperative prose**, not bullet checklists. Six patterns: refusal ("Do not X until Y"), anchor ("**This is the rule.**"), falsifiability ("If you cannot X, the Y is a vibe — discard"), contrast ("A; not-A"), action-observation ("Action. Watch result."), inline don't (do + negation in same sentence).

Tables are for lookup (config defaults, parameter mappings, schemas). Prose for discipline. The Moat-binding rules table above is a reference table and stays as a table.

```

## agents.md
```markdown
# AGENTS.md

Repo-wide rules. Loaded by Claude Code (via `@AGENTS.md` in `CLAUDE.md`), Codex CLI, Cursor, Aider, Continue.

## Architecture

Growth Engine = Growth Core (single backend) + Engines (plug-in domain modules).

- Browser talks to Core only.
- Engines never see raw Logto tokens.
  - In-process engines (default for new engines) receive a `RequestContext` constructed by Core in the same process.
  - Remote engines (existing services like SEO/GEO) receive a Core-signed internal context envelope and verify it.
- Core owns all platform facts (identity, tenancy, credentials, runs, artifacts, actions, schedules, observability). Engines own domain logic only.
- Engine deployment mode is per-engine: in-process module under Core by default; remote service when justified (existing service, different language stack, hard isolation requirement). See [`docs/adr/0001-engine-deployment-mode.md`](docs/adr/0001-engine-deployment-mode.md).

## Current structure

Architecture and migration docs live under `docs/`; navigation starts at
`docs/INDEX.md`. The repository also contains an existing SEO/GEO engine tree at
`engines/geo-seo/`. The Growth Core runtime tree (`core/`) has not been created
yet and should be introduced only through the migration plan.

## Target structure (Phase 1+)

```
growth-engine/
├── core/                        Core platform service (single deployable)
│   ├── identity/                Logto verify, user/org sync, role/flag evaluator
│   ├── runs/                    workflow_runs, engine_runs, run_events ledgers
│   ├── credentials/             credential records and lease issuer
│   ├── schedules/               workflow_schedules and poller
│   ├── observability/           Sentry/Langfuse helpers, run-event redactor
│   ├── core_sdk/                transport abstraction (in-process + signed-http)
│   └── engines/<name>/          in-process engine modules (default for new engines)
├── engines/<name>/              remote engine services (existing SEO/GEO; new engines that opt remote)
└── docs/                        specs, ADRs, runbooks, FUTURE_SCOPE
```

The `core/engines/` and `engines/` split encodes the deployment-mode choice from
ADR-0001: `core/engines/<name>/` is in-process under Core, `engines/<name>/` is a
separate deployable.

## Moat-binding rules

| # | Rule | Source | Breaks if violated |
|---|---|---|---|
| 1 | Core is the only browser-facing surface; engines never receive raw Logto tokens. The trust boundary is logical — applies to in-process modules and remote services equally | series/11 §6, series/12 §2; ADR-0001 | identity stitching |
| 2 | Platform facts written through `core_sdk` (`workflow_runs`, `engine_runs`, `run_events`, `growth_artifacts`, `action_ledger`) | series/11 §2 | attribution graph; audit trail |
| 3 | Credentials never leave Core; engines get scoped, time-bound leases | series/11 §7, series/12 §4.1 | credential rotation |
| 4 | Sentry + Langfuse + run-event log via `core/observability` only | series/11 §11 | trace correlation |
| 5 | Industry adaptation = domain packs, not `if industry == "..."`; generic labels (`SaaS`, `legal`, `e-commerce`) forbidden — require product-vertical specificity | series/12 §1; Stometa 2026-04-28 | scaling to N industries |
| 6 | Schedules registered in Core in Phase 1; engines do NOT run own cron loops | series/11 §4.1, series/12 §2 | Phase 2 Temporal migration |

## Established rules

- Branches: `feat/`, `fix/`, `docs/`, `refactor/` — never push to `main`
- Commits: Conventional Commits; no `Co-Authored-By`; atomic (one concern per commit)
- No secrets in git; if leaked, rotate FIRST then clean history
- No `--no-verify`, no force-push to shared branches, no `--amend` on pushed commits without permission
- No PII in logs; observability helpers must redact before write
- Doc-first for non-trivial changes — needs `docs/series/` or `docs/adr/` paper trail before code lands
- PR descriptions: Summary + Why + Out of scope + Validation

## Hard Rules

Extend the **Moat-binding rules** and **Established rules** above. Apply every task.

**Cite file:line for any code claim.** "Core verifies tenant scoping" is not evidence; `core/identity/verify.py:88` is. If you cannot cite, you have not verified — say so.

**Never fabricate command output.** Run `pytest`, run the migration, run `curl`. Paste the real output. Inferred output is fiction — discard it. If you cannot run a command (no env, no perms), say so explicitly.

**Restate before multi-file edits.** Restate the goal, target directory, and deliverable in one sentence each. If you cannot, ask one clarifying question — do not proceed on assumed scope.

**Challenge before endorsing.** In architecture discussions, surface counterpoints first. Name the constraint that rules out alternatives. If you cannot name one, you have made a guess — not a recommendation.

## Writing Discipline

Principles in this AGENTS.md and in `docs/series/`, `docs/adr/` use **imperative prose**, not bullet checklists. Six patterns: refusal ("Do not X until Y"), anchor ("**This is the rule.**"), falsifiability ("If you cannot X, the Y is a vibe — discard"), contrast ("A; not-A"), action-observation ("Action. Watch result."), inline don't (do + negation in same sentence).

Tables are for lookup (config defaults, parameter mappings, schemas). Prose for discipline. The Moat-binding rules table above is a reference table and stays as a table.

```
