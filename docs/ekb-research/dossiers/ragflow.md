# RAGFlow Dossier

Status: CP03 boot smoke captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Framework | RAGFlow |
| Repository | https://github.com/infiniflow/ragflow.git |
| Pinned SHA | f90be41eab4ccb9ad2c52031e6c5d3d89d998909 |
| INSTRUMENT_HASH | 1a2434beba68e3381d07a34c81babcc12e2b02caac4a56b58203fc55cc899f19 |
| Security gate | N/A in CP03 |

## Dossier Dimensions

### 1. Boot outcome

Verdict: PASS for local Docker boot smoke.

Evidence:

- Source pin: `.harness/ekb-research/checkpoints/03/iter-1/evidence/clone.txt`
- RAGFlow prerequisites: `.harness/ekb-research/workspace/ragflow/README.md:151` through `.harness/ekb-research/workspace/ragflow/README.md:155`
- Local compose services: `.harness/ekb-research/checkpoints/03/iter-1/evidence/compose-services.txt`
- Local deploy overrides: `.harness/ekb-research/checkpoints/03/iter-1/evidence/local-deploy-overrides.diff`
- Compose config transcript: `.harness/ekb-research/checkpoints/03/iter-1/evidence/compose-config.yml`
- Compose up transcript: `.harness/ekb-research/checkpoints/03/iter-1/evidence/compose-up.txt`
- Post-up status: `.harness/ekb-research/checkpoints/03/iter-1/evidence/compose-ps-after-up.txt`
- Post-smoke status: `.harness/ekb-research/checkpoints/03/iter-1/evidence/compose-ps-after-smoke.txt`
- Runtime readiness log: `.harness/ekb-research/checkpoints/03/iter-1/evidence/ragflow-cpu-logs-tail.txt`
- Web smoke: `.harness/ekb-research/checkpoints/03/iter-1/evidence/smoke-ui-18080.txt`
- API smoke: `.harness/ekb-research/checkpoints/03/iter-1/evidence/smoke-api-19380-after-ready.txt`
- Teardown: `.harness/ekb-research/checkpoints/03/iter-1/evidence/compose-down.txt`
- Teardown residue checks: `.harness/ekb-research/checkpoints/03/iter-1/evidence/teardown-containers.txt` and `.harness/ekb-research/checkpoints/03/iter-1/evidence/teardown-volumes.txt`

Observed behavior:

- Boot command used `docker compose -f docker-compose.yml -f docker-compose.cp03-arm64.yml --profile elasticsearch --profile cpu up -d` with `COMPOSE_PROJECT_NAME=ekbcp03ragflow`.
- Services started: `mysql`, `redis`, `es01`, `minio`, and `ragflow-cpu`.
- `mysql`, `redis`, `es01`, and `minio` reached Docker healthy status. `ragflow-cpu` has no Docker healthcheck but logged `RAGFlow server is ready after 24.228793144226074s initialization`.
- `GET http://localhost:18080/` returned `HTTP/1.1 200 OK` with the RAGFlow web shell.
- `GET http://localhost:19380/` returned structured JSON `404 Not Found`, proving the Python service was accepting HTTP after readiness.
- `docker compose down -v` removed the CP03 containers, network, and four project volumes. Follow-up filtered container and volume checks returned only headers.

Findings:

- F-RAGFLOW-001
- F-RAGFLOW-002

### 2. Ingestion behavior

Status: not exercised in CP03.

Evidence:

- Planned for later benchmark checkpoints.

Findings:

- none

### 3. Retrieval behavior

Status: not exercised in CP03.

Evidence:

- Planned for later benchmark checkpoints.

Findings:

- none

### 4. Tenant isolation mechanism

Status: not exercised in CP03.

Evidence:

- Planned for later source inspection and benchmark checkpoints.

Findings:

- none

### 5. Permission/ACL model

Status: not exercised in CP03.

Evidence:

- Planned for later source inspection and benchmark checkpoints.

Findings:

- none

### 6. Data model reconstruction

Status: not exercised in CP03.

Evidence:

- Planned for later source inspection.

Findings:

- none

### 7. Generation and citation

Status: not exercised in CP03.

Evidence:

- Planned for later benchmark checkpoints.

Findings:

- none

### 8. Tool/MCP surface

Status: not exercised in CP03.

Evidence:

- Planned for later source inspection.

Findings:

- none

### 9. Observability and eval

Status: partial boot-level observation only.

Evidence:

- Runtime logs: `.harness/ekb-research/checkpoints/03/iter-1/evidence/ragflow-cpu-logs-tail.txt`

Findings:

- none

### 10. Extraction candidates

Status: not assessed in CP03.

Evidence:

- Planned for later synthesis.

Findings:

- none

### 11. License posture

Status: not assessed in CP03.

Evidence:

- Planned for later source inspection.

Findings:

- none

### 12. Benchmark grid result

Status: not run in CP03.

Evidence:

- Query instrument frozen in `docs/ekb-research/benchmark/queries.json`.

Findings:

- none

### 13. Gaps vs target design

Status: not assessed in CP03.

Evidence:

- Planned for final cross-framework synthesis.

Findings:

- none

## Seven-Dimension Benchmark Grid

| Dimension | Capability level | Earned maturity | Verdict | Transcript evidence | Finding ids |
| --- | --- | --- | --- | --- | --- |
| R retrieval+citation | N/A | N/A | N/A | not run in CP03 | none |
| I tenant isolation | N/A | N/A | N/A | not run in CP03 | none |
| P permission scope | N/A | N/A | N/A | not run in CP03 | none |
| N no-answer | N/A | N/A | N/A | not run in CP03 | none |
| M multilingual | N/A | N/A | N/A | not run in CP03 | none |
| A multi-agent/tool | N/A | N/A | N/A | not run in CP03 | none |
| F freshness | N/A | N/A | N/A | not run in CP03 | none |

## Findings View

Rows mirror `docs/ekb-research/findings/ledger.md`.

| finding_id | source_checkpoint | category | severity | subsystem | status |
| --- | --- | --- | --- | --- | --- |
| F-RAGFLOW-001 | CP03 | deploy-friction | major | docker-compose | confirmed |
| F-RAGFLOW-002 | CP03 | deploy-friction | medium | local-runtime | confirmed |
