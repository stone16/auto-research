# WeKnora Dossier

Status: CP08 ingest/query/code-audit captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Framework | WeKnora |
| Repository | https://github.com/Tencent/WeKnora |
| Pinned SHA | 7d8a80ae8d8ab3e54c769363439b697613a810e9 |
| INSTRUMENT_HASH | 1a2434beba68e3381d07a34c81babcc12e2b02caac4a56b58203fc55cc899f19 |
| Security gate | PASS: 0 forbidden-source leaks across I*/P*/P5/A2/F1 transcripts. One non-security PARTIAL remains: N2 missed required D03 under keyword retrieval. |

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
- CP07 teardown: `.harness/ekb-research/checkpoints/07/iter-1/evidence/compose-down-with-mcp-health.txt`
- CP07 teardown residue checks: `.harness/ekb-research/checkpoints/07/iter-1/evidence/teardown-containers-with-mcp-health.txt`, `.harness/ekb-research/checkpoints/07/iter-1/evidence/teardown-volumes-with-mcp-health.txt`, and `.harness/ekb-research/checkpoints/07/iter-1/evidence/teardown-networks-with-mcp-health.txt`
- CP08 ready status with MCP image built: `.harness/ekb-research/checkpoints/08/iter-1/evidence/compose-ps-ready.txt`
- CP08 API smoke: `.harness/ekb-research/checkpoints/08/iter-1/evidence/smoke-api-health.headers` and `.harness/ekb-research/checkpoints/08/iter-1/evidence/smoke-api-health.body`

Observed behavior:

- CP07 cloned WeKnora at pinned SHA `7d8a80ae8d8ab3e54c769363439b697613a810e9`.
- The first shallow clone attempt failed with a GitHub HTTP/2 stream reset. A retry with HTTP/1.1 and shallow single-branch clone succeeded.
- The local stack used Docker Compose projects `ekbcp07weknora` and `ekbcp08weknora`, host ports `18082` for frontend, `18083` for app, and `18084` for MCP, plus a local MCP health override.
- Services started for the benchmark stack: `frontend`, `app`, `docreader`, `postgres`, `redis`, and targeted profile service `mcp`.
- `GET http://localhost:18083/health` returned HTTP 200 with `{"status":"ok"}`.
- `GET http://localhost:18082/` returned HTTP 200 with the WeKnora HTML shell in CP07.
- `GET http://localhost:18084/mcp` returned HTTP 406 from uvicorn in CP07, proving the MCP HTTP endpoint was live and enforcing its expected transport contract.
- `docker compose down -v` had to be run with `COMPOSE_PROFILES=full` and the local health override so targeted `mcp` profile resources were removed.
- CP08 had to build the local MCP image before `docker compose up --no-build` could succeed.

Findings:

- F-WEKNORA-001
- F-WEKNORA-002

### 2. Ingestion behavior

Verdict: PASS for corpus ingestion and source accounting.

Evidence:

- Benchmark summary: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-benchmark-summary.json`
- Upload records: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-upload-documents-final.json`
- Source-to-KB map: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-source-kb-map.json`
- Source-to-knowledge map: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-source-knowledge-map.json`
- Chunk counts: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-chunk-counts.json`
- Runner output: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-runner-output.txt`

Observed behavior:

- The runner ingested 21/21 manifest documents at matching INSTRUMENT_HASH `1a2434beba68e3381d07a34c81babcc12e2b02caac4a56b58203fc55cc899f19`.
- All 21 documents received WeKnora knowledge IDs and reached completed status.
- SHA-256 mismatches: none.
- Manual fallback uploads: none.
- Chunk totals were one chunk for D01-D12 and D14-D21, and seven chunks for D13.
- The run used deterministic local embeddings and WeKnora hybrid-search with vector matching disabled; ingestion evidence is source/accounting evidence, not production embedding-quality evidence.

Findings:

- F-WEKNORA-003

### 3. Retrieval behavior

Verdict: PARTIAL overall because all queries ran and leak gate passed, but N2 missed required D03.

Evidence:

- Query results: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-query-results.json`
- Benchmark summary: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-benchmark-summary.json`
- Transcripts: `docs/ekb-research/benchmark/runs/weknora/`
- N2 transcript: `docs/ekb-research/benchmark/runs/weknora/N2.md`

Observed behavior:

- All 22 benchmark queries were attempted.
- Verdict counts: 6 `PASS`, 15 `PASS-with-source-filter`, and 1 `PARTIAL`.
- The single `PARTIAL` was N2, where no forbidden source was returned but required D03 was missing. Returned sources were D04, D05, D07, D10, D11, D13, D17, and D21.
- R1-R5 passed under keyword retrieval. R6 passed with source filtering.
- Results should be read as retrieval/source-selection evidence only. CP08 did not run generated answer assembly, final citation formatting, or refusal text evaluation.

Findings:

- F-WEKNORA-003
- F-WEKNORA-004

### 4. Tenant isolation mechanism

Verdict: PASS-with-source-filter for the benchmark isolation queries.

Evidence:

- Tenant/API-key setup: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-tenants-auth.json`
- Knowledge base setup: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-knowledge-bases.json`
- I1 transcript: `docs/ekb-research/benchmark/runs/weknora/I1.md`
- I2 transcript: `docs/ekb-research/benchmark/runs/weknora/I2.md`
- I3 transcript: `docs/ekb-research/benchmark/runs/weknora/I3.md`
- RBAC route injection: `.harness/ekb-research/workspace/weknora/internal/router/router.go:175` through `.harness/ekb-research/workspace/weknora/internal/router/router.go:202`
- KB access guard design: `.harness/ekb-research/workspace/weknora/internal/middleware/kb_access.go:17` through `.harness/ekb-research/workspace/weknora/internal/middleware/kb_access.go:53`
- KB hybrid-search route guard: `.harness/ekb-research/workspace/weknora/internal/router/router.go:379` through `.harness/ekb-research/workspace/weknora/internal/router/router.go:400`

Observed behavior:

- CP08 created separate Acme and Globex tenants and used tenant-specific API keys for the benchmark requests.
- I1, I2, and I3 returned zero forbidden-source leaks.
- The native boundary exercised by WeKnora was tenant/API-key plus KB read access. The benchmark's finer workspace, document, group, grant, clearance, and revocation fixtures were enforced externally with `knowledge_ids` source filters.
- Code audit found route-level role guards and KB access middleware, including read gating on `POST /knowledge-bases/:id/hybrid-search`.

Findings:

- F-WEKNORA-003

### 5. Permission/ACL model

Verdict: PASS-with-source-filter for benchmark permission queries; native document-level principal policy was not proven.

Evidence:

- P1 transcript: `docs/ekb-research/benchmark/runs/weknora/P1.md`
- P2 transcript: `docs/ekb-research/benchmark/runs/weknora/P2.md`
- P3 transcript: `docs/ekb-research/benchmark/runs/weknora/P3.md`
- P4 transcript: `docs/ekb-research/benchmark/runs/weknora/P4.md`
- P5 transcript: `docs/ekb-research/benchmark/runs/weknora/P5.md`
- Knowledge upload/list guards: `.harness/ekb-research/workspace/weknora/internal/router/router.go:293` through `.harness/ekb-research/workspace/weknora/internal/router/router.go:299`
- Knowledge document guards: `.harness/ekb-research/workspace/weknora/internal/router/router.go:302` through `.harness/ekb-research/workspace/weknora/internal/router/router.go:330`
- Chunk route guards: `.harness/ekb-research/workspace/weknora/internal/router/router.go:260` through `.harness/ekb-research/workspace/weknora/internal/router/router.go:269`
- Denied-role audit hook: `.harness/ekb-research/workspace/weknora/internal/middleware/rbac.go:91` through `.harness/ekb-research/workspace/weknora/internal/middleware/rbac.go:98`

Observed behavior:

- P1-P5 all passed the leak gate.
- CP08 used WeKnora tenant/API-key separation and explicit `knowledge_ids` filters to match each benchmark principal's permitted source set.
- WeKnora has KB-level route guards for reads/writes and ownership/admin checks for mutations. CP08 did not find a native model equivalent to the benchmark's per-document workspace/group/grant/clearance fixtures on the exercised search path.

Findings:

- F-WEKNORA-003

### 6. Data model reconstruction

Verdict: PASS for benchmark-accounting reconstruction.

Evidence:

- Source-to-KB map: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-source-kb-map.json`
- Source-to-knowledge map: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-source-knowledge-map.json`
- Chunk counts: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-chunk-counts.json`
- Query results: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-query-results.json`

Observed behavior:

- CP08 reconstructed a source-id to WeKnora KB/knowledge-id mapping for every benchmark document.
- Acme sources were split into sales, HR, and ops KBs; Globex sources were isolated in the Globex sales KB.
- The transcript layer records principal, tenant/API-key scope, requested KB IDs, requested source IDs, required sources, forbidden sources, returned source IDs, and top chunks.

Findings:

- F-WEKNORA-003

### 7. Generation and citation

Verdict: NOT EVALUATED as generated-answer behavior.

Evidence:

- Query transcripts: `docs/ekb-research/benchmark/runs/weknora/`
- Query results: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-query-results.json`

Observed behavior:

- CP08 evaluated retrieved chunks and source IDs only.
- WeKnora returned chunk metadata and knowledge names adequate for source-selection transcripts.
- CP08 did not evaluate final answer wording, citation rendering, refusal behavior, or trace export in generated responses.

Findings:

- F-WEKNORA-004

### 8. Tool/MCP surface

Verdict: PARTIAL. The MCP service boots and has tool-management code paths, but CP08 did not use MCP for benchmark search because the exposed search tool lacks `knowledge_ids` filtering.

Evidence:

- MCP compose service: `.harness/ekb-research/workspace/weknora/docker-compose.yml:768` through `.harness/ekb-research/workspace/weknora/docker-compose.yml:784`
- MCP smoke: `.harness/ekb-research/checkpoints/07/iter-1/evidence/smoke-mcp-get-with-mcp-health.txt`
- A1 transcript: `docs/ekb-research/benchmark/runs/weknora/A1.md`
- A2 transcript: `docs/ekb-research/benchmark/runs/weknora/A2.md`
- MCP service routes: `.harness/ekb-research/workspace/weknora/internal/router/router.go:849` through `.harness/ekb-research/workspace/weknora/internal/router/router.go:879`
- MCP create handler tenant and SSRF handling: `.harness/ekb-research/workspace/weknora/internal/handler/mcp_service.go:61` through `.harness/ekb-research/workspace/weknora/internal/handler/mcp_service.go:89`
- MCP tool listing tenant scope: `.harness/ekb-research/workspace/weknora/internal/handler/mcp_service.go:445` through `.harness/ekb-research/workspace/weknora/internal/handler/mcp_service.go:467`
- MCP approval handlers: `.harness/ekb-research/workspace/weknora/internal/handler/mcp_service.go:506` through `.harness/ekb-research/workspace/weknora/internal/handler/mcp_service.go:580`
- MCP service test path: `.harness/ekb-research/workspace/weknora/internal/application/service/mcp_service.go:338` through `.harness/ekb-research/workspace/weknora/internal/application/service/mcp_service.go:417`
- Standalone MCP API-key header: `.harness/ekb-research/workspace/weknora/mcp-server/weknora_mcp_server.py:31` through `.harness/ekb-research/workspace/weknora/mcp-server/weknora_mcp_server.py:65`
- MCP `hybrid_search` schema: `.harness/ekb-research/workspace/weknora/mcp-server/weknora_mcp_server.py:588` through `.harness/ekb-research/workspace/weknora/mcp-server/weknora_mcp_server.py:617`
- MCP `hybrid_search` call path: `.harness/ekb-research/workspace/weknora/mcp-server/weknora_mcp_server.py:1070` through `.harness/ekb-research/workspace/weknora/mcp-server/weknora_mcp_server.py:1084`

Observed behavior:

- CP07/CP08 proved the MCP HTTP service can start beside the app.
- Code audit found app-side MCP service registration/listing/testing/approval routes with role gates, tenant IDs, SSRF validation, and secret-omitting DTO responses.
- The standalone MCP server uses `WEKNORA_API_KEY` as an `X-API-Key` header to call WeKnora APIs.
- The MCP `hybrid_search` tool accepts KB ID, query, thresholds, and match count, but not `knowledge_ids`. CP08 therefore used REST `hybrid-search` for source-gated benchmark queries and marked A2 as no tool invocation.

Findings:

- F-WEKNORA-005

### 9. Observability and eval

Verdict: PARTIAL implementation support.

Evidence:

- Langfuse middleware registration: `.harness/ekb-research/workspace/weknora/internal/router/router.go:171` through `.harness/ekb-research/workspace/weknora/internal/router/router.go:173`
- Audit log schema: `.harness/ekb-research/workspace/weknora/migrations/versioned/000044_audit_log.up.sql:20` through `.harness/ekb-research/workspace/weknora/migrations/versioned/000044_audit_log.up.sql:64`
- Audit log type: `.harness/ekb-research/workspace/weknora/internal/types/audit_log.go:131` through `.harness/ekb-research/workspace/weknora/internal/types/audit_log.go:157`
- Audit service write/dedup path: `.harness/ekb-research/workspace/weknora/internal/application/service/audit_log.go:44` through `.harness/ekb-research/workspace/weknora/internal/application/service/audit_log.go:138`
- Tenant audit feed route: `.harness/ekb-research/workspace/weknora/internal/router/router.go:609` through `.harness/ekb-research/workspace/weknora/internal/router/router.go:615`
- System audit feed route: `.harness/ekb-research/workspace/weknora/internal/router/router.go:823` through `.harness/ekb-research/workspace/weknora/internal/router/router.go:831`

Observed behavior:

- WeKnora includes Langfuse middleware, but CP08 did not configure external Langfuse credentials or validate exported traces.
- Code audit found a per-tenant `audit_logs` table, indexes for tenant feeds/action filtering/retention, a denied-access action, deduplicated denial logging, and tenant/system audit feed routes.
- CP08 did not run live audit-log assertions; this is implementation evidence, not runtime audit coverage.

Findings:

- F-WEKNORA-006

### 10. Extraction candidates

Status: candidate with guardrails.

Evidence:

- Boot evidence listed in dimension 1.
- Ingest/query evidence listed in dimensions 2 and 3.
- RBAC, audit, and MCP code-audit evidence listed in dimensions 4, 5, 8, and 9.

Observed behavior:

- WeKnora is a viable extraction candidate for local boot, corpus ingestion, tenant/API-key scoped KB retrieval, route-level RBAC, per-tenant audit logging, and MCP service management.
- Extraction should not claim benchmark-equivalent document-level ACLs, production semantic retrieval quality, generated answer citation quality, or MCP source-gated search without additional implementation or tests.

Findings:

- F-WEKNORA-003
- F-WEKNORA-004
- F-WEKNORA-005
- F-WEKNORA-006

### 11. License posture

Verdict: PASS for top-level license identification; dependency-license audit not performed.

Evidence:

- Main license: `.harness/ekb-research/workspace/weknora/LICENSE:1` through `.harness/ekb-research/workspace/weknora/LICENSE:4`
- Third-party license section begins at `.harness/ekb-research/workspace/weknora/LICENSE:31`
- MCP server license file: `.harness/ekb-research/workspace/weknora/mcp-server/LICENSE`

Observed behavior:

- The top-level repository states MIT licensing for the project, with separately listed third-party components under other licenses.
- CP08 did not perform a full transitive dependency-license audit.

Findings:

- none

### 12. Benchmark grid result

Verdict: PARTIAL overall with PASS leak gate.

Evidence:

- CP08 context: `.harness/ekb-research/checkpoints/08/context.md`
- Summary: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-benchmark-summary.json`
- Query results: `.harness/ekb-research/checkpoints/08/iter-1/evidence/cp08-query-results.json`
- Transcripts: `docs/ekb-research/benchmark/runs/weknora/`

Observed behavior:

- 22/22 queries attempted.
- 0 leak failures.
- Verdict counts: 6 `PASS`, 15 `PASS-with-source-filter`, 1 `PARTIAL`.
- The grid is source-selection/retrieval evidence, not generated-answer evidence.

Findings:

- F-WEKNORA-003
- F-WEKNORA-004
- F-WEKNORA-005

### 13. Gaps vs target design

Verdict: DOCUMENTED.

Evidence:

- RBAC evidence listed in dimensions 4 and 5.
- MCP evidence listed in dimension 8.
- Query evidence listed in dimension 12.

Observed gaps:

- Native ACL gap: benchmark workspace, document group, explicit grant, clearance, and revocation fixtures were modeled externally through `knowledge_ids` filters rather than natively by WeKnora.
- Retrieval-quality gap: N2 missed required D03 under deterministic, vector-disabled keyword retrieval.
- Tool gap: MCP `hybrid_search` lacks the `knowledge_ids` filter needed to preserve the benchmark source gate.
- Observability gap: audit and Langfuse hooks are code-audited, but not live-export verified.

Findings:

- F-WEKNORA-003
- F-WEKNORA-004
- F-WEKNORA-005
- F-WEKNORA-006

## Seven-Dimension Benchmark Grid

| Dimension | Capability level | Earned maturity | Verdict | Transcript evidence | Finding ids |
| --- | --- | --- | --- | --- | --- |
| R retrieval+citation | Retrieval chunks/source IDs only; generated citations not evaluated | medium for source selection, low for answer citation | 5 PASS, 1 PASS-with-source-filter | `R1.md`, `R2.md`, `R3.md`, `R4.md`, `R5.md`, `R6.md` | F-WEKNORA-003 |
| I tenant isolation | Native tenant/API-key boundary plus external `knowledge_ids` source gate | medium | 3 PASS-with-source-filter | `I1.md`, `I2.md`, `I3.md` | F-WEKNORA-003 |
| P permission scope | KB route RBAC exists; benchmark document-level principal policy enforced externally | low-to-medium | 5 PASS-with-source-filter | `P1.md`, `P2.md`, `P3.md`, `P4.md`, `P5.md` | F-WEKNORA-003 |
| N no-answer | Source-gate behavior only; refusal text not evaluated | low | 1 PASS, 1 PASS-with-source-filter, 1 PARTIAL | `N1.md`, `N2.md`, `N3.md` | F-WEKNORA-004 |
| M multilingual | Source-gate behavior under multilingual prompts | low-to-medium | 2 PASS-with-source-filter | `M1.md`, `M2.md` | F-WEKNORA-003 |
| A multi-agent/tool | MCP boots and has tool routes; benchmark search used REST because MCP lacks source filter | low | 2 PASS-with-source-filter | `A1.md`, `A2.md` | F-WEKNORA-005 |
| F freshness | Source-gated retrieval avoided forbidden stale source in F1 | low-to-medium | 1 PASS-with-source-filter | `F1.md` | F-WEKNORA-003 |

## Findings View

Rows here mirror docs/ekb-research/findings/ledger.md. Do not create dossier-only findings.

| finding_id | summary |
| --- | --- |
| F-WEKNORA-001 | WeKnora local MCP boot is profile-gated and needs an explicit health override for checkpoint-grade readiness evidence. |
| F-WEKNORA-002 | WeKnora boot succeeded but introduced a large image footprint and profile-created volumes, so local runs require disciplined teardown and deferred image cleanup. |
| F-WEKNORA-003 | WeKnora CP08 passed the leak gate only with tenant/API-key boundaries plus external `knowledge_ids` source filters; benchmark document-level principal policy was not native. |
| F-WEKNORA-004 | WeKnora CP08 keyword retrieval missed required D03 on N2 despite zero leaks, so no-answer/source-selection quality remains partial. |
| F-WEKNORA-005 | WeKnora MCP `hybrid_search` lacks `knowledge_ids`, so the MCP search surface cannot preserve the benchmark document-level source gate as exercised. |
| F-WEKNORA-006 | WeKnora includes per-tenant audit and Langfuse hooks in code, but CP08 did not validate live audit rows or trace export. |
