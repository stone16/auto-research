# Repo: attribution_v2

## README.md
```markdown
# attribution_v2

GetuAI ads attribution and lead tracking — v2. A browser SDK + two FastAPI services + a Next.js dashboard for turning UTM-tagged, cross-subdomain user journeys into scored, enriched leads.

## What

`attribution_v2` replaces the first-generation Getu attribution stack with a cleaner split:

- **`sdk/`** — a TypeScript browser SDK customers embed on their sites to emit events, carry UTM parameters across subdomains, and bridge anonymous sessions to identified users.
- **`events-track-server/`** — a Python/FastAPI pair (ingress + consumer) that takes SDK events, enriches them (GeoIP, device, ad params), queues via GCP Pub/Sub, and persists into the event tables.
- **`server/`** — the Python/FastAPI dashboard API: attribution aggregation, lead extraction, scoring, billing, and auth.
- **`frontend-v2/`** — a Next.js 14 UI for analysts to explore campaigns, cohorts, and lead pipelines. (`frontend/` is the legacy v1 React+Vite app, kept only for parity during the migration.)

The active refactor goals are tracked in [`target.md`](target.md): reshape backend/tracker/SDK to power the `frontend-v2` UI while keeping legacy APIs and historical data intact.

## Status

- **Lifecycle stage**: MVP → Scaling (v2 refactor in progress)
- **Live traffic**: yes (production)
- **Primary owner**: @Optiminds-Inc/engineering  <!-- refine once team boundaries are set -->

## Architecture

```
                  ┌──────────────────┐
  customer site → │   sdk (browser)  │
                  └────────┬─────────┘
                           │  HTTPS, events+attribution
                           ▼
   ┌──────────────────────────────────────────────┐
   │  nginx (see nginx.conf)                       │
   │   /tracker/api/  → events-track-server (ingress)
   │   /consumer/api/ → events-track-server (consumer)
   │   /dashboard/api/→ server (dashboard API)
   │   /              → frontend-v2 (:3103)
   └──────────────────┬────────────────┬──────────┘
                      │                │
               ┌──────▼──────┐   ┌─────▼─────┐
               │ MySQL         │   │ MySQL      │
               │ DATA_DB       │   │ ADS_DB     │
               │ (events, leads)│   │ (attribution)
               └───────────────┘   └────────────┘
                      ▲
                      │
               ┌──────┴──────────┐
               │ GCP Pub/Sub     │
               │ (event queue +  │
               │  dead-letter)   │
               └─────────────────┘
```

Full architectural landmines (dual-DB routing, cross-subdomain session, SDK dispatch bifurcation, user-id rotation semantics) live in [CLAUDE.md](CLAUDE.md). Read it before writing non-trivial code.

## Run Locally

### Prerequisites

- **Node 20+** (SDK, frontend)
- **Python 3.12+** (server), **3.11+** (events-track-server)
- **uv** (Python package manager) — `brew install uv`
- **MySQL** running locally (or access to a dev instance)
- **Docker** (optional, for supporting services)
- Access to shared secrets (GCP Pub/Sub credentials, DB credentials)

### Setup

```bash
# 1. SDK
cd sdk && npm install && npm run build

# 2. Dashboard API (server/)
cd ../server
uv sync
cp env.example .env                 # fill DB_HOST / ADS_DB_NAME / DATA_DB_NAME
alembic upgrade head
python start.py                     # :8000

# 3. Event ingress + consumer (events-track-server/)
cd ../events-track-server
uv sync
cp configs/env.example .env         # DB, Redis, Pub/Sub credentials
python -m api.main                  # :8019

# 4. Frontend v2 (current UI)
cd ../frontend-v2
npm install
npm run dev                         # http://localhost:3103
```

### Expected

`curl http://localhost:8000/dashboard/api/health` → 200. `curl http://localhost:8019/tracker/api/health` → 200. The Next.js dev server at :3103 renders without API errors in the browser console.

## Run Tests

- **SDK**: `cd sdk && npm test` / `npm run test:regression` (cross-subdomain + session rotation).
- **Server / events-track-server**: `pytest tests/` (per-sub-package; coverage wiring still evolving).

## Deploy

`cd deploy && ./deploy.sh -b main -e production -y`. Full rollout procedure, branches-to-env mapping, and rollback steps are in [`deploy/DEPLOYMENT.md`](deploy/DEPLOYMENT.md) and [`docs/runbooks/deploy.md`](docs/runbooks/deploy.md).

## Observability

- **Logs**: <!-- TODO: paste production log aggregator link -->
- **Metrics / Traces**: <!-- TODO: Grafana dashboard URL -->
- **Errors**: <!-- TODO: Sentry project link -->

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| SDK cookies not shared across subdomains | eTLD+1 landed on a public suffix (`.vercel.app`, `.github.io`) | Pass explicit `domain` to the SDK init |
| `alembic upgrade head` hits "multiple heads" | Feature branches added migrations in parallel | `alembic merge heads -m "..."` then upgrade |
| Lead table missing rows for known users | Event extracts `name`/`email` lazily; `setUserId` hasn't fired yet | Check SDK `setUserId` wiring on the customer site |

## Contributing

- Read [CLAUDE.md](CLAUDE.md) and [AGENTS.md](AGENTS.md) before non-trivial changes.
- PR expectations: [.github/pull_request_template.md](.github/pull_request_template.md).
- Architecture decisions: [docs/adr/](docs/adr/).

## Related Repos

- Downstream consumers of the SDK — <!-- TODO: list known integrators -->

---

<sub>Scaffolded from [optiminds-repo-template](https://github.com/Optiminds-Inc/optiminds-repo-template).</sub>

```

## CLAUDE.md
```markdown
# CLAUDE.md

<!-- Per-repo identity. Org-wide rules live in AGENTS.md. Keep <~50 lines. -->

@AGENTS.md

## Purpose

GetuAI Attribution v2 — ads attribution and lead tracking. A browser SDK captures UTM-driven user journeys across subdomains; two FastAPI services ingest events and expose a dashboard API; a Next.js app renders analytics and lead management. Current focus: refactor `server/` / `events-track-server/` / `sdk/` to feed `frontend-v2/`'s new UI. Current refactor scope is tracked in `target.md`.

## Architecture (5 landmines)

- **Monorepo, 4 active deployables**: `sdk/` (browser JS), `events-track-server/` (FastAPI ingress + consumer), `server/` (FastAPI dashboard API), `frontend-v2/` (Next.js 14, :3103). `frontend/` is legacy v1 — prefer `frontend-v2/` for anything new.
- **Dual MySQL schemas in `server/`** — `ADS_DB_NAME` (default; alembic migrations target this) + `DATA_DB_NAME`. Writes/reads may land in either depending on the table; check `server/core/database.py` before adding a model.
- **Cross-subdomain session via root-domain cookies** — SDK auto-detects eTLD+1 and writes `_getuai_session` / `_getuai_attrib` / `getuai_user_id` there. Public suffixes (`.vercel.app`, `.github.io`) break auto-detection and need an explicit `domain` config. See `sdk/src/session/`.
- **Event dispatch bifurcates** — `PURCHASE` / `LOGIN` / `SIGNUP` / `FORM_SUBMIT` / `EMAIL_VERIFICATION` / `AUDIT_APPROVED` send **immediately**; all others batch every 2s or at 100 events. Don't silently add a new "conversion-type" event to the batch path — data loss is invisible.
- **`setUserId` session rotation** — anonymous → `setUserId(A)` keeps the same `session_id` (backend backfills). `setUserId(A)` → `setUserId(B)` **rotates** `session_id`. Logout alone does NOT rotate.

## Domain Vocabulary

- **tracking_user_id** — per-company identifier: UUID for anonymous, caller-provided for identified users.
- **lead** — `(company_id, tracking_user_id)` tuple with name/email/phone extracted from form_submit / signup / login events; fields: `score` 0–100, `status` ∈ {new, engaged, qualified, opportunity, customer, churned}, `signal_strength` ∈ {hot, warm, cold}.
- **attribution** — first-touch + last-touch UTM snapshot, one record per session (not per user).
- **session_id** — survives cross-subdomain navigation; rotates only on user-identity change.

## Run Locally

```bash
# SDK
cd sdk && npm install && npm run build

# Dashboard API (server/)
cd server && uv sync && cp env.example .env    # fill DB_HOST / ADS_DB_NAME / DATA_DB_NAME
alembic upgrade head && python start.py         # :8000

# Event ingress + consumer (events-track-server/)
cd events-track-server && uv sync && cp configs/env.example .env
python -m api.main                              # :8019

# Frontend v2 (current UI)
cd frontend-v2 && npm install && npm run dev    # :3103
```

## Common Tasks

- **SDK tests**: `cd sdk && npm test` — cross-subdomain + session-rotation regressions via `npm run test:regression`.
- **SDK version bump**: edit `sdk/package.json` version → `npm run build` (scripts/update-version.js syncs `src/version.ts`).
- **DB migrations**: `alembic upgrade head` — run in `server/` and `events-track-server/` separately (each has its own `alembic/`).
- **Deploy**: `cd deploy && ./deploy.sh -b main -e production -y`; full docs in `deploy/DEPLOYMENT.md`.

## File Ownership (per-repo caution levels)

- **High caution** (ask before editing): `server/alembic/`, `events-track-server/alembic/`, `sdk/src/` public API surface, `nginx.conf` routing.
- **Legacy — prefer `frontend-v2/`**: `frontend/` is v1 React+Vite, only touch for critical bugs.
- **AGENTS.md §Core Principles #3 known exception**: `events-track-server/consumer/dead_letter_service.py` and `events-track-server/service/queue/pubsub_queue_client.py` directly import `google.cloud.pubsub_v1`. See `docs/adr/0001-accept-gcp-pubsub-in-events-tracker.md`.
- **Active security debt**: see `docs/security/known-leaks.md` — a GCP service-account private key is currently tracked in HEAD (`events-track-server/credentials/gcp-pub-sub.json`), rotation deferred. New credentials MUST go through env / Secret Manager, never into a file under `credentials/`.

<!-- Path-based review routing: see .github/CODEOWNERS (pending team setup) -->

每次做spec最终测试，都需要把env和credentials通过worktree-setup.shcp到相关的worktree，来启动浏览器测试环境或者必要的带环境的代码测试

---

<sub>Org-wide rules: [AGENTS.md](AGENTS.md). Deep guides auto-trigger as skills — list via `~/.optiminds/scripts/install-skills.sh list`.</sub>

```

## AGENTS.md
```markdown
# AGENTS.md

<!--
Organization-wide agent instructions for every Optiminds repository. This
file is the single source of truth for cross-repo rules. It is readable by
Claude Code (via `@AGENTS.md` reference in CLAUDE.md), Codex CLI (native),
Cursor, Aider, and Continue (all auto-load AGENTS.md).

Per-repo identity lives in CLAUDE.md, not here. This file should almost
never diverge between repos — if you feel the urge to override a rule
here for one repo, write an ADR instead.

Keep under ~200 lines. When a topic needs more depth, add it as a skill in
`skills/optiminds-<topic>/SKILL.md` — skills auto-trigger on matching
context and don't bloat the always-loaded AGENTS.md.
-->

## Core Principles

<!-- DRAFT: Stometa to finalize. These 7 principles were drafted from the
2026-04-21 CTO brainstorm (rankgale incident, cloud migration, harness
model). Refine the wording / ordering / add-remove as needed before the
first major adoption. -->

1. **Never commit secrets.** Every `.env*`, `credentials/`, `keys/`, token,
   or API key must be in `.gitignore` **before** the file is written.
   If a secret leaks to git history: rotate first in Key Vault, then clean
   history. Never reverse that order.

2. **CI must pass to merge.** No `--no-verify`, no skipping checks, no
   direct-to-main commits. If CI is broken and the fix is unclear, stop
   and ask. Broken CI is a P1.

3. **No cloud-vendor SDK in business code.** No `azure.*`, `@azure/*`,
   `google-cloud-*`, `@aws-sdk/*` imports under `/src/`, `/backend/`, `/api/`,
   `/frontend/`, `/sdk/`, `/cli/`. Secrets, storage, queues all come
   through `os.environ[...]` / `process.env.*`. Cloud migration must cost
   days, not months.

4. **Structured logs + metrics + traces on every production code path.**
   New endpoint / new agent / new background job = three signals emitted.
   No `print()`, no bare `logging.info("...")`. See skill `optiminds-obs`
   for the exact conventions (skill auto-triggers on relevant tasks).

5. **Tests ship with the code.** Same PR, not a follow-up. If a bugfix has
   no regression test, the bug will come back.

6. **Architectural changes need an ADR.** Any decision that's "1+ week of
   work", introduces a new external dependency, or changes a public
   contract goes in `docs/adr/` as a MADR-style record before or with the
   implementation PR.

7. **When in doubt, stop and ask.** Read AGENTS.md first, check relevant
   skill descriptions, consult `docs/adr/`, then ask a human. Never
   fabricate conventions under pressure.

## Git & PR Workflow

- **Branches**: `feature/<slug>` or `fix/<slug>`. Never push to `main`.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`,
  `test:`, `chore:`, `perf:`, `ci:`). Short subject, body explains WHY.
- **No `Co-Authored-By:` lines** on AI-assisted commits. Authorship =
  the human who approved the PR.
- **PR template**: see `.github/pull_request_template.md`. All 8 sections
  are required — "rollback" and "observability" especially.
- **Review**: every PR gets (a) Codex 3-pass AI review, (b) at least one
  human reviewer per CODEOWNERS. Strict paths (`billing/`, `auth/`,
  `migrations/`) require human approval to merge.
- **Merge**: squash-merge by default; merge commit for release PRs.

## Security Red Lines

These are non-negotiable. Violation = immediate revert + incident ticket.

| Red line | Enforcement |
|---|---|
| No secrets in git (past or present) | `gitleaks` pre-commit + CI + nightly full-history scan |
| No cloud-SDK in business code | (v0.3) `lint-cloud-sdk-imports.sh` in CI |
| No plaintext PII in logs | observability lint (v0.3) + manual review |
| No dynamic code execution on user input | code review + ruff / eslint rules |
| No disabling CI to merge | branch protection rules |
| No force-push to `main` | branch protection rules |

## Testing

- Minimum coverage: 80% on lines changed in a PR.
- TDD discipline: write the failing test first, implement to green, refactor.
- Unit + integration + at least one E2E per critical user flow.
- Never mock what you can inject (dependency inversion > magic mocks).
- See skill `optiminds-testing` for stack-specific patterns (Python pytest,
  TS vitest, etc.) — skill auto-triggers when you're writing tests.

## Engineering Discipline

Rules distilled from harness retros. Each bullet is a load-bearing
invariant — a past task shipped or nearly shipped a bug because the rule
wasn't followed. Source retros tagged `harness-retro` in the issue tracker.

### Planning discipline

- **SC / CP scope parity** — when a Success Criterion uses a universal-tree
  predicate ("no references in surviving files", "all callers", "nothing
  imports X"), the enforcing Checkpoint acceptance criterion MUST evaluate
  the same scope. If the CP is narrower, require BOTH a CP-local check AND
  a spec-level residual check (whole-tree grep against a sentinel whitelist).
  Narrower-CP-only defers drift detection to E2E. _(retro: v0.3.0 ship)_
- **Tool-behaviour claims need evidence at spec time** — any spec assertion
  about a third-party tool (bats, jq, shellcheck, release-please,
  actions/checkout, etc.) must cite evidence against the repo's **pinned**
  version: a runnable command + literal output (≤20 lines) + ISO-8601 date,
  OR a changelog/docs link for that version. Tool behaviour changes across
  versions; "it should work" is not a spec claim. _(retro: version-check-e2e)_

### Code discipline

- **Git worktree detection** — detect a working tree with
  `git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1`,
  NEVER `[[ -d "$TARGET/.git" ]]` or `[[ -e "$TARGET/.git" ]]`. In worktrees
  and submodules, `.git` is a regular file pointing into the main repo's
  `.git/worktrees/` dir — the directory test fails silently on valid
  setups. Regression-test any such check with `git worktree add`.
  _(retro: v0.3.0 ship)_
- **Atomic file writes require same-filesystem tempfile** — use
  `tmp=$(mktemp "${target}.XXXXXX")` (same dir → same fs), then
  `write_to "$tmp" && mv "$tmp" "$target"`. Naked `mktemp` defaults to
  `$TMPDIR` (typically `/tmp`), which on macOS, CI runners, and most
  Linux distros is a separate filesystem — cross-fs `mv` degrades to
  copy-then-unlink and is NOT atomic. Reviewers: an unadorned `mktemp`
  on an "atomic writer" AC is a finding, not a pass. _(retro: version-check-e2e)_
- **Bash arithmetic on parsed integers needs `10#` base prefix** — any
  `$((expr))` whose operands come from parsed string input (arguments,
  file content, SemVer components, line numbers) MUST prefix each
  operand: `(( 10#$major > 10#$other_major ))`. Bash parses leading-zero
  decimals as octal; `08` and `09` are invalid octal digits → "value
  too great for base". Literal integers written in script source are
  exempt (author controls their form). Every shell lib doing arithmetic
  on parsed integers must include a leading-zero test. _(retro: version-check-e2e)_

### CI discipline

- **Default `GITHUB_TOKEN` does NOT trigger downstream workflows** —
  GitHub intentionally skips downstream workflow triggers for events
  produced by actions running with the default token (security feature
  to prevent action self-escalation). For `workflow-A creates event →
  workflow-B runs` chains, choose one: (a) **inline** the downstream
  work into A (preferred — self-contained, no token management), (b)
  use a PAT or GitHub App token in A, or (c) document explicitly that
  B runs only on human-pushed events. Every cross-workflow handoff
  needs a dry-run or CI test before shipping.
  Ref: <https://docs.github.com/en/actions/security-guides/automatic-token-authentication>
  _(retro: v0.3.0 ship)_

### Documentation discipline

- **Flow-change doc-sync** — when changing a user-visible flow (release,
  deploy, adoption, onboarding), (1) grep the tree for every doc that
  describes the flow BEFORE changing it, (2) update every match in the
  SAME commit/PR as the code change, (3) cross-model review must
  explicitly verify doc-to-code consistency after the change. Three
  docs can describe a single flow; the old description silently outlives
  the code if doc-sync isn't forced. _(retro: v0.3.0 ship — README,
  CONTRIBUTING, CHANGELOG each independently described the broken
  pre-fix release flow and all three survived the first-pass review)_

### Evaluation discipline

- **Malformed-input fault-path probe** — every backend check whose code
  reads or parses external input (files, env vars, stdin, arguments
  that flow into `jq` / `sed` / `awk` / `python` / bash parameter
  expansion) MUST test the malformed-input branch in its evaluation:
  either (a) a test in the CP suite feeding invalid JSON / non-numeric
  version / trailing backslash / embedded newline and asserting a
  well-defined behaviour (error message + exit code, or graceful-
  degrade), OR (b) an evaluator-led simulation documenting
  stdout/stderr/exit code under a `Fault-path probe` heading. Pure-
  computation CPs with no external input must state
  `Fault-path probe: N/A` explicitly so the question is visibly asked
  and answered. Atomic-writer patterns require the same-fs tempfile
  check from Code discipline above. _(retro: version-check-e2e — 3
  malformed-input crashes caught by peer after all internal evaluators
  passed happy-path)_

## Tooling Setup

This repo assumes Optiminds organization-wide AI skills and subagents are
installed — once per developer machine. Skills auto-trigger in your CLI
based on task context. For the exact install / update / troubleshoot
commands, see [`docs/tooling-setup.md`](../docs/tooling-setup.md).

## Cross-Repo Glossary

<!-- Terms that mean the same thing across all Optiminds repos. Resist the
urge to redefine per-repo. Additions to this glossary happen via platform-
owners review. -->

- **Consumer** — a paying end-user of an Optiminds product (e.g., a law firm
  on lawyer_marketing). NOT synonymous with "customer" in billing contexts.
- **Tenant** — a logical isolation boundary in multi-tenant services
  (one customer org = one tenant = one `tenant_id` on every structured log).
- **Service** — a deployable unit (a FastAPI app, a worker, a CLI). Each
  repo may host multiple services under separate directories.
- **Agent** — an LLM-orchestrated workflow (Claude / Codex / in-house).
  NOT a user role.

## References

- Per-repo identity: `CLAUDE.md` (repo root)
- Deep guides: skills auto-trigger from `~/.claude/plugins/optiminds/skills/`
  (or your CLI's equivalent). List them: `~/.optiminds/scripts/install-skills.sh list`
- PR template: `.github/pull_request_template.md`
- CODEOWNERS: `.github/CODEOWNERS`
- Review rules: `.codex.yaml`
- Incident SLA: `SECURITY.md`
- Change governance: `CONTRIBUTING.md`

---

<sub>Structure from [optiminds-repo-template](https://github.com/Optiminds-Inc/optiminds-repo-template). Do not edit Core Principles / Security Red Lines without platform-owners review. Domain-specific sections can be added below this line per-repo if strictly necessary — prefer `CLAUDE.md` or a skill first.</sub>

```

## agents.md
```markdown
# AGENTS.md

<!--
Organization-wide agent instructions for every Optiminds repository. This
file is the single source of truth for cross-repo rules. It is readable by
Claude Code (via `@AGENTS.md` reference in CLAUDE.md), Codex CLI (native),
Cursor, Aider, and Continue (all auto-load AGENTS.md).

Per-repo identity lives in CLAUDE.md, not here. This file should almost
never diverge between repos — if you feel the urge to override a rule
here for one repo, write an ADR instead.

Keep under ~200 lines. When a topic needs more depth, add it as a skill in
`skills/optiminds-<topic>/SKILL.md` — skills auto-trigger on matching
context and don't bloat the always-loaded AGENTS.md.
-->

## Core Principles

<!-- DRAFT: Stometa to finalize. These 7 principles were drafted from the
2026-04-21 CTO brainstorm (rankgale incident, cloud migration, harness
model). Refine the wording / ordering / add-remove as needed before the
first major adoption. -->

1. **Never commit secrets.** Every `.env*`, `credentials/`, `keys/`, token,
   or API key must be in `.gitignore` **before** the file is written.
   If a secret leaks to git history: rotate first in Key Vault, then clean
   history. Never reverse that order.

2. **CI must pass to merge.** No `--no-verify`, no skipping checks, no
   direct-to-main commits. If CI is broken and the fix is unclear, stop
   and ask. Broken CI is a P1.

3. **No cloud-vendor SDK in business code.** No `azure.*`, `@azure/*`,
   `google-cloud-*`, `@aws-sdk/*` imports under `/src/`, `/backend/`, `/api/`,
   `/frontend/`, `/sdk/`, `/cli/`. Secrets, storage, queues all come
   through `os.environ[...]` / `process.env.*`. Cloud migration must cost
   days, not months.

4. **Structured logs + metrics + traces on every production code path.**
   New endpoint / new agent / new background job = three signals emitted.
   No `print()`, no bare `logging.info("...")`. See skill `optiminds-obs`
   for the exact conventions (skill auto-triggers on relevant tasks).

5. **Tests ship with the code.** Same PR, not a follow-up. If a bugfix has
   no regression test, the bug will come back.

6. **Architectural changes need an ADR.** Any decision that's "1+ week of
   work", introduces a new external dependency, or changes a public
   contract goes in `docs/adr/` as a MADR-style record before or with the
   implementation PR.

7. **When in doubt, stop and ask.** Read AGENTS.md first, check relevant
   skill descriptions, consult `docs/adr/`, then ask a human. Never
   fabricate conventions under pressure.

## Git & PR Workflow

- **Branches**: `feature/<slug>` or `fix/<slug>`. Never push to `main`.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`,
  `test:`, `chore:`, `perf:`, `ci:`). Short subject, body explains WHY.
- **No `Co-Authored-By:` lines** on AI-assisted commits. Authorship =
  the human who approved the PR.
- **PR template**: see `.github/pull_request_template.md`. All 8 sections
  are required — "rollback" and "observability" especially.
- **Review**: every PR gets (a) Codex 3-pass AI review, (b) at least one
  human reviewer per CODEOWNERS. Strict paths (`billing/`, `auth/`,
  `migrations/`) require human approval to merge.
- **Merge**: squash-merge by default; merge commit for release PRs.

## Security Red Lines

These are non-negotiable. Violation = immediate revert + incident ticket.

| Red line | Enforcement |
|---|---|
| No secrets in git (past or present) | `gitleaks` pre-commit + CI + nightly full-history scan |
| No cloud-SDK in business code | (v0.3) `lint-cloud-sdk-imports.sh` in CI |
| No plaintext PII in logs | observability lint (v0.3) + manual review |
| No dynamic code execution on user input | code review + ruff / eslint rules |
| No disabling CI to merge | branch protection rules |
| No force-push to `main` | branch protection rules |

## Testing

- Minimum coverage: 80% on lines changed in a PR.
- TDD discipline: write the failing test first, implement to green, refactor.
- Unit + integration + at least one E2E per critical user flow.
- Never mock what you can inject (dependency inversion > magic mocks).
- See skill `optiminds-testing` for stack-specific patterns (Python pytest,
  TS vitest, etc.) — skill auto-triggers when you're writing tests.

## Engineering Discipline

Rules distilled from harness retros. Each bullet is a load-bearing
invariant — a past task shipped or nearly shipped a bug because the rule
wasn't followed. Source retros tagged `harness-retro` in the issue tracker.

### Planning discipline

- **SC / CP scope parity** — when a Success Criterion uses a universal-tree
  predicate ("no references in surviving files", "all callers", "nothing
  imports X"), the enforcing Checkpoint acceptance criterion MUST evaluate
  the same scope. If the CP is narrower, require BOTH a CP-local check AND
  a spec-level residual check (whole-tree grep against a sentinel whitelist).
  Narrower-CP-only defers drift detection to E2E. _(retro: v0.3.0 ship)_
- **Tool-behaviour claims need evidence at spec time** — any spec assertion
  about a third-party tool (bats, jq, shellcheck, release-please,
  actions/checkout, etc.) must cite evidence against the repo's **pinned**
  version: a runnable command + literal output (≤20 lines) + ISO-8601 date,
  OR a changelog/docs link for that version. Tool behaviour changes across
  versions; "it should work" is not a spec claim. _(retro: version-check-e2e)_

### Code discipline

- **Git worktree detection** — detect a working tree with
  `git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1`,
  NEVER `[[ -d "$TARGET/.git" ]]` or `[[ -e "$TARGET/.git" ]]`. In worktrees
  and submodules, `.git` is a regular file pointing into the main repo's
  `.git/worktrees/` dir — the directory test fails silently on valid
  setups. Regression-test any such check with `git worktree add`.
  _(retro: v0.3.0 ship)_
- **Atomic file writes require same-filesystem tempfile** — use
  `tmp=$(mktemp "${target}.XXXXXX")` (same dir → same fs), then
  `write_to "$tmp" && mv "$tmp" "$target"`. Naked `mktemp` defaults to
  `$TMPDIR` (typically `/tmp`), which on macOS, CI runners, and most
  Linux distros is a separate filesystem — cross-fs `mv` degrades to
  copy-then-unlink and is NOT atomic. Reviewers: an unadorned `mktemp`
  on an "atomic writer" AC is a finding, not a pass. _(retro: version-check-e2e)_
- **Bash arithmetic on parsed integers needs `10#` base prefix** — any
  `$((expr))` whose operands come from parsed string input (arguments,
  file content, SemVer components, line numbers) MUST prefix each
  operand: `(( 10#$major > 10#$other_major ))`. Bash parses leading-zero
  decimals as octal; `08` and `09` are invalid octal digits → "value
  too great for base". Literal integers written in script source are
  exempt (author controls their form). Every shell lib doing arithmetic
  on parsed integers must include a leading-zero test. _(retro: version-check-e2e)_

### CI discipline

- **Default `GITHUB_TOKEN` does NOT trigger downstream workflows** —
  GitHub intentionally skips downstream workflow triggers for events
  produced by actions running with the default token (security feature
  to prevent action self-escalation). For `workflow-A creates event →
  workflow-B runs` chains, choose one: (a) **inline** the downstream
  work into A (preferred — self-contained, no token management), (b)
  use a PAT or GitHub App token in A, or (c) document explicitly that
  B runs only on human-pushed events. Every cross-workflow handoff
  needs a dry-run or CI test before shipping.
  Ref: <https://docs.github.com/en/actions/security-guides/automatic-token-authentication>
  _(retro: v0.3.0 ship)_

### Documentation discipline

- **Flow-change doc-sync** — when changing a user-visible flow (release,
  deploy, adoption, onboarding), (1) grep the tree for every doc that
  describes the flow BEFORE changing it, (2) update every match in the
  SAME commit/PR as the code change, (3) cross-model review must
  explicitly verify doc-to-code consistency after the change. Three
  docs can describe a single flow; the old description silently outlives
  the code if doc-sync isn't forced. _(retro: v0.3.0 ship — README,
  CONTRIBUTING, CHANGELOG each independently described the broken
  pre-fix release flow and all three survived the first-pass review)_

### Evaluation discipline

- **Malformed-input fault-path probe** — every backend check whose code
  reads or parses external input (files, env vars, stdin, arguments
  that flow into `jq` / `sed` / `awk` / `python` / bash parameter
  expansion) MUST test the malformed-input branch in its evaluation:
  either (a) a test in the CP suite feeding invalid JSON / non-numeric
  version / trailing backslash / embedded newline and asserting a
  well-defined behaviour (error message + exit code, or graceful-
  degrade), OR (b) an evaluator-led simulation documenting
  stdout/stderr/exit code under a `Fault-path probe` heading. Pure-
  computation CPs with no external input must state
  `Fault-path probe: N/A` explicitly so the question is visibly asked
  and answered. Atomic-writer patterns require the same-fs tempfile
  check from Code discipline above. _(retro: version-check-e2e — 3
  malformed-input crashes caught by peer after all internal evaluators
  passed happy-path)_

## Tooling Setup

This repo assumes Optiminds organization-wide AI skills and subagents are
installed — once per developer machine. Skills auto-trigger in your CLI
based on task context. For the exact install / update / troubleshoot
commands, see [`docs/tooling-setup.md`](../docs/tooling-setup.md).

## Cross-Repo Glossary

<!-- Terms that mean the same thing across all Optiminds repos. Resist the
urge to redefine per-repo. Additions to this glossary happen via platform-
owners review. -->

- **Consumer** — a paying end-user of an Optiminds product (e.g., a law firm
  on lawyer_marketing). NOT synonymous with "customer" in billing contexts.
- **Tenant** — a logical isolation boundary in multi-tenant services
  (one customer org = one tenant = one `tenant_id` on every structured log).
- **Service** — a deployable unit (a FastAPI app, a worker, a CLI). Each
  repo may host multiple services under separate directories.
- **Agent** — an LLM-orchestrated workflow (Claude / Codex / in-house).
  NOT a user role.

## References

- Per-repo identity: `CLAUDE.md` (repo root)
- Deep guides: skills auto-trigger from `~/.claude/plugins/optiminds/skills/`
  (or your CLI's equivalent). List them: `~/.optiminds/scripts/install-skills.sh list`
- PR template: `.github/pull_request_template.md`
- CODEOWNERS: `.github/CODEOWNERS`
- Review rules: `.codex.yaml`
- Incident SLA: `SECURITY.md`
- Change governance: `CONTRIBUTING.md`

---

<sub>Structure from [optiminds-repo-template](https://github.com/Optiminds-Inc/optiminds-repo-template). Do not edit Core Principles / Security Red Lines without platform-owners review. Domain-specific sections can be added below this line per-repo if strictly necessary — prefer `CLAUDE.md` or a skill first.</sub>

```
