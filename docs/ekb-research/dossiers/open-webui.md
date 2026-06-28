# Open WebUI Dossier

Status: CP10 boot/ingest/query/code-audit captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Framework | Open WebUI |
| Repository | https://github.com/open-webui/open-webui.git |
| Pinned SHA | 02dc3e689ceac915a870b373318b99c029ddf603 |
| INSTRUMENT_HASH | 1a2434beba68e3381d07a34c81babcc12e2b02caac4a56b58203fc55cc899f19 |
| Security gate | PASS: 0 forbidden-source leaks across I*/P*/P5/A2/F1 transcripts. Eight non-security PARTIAL results remain under CP10 source-gated retrieval: R1, R2, R5, P3, P4, N2, M1, and M2. |

## Dossier Dimensions

### 1. Boot outcome

Verdict: PASS for local Docker boot smoke.

Evidence:

- Source pin: `.harness/ekb-research/checkpoints/10/iter-1/evidence/pinned-sha.txt`
- Upstream Docker run instruction: `.harness/ekb-research/checkpoints/10/iter-1/evidence/upstream-readme-docker-rag.txt`
- Local compose config: `.harness/ekb-research/checkpoints/10/iter-1/open-webui-compose.yml`
- Main image pull attempts: `.harness/ekb-research/checkpoints/10/iter-1/evidence/compose-up.txt` and `.harness/ekb-research/checkpoints/10/iter-1/evidence/compose-up-retry1.txt`
- Successful slim-image boot: `.harness/ekb-research/checkpoints/10/iter-1/evidence/compose-up-main-slim.txt`
- Container status and health: `.harness/ekb-research/checkpoints/10/iter-1/evidence/compose-ps-after-up.txt`, `.harness/ekb-research/checkpoints/10/iter-1/evidence/health-poll.txt`, and `.harness/ekb-research/checkpoints/10/iter-1/evidence/health-status.json`
- HTTP smoke: `.harness/ekb-research/checkpoints/10/iter-1/evidence/smoke-root.headers`, `.harness/ekb-research/checkpoints/10/iter-1/evidence/smoke-root.body`, `.harness/ekb-research/checkpoints/10/iter-1/evidence/smoke-health.headers`, and `.harness/ekb-research/checkpoints/10/iter-1/evidence/smoke-health.body`
- Disk accounting: `.harness/ekb-research/checkpoints/10/iter-1/evidence/docker-system-df-before-up.txt`
- Teardown: `.harness/ekb-research/checkpoints/10/iter-1/evidence/compose-down.txt`
- Teardown residue checks: `.harness/ekb-research/checkpoints/10/iter-1/evidence/container-status-after-down.txt`, `.harness/ekb-research/checkpoints/10/iter-1/evidence/volume-residual-after-down.txt`, `.harness/ekb-research/checkpoints/10/iter-1/evidence/network-residual-after-down.txt`, `.harness/ekb-research/checkpoints/10/iter-1/evidence/port-18094-after-down.txt`, `.harness/ekb-research/checkpoints/10/iter-1/evidence/port-18095-after-down.txt`, `.harness/ekb-research/checkpoints/10/iter-1/evidence/open-webui-data-du-before-remove.txt`, `.harness/ekb-research/checkpoints/10/iter-1/evidence/open-webui-data-removed-check.txt`, and `.harness/ekb-research/checkpoints/10/iter-1/evidence/docker-system-df-after-down.txt`

Observed behavior:

- CP10 cloned Open WebUI at pinned SHA `02dc3e689ceac915a870b373318b99c029ddf603`.
- Upstream documents a `ghcr.io/open-webui/open-webui:main` Docker run with persistent `/app/backend/data`; CP10 used a local compose wrapper on host port `18094`.
- Pulling `main` stalled on large image layers in two attempts, so CP10 booted `ghcr.io/open-webui/open-webui:main-slim` with a deterministic local OpenAI-compatible embedding sidecar.
- `GET http://localhost:18094/health` returned HTTP 200 and `{"status":true}` after startup polling.
- The stack was removed with `docker compose down -v`; CP10's bind-mounted Open WebUI data directory was 5.6M before deletion, the directory was removed, and ports `18094` and `18095` had no listeners after teardown.
- After CP10 teardown, Docker still reported 21.01GB reclaimable images and 34.63GB reclaimable local volumes from the broader multi-framework run. Those are retained until the full harness completes to avoid repeated large pulls.

Findings:

- F-OPENWEBUI-001

### 2. Ingestion behavior

Verdict: PASS for corpus ingestion and source accounting.

Evidence:

- Corpus hash checks: `.harness/ekb-research/checkpoints/10/iter-1/evidence/cp10-corpus-hash-checks.json`
- Ingestion records: `.harness/ekb-research/checkpoints/10/iter-1/evidence/cp10-ingest.json`
- Source-to-knowledge map: `.harness/ekb-research/checkpoints/10/iter-1/evidence/cp10-source-knowledge-map.json`
- Source-to-file map: `.harness/ekb-research/checkpoints/10/iter-1/evidence/cp10-source-file-map.json`
- Chunk counts: `.harness/ekb-research/checkpoints/10/iter-1/evidence/cp10-chunk-counts.json`
- Final DB counts before teardown: `.harness/ekb-research/checkpoints/10/iter-1/evidence/db-counts-before-down.txt`
- Chroma collection counts: `.harness/ekb-research/checkpoints/10/iter-1/evidence/chroma-counts-by-collection.txt`
- Data file inventory: `.harness/ekb-research/checkpoints/10/iter-1/evidence/open-webui-data-files.txt`

Observed behavior:

- CP10 ingested 21/21 manifest documents at matching INSTRUMENT_HASH.
- SHA-256 mismatches: none.
- The Open WebUI application DB contained 21 `file` rows, 21 `knowledge` rows, and 21 `knowledge_file` rows before teardown.
- Chroma contained 69 embeddings total. The benchmark query collections accounted for 24 knowledge-collection embeddings: one for most sources and four for long PDF D13. File collections accounted for another 24 embeddings, and Open WebUI's system `knowledge-bases` collection accounted for 21 embeddings.
- CP10 uploaded raw files with `process=false`, injected deterministic extracted text through the file content update path, then attached each file to one per-source knowledge collection.

Findings:

- F-OPENWEBUI-002

### 3. Retrieval behavior

Verdict: PARTIAL overall because all queries ran and the leak gate passed, but eight required-source checks missed.

Evidence:

- Query results: `.harness/ekb-research/checkpoints/10/iter-1/evidence/cp10-query-results.json`
- Benchmark summary: `.harness/ekb-research/checkpoints/10/iter-1/evidence/cp10-benchmark-summary.json`
- Transcripts: `docs/ekb-research/benchmark/runs/open-webui/`
- Partial transcripts: `docs/ekb-research/benchmark/runs/open-webui/R1.md`, `docs/ekb-research/benchmark/runs/open-webui/R2.md`, `docs/ekb-research/benchmark/runs/open-webui/R5.md`, `docs/ekb-research/benchmark/runs/open-webui/P3.md`, `docs/ekb-research/benchmark/runs/open-webui/P4.md`, `docs/ekb-research/benchmark/runs/open-webui/N2.md`, `docs/ekb-research/benchmark/runs/open-webui/M1.md`, and `docs/ekb-research/benchmark/runs/open-webui/M2.md`
- Query collection route: `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/retrieval.py:2458` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/retrieval.py:2492`
- Collection access validation: `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/retrieval.py:2365` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/retrieval.py:2378`

Observed behavior:

- All 22 benchmark queries were attempted.
- Verdict counts: 3 `PASS`, 11 `PASS-with-source-filter`, and 8 `PARTIAL`.
- The eight `PARTIAL` results were R1 missing D01, R2 missing D02, R5 missing D17, P3 missing D02, P4 leak-free in the main run but missing D11 in the paired control, N2 missing D03, M1 missing D14, and M2 missing D14.
- CP10 used `/api/v1/retrieval/query/collection` with hybrid search, BM25 weight `1.0`, and local deterministic fake OpenAI-compatible embeddings. Results should be read as retrieval/source-selection evidence only.
- CP10 did not evaluate generated answer wording, citation rendering, refusal text, or chat trace export.

Findings:

- F-OPENWEBUI-002
- F-OPENWEBUI-003

### 4. Tenant isolation mechanism

Verdict: PASS-with-source-filter for benchmark isolation queries.

Evidence:

- I1 transcript: `docs/ekb-research/benchmark/runs/open-webui/I1.md`
- I2 transcript: `docs/ekb-research/benchmark/runs/open-webui/I2.md`
- I3 transcript: `docs/ekb-research/benchmark/runs/open-webui/I3.md`
- Query results: `.harness/ekb-research/checkpoints/10/iter-1/evidence/cp10-query-results.json`
- Collection filter implementation: `.harness/ekb-research/workspace/open-webui/backend/open_webui/retrieval/utils.py:1086` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/retrieval/utils.py:1149`

Observed behavior:

- I1, I2, and I3 returned zero forbidden-source leaks.
- The benchmark isolation gate was external: the runner selected per-source knowledge collection IDs according to the benchmark principal tenant and forbidden-source list.
- Open WebUI validates requested collection IDs against knowledge/file access, but CP10 did not prove a native tenant/workspace/group/clearance/revocation principal envelope equivalent to the benchmark fixtures.

Findings:

- F-OPENWEBUI-002

### 5. Permission/ACL model

Verdict: PASS for code-audited user/group grants; benchmark-equivalent document ACL was not proven live.

Evidence:

- AccessGrant schema: `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/access_grants.py:20` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/access_grants.py:40`
- Grant normalization and legacy conversion: `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/access_grants.py:78` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/access_grants.py:181`
- Grant replacement: `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/access_grants.py:400` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/access_grants.py:435`
- User/group access check: `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/access_grants.py:497` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/access_grants.py:555`
- Batch resource preview helper: `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/access_grants.py:557` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/access_grants.py:611`
- Knowledge create and read gates: `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/knowledge.py:198` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/knowledge.py:219`, and `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/knowledge.py:427` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/models/knowledge.py:442`
- Knowledge route gates: `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/knowledge.py:112` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/knowledge.py:158`, `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/knowledge.py:249` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/knowledge.py:285`, `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/knowledge.py:391` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/knowledge.py:420`, and `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/knowledge.py:699` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/knowledge.py:778`

Observed behavior:

- Open WebUI stores grants in a first-class `access_grant` table over resource type, resource id, principal type, principal id, and permission.
- The grant model supports public user wildcard grants, specific user grants, and group grants for read/write permissions.
- Knowledge creation stores access grants, knowledge retrieval checks owner/admin/read grants, and file attachment requires both knowledge write access and file read access.
- In the CP10 runtime, benchmark-created knowledge bases had empty access grants and were queried by the admin account; the benchmark source gate remained outside native principal resolution.

Findings:

- F-OPENWEBUI-002

### 6. Permission preview UX

Verdict: PASS for code-audited group/resource permission preview.

Evidence:

- Admin preview route: `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/groups.py:287` through `.harness/ekb-research/workspace/open-webui/backend/open_webui/routers/groups.py:351`
- Frontend preview API: `.harness/ekb-research/workspace/open-webui/src/lib/apis/groups/index.ts:271` through `.harness/ekb-research/workspace/open-webui/src/lib/apis/groups/index.ts:295`
- Frontend preview panel: `.harness/ekb-research/workspace/open-webui/src/lib/components/admin/Users/Groups/GroupPreviewPanel.svelte:1` through `.harness/ekb-research/workspace/open-webui/src/lib/components/admin/Users/Groups/GroupPreviewPanel.svelte:135`

Observed behavior:

- Open WebUI includes an admin-only `GET /groups/id/{id}/preview` route that batch-checks group-readable model, knowledge, and tool resources through `AccessGrants.get_accessible_resource_ids`.
- The frontend calls the route via `getGroupPreview` and renders accessible models, knowledge bases, and tools with accessible-count summaries.
- CP10 did not click through the browser UI because no benchmark group grant matrix was created live; this remains code-audit evidence rather than live UX proof.

Findings:

- F-OPENWEBUI-004

### 7. Generation, tools, and observability

Verdict: NOT EVALUATED as generated-answer, tool, or trace behavior.

Evidence:

- Query transcripts: `docs/ekb-research/benchmark/runs/open-webui/`
- Query results: `.harness/ekb-research/checkpoints/10/iter-1/evidence/cp10-query-results.json`
- Upstream feature claims: `.harness/ekb-research/checkpoints/10/iter-1/evidence/upstream-readme-docker-rag.txt`

Observed behavior:

- CP10 evaluated retrieved chunks and source IDs only.
- Open WebUI upstream documents RAG, RBAC, vector database support, tools, and observability capabilities, but CP10 did not exercise generated chat answers, citation assembly, Python/tool calling, OpenTelemetry export, or UI audit events.

Findings:

- F-OPENWEBUI-003
