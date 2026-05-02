# Repo: optiminds-org-config

## README.md
```markdown
# optiminds-org-config

Infrastructure-as-Code for the **Optiminds-Inc** GitHub organization.

All org-level policies (branch protection rulesets, org settings, webhooks, etc.) live here as version-controlled JSON. This repo is the **source of truth** — if a rule in GitHub's UI diverges from what's checked in here, the JSON wins and should be re-applied.

## Why this exists

Rulesets and org settings are editable directly in the GitHub UI, which means they can be silently changed or deleted. Without a git-tracked definition:

- Nobody can review changes before they happen
- Accidental deletion is unrecoverable without manual memory
- There's no history of *why* a rule exists

Storing the JSON here fixes all three.

## Layout

```
.
├── rulesets/               # Organization-level rulesets (one JSON per file)
│   ├── main-protection.json
│   └── README.md           # Rationale for each ruleset
├── webhooks/               # Organization-level webhooks (one JSON per file)
│   ├── pr-to-lark.json     # PR events → Lark group bot
│   └── README.md           # Rationale and event list
├── worker/                 # Cloudflare Worker that adapts GitHub → Lark payloads
│   └── README.md           # Deploy instructions
└── scripts/
    ├── apply-ruleset.sh    # Idempotent upsert: create or update ruleset from JSON
    └── apply-webhook.sh    # Idempotent upsert: create or update org webhook from JSON
```

## Prerequisites

- [`gh` CLI](https://cli.github.com/) authenticated as an org admin
- `gh` token must include `admin:org` scope:
  ```bash
  gh auth refresh -h github.com -s admin:org
  ```
- `jq` (`brew install jq`)

## Apply a ruleset

```bash
scripts/apply-ruleset.sh rulesets/main-protection.json
```

The script is **idempotent** — re-running it updates an existing ruleset in place rather than creating a duplicate.

## Apply a webhook

Webhooks ship in two parts: a JSON config (in `webhooks/`) and the Cloudflare Worker that adapts the payload (in `worker/`). Deploy the Worker first, then apply the webhook with the Worker URL injected from env:

```bash
# One-time: deploy the Worker (see worker/README.md for full instructions)
cd worker && npm install && npx wrangler login && \
  npx wrangler secret put GITHUB_WEBHOOK_SECRET && \
  npx wrangler secret put LARK_BOT_URL && \
  npm run deploy

# Then apply the org webhook
export WORKER_URL="https://github-pr-to-lark.<your-subdomain>.workers.dev"
export GITHUB_WEBHOOK_SECRET="<same value you set on the Worker>"
scripts/apply-webhook.sh webhooks/pr-to-lark.json
```

## Workflow

1. Edit the JSON file (e.g. `rulesets/main-protection.json`)
2. Open a PR against this repo so the change gets reviewed
3. After merge, run `scripts/apply-ruleset.sh <file>` to push the change to GitHub
4. Verify in the GitHub UI: `Organization settings → Repository rulesets`

## Future additions

- `settings/` — org-level settings snapshots (via `gh api /orgs/{org}`)
- `.github/workflows/apply.yml` — auto-apply on merge to `main`
- Terraform migration if ruleset count exceeds ~5 or we expand to multiple orgs

```
