# WeKnora Dossier

Status: CP07 boot smoke captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Framework | WeKnora |
| Repository | https://github.com/Tencent/WeKnora |
| Pinned SHA | 7d8a80ae8d8ab3e54c769363439b697613a810e9 |
| INSTRUMENT_HASH | 1a2434beba68e3381d07a34c81babcc12e2b02caac4a56b58203fc55cc899f19 |
| Security gate | N/A until CP08. CP07 proves local boot and smoke only; no benchmark query or leak gate was run. |

## Dossier Dimensions

### 1. Boot outcome

Verdict: PASS for local Docker boot smoke.

Evidence:

- Source pin: `.harness/ekb-research/checkpoints/07/iter-1/evidence/pinned-sha.txt`
- Clone retry log: `.harness/ekb-research/checkpoints/07/iter-1/evidence/clone-command-retry1.txt`
- Upstream Docker launch instructions: `.harness/ekb-research/workspace/weknora/README.md:201` through `.harness/ekb-research/workspace/weknora/README.md:208`
- Upstream profile table: `.harness/ekb-research/workspace/weknora/README.md:216` through `.harness/ekb-research/workspace/weknora/README.md:226`
- App and frontend compose services: `.harness/ekb-research/workspace/weknora/docker-compose.yml:1` through `.harness/ekb-research/workspace/weknora/docker-compose.yml:64`
- Docreader and Postgres healthchecks: `.harness/ekb-research/workspace/weknora/docker-compose.yml:223` through `.harness/ekb-research/workspace/weknora/docker-compose.yml:310`
- MCP compose service: `.harness/ekb-research/workspace/weknora/docker-compose.yml:768` through `.harness/ekb-research/workspace/weknora/docker-compose.yml:784`
- Local MCP health override: `.harness/ekb-research/workspace/weknora/docker-compose.cp07-health.yml:1`
- Ready status: `.harness/ekb-research/checkpoints/07/iter-1/evidence/compose-ps-ready-with-mcp-health.txt`
- API smoke: `.harness/ekb-research/checkpoints/07/iter-1/evidence/smoke-api-health-with-mcp-health.txt`
- Frontend smoke: `.harness/ekb-research/checkpoints/07/iter-1/evidence/smoke-frontend-root-with-mcp-health.txt`
- MCP smoke: `.harness/ekb-research/checkpoints/07/iter-1/evidence/smoke-mcp-get-with-mcp-health.txt`
- Runtime logs: `.harness/ekb-research/checkpoints/07/iter-1/evidence/compose-logs-ready-with-mcp-health-tail.txt`
- Teardown: `.harness/ekb-research/checkpoints/07/iter-1/evidence/compose-down-with-mcp-health.txt`
- Teardown residue checks: `.harness/ekb-research/checkpoints/07/iter-1/evidence/teardown-containers-with-mcp-health.txt`, `.harness/ekb-research/checkpoints/07/iter-1/evidence/teardown-volumes-with-mcp-health.txt`, and `.harness/ekb-research/checkpoints/07/iter-1/evidence/teardown-networks-with-mcp-health.txt`

Observed behavior:

- CP07 cloned WeKnora at pinned SHA `7d8a80ae8d8ab3e54c769363439b697613a810e9`.
- The first shallow clone attempt failed with a GitHub HTTP/2 stream reset. A retry with HTTP/1.1 and shallow single-branch clone succeeded.
- The local stack used Docker Compose project `ekbcp07weknora`, a local `.env` copied from `.env.example`, host ports `18082` for frontend, `18083` for app, and `18084` for MCP, plus a local MCP health override.
- Services started: `frontend`, `app`, `docreader`, `postgres`, `redis`, and targeted profile service `mcp`.
- `app`, `docreader`, `postgres`, and `mcp` reached Docker healthy status in the final run. `frontend` and `redis` were running; upstream compose does not define healthchecks for those services.
- `GET http://localhost:18083/health` returned `HTTP/1.1 200 OK` with `{"status":"ok"}`.
- `GET http://localhost:18082/` returned `HTTP/1.1 200 OK` with the WeKnora HTML shell.
- `GET http://localhost:18084/mcp` returned `HTTP/1.1 406 Not Acceptable` from uvicorn with a JSON-RPC error requiring `text/event-stream`, proving the MCP HTTP endpoint was live and enforcing the expected transport contract.
- `docker compose down -v` had to be run with `COMPOSE_PROFILES=full` and the local health override so the targeted `mcp` profile service and profile-created volumes were removed. Final residue checks returned only headers for CP07 containers, volumes, and networks.

Findings:

- F-WEKNORA-001
- F-WEKNORA-002

### 2. Ingestion behavior

Verdict: PENDING CP08.

Evidence:

- none yet

Findings:

- none

### 3. Retrieval behavior

Verdict: PENDING CP08.

Evidence:

- none yet

Findings:

- none

### 4. Tenant isolation mechanism

Verdict: PENDING CP08.

Evidence:

- none yet

Findings:

- none

### 5. Permission/ACL model

Verdict: PENDING CP08.

Evidence:

- none yet

Findings:

- none

### 6. Data model reconstruction

Verdict: PENDING CP08.

Evidence:

- none yet

Findings:

- none

### 7. Generation and citation

Verdict: PENDING CP08.

Evidence:

- none yet

Findings:

- none

### 8. Tool/MCP surface

Verdict: BOOT-SMOKE-ONLY.

Evidence:

- MCP compose service: `.harness/ekb-research/workspace/weknora/docker-compose.yml:768` through `.harness/ekb-research/workspace/weknora/docker-compose.yml:784`
- MCP Dockerfile: `.harness/ekb-research/workspace/weknora/mcp-server/Dockerfile:1` through `.harness/ekb-research/workspace/weknora/mcp-server/Dockerfile:16`
- MCP smoke: `.harness/ekb-research/checkpoints/07/iter-1/evidence/smoke-mcp-get-with-mcp-health.txt`
- MCP logs: `.harness/ekb-research/checkpoints/07/iter-1/evidence/compose-logs-ready-with-mcp-health-tail.txt`

Observed behavior:

- CP07 proved that the MCP HTTP service can start beside the app and answer a protocol-level HTTP request.
- CP07 did not configure a WeKnora API key, list MCP tools, or invoke MCP tools. Tool authorization and MCP bypass behavior remain CP08 scope.

Findings:

- F-WEKNORA-001

### 9. Observability and eval

Verdict: PENDING CP08.

Evidence:

- none yet

Findings:

- none

### 10. Extraction candidates

Status: preliminary.

Evidence:

- Boot evidence listed in dimension 1.

Observed behavior:

- WeKnora remains eligible for CP08 ingest/query/code-audit because CP07 boot and smoke passed.
- No subsystem should be selected for extraction from CP07 alone.

Findings:

- F-WEKNORA-001
- F-WEKNORA-002

### 11. License posture

Verdict: PENDING CP08.

Evidence:

- none yet

Findings:

- none

### 12. Benchmark grid result

Verdict: NOT RUN in CP07.

Evidence:

- CP07 context: `.harness/ekb-research/checkpoints/07/context.md`

Observed behavior:

- CP07 did not ingest the frozen corpus or run any of the 22 benchmark queries.
- The seven-dimension grid remains pending until CP08.

Findings:

- none

### 13. Gaps vs target design

Verdict: PENDING CP08.

Evidence:

- none yet

Findings:

- none

## Seven-Dimension Benchmark Grid

| Dimension | Capability level | Earned maturity | Verdict | Transcript evidence | Finding ids |
| --- | --- | --- | --- | --- | --- |
| R retrieval+citation | pending | pending | PENDING CP08 | none yet | none |
| I tenant isolation | pending | pending | PENDING CP08 | none yet | none |
| P permission scope | pending | pending | PENDING CP08 | none yet | none |
| N no-answer | pending | pending | PENDING CP08 | none yet | none |
| M multilingual | pending | pending | PENDING CP08 | none yet | none |
| A multi-agent/tool | pending | pending | PENDING CP08 | none yet | none |
| F freshness | pending | pending | PENDING CP08 | none yet | none |

## Findings View

Rows here mirror docs/ekb-research/findings/ledger.md. Do not create dossier-only findings.

| finding_id | summary |
| --- | --- |
| F-WEKNORA-001 | WeKnora local MCP boot is profile-gated and needs an explicit health override for checkpoint-grade readiness evidence. |
| F-WEKNORA-002 | WeKnora boot succeeded but introduced a large image footprint and profile-created volumes, so local runs require disciplined teardown and deferred image cleanup. |
