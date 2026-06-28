# Dify Dossier

Status: CP05 boot smoke captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Framework | Dify |
| Repository | https://github.com/langgenius/dify.git |
| Pinned SHA | 7bb94cb6fecabb40662cc78d0dfabcb35df55b5c |
| INSTRUMENT_HASH | 1a2434beba68e3381d07a34c81babcc12e2b02caac4a56b58203fc55cc899f19 |
| Security gate | N/A in CP05; boot smoke only, no benchmark ingestion or retrieval leak gate was exercised. |

## Dossier Dimensions

### 1. Boot outcome

Verdict: PASS for local Docker boot smoke.

Evidence:

- Source pin: `.harness/ekb-research/checkpoints/05/iter-1/evidence/clone.txt`
- Dify Docker start instructions: `.harness/ekb-research/workspace/dify/README.md:74` through `.harness/ekb-research/workspace/dify/README.md:83`
- Dify custom configuration note: `.harness/ekb-research/workspace/dify/README.md:140`
- Local compose services: `.harness/ekb-research/checkpoints/05/iter-1/evidence/compose-services.txt`
- Local port/profile overrides: `.harness/ekb-research/checkpoints/05/iter-1/evidence/local-env-overrides.diff`
- Local health override: `.harness/ekb-research/workspace/dify/docker/docker-compose.cp05-health.yml:1`
- Compose config transcript: `.harness/ekb-research/checkpoints/05/iter-1/evidence/compose-config.yml`
- Compose up transcript: `.harness/ekb-research/checkpoints/05/iter-1/evidence/compose-up-health-reconcile.txt`
- Healthy service status: `.harness/ekb-research/checkpoints/05/iter-1/evidence/compose-ps-health-ready.txt`
- Readiness loop: `.harness/ekb-research/checkpoints/05/iter-1/evidence/compose-health-readiness-loop-final.txt`
- Smoke summary: `.harness/ekb-research/checkpoints/05/iter-1/evidence/smoke-summary-health.txt`
- Runtime feature flags: `.harness/ekb-research/checkpoints/05/iter-1/evidence/runtime-feature-flags-health.txt`
- Teardown: `.harness/ekb-research/checkpoints/05/iter-1/evidence/compose-down-health.txt`
- Teardown residue checks: `.harness/ekb-research/checkpoints/05/iter-1/evidence/teardown-containers-health.txt`, `.harness/ekb-research/checkpoints/05/iter-1/evidence/teardown-volumes-health.txt`, and `.harness/ekb-research/checkpoints/05/iter-1/evidence/teardown-networks-health.txt`

Observed behavior:

- Boot command used `docker compose -f docker-compose.yaml -f docker-compose.cp05-health.yml up -d` with `COMPOSE_PROJECT_NAME=ekbcp05dify`.
- Services started: `db_postgres`, `init_permissions`, `redis`, `api`, `plugin_daemon`, `worker`, `worker_beat`, `sandbox`, `ssrf_proxy`, `weaviate`, `api_websocket`, `web`, and `nginx`.
- `api`, `worker`, `worker_beat`, `web`, `db_postgres`, `redis`, `sandbox`, and `weaviate` reached Docker healthy status after CP05 enabled or added local healthchecks for worker, web, and weaviate.
- `GET http://localhost:18081/install` returned `HTTP/1.1 200 OK`.
- `GET http://localhost:18081/` returned `HTTP/1.1 307 Temporary Redirect` with `location: /install`.
- `GET http://localhost:18081/console/api/setup` returned `HTTP/1.1 200 OK` with `{"step":"not_started","setup_at":null}`.
- `docker compose down -v` removed the CP05 containers and networks. Follow-up filtered container, volume, and network checks returned only headers.

Findings:

- F-DIFY-001
- F-DIFY-002

### 2. Ingestion behavior

Verdict: NOT EXERCISED in CP05.

Evidence:

- Planned for CP06.

Findings:

- none

### 3. Retrieval behavior

Verdict: NOT EXERCISED in CP05.

Evidence:

- Planned for CP06.

Findings:

- none

### 4. Tenant isolation mechanism

Verdict: PRELIMINARY.

Evidence:

- Runtime feature flags: `.harness/ekb-research/checkpoints/05/iter-1/evidence/runtime-feature-flags-health.txt`
- Edition defaults: `.harness/ekb-research/checkpoints/05/iter-1/evidence/source-edition-lines.txt`
- Enterprise RBAC default: `.harness/ekb-research/workspace/dify/api/configs/enterprise/__init__.py:32` through `.harness/ekb-research/workspace/dify/api/configs/enterprise/__init__.py:34`
- System feature mapping: `.harness/ekb-research/workspace/dify/api/services/feature_service.py:252` and `.harness/ekb-research/workspace/dify/api/services/feature_service.py:282`

Observed behavior:

- The booted runtime exposed `data-edition="SELF_HOSTED"`, `data-allow-create-workspace="true"`, and `data-rbac-enabled="false"` in the install page.
- The code path defines enterprise RBAC as disabled by default and maps runtime `rbac_enabled` from `RBAC_ENABLED`.
- CP05 did not create users, tenants, datasets, or benchmark principals; tenant isolation remains unscored until CP06 or later security-specific checks.

Findings:

- F-DIFY-002

### 5. Permission/ACL model

Verdict: PRELIMINARY.

Evidence:

- Enterprise RBAC default: `.harness/ekb-research/workspace/dify/api/configs/enterprise/__init__.py:32` through `.harness/ekb-research/workspace/dify/api/configs/enterprise/__init__.py:34`
- Dataset RBAC branch: `.harness/ekb-research/workspace/dify/api/services/dataset_service.py:240` through `.harness/ekb-research/workspace/dify/api/services/dataset_service.py:245`
- Legacy dataset visibility branch: `.harness/ekb-research/workspace/dify/api/services/dataset_service.py:277` through `.harness/ekb-research/workspace/dify/api/services/dataset_service.py:297`

Observed behavior:

- Dataset permissions branch on `dify_config.RBAC_ENABLED`.
- When RBAC is disabled, Dify keeps legacy dataset visibility rules instead of enterprise RBAC permission-key enforcement.
- CP05 boot evidence is not enough to score native benchmark permission scope.

Findings:

- F-DIFY-002

### 6. Data model reconstruction

Verdict: NOT EXERCISED in CP05.

Evidence:

- Planned for CP06.

Findings:

- none

### 7. Generation and citation

Verdict: NOT EXERCISED in CP05.

Evidence:

- Planned for CP06.

Findings:

- none

### 8. Tool/MCP surface

Verdict: NOT EXERCISED in CP05.

Evidence:

- Planned for later synthesis if exposed by the exercised Dify app surface.

Findings:

- none

### 9. Observability and eval

Verdict: PARTIAL.

Evidence:

- Healthy service status: `.harness/ekb-research/checkpoints/05/iter-1/evidence/compose-ps-health-ready.txt`
- Runtime logs: `.harness/ekb-research/checkpoints/05/iter-1/evidence/api-logs-tail-health.txt`, `.harness/ekb-research/checkpoints/05/iter-1/evidence/worker-logs-tail-health.txt`, `.harness/ekb-research/checkpoints/05/iter-1/evidence/web-logs-tail-health.txt`, and `.harness/ekb-research/checkpoints/05/iter-1/evidence/weaviate-logs-tail-health.txt`
- Docker footprint before and after teardown: `.harness/ekb-research/checkpoints/05/iter-1/evidence/docker-system-df-before-health-down.txt` and `.harness/ekb-research/checkpoints/05/iter-1/evidence/docker-system-df-after-health-down.txt`

Observed behavior:

- CP05 captured `docker compose ps`, Docker health states, selected service logs, HTTP smoke responses, and teardown residue checks.
- Dify images remained available after teardown because CP06 depends on the same stack. Project containers, networks, and project volumes were removed.

Findings:

- F-DIFY-001

### 10. Extraction candidates

Status: preliminary.

Evidence:

- Boot and feature-flag evidence listed above.

Candidates:

- Dify's self-hosted Docker compose stack is viable as a repeatable benchmark target once local ports, vector profile, and health probes are pinned.
- Runtime feature flags provide an early extraction point for edition, registration, workspace creation, and RBAC posture before ingestion work begins.

Findings:

- F-DIFY-001
- F-DIFY-002

### 11. License posture

Status: preliminary.

Evidence:

- Runtime feature flags: `.harness/ekb-research/checkpoints/05/iter-1/evidence/runtime-feature-flags-health.txt`
- Edition defaults: `.harness/ekb-research/checkpoints/05/iter-1/evidence/source-edition-lines.txt`

Observed behavior:

- The exercised images defaulted to `SELF_HOSTED`.
- CP05 did not complete a license text audit; it only captured runtime edition and RBAC/workspace flags relevant to local evaluation.

Findings:

- F-DIFY-002

### 12. Benchmark grid result

Verdict: NOT STARTED for benchmark queries.

Evidence:

- No `docs/ekb-research/benchmark/runs/dify/` transcripts were created in CP05.

Findings:

- none

### 13. Gaps vs target design

Evidence:

- CP05 scope: `.harness/ekb-research/checkpoints/05/context.md`

Gaps:

- No corpus ingestion, retrieval, generated answer, citation, no-answer, multilingual, tool, freshness, or security leak gates were attempted in CP05.
- RBAC and workspace observations are preliminary runtime/code posture only.

Findings:

- F-DIFY-002

## Seven-Dimension Benchmark Grid

| Dimension | Capability level | Earned maturity | Verdict | Transcript evidence | Finding ids |
| --- | --- | --- | --- | --- | --- |
| R retrieval+citation | N/A | N/A | NOT TESTED | none in CP05 | none |
| I tenant isolation | N/A | N/A | NOT TESTED | none in CP05 | F-DIFY-002 |
| P permission scope | N/A | N/A | NOT TESTED | none in CP05 | F-DIFY-002 |
| N no-answer | N/A | N/A | NOT TESTED | none in CP05 | none |
| M multilingual | N/A | N/A | NOT TESTED | none in CP05 | none |
| A multi-agent/tool | N/A | N/A | NOT TESTED | none in CP05 | none |
| F freshness | N/A | N/A | NOT TESTED | none in CP05 | none |

## Findings View

Rows here mirror `docs/ekb-research/findings/ledger.md`. Do not create dossier-only findings.

| finding_id | source_checkpoint | category | severity | status |
| --- | --- | --- | --- | --- |
| F-DIFY-001 | CP05 | deploy-friction | major | confirmed |
| F-DIFY-002 | CP05 | license-and-authorization | major | confirmed |
