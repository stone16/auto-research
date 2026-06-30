# AnythingLLM Dossier

Status: CP12 boot/ingest/query/code-audit captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Framework | AnythingLLM |
| Repository | https://github.com/Mintplex-Labs/anything-llm.git |
| Pinned SHA | 94735ac54ff22e22d3957e5a633e30760227aa7b |
| INSTRUMENT_HASH | 1a2434beba68e3381d07a34c81babcc12e2b02caac4a56b58203fc55cc899f19 |
| Security gate | PASS: 0 forbidden-source leaks across I*/P*/P5/A2/F1 transcripts. Two PARTIAL results remain under CP12 source-gated AnythingLLM chunk scanning: N2 missed D03 and A1 retrieved D17 without a live MCP/tool trace. |

## Dossier Dimensions

### 1. Boot outcome

Verdict: PASS for local Docker boot smoke.

Evidence:

- Source pin: `.harness/ekb-research/checkpoints/12/iter-1/pinned-sha.txt`
- Upstream Docker image instructions: `.harness/ekb-research/workspace/anythingllm/docker/HOW_TO_USE_DOCKER.md:40` through `.harness/ekb-research/workspace/anythingllm/docker/HOW_TO_USE_DOCKER.md:63`
- Upstream compose shape: `.harness/ekb-research/workspace/anythingllm/docker/HOW_TO_USE_DOCKER.md:94` through `.harness/ekb-research/workspace/anythingllm/docker/HOW_TO_USE_DOCKER.md:115`
- Repo compose storage/env surface: `.harness/ekb-research/workspace/anythingllm/docker/docker-compose.yml:7` through `.harness/ekb-research/workspace/anythingllm/docker/docker-compose.yml:31`
- Local compose config: `.harness/ekb-research/checkpoints/12/iter-1/anythingllm-compose.yml`
- Image inspect: `.harness/ekb-research/checkpoints/12/iter-1/evidence/image-inspect-anythingllm-latest.json`
- Boot: `.harness/ekb-research/checkpoints/12/iter-1/evidence/compose-up.txt`, `.harness/ekb-research/checkpoints/12/iter-1/evidence/health-poll.txt`, `.harness/ekb-research/checkpoints/12/iter-1/evidence/container-ps-after-up.txt`, and `.harness/ekb-research/checkpoints/12/iter-1/evidence/compose-ps-after-up.txt`
- HTTP smoke: `.harness/ekb-research/checkpoints/12/iter-1/evidence/smoke-ping.headers`, `.harness/ekb-research/checkpoints/12/iter-1/evidence/smoke-ping.body`, `.harness/ekb-research/checkpoints/12/iter-1/evidence/smoke-root.headers`, and `.harness/ekb-research/checkpoints/12/iter-1/evidence/smoke-root.body`
- Teardown: `.harness/ekb-research/checkpoints/12/iter-1/evidence/compose-down.txt`, `.harness/ekb-research/checkpoints/12/iter-1/evidence/container-status-after-down.txt`, `.harness/ekb-research/checkpoints/12/iter-1/evidence/volume-residual-after-down.txt`, `.harness/ekb-research/checkpoints/12/iter-1/evidence/network-residual-after-down.txt`, `.harness/ekb-research/checkpoints/12/iter-1/evidence/port-18097-after-down.txt`, `.harness/ekb-research/checkpoints/12/iter-1/evidence/anythingllm-storage-du-before-remove.txt`, and `.harness/ekb-research/checkpoints/12/iter-1/evidence/anythingllm-storage-removed-check.txt`

Observed behavior:

- CP12 cloned AnythingLLM at pinned SHA `94735ac54ff22e22d3957e5a633e30760227aa7b`.
- CP12 used the upstream `mintplexlabs/anythingllm:latest` image on host port `18097`, with `STORAGE_DIR=/app/server/storage` bound to a checkpoint-local directory.
- `GET http://localhost:18097/api/ping` returned HTTP 200 with `{"online":true}` while the container was healthy.
- The official image size was about 3.14 GB. After teardown, Docker still reported 27.63 GB reclaimable images and 34.63 GB reclaimable local volumes from the broader multi-framework run; global pruning is deferred until the full harness completes.
- The stack was removed with `docker compose down -v`; the CP12 storage bind mount was 704K before deletion and was removed after teardown.

Findings:

- F-ANYTHINGLLM-001

### 2. Ingestion behavior

Verdict: PASS for corpus persistence and source accounting.

Evidence:

- Corpus hash checks: `.harness/ekb-research/checkpoints/12/iter-1/evidence/cp12-corpus-hash-checks.json`
- API key, workspace, and document API verification: `.harness/ekb-research/checkpoints/12/iter-1/evidence/cp12-anythingllm-api-check.json`
- Source-to-workspace map: `.harness/ekb-research/checkpoints/12/iter-1/evidence/cp12-source-workspace-map.json`
- Document counts: `.harness/ekb-research/checkpoints/12/iter-1/evidence/cp12-document-counts.json`
- DB counts before teardown: `.harness/ekb-research/checkpoints/12/iter-1/evidence/db-counts-before-down.txt`
- SQLite schema: `.harness/ekb-research/workspace/anythingllm/server/prisma/schema.prisma:13` through `.harness/ekb-research/workspace/anythingllm/server/prisma/schema.prisma:39`
- Workspace/document schema: `.harness/ekb-research/workspace/anythingllm/server/prisma/schema.prisma:121` through `.harness/ekb-research/workspace/anythingllm/server/prisma/schema.prisma:152`
- Document model and vector namespace: `.harness/ekb-research/workspace/anythingllm/server/models/documents.js:83` through `.harness/ekb-research/workspace/anythingllm/server/models/documents.js:160`
- Raw-text document API: `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/document/index.js:480` through `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/document/index.js:615`

Observed behavior:

- CP12 ingested 21/21 manifest documents at matching INSTRUMENT_HASH.
- SHA-256 mismatches: none.
- CP12 seeded one AnythingLLM workspace and one `workspace_documents` row per benchmark source, then restarted the app so the API read back the externally seeded SQLite state.
- Final DB counts before teardown: 1 CP12 API key, 21 CP12 workspaces, 21 CP12 workspace document rows, and 2 system settings rows.
- `/api/v1/auth`, `/api/v1/workspaces`, `/api/v1/workspace/cp12-d01`, and `/api/v1/documents` returned HTTP 200 with the CP12 API key.
- CP12 did not run production embeddings. It used deterministic chunks extracted from the same source texts for benchmark query scoring.

Findings:

- F-ANYTHINGLLM-003

### 3. Retrieval behavior

Verdict: PARTIAL overall because all queries ran and the leak gate passed, but N2 and A1 did not satisfy their full non-security rubrics.

Evidence:

- Query results: `.harness/ekb-research/checkpoints/12/iter-1/evidence/cp12-query-results.json`
- Benchmark summary: `.harness/ekb-research/checkpoints/12/iter-1/evidence/cp12-benchmark-summary.json`
- Runner stdout: `.harness/ekb-research/checkpoints/12/iter-1/evidence/cp12-runner.stdout.json`
- Transcripts: `docs/ekb-research/benchmark/runs/anythingllm/`
- Partial transcripts: `docs/ekb-research/benchmark/runs/anythingllm/N2.md` and `docs/ekb-research/benchmark/runs/anythingllm/A1.md`

Observed behavior:

- All 22 benchmark queries were attempted.
- Verdict counts: 8 `PASS`, 11 `PASS-with-source-filter`, 1 `PASS-without-tool`, and 2 `PARTIAL`.
- N2 was PARTIAL because the ambiguous deal-approval query missed required D03 under deterministic chunk scoring.
- A1 was PARTIAL because D17 was retrieved, but CP12 did not execute a native MCP or tool call trace.
- Results should be read as source-selection and workspace/document persistence evidence only. CP12 did not evaluate generated answer wording, citation rendering, semantic embeddings, reranking, or live tool execution.

Findings:

- F-ANYTHINGLLM-003

### 4. Tenant isolation mechanism

Verdict: PASS-with-source-filter for benchmark isolation queries.

Evidence:

- I1 transcript: `docs/ekb-research/benchmark/runs/anythingllm/I1.md`
- I2 transcript: `docs/ekb-research/benchmark/runs/anythingllm/I2.md`
- I3 transcript: `docs/ekb-research/benchmark/runs/anythingllm/I3.md`
- Query summary: `.harness/ekb-research/checkpoints/12/iter-1/evidence/cp12-benchmark-summary.json`
- API key middleware: `.harness/ekb-research/workspace/anythingllm/server/utils/middleware/validApiKey.js:4` through `.harness/ekb-research/workspace/anythingllm/server/utils/middleware/validApiKey.js:24`
- UI workspace validation: `.harness/ekb-research/workspace/anythingllm/server/utils/middleware/validWorkspace.js:5` through `.harness/ekb-research/workspace/anythingllm/server/utils/middleware/validWorkspace.js:19`
- Workspace membership query: `.harness/ekb-research/workspace/anythingllm/server/models/workspace.js:290` through `.harness/ekb-research/workspace/anythingllm/server/models/workspace.js:324`
- Multi-workspace list with user filter: `.harness/ekb-research/workspace/anythingllm/server/models/workspace.js:411` through `.harness/ekb-research/workspace/anythingllm/server/models/workspace.js:438`

Observed behavior:

- I1, I2, and I3 returned zero forbidden-source leaks.
- The benchmark isolation gate was external: the runner selected per-source AnythingLLM workspaces according to the benchmark principal and forbidden-source fixtures.
- AnythingLLM has a multi-user workspace membership model through `workspace_users`, and UI/internal routes call `Workspace.getWithUser` when multi-user mode is active.
- CP12 did not prove a native AnythingLLM tenant/workspace/group/grant/clearance/revocation policy equivalent to the benchmark fixtures.

Findings:

- F-ANYTHINGLLM-002

### 5. Permission, RBAC, and developer API model

Verdict: PASS for code-audited role and membership surfaces; benchmark-equivalent document ACL was not proven.

Evidence:

- Multi-user role middleware: `.harness/ekb-research/workspace/anythingllm/server/utils/middleware/multiUserProtected.js:23` through `.harness/ekb-research/workspace/anythingllm/server/utils/middleware/multiUserProtected.js:83`
- Workspace-user membership table: `.harness/ekb-research/workspace/anythingllm/server/prisma/schema.prisma:214` through `.harness/ekb-research/workspace/anythingllm/server/prisma/schema.prisma:220`
- Workspace-user model helpers: `.harness/ekb-research/workspace/anythingllm/server/models/workspaceUsers.js:3` through `.harness/ekb-research/workspace/anythingllm/server/models/workspaceUsers.js:103`
- API workspace list and detail endpoints: `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/workspace/index.js:109` through `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/workspace/index.js:210`
- API direct workspace query helper: `.harness/ekb-research/workspace/anythingllm/server/models/workspace.js:556` through `.harness/ekb-research/workspace/anythingllm/server/models/workspace.js:570`
- API chat and OpenAI-compatible workspace access: `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/workspace/index.js:600` through `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/workspace/index.js:718`, and `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/openai/index.js:75` through `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/openai/index.js:155`
- P* transcripts: `docs/ekb-research/benchmark/runs/anythingllm/P1.md` through `docs/ekb-research/benchmark/runs/anythingllm/P5.md`

Observed behavior:

- Multi-user UI routes enforce role checks through `strictMultiUserRoleValid` or `flexUserRoleValid`.
- UI/internal workspace lookups can restrict non-admin/non-manager users through `workspace_users`.
- The developer API key middleware validates only the bearer API key and does not bind the key to a workspace, user, group, or per-document clearance.
- Developer API workspace list/detail/chat/OpenAI-compatible routes use direct `Workspace._findMany`, `Workspace.get`, or `Workspace.where` access. Those are useful integration surfaces, but they are not benchmark-equivalent principal scoping.
- CP12 therefore records no native document ACL proof for the benchmark. Source gates stayed outside AnythingLLM.

Findings:

- F-ANYTHINGLLM-002
- F-ANYTHINGLLM-004

### 6. Agent, MCP, and integration surfaces

Verdict: PASS for code-audited API, OpenAI-compatible, raw-text ingestion, and MCP/agent surfaces; live benchmark exercised only API and SQLite document/workspace reads.

Evidence:

- Developer API registration: `.harness/ekb-research/workspace/anythingllm/server/index.js:81` through `.harness/ekb-research/workspace/anythingllm/server/index.js:91`, and `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/index.js:1` through `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/index.js:18`
- Raw-text ingestion and workspace upload path: `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/document/index.js:31` through `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/document/index.js:52`, `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/document/index.js:610` through `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/document/index.js:615`, and `.harness/ekb-research/workspace/anythingllm/server/models/documents.js:324` through `.harness/ekb-research/workspace/anythingllm/server/models/documents.js:359`
- OpenAI-compatible model and chat routes: `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/openai/index.js:18` through `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/openai/index.js:68`, and `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/openai/index.js:75` through `.harness/ekb-research/workspace/anythingllm/server/endpoints/api/openai/index.js:155`
- MCP admin endpoints: `.harness/ekb-research/workspace/anythingllm/server/endpoints/mcpServers.js:12` through `.harness/ekb-research/workspace/anythingllm/server/endpoints/mcpServers.js:124`
- MCP-to-agent tool wrapper: `.harness/ekb-research/workspace/anythingllm/server/utils/MCP/index.js:17` through `.harness/ekb-research/workspace/anythingllm/server/utils/MCP/index.js:127`
- Agent document citation injection: `.harness/ekb-research/workspace/anythingllm/server/utils/agents/index.js:736` through `.harness/ekb-research/workspace/anythingllm/server/utils/agents/index.js:770`

Observed behavior:

- AnythingLLM exposes a broad developer API for workspace creation/listing, document upload/raw text, workspace chat, OpenAI-compatible models/chat, and document management.
- It has an MCP compatibility layer that converts active MCP server tools into agent plugins and admin-only UI endpoints for listing/toggling MCP servers and tools.
- Document context can be injected into agent messages with citation metadata.
- CP12 did not create a live MCP server, run JSON-RPC, or execute generated answers. Tool and MCP maturity is code-audit only for this checkpoint.

Findings:

- F-ANYTHINGLLM-004

### 7. Generation, citations, tools, and observability

Verdict: NOT EVALUATED as generated-answer, citation-rendering, live tool, or trace-export behavior.

Evidence:

- Query transcripts: `docs/ekb-research/benchmark/runs/anythingllm/`
- Query results: `.harness/ekb-research/checkpoints/12/iter-1/evidence/cp12-query-results.json`
- Benchmark summary: `.harness/ekb-research/checkpoints/12/iter-1/evidence/cp12-benchmark-summary.json`
- A1 transcript: `docs/ekb-research/benchmark/runs/anythingllm/A1.md`
- A2 transcript: `docs/ekb-research/benchmark/runs/anythingllm/A2.md`

Observed behavior:

- CP12 evaluated stored text chunks and source IDs only.
- A2 passed because no tool invocation occurred and no forbidden fixture output was returned; this should not be read as proof of native tool-permission policy.
- AnythingLLM source code shows chat, OpenAI-compatible, MCP, agent, and citation surfaces, but CP12 did not execute generated answer calls, citation rendering, refusal text, live MCP tool invocation, or exported traces.

Findings:

- F-ANYTHINGLLM-003
- F-ANYTHINGLLM-004

## Findings Summary

Rows mirror `docs/ekb-research/findings/ledger.md`.

| finding_id | Short title |
| --- | --- |
| F-ANYTHINGLLM-001 | Local boot succeeded with official Docker image and temporary storage footprint. |
| F-ANYTHINGLLM-002 | Multi-user workspace membership exists, but developer API keys are global and benchmark ACL fixtures were external. |
| F-ANYTHINGLLM-003 | Corpus persisted and leak gate passed, while N2/A1 remained partial and generated/tool behavior was not evaluated. |
| F-ANYTHINGLLM-004 | API, OpenAI-compatible, raw-text, agent, and MCP surfaces are useful extraction candidates with workspace-scoped document primitives. |
