# Repo: optiminds-repo-template

## README.md
```markdown
# optiminds-repo-template

Lightweight harness for Optiminds, Inc. repositories. Two deliverables:

1. **Org-wide AI skills** that auto-trigger across Claude Code / Codex / Gemini / OpenCode.
2. **A baseline CI + governance layer** that any repo can adopt via one command.

No code scaffolding, no stack templates — those are the agent's job once the rules
and skills are in place.

## What you get

Three concerns, cleanly separated:

```
WHAT (rules, always-loaded)      — AGENTS.md                cross-repo, ~200 lines
                                   Core Principles, Security Red Lines,
                                   Git/PR workflow, Testing bar, Glossary

HOW (deep guides, on-demand)     — skills/optiminds-*/      org-wide, auto-trigger
                                   secrets, observability, cloud portability,
                                   testing, API patterns, LLM cost

WHO (per-repo identity)          — CLAUDE.md                per-repo, <50 lines
                                   Purpose, Architecture, Domain vocab,
                                   @AGENTS.md reference

ENFORCEMENT (hard gates)         — .github/workflows/       per-repo, copied by apply.sh
                                   + .pre-commit-config     + CODEOWNERS
```

Per-repo business logic, owners, and product specifics are **out of scope** — those
live in each consumer repo and this template never touches them.

## Quick start

**Once per developer machine** — install org-wide skills into all detected CLIs:

```bash
git clone git@github.com:Optiminds-Inc/optiminds-repo-template.git ~/.optiminds
~/.optiminds/scripts/install-skills.sh
~/.optiminds/scripts/install-skills.sh status
```

**Per repo** — apply Layer 0 (AGENTS.md, CLAUDE.md, CI workflows, hygiene):

```bash
./scripts/apply.sh /path/to/target-repo
```

`apply.sh` is idempotent (File-SHA + gitignore marker/fingerprint checks), so
re-running it on an already-adopted repo is a no-op unless the template itself
has new files.

## Version check

`apply.sh --check` is a read-only query that answers "am I behind the
template, and by how much?" by comparing the consumer repo's recorded
`template_version` against the template clone's `origin/main:version.txt`.
It reuses whatever git auth the template clone already has (SSH or HTTPS),
so it works against private repos without `gh` or a PAT.

Default (pull-mode) usage:

```bash
~/.optiminds/scripts/apply.sh --check ~/dev/my-repo
```

Sample up-to-date output:

```
==> Fetching latest template version...
==> Current applied:  0.4.1
==> Template latest:  0.4.1  (up-to-date)
```

Strict mode for CI exits non-zero when the consumer is behind, so a
pipeline step can surface the drift:

```bash
~/.optiminds/scripts/apply.sh --check --strict ~/dev/my-repo
```

Sample behind output:

```
==> Fetching latest template version...
==> Current applied:  0.3.0
==> Template latest:  0.4.1  (behind 1 minor, 1 patch)

Files that would change if you re-apply:
  M  .github/workflows/codex-review.yml         (template updated)
  !  AGENTS.md                                   (consumer modified — would skip without --force)
  +  docs/runbooks/cost-monitoring.template.md   (new in template)

Run: ~/.optiminds/scripts/apply.sh ~/dev/my-repo
```

Exit codes follow the `grep`/`diff` convention: `0` for up-to-date,
`2` for behind (under `--strict` only; default always exits 0), `1` for
real errors (missing metadata, malformed JSON, target not a git repo).

A compact push-mode banner fires automatically on `apply.sh <target>`
when the consumer's `template_version` is behind the template's current
version — no separate command needed. Sample banner when the consumer is
one minor + one patch behind:

```
==> Template metadata upgrade: 0.3.0 → 0.4.1 (1 minor + 1 patch)
==>   Run `apply.sh --check ~/dev/my-repo` for file-level diff before re-applying.
```

Set `OPTIMINDS_QUIET_VERSION=1` to silence the push-mode banner for
CI/scripted consumers that have already acknowledged the drift and don't
want log noise:

```bash
OPTIMINDS_QUIET_VERSION=1 ~/.optiminds/scripts/apply.sh ~/dev/my-repo
```

- Suppresses the minor / patch / ahead / first-tracking banners.
- Does **not** suppress the BREAKING banner for major version jumps — by
  design. Silently crossing a major boundary is the exact failure mode
  SemVer's major signal exists to prevent, so the BREAKING line is the
  one guard rail you cannot disable.

**Known limitation** — `--check` relies on the template clone's local
`origin/main` ref. A stale clone (corporate proxy that caches DNS, an
offline laptop, or a long-lived checkout) can report a false "up-to-date".
Run `git -C ~/.optiminds pull` periodically — or before a `--check` run
you care about — to refresh the local ref.

## What's in Layer 0 (the always-applies set)

| File | Purpose |
|---|---|
| `.github/workflows/codex-review.yml` | 3-pass Codex AI review on every PR (quality / security / dependencies) |
| `.github/workflows/secrets-scan.yml` | gitleaks + trufflehog on PR + nightly + `.gitignore` audit |
| `.github/CODEOWNERS.template` | Path-based review routing (billing / auth / migrations / infra) |
| `.github/pull_request_template.md` | 8-section PR template — what / why / test / obs / rollback / cost / cross-repo |
| `.github/ISSUE_TEMPLATE/` | Bug / feature / incident templates |
| `.pre-commit-config.base.yaml` | gitleaks + detect-secrets + basic hygiene hooks |
| `.gitignore.base` | Comprehensive secret + OS + IDE + build artifact patterns |
| `.codex.yaml.base` | Path-based Codex review strictness (strict for billing/auth, lenient for tests/docs) |
| **`AGENTS.md.template`** | **Org-wide agent rules — Core Principles + Security Red Lines + Tooling Setup. Loaded by Claude Code via `@AGENTS.md` in CLAUDE.md; natively read by Codex/Cursor/Aider.** |
| `CLAUDE.md.template` | Per-repo identity skeleton (<50 lines) — references `@AGENTS.md` for org rules |
| `README.md.template` | 6-section README skeleton |
| `docs/adr/0000-TEMPLATE.md` | ADR template (MADR-style) |
| `docs/runbooks/deploy.template.md` | Deploy runbook skeleton |
| `docs/runbooks/incident-response.template.md` | Incident response runbook skeleton |

## Org-wide skills (ship via `~/.optiminds`, not per-repo)

| Skill | Triggers on | Status |
|---|---|---|
| `optiminds-secrets` | `.env*`, credentials, Azure Key Vault, OIDC auth | ✓ shipped |
| `optiminds-obs` | logging, metrics, traces, LLM cost attribution | planned |
| `optiminds-cloud-port` | cloud SDK imports, blob / queue / DB drivers | planned |
| `optiminds-testing` | writing tests, fixtures, CI test stages | planned |
| `optiminds-api` | API routes, request/response schemas, versioning | planned |
| `optiminds-llm-cost` | Anthropic / OpenAI calls, agent logic, LLM tracing | planned |

Skills live once in this repo's `skills/` directory and symlink into each
CLI via `./scripts/install-skills.sh`. Updating a skill = `git pull` on
`~/.optiminds` + re-run install; every repo on your machine sees the new
version instantly (no per-repo PR).

## How updates propagate

| What | Mechanism | Propagation |
|---|---|---|
| Skills (`skills/optiminds-*/`) | `~/.optiminds` clone + `install-skills.sh` symlinks | Seconds — just `git pull` |
| Layer 0 files (workflows, AGENTS.md, CLAUDE.md, etc.) | `apply.sh` re-run on consumer repo (idempotent; preserves consumer edits) | Manual, per repo |

Skills are the fast-path: organization-wide knowledge that's identical across
every Optiminds repo, so it lives once and symlinks everywhere. Layer 0 files
live per-consumer-repo because CODEOWNERS, pre-commit config, and CLAUDE.md
are customized; `apply.sh` uses File-SHA tracking so re-applying never
overwrites consumer edits.

### Open TODO: auto-PR for Layer 0 drift

Layer 0 propagation today is **manual** — consumers re-run `apply.sh` when
they choose, and `apply.sh --check --strict` in consumer CI can surface
drift as a red light. This is sufficient at current scale (~7-8 consumer
repos), but has a known UX flaw as the consumer count grows: the CI signal
lands on whichever unrelated PR happens to open next, not on the repo
owner who should actually decide about template updates. Friction falls on
the wrong person.

**Upgrade path** (trigger: consumer count ≥ ~10, or misrouted-friction
complaints start surfacing):

1. Scheduled workflow in this template repo that runs `apply.sh --check`
   against every registered consumer repo.
2. On drift, `gh pr create` in the consumer repo with the proposed diff —
   Dependabot / Renovate-style. Consumer repo owner reviews and merges
   at their own pace, preserving the "human decides adoption" principle.
3. Auth via a short-lived GitHub App installation token, not a long-lived PAT.

Deferred for now — the manual `apply.sh` flow has better ROI than bot
maintenance at current scale. When picked up, design decisions belong in
an ADR under `docs/adr/`.

## Governance

- Major changes (breaking policy, removing files) require ADR in `docs/adr/` + approval from platform owners.
- Minor changes (tightening rules, adding new skills) follow normal PR flow via Conventional Commits.
- Releases are automated via release-please: merge the "Release PR" it opens; the `release-please.yml` workflow creates the tag + GitHub Release and sends the Lark notification inline. (`release.yml` handles the manual-tag path — human-pushed tags from `scripts/release.sh` — since default `GITHUB_TOKEN` events don't cascade to trigger it from release-please.)
- Every tagged release has a `CHANGELOG.md` entry with migration notes if breaking.

## Who maintains this

| Surface | Owner |
|---|---|
| Layer 0 (CI workflows, AGENTS.md, CLAUDE.md template) | `@Optiminds-Inc/platform-owners` |
| Skills (`skills/optiminds-*/`) | Domain owner per skill (secrets → security lead, obs → platform lead, etc.) |
| Per-repo adoption (CODEOWNERS, CLAUDE.md content) | Consumer repo team (not this template) |

## Repository layout

```
optiminds-repo-template/
├── layer0-core/              # What apply.sh copies into consumer repos
│   ├── .github/              # Workflows, CODEOWNERS, PR/issue templates
│   ├── docs/                 # ADR + runbook templates
│   ├── AGENTS.md.template    # Org-wide rules
│   ├── CLAUDE.md.template    # Per-repo identity skeleton
│   ├── README.md.template
│   ├── .pre-commit-config.base.yaml
│   ├── .codex.yaml.base
│   └── .gitignore.base
├── skills/                   # Org-wide AI skills (Channel C)
│   ├── README.md
│   └── optiminds-secrets/    # First shipped skill
├── scripts/
│   ├── apply.sh              # Copies layer0-core/ into a target repo
│   ├── install-skills.sh     # Symlinks skills/* into Claude/Codex/Gemini/OpenCode
│   ├── bootstrap.sh          # Dev-tool audit
│   └── release.sh            # Manual version bump (auto-bumper lives in workflow)
├── .github/workflows/        # Template's OWN CI — not copied to consumers
│   ├── validate.yml          # shellcheck + yamllint + bats
│   ├── release-please.yml    # Auto-bumper: Conventional Commits → Release PR
│   └── release.yml           # On tag push: GitHub Release + Lark notify
├── tests/                    # bats suite for apply.sh + release.sh
├── docs/                     # Reference docs (not copied by apply.sh)
└── CONTRIBUTING.md / SECURITY.md / LICENSE / CHANGELOG.md / version.txt
```

```

## skills/README.md
```markdown
# Optiminds Skills — organization-wide AI agent knowledge

Single source of truth for Optiminds-wide AI skills. Skills auto-trigger in
Claude Code / Codex / Gemini / OpenCode based on their `description` fields —
no manual invocation needed.

## Why here (not per-repo)

Skills are **organization-level assets**. A convention for `observability`,
`secrets`, or `cloud-portability` should be identical across every Optiminds
repo. Embedding them per-repo would mean 30 copies and a per-repo PR cycle
on every update. Centralizing here = update once, 30 repos see it instantly
(symlink-based propagation — see top-level `README.md`'s "How updates propagate").

## Structure

```
skills/
├── optiminds-secrets/SKILL.md        secrets handling (Azure KV pattern + rankgale lessons)
├── optiminds-obs/SKILL.md            observability conventions         [v0.4 planned]
├── optiminds-cloud-port/SKILL.md     cloud-portability rules           [v0.4 planned]
├── optiminds-testing/SKILL.md        testing standards                 [v0.4 planned]
├── optiminds-api/SKILL.md            FastAPI route patterns            [v0.4 planned]
└── optiminds-llm-cost/SKILL.md       LLM cost attribution              [v0.4 planned]
```

## Install to your CLI

One-time per developer machine:

```bash
git clone git@github.com:Optiminds-Inc/optiminds-repo-template.git ~/.optiminds
~/.optiminds/scripts/install-skills.sh
```

This symlinks skills into all detected CLIs:

| CLI         | Target path                                | Mechanism                         |
|-------------|--------------------------------------------|-----------------------------------|
| Claude Code | `~/.claude/plugins/optiminds/skills/`      | symlinks (Bug #14836 workaround)  |
| Codex       | `~/.codex/skills/`                         | native symlinks                   |
| Gemini      | `~/.gemini/skills/`                        | native symlinks                   |
| OpenCode    | `~/.config/opencode/agent/`                | format-converted copies           |

## Update

```bash
cd ~/.optiminds && git pull
./scripts/install-skills.sh
```

## Adding a new skill

1. Create `skills/optiminds-<name>/SKILL.md` with frontmatter:
   ```yaml
   ---
   name: optiminds-<name>
   version: 0.1.0
   description: |
     Use when <concrete trigger keywords>. <What this skill enforces>.
   ---
   ```
2. Description must contain **specific technical keywords** that match real
   task context (e.g. "Azure Key Vault", "OpenTelemetry", not "observability
   stuff").
3. Verify with `./scripts/install-skills.sh list`
4. PR per [`CONTRIBUTING.md`](../CONTRIBUTING.md)

Use [`optiminds-secrets/SKILL.md`](optiminds-secrets/SKILL.md) as the reference
pattern.

## Governance

Skills live in Layer 0 (stack-agnostic, organization-wide). Per-repo
specializations belong in that repo's own `.claude/skills/` — not here.

```

## skills/optiminds-secrets/SKILL.md
```markdown
---
name: optiminds-secrets
version: 0.1.0
description: |
  Use when touching .env, .envrc, credentials/, secrets/, Azure Key Vault,
  OIDC federated credentials, or any code path that reads API keys /
  database URLs / OAuth client secrets. Enforces the "no Azure SDK in
  business code" rule and the three-location pattern (local dev via direnv,
  CI via azure/cli OIDC, production via managed identity). Prevents
  rankgale-style credential leaks to git history.
---

# Optiminds Secrets Handling

Canonical pattern for every Optiminds service. Defines three concrete
scenarios (local dev, GitHub Actions, production) and the one hard rule
that keeps us cloud-portable.

## The hard rule

> **Azure SDK MUST NOT appear in business code.**

The moment a request handler imports `azure.keyvault.*`, we lose cloud
portability. Migrating Azure → GCP then means rewriting every handler,
not just deploy YAML.

### Forbidden in `/backend*/`, `/server/`, `/api/`, `/frontend/`, `/sdk/`, `/cli/`

```python
# FORBIDDEN
import azure.identity
import azure.keyvault.secrets
from azure.keyvault.secrets import SecretClient

client = SecretClient(vault_url=..., credential=DefaultAzureCredential())
secret = client.get_secret("stripe-secret-key-prod").value
```

TypeScript equivalent (also forbidden in business code):

```typescript
import { SecretClient } from "@azure/keyvault-secrets";
import { DefaultAzureCredential } from "@azure/identity";
```

### Permitted paths only

- `/scripts/` — bootstrap / rotation tooling
- `/tools/` — template-repo internal tooling
- `/deploy/` — infra-only bootstrap
- `/.github/workflows/*.yml` — CI steps (uses `azure/cli@v2`, not SDK from app)

Business code reads secrets through `os.environ[...]` / `process.env.*` only.

## The three-location pattern

| Location       | Mechanism                                     | App code sees    |
|----------------|-----------------------------------------------|------------------|
| Local dev      | `az keyvault secret show` → `export` via direnv | `os.environ[...]` |
| GitHub Actions | `azure/cli@v2` → `$GITHUB_ENV`                | `os.environ[...]` |
| Container Apps | `secretRef` + managed identity                | `os.environ[...]` |

**The app code column never changes. That is the invariant.**

## Pattern 1 — Local development (direnv + az)

Prereqs: `az` CLI + `Key Vault Secrets User` role on `dev-optiminds-kv`.

```bash
# one-time
az login
az account set --subscription optiminds-dev
```

Per-project `.envrc` (gitignored; `.envrc.template` is the committed skeleton):

```bash
export ENV=development
export AZURE_KEY_VAULT_NAME=dev-optiminds-kv
export SERVICE_NAME=<service>

# One az call per secret — individual env vars, never one JSON blob
export STRIPE_SECRET_KEY=$(az keyvault secret show \
    --vault-name "$AZURE_KEY_VAULT_NAME" --name stripe-secret-key-dev \
    --query value -o tsv)
export DATABASE_URL=$(az keyvault secret show \
    --vault-name "$AZURE_KEY_VAULT_NAME" --name <service>-db-url-dev \
    --query value -o tsv)
# ... one line per secret
```

**Why individual env vars, not a JSON blob**:
- App code stays vanilla: `os.environ["STRIPE_SECRET_KEY"]`, no parsing.
- Rotate one key → `direnv reload` → no app change.
- Git-leak forensics: one leaked env-var name = one secret, not all of them.

## Pattern 2 — GitHub Actions (OIDC federated, no long-lived secret)

```yaml
permissions:
  id-token: write          # required for OIDC
  contents: read

jobs:
  deploy:
    steps:
      - uses: actions/checkout@v4
      - name: Azure login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Hydrate secrets from Key Vault
        uses: azure/cli@v2
        with:
          inlineScript: |
            set -euo pipefail
            VAULT=prod-optiminds-kv
            for pair in \
              "STRIPE_SECRET_KEY:stripe-secret-key-prod" \
              "DATABASE_URL:<service>-db-url-prod" \
              "OPENAI_API_KEY:openai-api-key-prod"
            do
              name=${pair%%:*}
              secret=${pair#*:}
              value=$(az keyvault secret show --vault-name "$VAULT" \
                      --name "$secret" --query value -o tsv)
              echo "::add-mask::$value"
              echo "$name=$value" >> "$GITHUB_ENV"
            done

      - name: Deploy (reads env vars, no Key Vault import)
        run: ./scripts/deploy.sh
```

**Why OIDC over service-principal password**: zero long-lived secrets in
`GITHUB_SECRETS`; identity scoped per-repo + per-environment; revocation is
one Azure AD click.

## Pattern 3 — Production (Azure Container Apps)

App reads `os.environ["STRIPE_SECRET_KEY"]`. Period. Platform injects the env
var via user-assigned managed identity bound to the container.

```yaml
# deploy/container-app.yaml (excerpt)
spec:
  identity:
    type: UserAssigned
    userAssignedIdentities:
      "/subscriptions/.../userAssignedIdentities/<service>-prod-mi": {}
  configuration:
    secrets:
      - name: stripe-secret-key
        keyVaultUrl: https://prod-optiminds-kv.vault.azure.net/secrets/stripe-secret-key-prod
        identity: /subscriptions/.../userAssignedIdentities/<service>-prod-mi
  template:
    containers:
      - image: optimindsacr.azurecr.io/<service>:v1.4.2
        env:
          - name: STRIPE_SECRET_KEY
            secretRef: stripe-secret-key
```

AKS equivalent: Secret Store CSI Driver + same managed-identity binding.

## Rotation

```bash
# Rotate a secret (runs against Key Vault; app picks up on next pod restart)
az keyvault secret set --vault-name prod-optiminds-kv \
    --name stripe-secret-key-prod \
    --value "<new-value>"

# Set expiration window (drives monitoring alerts)
az keyvault secret set-attributes --vault-name prod-optiminds-kv \
    --name stripe-secret-key-prod \
    --expires 2026-10-21T00:00:00Z
```

If a secret is **leaked to git history** (the rankgale-2026-04 lesson):
1. **Rotate first** — new value in Key Vault before cleanup
2. Then BFG / `git filter-repo` the old value from history
3. Force-push with coordinated team notification
4. Document in `docs/incidents/`

## Cloud-migration tax (Azure → GCP, 6-18mo)

What changes vs. what stays portable:

| Component                                      | Change needed     | Why                                     |
|------------------------------------------------|-------------------|-----------------------------------------|
| Business code `os.environ["X"]`                | **0 LOC**         | SDK never imported                      |
| Logger / structlog processors                  | 0 LOC             | Env-var driven                          |
| `.github/workflows/*.yml` hydrate step         | ~30 LOC           | `azure/cli` → `google-github-actions`   |
| Local dev `.envrc`                             | ~60 LOC           | `az` loop → `gcloud secrets` loop       |
| Production deploy manifest                     | ~90 LOC           | Container Apps `secretRef` → Cloud Run `--set-secrets` |
| OIDC federation                                | 1-day org setup   | Azure AD federated → GCP Workload Identity |
| **Total**                                      | **≈ 3 engineer-days** | Paid once                          |

The 3-day migration budget is the justification for choosing AKV over a
vendor-neutral secrets manager. Paying $0 today + 3 days in 2027 beats
paying $X K / year forever.

## What to do when you encounter

### "I need to add a new secret to this service"

1. Add it to Azure Key Vault: `az keyvault secret set --vault-name dev-optiminds-kv --name <secret-name>-dev --value "..."`
2. Add corresponding `-staging` and `-prod` entries (or ask platform-owners for prod)
3. Add one `export` line in `.envrc.template` (with placeholder)
4. Add one entry in the CI `for pair in ...` loop in `.github/workf

[... truncated to 8KB ...]

```
