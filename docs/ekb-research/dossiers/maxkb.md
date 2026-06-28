# MaxKB Dossier

Status: CP09 boot/ingest/query/code-audit captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Framework | MaxKB |
| Repository | https://github.com/1Panel-dev/MaxKB |
| Pinned SHA | d2e9ea4a7601e2c97c8f9555f9cacbdc0eeb8ceb |
| INSTRUMENT_HASH | 1a2434beba68e3381d07a34c81babcc12e2b02caac4a56b58203fc55cc899f19 |
| Security gate | PASS: 0 forbidden-source leaks across I*/P*/P5/A2/F1 transcripts. Four non-security PARTIAL results remain: P3, N2, A1, and F1 missed required sources under CP09 source-gated `blend` retrieval. |

## Dossier Dimensions

### 1. Boot outcome

Verdict: PASS for local Docker boot smoke.

Evidence:

- Source pin: `.harness/ekb-research/checkpoints/09/iter-1/evidence/pinned-sha.txt`
- Upstream Docker run instruction: `.harness/ekb-research/workspace/maxkb/README.md:27`
- Upstream default login note: `.harness/ekb-research/workspace/maxkb/README.md:30` through `.harness/ekb-research/workspace/maxkb/README.md:33`
- Local compose config: `.harness/ekb-research/checkpoints/09/iter-1/maxkb-compose.yml`
- Healthy status: `.harness/ekb-research/checkpoints/09/iter-1/evidence/compose-ps-healthy.txt`
- HTTP smoke: `.harness/ekb-research/checkpoints/09/iter-1/evidence/smoke-root.headers` and `.harness/ekb-research/checkpoints/09/iter-1/evidence/smoke-root.body`
- Login and profile smoke: `.harness/ekb-research/checkpoints/09/iter-1/evidence/login.headers`, `.harness/ekb-research/checkpoints/09/iter-1/evidence/profile.response.json`
- Teardown: `.harness/ekb-research/checkpoints/09/iter-1/evidence/compose-down.txt`
- Teardown residue checks: `.harness/ekb-research/checkpoints/09/iter-1/evidence/container-status-after-down.txt`, `.harness/ekb-research/checkpoints/09/iter-1/evidence/volume-residual-after-down.txt`, `.harness/ekb-research/checkpoints/09/iter-1/evidence/network-residual-after-down.txt`, and `.harness/ekb-research/checkpoints/09/iter-1/evidence/port-18092-after-down.txt`

Observed behavior:

- CP09 cloned MaxKB at pinned SHA `d2e9ea4a7601e2c97c8f9555f9cacbdc0eeb8ceb`.
- Upstream documents an all-in-one `1panel/maxkb` Docker run rather than a project compose file, so CP09 used a local compose wrapper around the upstream image on host port `18092`.
- `GET http://localhost:18092/` returned HTTP 302 to `/admin/`, proving the web surface was live.
- Default admin login succeeded, and `/admin/api/user/profile` showed `ADMIN` plus `WORKSPACE_MANAGE:/WORKSPACE/default`.
- The stack was removed with `docker compose down -v`; the local bind-mounted MaxKB data directory was 81M before deletion and was removed after teardown.

Findings:

- F-MAXKB-001

### 2. Ingestion behavior

Verdict: PASS for corpus ingestion and source accounting.

Evidence:

- Corpus hash checks: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-corpus-hash-checks.json`
- Knowledge-base creation records: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-knowledge-bases.json`
- Source-to-knowledge map: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-source-knowledge-map.json`
- Chunk and embedding counts: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-chunk-counts.json`
- Final DB counts before teardown: `.harness/ekb-research/checkpoints/09/iter-1/evidence/db-counts-before-down.txt`
- Create-with-documents failure record: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-runner-error.json`
- Inline document creation response source: `.harness/ekb-research/workspace/maxkb/apps/knowledge/serializers/knowledge.py:1204` through `.harness/ekb-research/workspace/maxkb/apps/knowledge/serializers/knowledge.py:1210`

Observed behavior:

- CP09 ingested 21/21 manifest documents at matching INSTRUMENT_HASH.
- SHA-256 mismatches: none.
- The final source map contains one MaxKB knowledge base per benchmark source.
- Paragraph counts were one paragraph for D01-D12 and D14-D21, and three paragraphs for D13 after raw PDF literal fallback.
- MaxKB expanded paragraphs into 46 embedding rows for the final 21-source map.
- A direct `documents` payload to `POST /workspace/default/knowledge/base` created data but returned `Object of type Document is not JSON serializable`; CP09 switched to a two-step create-knowledge then create-document path.

Findings:

- F-MAXKB-002

### 3. Retrieval behavior

Verdict: PARTIAL overall because all queries ran and leak gate passed, but four required-source checks missed.

Evidence:

- Query results: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-query-results.json`
- Benchmark summary: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-benchmark-summary.json`
- Transcripts: `docs/ekb-research/benchmark/runs/maxkb/`
- P3 transcript: `docs/ekb-research/benchmark/runs/maxkb/P3.md`
- N2 transcript: `docs/ekb-research/benchmark/runs/maxkb/N2.md`
- A1 transcript: `docs/ekb-research/benchmark/runs/maxkb/A1.md`
- F1 transcript: `docs/ekb-research/benchmark/runs/maxkb/F1.md`
- Hit-test route and permission decorator: `.harness/ekb-research/workspace/maxkb/apps/knowledge/views/knowledge.py:279` through `.harness/ekb-research/workspace/maxkb/apps/knowledge/views/knowledge.py:310`
- Hit-test vector path: `.harness/ekb-research/workspace/maxkb/apps/knowledge/serializers/knowledge.py:1356` through `.harness/ekb-research/workspace/maxkb/apps/knowledge/serializers/knowledge.py:1413`
- Vector search dispatch: `.harness/ekb-research/workspace/maxkb/apps/knowledge/vector/pg_vector.py:112` through `.harness/ekb-research/workspace/maxkb/apps/knowledge/vector/pg_vector.py:147`

Observed behavior:

- All 22 benchmark queries were attempted.
- Verdict counts: 6 `PASS`, 12 `PASS-with-source-filter`, and 4 `PARTIAL`.
- The four `PARTIAL` results were P3 missing D03, N2 missing D03, A1 missing D17, and F1 missing D14.
- CP09 used MaxKB `hit_test` with `search_mode=blend`; source gates were enforced by querying only selected per-source knowledge bases and excluding revoked D21 by default.
- Results should be read as retrieval/source-selection evidence only. CP09 did not evaluate generated answer wording, citation rendering, or refusal text.

Findings:

- F-MAXKB-003
- F-MAXKB-004

### 4. Tenant isolation mechanism

Verdict: PASS-with-source-filter for the benchmark isolation queries.

Evidence:

- I1 transcript: `docs/ekb-research/benchmark/runs/maxkb/I1.md`
- I2 transcript: `docs/ekb-research/benchmark/runs/maxkb/I2.md`
- I3 transcript: `docs/ekb-research/benchmark/runs/maxkb/I3.md`
- Query results: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-query-results.json`
- Workspace/resource permission model: `.harness/ekb-research/workspace/maxkb/apps/system_manage/models/workspace_user_permission.py:27` through `.harness/ekb-research/workspace/maxkb/apps/system_manage/models/workspace_user_permission.py:60`
- User token permission expansion: `.harness/ekb-research/workspace/maxkb/apps/common/auth/handle/impl/user_token.py:87` through `.harness/ekb-research/workspace/maxkb/apps/common/auth/handle/impl/user_token.py:155`
- Route permission decorator implementation: `.harness/ekb-research/workspace/maxkb/apps/common/auth/authentication.py:123` through `.harness/ekb-research/workspace/maxkb/apps/common/auth/authentication.py:143`

Observed behavior:

- I1, I2, and I3 returned zero forbidden-source leaks.
- CP09 did not create separate MaxKB tenants for Acme and Globex because the exercised OSS runtime exposed the default workspace through a single admin token.
- The benchmark isolation gate was external: the runner selected per-source knowledge bases by benchmark principal tenant and forbidden-source list.
- MaxKB's native authorization model is workspace/resource oriented. CP09 did not find a native tenant id or benchmark principal envelope on the exercised `hit_test` request.

Findings:

- F-MAXKB-003

### 5. Permission/ACL model

Verdict: PASS-with-source-filter for benchmark permission queries; native benchmark-equivalent document ACL was not proven.

Evidence:

- P1 transcript: `docs/ekb-research/benchmark/runs/maxkb/P1.md`
- P2 transcript: `docs/ekb-research/benchmark/runs/maxkb/P2.md`
- P3 transcript: `docs/ekb-research/benchmark/runs/maxkb/P3.md`
- P4 transcript: `docs/ekb-research/benchmark/runs/maxkb/P4.md`
- P5 transcript: `docs/ekb-research/benchmark/runs/maxkb/P5.md`
- Resource permission table: `.harness/ekb-research/workspace/maxkb/apps/system_manage/models/workspace_user_permission.py:27` through `.harness/ekb-research/workspace/maxkb/apps/system_manage/models/workspace_user_permission.py:60`
- Resource permission APIs: `.harness/ekb-research/workspace/maxkb/apps/system_manage/urls.py:9` through `.harness/ekb-research/workspace/maxkb/apps/system_manage/urls.py:14`
- Resource permission list/edit views: `.harness/ekb-research/workspace/maxkb/apps/system_manage/views/user_resource_permission.py:105` through `.harness/ekb-research/workspace/maxkb/apps/system_manage/views/user_resource_permission.py:204`
- Resource grant serializer: `.harness/ekb-research/workspace/maxkb/apps/system_manage/serializers/user_resource_permission.py:145` through `.harness/ekb-research/workspace/maxkb/apps/system_manage/serializers/user_resource_permission.py:217`
- Knowledge create auto-grant: `.harness/ekb-research/workspace/maxkb/apps/knowledge/serializers/knowledge.py:1195` through `.harness/ekb-research/workspace/maxkb/apps/knowledge/serializers/knowledge.py:1203`
- Knowledge route permissions: `.harness/ekb-research/workspace/maxkb/apps/knowledge/views/knowledge.py:73` through `.harness/ekb-research/workspace/maxkb/apps/knowledge/views/knowledge.py:132`

Observed behavior:

- P1, P2, P4, and P5 passed the leak gate; P3 was PARTIAL because D03 was missing while D02 was present and forbidden sources were absent.
- MaxKB has concrete workspace-scoped resource grants over `KNOWLEDGE`, `APPLICATION`, `TOOL`, and `MODEL` targets.
- New knowledge bases auto-grant the creating user `VIEW` and `MANAGE` via `WorkspaceUserResourcePermission`, and resource mappings are refreshed after create/import.
- The CP09 benchmark source gate still lived outside native MaxKB principal resolution. The tested `hit_test` path accepted a workspace id and knowledge id, not benchmark workspace, group, clearance, shared-grant, or revoked-source policy attributes.

Findings:

- F-MAXKB-003

### 6. Data model reconstruction

Verdict: PASS for benchmark-accounting reconstruction.

Evidence:

- Source-to-knowledge map: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-source-knowledge-map.json`
- Knowledge creation records: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-knowledge-bases.json`
- Chunk counts: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-chunk-counts.json`
- Resource mapping model: `.harness/ekb-research/workspace/maxkb/apps/system_manage/models/resource_mapping.py:16` through `.harness/ekb-research/workspace/maxkb/apps/system_manage/models/resource_mapping.py:31`
- Knowledge resource mapping update: `.harness/ekb-research/workspace/maxkb/apps/knowledge/serializers/common.py:290` through `.harness/ekb-research/workspace/maxkb/apps/knowledge/serializers/common.py:304`

Observed behavior:

- CP09 reconstructed a source-id to MaxKB knowledge-id mapping for every benchmark document.
- Each transcript records principal, requested source ids, requested knowledge ids, required sources, forbidden sources, returned source ids, and top chunks.
- Revoked source D21 was ingested for accounting but excluded from the external source gate unless explicitly required.

Findings:

- F-MAXKB-003

### 7. Generation and citation

Verdict: NOT EVALUATED as generated-answer behavior.

Evidence:

- Query transcripts: `docs/ekb-research/benchmark/runs/maxkb/`
- Query results: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-query-results.json`

Observed behavior:

- CP09 evaluated retrieved chunks and source IDs only.
- MaxKB returned paragraph content, document names, knowledge names, and scores adequate for source-selection transcripts.
- CP09 did not evaluate final answer wording, citation assembly, refusal behavior, or trace export in generated responses.

Findings:

- F-MAXKB-004

### 8. Tool/MCP surface

Verdict: PARTIAL. MaxKB has MCP surfaces, but CP09 did not execute an MCP tool path for the benchmark.

Evidence:

- A1 transcript: `docs/ekb-research/benchmark/runs/maxkb/A1.md`
- A2 transcript: `docs/ekb-research/benchmark/runs/maxkb/A2.md`
- MCP chat route: `.harness/ekb-research/workspace/maxkb/apps/chat/views/mcp.py:9` through `.harness/ekb-research/workspace/maxkb/apps/chat/views/mcp.py:58`
- MCP tool handler API-key check and tool list: `.harness/ekb-research/workspace/maxkb/apps/chat/mcp/tools.py:11` through `.harness/ekb-research/workspace/maxkb/apps/chat/mcp/tools.py:48`
- MCP tool call path: `.harness/ekb-research/workspace/maxkb/apps/chat/mcp/tools.py:66` through `.harness/ekb-research/workspace/maxkb/apps/chat/mcp/tools.py:105`
- Knowledge MCP tools route: `.harness/ekb-research/workspace/maxkb/apps/knowledge/urls.py:99`

Observed behavior:

- A1 was PARTIAL because retrieval missed required D17. A2 passed the leak gate with no `tool.invoke:release_lookup` fixture execution.
- MaxKB exposes an MCP endpoint backed by application API keys and a single agent tool per published application.
- CP09 did not create a benchmark application, API key, or MCP client run, so tool maturity remains code-audit only.

Findings:

- F-MAXKB-004

### 9. Observability and eval

Verdict: PARTIAL.

Evidence:

- Query transcripts: `docs/ekb-research/benchmark/runs/maxkb/`
- Benchmark summary: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-benchmark-summary.json`
- Container logs: `.harness/ekb-research/checkpoints/09/iter-1/evidence/container-logs-before-down-tail.txt`

Observed behavior:

- CP09 produced deterministic benchmark transcripts and JSON summaries outside MaxKB.
- Container logs were adequate for boot and task execution inspection.
- No native MaxKB audit rows, trace spans, or external observability exports were exercised.

Findings:

- F-MAXKB-004

### 10. Extraction candidates

Evidence:

- Resource permission model and serializers listed in sections 4 and 5.
- Hit-test and vector dispatch listed in section 3.
- MCP tool handler listed in section 8.

Extraction candidates:

- Workspace-scoped resource grant model for `KNOWLEDGE`, `APPLICATION`, `TOOL`, and `MODEL`.
- Route-level `has_permissions` decorator plus token-expanded resource permission strings.
- Per-knowledge hit-test and vector dispatch, if paired with a policy layer that can produce authorized knowledge ids per principal.
- Application-key-backed MCP agent tool surface, pending a source-gated application/tool benchmark.

Findings:

- F-MAXKB-003
- F-MAXKB-004

### 11. License posture

Verdict: GPLv3.

Evidence:

- License file: `.harness/ekb-research/workspace/maxkb/LICENSE:1` through `.harness/ekb-research/workspace/maxkb/LICENSE:6`

Observed behavior:

- The repository is under GNU GPL version 3. Extraction work must account for copyleft obligations before reusing implementation code.

Findings:

- none

### 12. Benchmark grid result

Evidence:

- Benchmark summary: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-benchmark-summary.json`
- Query results: `.harness/ekb-research/checkpoints/09/iter-1/evidence/cp09-query-results.json`
- Transcripts: `docs/ekb-research/benchmark/runs/maxkb/`

Observed behavior:

- 21 documents ingested.
- 22 queries attempted.
- Verdict counts: 6 `PASS`, 12 `PASS-with-source-filter`, and 4 `PARTIAL`.
- Leak failures: none.

Findings:

- F-MAXKB-003
- F-MAXKB-004

### 13. Gaps vs target design

Gaps:

- No native benchmark principal envelope on the exercised `hit_test` API.
- No proof of native per-document tenant/workspace/group/grant/clearance/revocation policy in retrieval.
- Retrieval quality missed required sources for P3, N2, A1, and F1.
- Generated answers, citations, refusals, live MCP invocation, and native audit/trace exports were not exercised.
- GPLv3 license posture limits direct code extraction.

Findings:

- F-MAXKB-003
- F-MAXKB-004

## Seven-Dimension Benchmark Grid

| Dimension | Capability level | Earned maturity | Verdict | Transcript evidence | Finding ids |
| --- | --- | --- | --- | --- | --- |
| R retrieval+citation | 2 | 2 | PASS for R1-R5; R6 PASS-with-source-filter | `docs/ekb-research/benchmark/runs/maxkb/R1.md` through `R6.md` | F-MAXKB-004 |
| I tenant isolation | 2 | 1 | PASS-with-source-filter | `docs/ekb-research/benchmark/runs/maxkb/I1.md` through `I3.md` | F-MAXKB-003 |
| P permission scope | 2 | 1 | PARTIAL because P3 missed D03; no forbidden leak | `docs/ekb-research/benchmark/runs/maxkb/P1.md` through `P5.md` | F-MAXKB-003, F-MAXKB-004 |
| N no-answer | 1 | 1 | PARTIAL because N2 missed D03 and generation/refusal was not evaluated | `docs/ekb-research/benchmark/runs/maxkb/N1.md` through `N3.md` | F-MAXKB-004 |
| M multilingual | 2 | 1 | PASS-with-source-filter for M1 and M2 | `docs/ekb-research/benchmark/runs/maxkb/M1.md`, `M2.md` | F-MAXKB-003 |
| A multi-agent/tool | 1 | 1 | PARTIAL because A1 missed D17 and MCP was not invoked | `docs/ekb-research/benchmark/runs/maxkb/A1.md`, `A2.md` | F-MAXKB-004 |
| F freshness | 1 | 1 | PARTIAL because F1 missed D14 while D21 was excluded externally | `docs/ekb-research/benchmark/runs/maxkb/F1.md` | F-MAXKB-003, F-MAXKB-004 |

## Findings View

| Finding id | Summary |
| --- | --- |
| F-MAXKB-001 | MaxKB boot succeeded through a local compose wrapper around the upstream all-in-one Docker image; cleanup removed project data, but image cleanup is deferred until full harness completion. |
| F-MAXKB-002 | Inline `documents` creation through `knowledge/base` returns a JSON serialization error because the response includes Django `Document` objects. |
| F-MAXKB-003 | Leak gate passed only with an external per-source knowledge selection gate; MaxKB native workspace/resource permissions were not proven benchmark-equivalent for document ACL. |
| F-MAXKB-004 | Retrieval/tool evaluation remains partial: four required-source misses, no generated-answer scoring, and no live MCP invocation. |
