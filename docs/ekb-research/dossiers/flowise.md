# Flowise Dossier

Status: CP11 boot/ingest/query/code-audit captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Framework | Flowise |
| Repository | https://github.com/FlowiseAI/Flowise.git |
| Pinned SHA | de3a91827fbe2ae4629bddcd16f1adfe0191385f |
| INSTRUMENT_HASH | 1a2434beba68e3381d07a34c81babcc12e2b02caac4a56b58203fc55cc899f19 |
| Security gate | PASS: 0 forbidden-source leaks across I*/P*/P5/A2/F1 transcripts. Two PARTIAL results remain under CP11 source-gated Flowise chunk scanning: N2 missed D03 and A1 retrieved D17 without a live MCP/tool trace. |

## Dossier Dimensions

### 1. Boot outcome

Verdict: PASS for local Docker boot smoke.

Evidence:

- Source pin: `.harness/ekb-research/checkpoints/11/iter-1/evidence/pinned-sha.txt`
- Upstream npm and Docker instructions: `.harness/ekb-research/workspace/flowise/README.md:41` through `.harness/ekb-research/workspace/flowise/README.md:61`
- Upstream Docker image and persistence notes: `.harness/ekb-research/workspace/flowise/docker/README.md:1` through `.harness/ekb-research/workspace/flowise/docker/README.md:21`
- Upstream compose image and env surface: `.harness/ekb-research/workspace/flowise/docker/docker-compose.yml:3` through `.harness/ekb-research/workspace/flowise/docker/docker-compose.yml:19`
- Local compose config: `.harness/ekb-research/checkpoints/11/iter-1/flowise-compose.yml`
- Image inspect: `.harness/ekb-research/checkpoints/11/iter-1/evidence/image-inspect-flowise-latest.json`
- Clean-run boot: `.harness/ekb-research/checkpoints/11/iter-1/evidence/compose-up-clean-run.txt`, `.harness/ekb-research/checkpoints/11/iter-1/evidence/health-poll-clean-run.txt`, `.harness/ekb-research/checkpoints/11/iter-1/evidence/container-ps-clean-run.txt`, and `.harness/ekb-research/checkpoints/11/iter-1/evidence/compose-ps-clean-run.txt`
- HTTP smoke: `.harness/ekb-research/checkpoints/11/iter-1/evidence/smoke-ping-clean-run.headers`, `.harness/ekb-research/checkpoints/11/iter-1/evidence/smoke-ping-clean-run.body`, `.harness/ekb-research/checkpoints/11/iter-1/evidence/smoke-root.headers`, and `.harness/ekb-research/checkpoints/11/iter-1/evidence/smoke-root.body`
- Auth setup: `.harness/ekb-research/checkpoints/11/iter-1/evidence/register.response.json`, `.harness/ekb-research/checkpoints/11/iter-1/evidence/login.response.json`, `.harness/ekb-research/checkpoints/11/iter-1/evidence/create-apikey.response.json`, and `.harness/ekb-research/checkpoints/11/iter-1/evidence/auth-status.txt`
- Teardown: `.harness/ekb-research/checkpoints/11/iter-1/evidence/compose-down.txt`
- Teardown residue checks: `.harness/ekb-research/checkpoints/11/iter-1/evidence/container-status-after-down.txt`, `.harness/ekb-research/checkpoints/11/iter-1/evidence/volume-residual-after-down.txt`, `.harness/ekb-research/checkpoints/11/iter-1/evidence/network-residual-after-down.txt`, `.harness/ekb-research/checkpoints/11/iter-1/evidence/port-18096-after-down.txt`, `.harness/ekb-research/checkpoints/11/iter-1/evidence/flowise-data-du-before-remove.txt`, `.harness/ekb-research/checkpoints/11/iter-1/evidence/flowise-data-removed-check.txt`, and `.harness/ekb-research/checkpoints/11/iter-1/evidence/docker-system-df-after-down.txt`

Observed behavior:

- CP11 cloned Flowise at pinned SHA `de3a91827fbe2ae4629bddcd16f1adfe0191385f`.
- Upstream documents `npx flowise start`, Docker Compose from the `docker` folder, and the DockerHub image `flowiseai/flowise`.
- CP11 used a local compose wrapper around `flowiseai/flowise:latest` on host port `18096`, with Flowise persistence under a checkpoint-local bind mount.
- `GET http://localhost:18096/api/v1/ping` returned `pong` after Docker health reached `healthy`.
- Open Source registration, login, and API key creation all succeeded. Protected `/api/v1/*` routes require either an internal JWT-cookie request or a Bearer API key.
- The stack was removed with `docker compose down -v`; the checkpoint-local Flowise data directory was 424K before deletion, the directory was removed, and port `18096` had no listener after teardown.
- After teardown, Docker still reported 24.36GB reclaimable images and 34.63GB reclaimable local volumes from the broader multi-framework run. Those are retained until the full harness completes to avoid repeated large pulls.

Findings:

- F-FLOWISE-001

### 2. Ingestion behavior

Verdict: PASS for corpus persistence and source accounting.

Evidence:

- Corpus hash checks: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-corpus-hash-checks.json`
- Document store creation records: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-document-stores.json`
- Source-to-store map: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-source-store-map.json`
- Chunk counts: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-chunk-counts.json`
- API list check: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-document-store-list-api.json`
- API chunk sample: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-document-store-chunks-api-sample.json`
- Final DB counts before teardown: `.harness/ekb-research/checkpoints/11/iter-1/evidence/db-counts-before-down.txt`
- Data file inventory: `.harness/ekb-research/checkpoints/11/iter-1/evidence/flowise-data-files-before-down.txt`
- Document store routes: `.harness/ekb-research/workspace/flowise/packages/server/src/routes/documentstore/index.ts:12` through `.harness/ekb-research/workspace/flowise/packages/server/src/routes/documentstore/index.ts:84`
- Document store persistence service: `.harness/ekb-research/workspace/flowise/packages/server/src/services/documentstore/index.ts:60` through `.harness/ekb-research/workspace/flowise/packages/server/src/services/documentstore/index.ts:112`
- Chunk read service: `.harness/ekb-research/workspace/flowise/packages/server/src/services/documentstore/index.ts:231` through `.harness/ekb-research/workspace/flowise/packages/server/src/services/documentstore/index.ts:305`
- Document store entities: `.harness/ekb-research/workspace/flowise/packages/server/src/database/entities/DocumentStore.ts:4` through `.harness/ekb-research/workspace/flowise/packages/server/src/database/entities/DocumentStore.ts:42`, and `.harness/ekb-research/workspace/flowise/packages/server/src/database/entities/DocumentStoreFileChunk.ts:4` through `.harness/ekb-research/workspace/flowise/packages/server/src/database/entities/DocumentStoreFileChunk.ts:24`

Observed behavior:

- CP11 ingested 21/21 manifest documents at matching INSTRUMENT_HASH.
- SHA-256 mismatches: none.
- CP11 created one Flowise document store per source through `POST /api/v1/document-store/store`.
- The final SQLite DB contained 21 `document_store` rows and 23 `document_store_file_chunk` rows before teardown.
- Chunks were persisted in Flowise's document store model with source metadata. CP11 did not configure a production vector store or embedding provider.
- `GET /api/v1/document-store/store` and `GET /api/v1/document-store/chunks/:storeId/all/1` verified the stored rows through Flowise's protected API.

Findings:

- F-FLOWISE-003

### 3. Retrieval behavior

Verdict: PARTIAL overall because all queries ran and the leak gate passed, but N2 and A1 did not satisfy their full non-security rubrics.

Evidence:

- Query results: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-query-results.json`
- Benchmark summary: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-benchmark-summary.json`
- Runner stdout: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-runner.stdout.json`
- Transcripts: `docs/ekb-research/benchmark/runs/flowise/`
- Partial transcripts: `docs/ekb-research/benchmark/runs/flowise/N2.md` and `docs/ekb-research/benchmark/runs/flowise/A1.md`

Observed behavior:

- All 22 benchmark queries were attempted.
- Verdict counts: 8 `PASS`, 11 `PASS-with-source-filter`, 1 `PASS-without-tool`, and 2 `PARTIAL`.
- N2 was PARTIAL because the ambiguous deal-approval query missed required D03 under deterministic chunk scoring.
- A1 was PARTIAL because D17 was retrieved, but CP11 did not execute a native MCP or tool call trace.
- Results should be read as source-selection and Flowise document-store plumbing evidence only. CP11 did not evaluate generated answer wording, citation rendering, refusal text, semantic embeddings, reranking, or live tool execution.

Findings:

- F-FLOWISE-003

### 4. Tenant isolation mechanism

Verdict: PASS-with-source-filter for benchmark isolation queries.

Evidence:

- I1 transcript: `docs/ekb-research/benchmark/runs/flowise/I1.md`
- I2 transcript: `docs/ekb-research/benchmark/runs/flowise/I2.md`
- I3 transcript: `docs/ekb-research/benchmark/runs/flowise/I3.md`
- Query summary: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-benchmark-summary.json`
- API middleware and API-key principal construction: `.harness/ekb-research/workspace/flowise/packages/server/src/index.ts:230` through `.harness/ekb-research/workspace/flowise/packages/server/src/index.ts:300`
- API key validation: `.harness/ekb-research/workspace/flowise/packages/server/src/utils/validateKey.ts:45` through `.harness/ekb-research/workspace/flowise/packages/server/src/utils/validateKey.ts:65`
- Workspace search helper: `.harness/ekb-research/workspace/flowise/packages/server/src/enterprise/utils/ControllerServiceUtils.ts:6` through `.harness/ekb-research/workspace/flowise/packages/server/src/enterprise/utils/ControllerServiceUtils.ts:18`

Observed behavior:

- I1, I2, and I3 returned zero forbidden-source leaks.
- The benchmark isolation gate was external: the runner selected per-source Flowise document stores according to the benchmark principal and forbidden-source fixtures.
- Flowise's protected API middleware maps a valid API key to `req.user` with permissions, organization, and active workspace.
- CP11 did not prove a native Flowise tenant/workspace/group/grant/clearance/revocation policy equivalent to the benchmark fixtures.

Findings:

- F-FLOWISE-002

### 5. Permission, RBAC, and workspace model

Verdict: PASS for code-audited workspace/API-key RBAC; benchmark-equivalent document ACL was not proven.

Evidence:

- Permission middleware: `.harness/ekb-research/workspace/flowise/packages/server/src/enterprise/rbac/PermissionCheck.ts:5` through `.harness/ekb-research/workspace/flowise/packages/server/src/enterprise/rbac/PermissionCheck.ts:45`
- API key route permissions: `.harness/ekb-research/workspace/flowise/packages/server/src/routes/apikey/index.ts:6` through `.harness/ekb-research/workspace/flowise/packages/server/src/routes/apikey/index.ts:16`
- API key permission validation and workspace binding: `.harness/ekb-research/workspace/flowise/packages/server/src/services/apikey/index.ts:20` through `.harness/ekb-research/workspace/flowise/packages/server/src/services/apikey/index.ts:88`, and `.harness/ekb-research/workspace/flowise/packages/server/src/services/apikey/index.ts:174` through `.harness/ekb-research/workspace/flowise/packages/server/src/services/apikey/index.ts:190`
- Open Source platform selection: `.harness/ekb-research/workspace/flowise/packages/server/src/IdentityManager.ts:102` through `.harness/ekb-research/workspace/flowise/packages/server/src/IdentityManager.ts:110`
- Feature flags and feature-gated routes: `.harness/ekb-research/workspace/flowise/packages/server/src/utils/quotaUsage.ts:8` through `.harness/ekb-research/workspace/flowise/packages/server/src/utils/quotaUsage.ts:20`, `.harness/ekb-research/workspace/flowise/packages/server/src/IdentityManager.ts:261` through `.harness/ekb-research/workspace/flowise/packages/server/src/IdentityManager.ts:289`, and `.harness/ekb-research/workspace/flowise/packages/server/src/routes/index.ts:88` through `.harness/ekb-research/workspace/flowise/packages/server/src/routes/index.ts:147`
- Chatflow route permissions and workspace filters: `.harness/ekb-research/workspace/flowise/packages/server/src/routes/chatflows/index.ts:6` through `.harness/ekb-research/workspace/flowise/packages/server/src/routes/chatflows/index.ts:64`, `.harness/ekb-research/workspace/flowise/packages/server/src/services/chatflows/index.ts:173` through `.harness/ekb-research/workspace/flowise/packages/server/src/services/chatflows/index.ts:220`, and `.harness/ekb-research/workspace/flowise/packages/server/src/services/chatflows/index.ts:280` through `.harness/ekb-research/workspace/flowise/packages/server/src/services/chatflows/index.ts:330`
- P* transcripts: `docs/ekb-research/benchmark/runs/flowise/P1.md` through `docs/ekb-research/benchmark/runs/flowise/P5.md`

Observed behavior:

- Flowise protects document-store, chatflow, credential, tool, API-key, and MCP configuration routes with named permission strings.
- API keys are bound to `workspaceId`, and protected services commonly filter by active workspace.
- In Open Source mode without `FLOWISE_EE_LICENSE_KEY`, `IdentityManager` sets `Platform.OPEN_SOURCE`. Feature-gated datasets, evaluations, evaluators, audit, roles, and logs require feature flags and return forbidden when no feature map is present.
- CP11 created a single owner, default workspace, and API key. It did not create benchmark principals or native per-document grants.
- The benchmark source gate still lived outside native Flowise principal resolution.

Findings:

- F-FLOWISE-002
- F-FLOWISE-004

### 6. Visual pipeline and integration surfaces

Verdict: PASS for code-audited API/CLI/SDK/MCP integration surfaces; live benchmark only exercised the API and document-store model.

Evidence:

- Monorepo module list and API documentation workspace: `.harness/ekb-research/workspace/flowise/README.md:84` through `.harness/ekb-research/workspace/flowise/README.md:92`
- Root start scripts: `.harness/ekb-research/workspace/flowise/package.json:13` through `.harness/ekb-research/workspace/flowise/package.json:39`
- Server package binary and oclif commands: `.harness/ekb-research/workspace/flowise/packages/server/package.json:1` through `.harness/ekb-research/workspace/flowise/packages/server/package.json:21`
- CLI entrypoint: `.harness/ekb-research/workspace/flowise/packages/server/bin/run:1` through `.harness/ekb-research/workspace/flowise/packages/server/bin/run:4`
- Route registry: `.harness/ekb-research/workspace/flowise/packages/server/src/routes/index.ts:77` through `.harness/ekb-research/workspace/flowise/packages/server/src/routes/index.ts:150`
- Prediction and vector APIs: `.harness/ekb-research/workspace/flowise/packages/server/src/routes/predictions/index.ts:1` through `.harness/ekb-research/workspace/flowise/packages/server/src/routes/predictions/index.ts:15`, and `.harness/ekb-research/workspace/flowise/packages/server/src/routes/vectors/index.ts:1` through `.harness/ekb-research/workspace/flowise/packages/server/src/routes/vectors/index.ts:16`
- Observe SDK API client: `.harness/ekb-research/workspace/flowise/packages/observe/ARCHITECTURE.md:138` through `.harness/ekb-research/workspace/flowise/packages/observe/ARCHITECTURE.md:162`, `.harness/ekb-research/workspace/flowise/packages/observe/ARCHITECTURE.md:230` through `.harness/ekb-research/workspace/flowise/packages/observe/ARCHITECTURE.md:306`, and `.harness/ekb-research/workspace/flowise/packages/observe/src/infrastructure/api/client.ts:1` through `.harness/ekb-research/workspace/flowise/packages/observe/src/infrastructure/api/client.ts:58`
- MCP endpoint route: `.harness/ekb-research/workspace/flowise/packages/server/src/routes/mcp-endpoint/index.ts:1` through `.harness/ekb-research/workspace/flowise/packages/server/src/routes/mcp-endpoint/index.ts:45`
- MCP endpoint token middleware: `.harness/ekb-research/workspace/flowise/packages/server/src/controllers/mcp-endpoint/index.ts:6` through `.harness/ekb-research/workspace/flowise/packages/server/src/controllers/mcp-endpoint/index.ts:55`
- MCP server config routes and token service: `.harness/ekb-research/workspace/flowise/packages/server/src/routes/mcp-server/index.ts:6` through `.harness/ekb-research/workspace/flowise/packages/server/src/routes/mcp-server/index.ts:21`, and `.harness/ekb-research/workspace/flowise/packages/server/src/services/mcp-server/index.ts:35` through `.harness/ekb-research/workspace/flowise/packages/server/src/services/mcp-server/index.ts:267`
- Custom MCP server routes and SSRF/header controls: `.harness/ekb-research/workspace/flowise/packages/server/src/routes/custom-mcp-servers/index.ts:7` through `.harness/ekb-research/workspace/flowise/packages/server/src/routes/custom-mcp-servers/index.ts:24`, and `.harness/ekb-research/workspace/flowise/packages/server/src/services/custom-mcp-servers/index.ts:50` through `.harness/ekb-research/workspace/flowise/packages/server/src/services/custom-mcp-servers/index.ts:64`
- Custom MCP server workspace and tool discovery: `.harness/ekb-research/workspace/flowise/packages/server/src/services/custom-mcp-servers/index.ts:137` through `.harness/ekb-research/workspace/flowise/packages/server/src/services/custom-mcp-servers/index.ts:180`, and `.harness/ekb-research/workspace/flowise/packages/server/src/services/custom-mcp-servers/index.ts:300` through `.harness/ekb-research/workspace/flowise/packages/server/src/services/custom-mcp-servers/index.ts:424`

Observed behavior:

- Flowise exposes broad REST surfaces for chatflows, predictions, vector upsert, document stores, tools, credentials, custom MCP servers, and MCP endpoint hosting.
- The CLI entrypoint is an oclif binary exposed as `flowise`; root scripts dispatch start, worker, and user commands through `packages/server/bin/run`.
- The `api-documentation` workspace is documented as auto-generated Swagger UI for the Express API.
- The observe package is an SDK-like client for executions/evaluations UI. Its API client sets `Authorization: Bearer <token>` when provided and documents the OSS cookie plus `x-request-from: internal` auth bridge.
- Flowise can expose a chatflow as an MCP server with generated token config and constant-time token verification. It can also register external/custom MCP servers with URL deny-list checks, masked secrets, workspace scoping, tool discovery, timeout, and response-size limits.
- CP11 did not create a chatflow or run MCP JSON-RPC. Tool and MCP maturity is code-audit only for this checkpoint.

Findings:

- F-FLOWISE-004

### 7. Generation, citations, tools, and observability

Verdict: NOT EVALUATED as generated-answer, citation-rendering, live tool, or trace-export behavior.

Evidence:

- Query transcripts: `docs/ekb-research/benchmark/runs/flowise/`
- Query results: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-query-results.json`
- Benchmark summary: `.harness/ekb-research/checkpoints/11/iter-1/evidence/cp11-benchmark-summary.json`
- A1 transcript: `docs/ekb-research/benchmark/runs/flowise/A1.md`
- A2 transcript: `docs/ekb-research/benchmark/runs/flowise/A2.md`

Observed behavior:

- CP11 evaluated stored chunks and source IDs only.
- Flowise source code shows prediction, vector, MCP, custom MCP, and observe SDK surfaces, but CP11 did not execute generated answer calls, citation assembly, refusal text, live MCP tool invocation, or exported traces.
- A2 passed because no tool invocation occurred and no forbidden fixture output was returned; this should not be read as proof of a native tool-permission policy.

Findings:

- F-FLOWISE-003
- F-FLOWISE-004

## Findings Summary

Rows mirror `docs/ekb-research/findings/ledger.md`.

| finding_id | Short title |
| --- | --- |
| F-FLOWISE-001 | Local boot succeeded with a local compose wrapper and temporary Docker footprint. |
| F-FLOWISE-002 | Workspace/API-key RBAC exists, but benchmark ACL fixtures were enforced externally. |
| F-FLOWISE-003 | Corpus persisted and leak gate passed, while N2/A1 remained partial and generated/tool behavior was not evaluated. |
| F-FLOWISE-004 | API, CLI, observe SDK, MCP endpoint, and custom MCP surfaces are useful extraction candidates with workspace/token controls. |
