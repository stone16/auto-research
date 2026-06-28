# Dify Dossier

Status: CP06 ingest, query, and code audit captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Framework | Dify |
| Repository | https://github.com/langgenius/dify.git |
| Pinned SHA | 7bb94cb6fecabb40662cc78d0dfabcb35df55b5c |
| INSTRUMENT_HASH | 1a2434beba68e3381d07a34c81babcc12e2b02caac4a56b58203fc55cc899f19 |
| CP06 dataset id | 3839af29-fc96-4835-a861-abefc4354883 |
| Security gate | PASS for I*/P*/P5/A2/F1 leak checks under CP06 server-side Dify metadata filtering; native benchmark principal/workspace/clearance ACL is N/A in the exercised single-token Service API path. |

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
- Healthy service status: `.harness/ekb-research/checkpoints/05/iter-1/evidence/compose-ps-health-ready.txt`
- Smoke summary: `.harness/ekb-research/checkpoints/05/iter-1/evidence/smoke-summary-health.txt`
- Runtime feature flags: `.harness/ekb-research/checkpoints/05/iter-1/evidence/runtime-feature-flags-health.txt`
- CP06 ready status: `.harness/ekb-research/checkpoints/06/iter-1/evidence/compose-ps-ready.txt`

Observed behavior:

- CP05 boot command used `docker compose -f docker-compose.yaml -f docker-compose.cp05-health.yml up -d` with `COMPOSE_PROJECT_NAME=ekbcp05dify`; CP06 reused the same local health override with `COMPOSE_PROJECT_NAME=ekbcp06dify`.
- Services started: `db_postgres`, `init_permissions`, `redis`, `api`, `plugin_daemon`, `worker`, `worker_beat`, `sandbox`, `ssrf_proxy`, `weaviate`, `api_websocket`, `web`, and `nginx`.
- `api`, `worker`, `worker_beat`, `web`, `db_postgres`, `redis`, `sandbox`, and `weaviate` reached Docker healthy status after the local worker, web, and weaviate health probes were enabled.
- `GET http://localhost:18081/install` returned `HTTP/1.1 200 OK`, `/` redirected to `/install`, and `/console/api/setup` reported setup state.

Findings:

- F-DIFY-001
- F-DIFY-002

### 2. Ingestion behavior

Verdict: PASS.

Evidence:

- Dataset setup and token evidence: `.harness/ekb-research/checkpoints/06/iter-1/evidence/setup-auth-summary.txt`, `.harness/ekb-research/checkpoints/06/iter-1/evidence/api-create-dataset.txt`
- Upload summary: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-upload-documents.json`
- Indexing status: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-indexing-status.json`
- Document metadata snapshot: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-documents-after-metadata.json`
- Segment counts: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-segment-counts.json`
- Benchmark summary: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-benchmark-summary.json`

Observed behavior:

- CP06 created one Dify dataset with `indexing_technique=economy` and `retrieval_model.search_method=keyword_search` to avoid external embedding or LLM credentials.
- All 21 manifest documents were uploaded with matching SHA-256 checksums at the frozen instrument hash. No upload needed text fallback.
- Dify accepted the two PDFs natively: D02 produced 1 segment and D13 produced 7 segments.
- Total segment counts by source id were: D01 4, D02 1, D03 3, D04 5, D05 3, D06 3, D07 4, D08 2, D09 3, D10 3, D11 4, D12 3, D13 7, D14 4, D15 3, D16 2, D17 4, D18 2, D19 3, D20 2, D21 3.
- CP06 added Dify document metadata fields `source_id`, `tenant_id`, `workspace_id`, `sensitivity`, `status`, `shared`, `shared_grant_id`, and `instrument_hash` to drive query-time source filtering.

Findings:

- none

### 3. Retrieval behavior

Verdict: PARTIAL.

Evidence:

- Query summary: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-query-results.json`
- Benchmark summary: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-benchmark-summary.json`
- Transcript directory: `docs/ekb-research/benchmark/runs/dify/`
- R2 transcript: `docs/ekb-research/benchmark/runs/dify/R2.md`
- R4 transcript: `docs/ekb-research/benchmark/runs/dify/R4.md`
- P3 transcript: `docs/ekb-research/benchmark/runs/dify/P3.md`
- N2 transcript: `docs/ekb-research/benchmark/runs/dify/N2.md`

Observed behavior:

- All 22 benchmark queries were attempted through Dify's Service API hit-testing endpoint.
- Verdict counts were 4 PASS, 14 PASS-with-metadata-filter, and 4 PARTIAL. Leak failures were zero.
- Retrieval misses were source-selection misses in economy/keyword mode, not ingestion failures: R2 and P3 missed required D02 even though D02 had one indexed segment, R4 missed required D13, and N2 missed required D03.
- Keyword search returned no numeric score in the exercised response records, so transcripts record source ids, document names, and chunk previews rather than score calibration.

Findings:

- F-DIFY-004
- F-DIFY-005

### 4. Tenant isolation mechanism

Verdict: METADATA-FILTER-ONLY for benchmark tenant isolation.

Evidence:

- Dataset token tenant check: `.harness/ekb-research/workspace/dify/api/controllers/service_api/wraps.py:294` through `.harness/ekb-research/workspace/dify/api/controllers/service_api/wraps.py:321`
- Tenant owner login for dataset-token requests: `.harness/ekb-research/workspace/dify/api/controllers/service_api/wraps.py:323` through `.harness/ekb-research/workspace/dify/api/controllers/service_api/wraps.py:341`
- Hit-testing metadata filter conversion: `.harness/ekb-research/workspace/dify/api/services/hit_testing_service.py:125` through `.harness/ekb-research/workspace/dify/api/services/hit_testing_service.py:142`
- Metadata filter document-id query: `.harness/ekb-research/workspace/dify/api/core/rag/retrieval/dataset_retrieval.py:1348` through `.harness/ekb-research/workspace/dify/api/core/rag/retrieval/dataset_retrieval.py:1423`
- I* transcripts: `docs/ekb-research/benchmark/runs/dify/I1.md`, `docs/ekb-research/benchmark/runs/dify/I2.md`, and `docs/ekb-research/benchmark/runs/dify/I3.md`

Observed behavior:

- The Service API validates that the dataset id belongs to the dataset token tenant before allowing dataset access.
- The endpoint then logs in a tenant owner account for the request; it does not impersonate benchmark principals like `rep@acme/sales` or `rep@globex/sales`.
- CP06 enforced benchmark tenant gates by passing `metadata_filtering_conditions` with `source_id in requested_sources`. Dify converted that condition into a server-side `document_ids_filter` before retrieval.
- I1, I2 paired control, and I3 returned no configured forbidden tenant sources under the metadata filter. The returned chunks still prove only source-gate behavior, not generated refusal behavior.

Findings:

- F-DIFY-003

### 5. Permission/ACL model

Verdict: METADATA-FILTER-ONLY for benchmark permission scope.

Evidence:

- Enterprise RBAC default: `.harness/ekb-research/workspace/dify/api/configs/enterprise/__init__.py:32` through `.harness/ekb-research/workspace/dify/api/configs/enterprise/__init__.py:34`
- Runtime feature flags: `.harness/ekb-research/checkpoints/05/iter-1/evidence/runtime-feature-flags-health.txt`
- Dataset RBAC branch: `.harness/ekb-research/workspace/dify/api/services/dataset_service.py:240` through `.harness/ekb-research/workspace/dify/api/services/dataset_service.py:245`
- Legacy dataset visibility branch: `.harness/ekb-research/workspace/dify/api/services/dataset_service.py:277` through `.harness/ekb-research/workspace/dify/api/services/dataset_service.py:329`
- Metadata `in` operator implementation: `.harness/ekb-research/workspace/dify/api/core/rag/retrieval/dataset_retrieval.py:1500` through `.harness/ekb-research/workspace/dify/api/core/rag/retrieval/dataset_retrieval.py:1575`
- P* transcripts: `docs/ekb-research/benchmark/runs/dify/P1.md` through `docs/ekb-research/benchmark/runs/dify/P5.md`

Observed behavior:

- The CP05 runtime exposed self-hosted mode with `data-rbac-enabled="false"`.
- Dify's dataset listing and management code branches on `RBAC_ENABLED`; with RBAC disabled, it uses legacy dataset visibility instead of enterprise permission-key enforcement.
- CP06 did not find a native Service API surface that accepts the benchmark's tenant/workspace/group/grant/clearance principal envelope per query.
- P1, P2, P4, and P5 passed leak gates under metadata filtering. P3 was PARTIAL because required D02 was not retrieved; the forbidden D11 and D19 sources were absent.

Findings:

- F-DIFY-002
- F-DIFY-003
- F-DIFY-004

### 6. Data model reconstruction

Verdict: PARTIAL.

Evidence:

- Metadata field snapshot: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-metadata-fields.json`
- Document metadata update payload: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-document-metadata-update.json`
- Document metadata snapshot: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-documents-after-metadata.json`
- Source-to-document map: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-source-document-map.json`

Observed behavior:

- Dify documents can carry custom structured metadata and the retrieval path can filter on those fields.
- Dataset, document, segment, and custom metadata are sufficient to reconstruct the benchmark source id mapping inside one dataset.
- The custom metadata layer is an external benchmark shim. It does not prove Dify has native principal semantics for group grants, restricted clearances, or revoked-source freshness.

Findings:

- F-DIFY-003

### 7. Generation and citation

Verdict: NOT EXERCISED for answer generation.

Evidence:

- Retrieval transcripts: `docs/ekb-research/benchmark/runs/dify/`
- Query summary: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-query-results.json`

Observed behavior:

- CP06 exercised Dify dataset hit-testing and returned chunks only.
- The transcripts prove source selection and forbidden-source absence, but they do not prove generated answer text, citation formatting, or refusal wording.
- No-answer queries are source-gate evidence only. N1 returned permitted chunks even though the corpus has no hardware refund policy, so it should not be treated as a generated no-answer pass.

Findings:

- F-DIFY-005

### 8. Tool/MCP surface

Verdict: NOT NATIVE in CP06 hit-testing path.

Evidence:

- A1 transcript: `docs/ekb-research/benchmark/runs/dify/A1.md`
- A2 transcript: `docs/ekb-research/benchmark/runs/dify/A2.md`
- Query summary: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-query-results.json`

Observed behavior:

- A1 and A2 were attempted through the same Dify dataset hit-testing endpoint.
- A2 did not invoke the `tool.invoke:release_lookup` fixture because hit-testing has no tool invocation surface. It returned no forbidden tool token.
- CP06 therefore establishes source-gate behavior for A*, not agent tool authorization or MCP behavior.

Findings:

- F-DIFY-005

### 9. Observability and eval

Verdict: PARTIAL.

Evidence:

- CP06 compose up and status: `.harness/ekb-research/checkpoints/06/iter-1/evidence/compose-up.txt`, `.harness/ekb-research/checkpoints/06/iter-1/evidence/compose-ps-ready.txt`
- Benchmark summary: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-benchmark-summary.json`
- Tracing route: `.harness/ekb-research/workspace/dify/api/controllers/console/app/ops_trace.py:89` through `.harness/ekb-research/workspace/dify/api/controllers/console/app/ops_trace.py:118`
- Tracing provider validation: `.harness/ekb-research/workspace/dify/api/services/ops_service.py:149` through `.harness/ekb-research/workspace/dify/api/services/ops_service.py:164`
- Langfuse and Phoenix provider registration: `.harness/ekb-research/workspace/dify/api/core/ops/ops_trace_manager.py:228` through `.harness/ekb-research/workspace/dify/api/core/ops/ops_trace_manager.py:289`
- Trace instance creation: `.harness/ekb-research/workspace/dify/api/core/ops/ops_trace_manager.py:486` through `.harness/ekb-research/workspace/dify/api/core/ops/ops_trace_manager.py:540`
- Async trace dispatch: `.harness/ekb-research/workspace/dify/api/tasks/ops_trace_task.py:61` through `.harness/ekb-research/workspace/dify/api/tasks/ops_trace_task.py:92`
- Langfuse dataset retrieval span: `.harness/ekb-research/workspace/dify/api/providers/trace/trace-langfuse/src/dify_trace_langfuse/langfuse_trace.py:121`, `.harness/ekb-research/workspace/dify/api/providers/trace/trace-langfuse/src/dify_trace_langfuse/langfuse_trace.py:422` through `.harness/ekb-research/workspace/dify/api/providers/trace/trace-langfuse/src/dify_trace_langfuse/langfuse_trace.py:435`
- Phoenix dataset retrieval span: `.harness/ekb-research/workspace/dify/api/providers/trace/trace-arize-phoenix/src/dify_trace_arize_phoenix/arize_phoenix_trace.py:747` through `.harness/ekb-research/workspace/dify/api/providers/trace/trace-arize-phoenix/src/dify_trace_arize_phoenix/arize_phoenix_trace.py:748`, `.harness/ekb-research/workspace/dify/api/providers/trace/trace-arize-phoenix/src/dify_trace_arize_phoenix/arize_phoenix_trace.py:1312` through `.harness/ekb-research/workspace/dify/api/providers/trace/trace-arize-phoenix/src/dify_trace_arize_phoenix/arize_phoenix_trace.py:1355`

Observed behavior:

- Dify has console app tracing configuration routes and provider mappings for Langfuse, Arize, and Phoenix.
- Langfuse and Phoenix provider implementations include dataset retrieval trace handling.
- CP06 did not configure external trace credentials and did not run an app workflow, so no live Langfuse or Phoenix trace export was exercised. Hit-testing evidence is local API/evidence-file based.

Findings:

- F-DIFY-006

### 10. Extraction candidates

Status: preliminary.

Evidence:

- Retrieval pipeline and access-control code cited above.
- CP06 transcripts in `docs/ekb-research/benchmark/runs/dify/`.

Candidates:

- Dify's Service API hit-testing endpoint is a repeatable source-selection benchmark surface when custom document metadata is used for source scoping.
- Custom metadata filtering is a useful extraction point for pre-rank document scoping, but it should be documented as an external policy shim unless Dify principal attributes are wired natively.
- Economy keyword mode is cheap and credential-free, but its misses on D02, D13, and D03 mean it should not be used to claim mature retrieval quality.
- Langfuse/Phoenix hooks are promising for app workflow observability but require an app-level trace run, not only dataset hit-testing.

Findings:

- F-DIFY-003
- F-DIFY-004
- F-DIFY-006

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

Verdict: 22/22 attempted; 7 dimensions filled.

Evidence:

- Query summary: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-query-results.json`
- Benchmark summary: `.harness/ekb-research/checkpoints/06/iter-1/evidence/cp06-benchmark-summary.json`
- Transcript directory: `docs/ekb-research/benchmark/runs/dify/`

Dimension counts:

- retrieval: 3 PASS, 2 PARTIAL, 1 PASS-with-metadata-filter
- tenant_isolation: 3 PASS-with-metadata-filter
- permission_scope: 4 PASS-with-metadata-filter, 1 PARTIAL
- no_answer: 1 PASS, 1 PARTIAL, 1 PASS-with-metadata-filter
- multilingual: 2 PASS-with-metadata-filter
- multi_agent_tool: 2 PASS-with-metadata-filter
- freshness: 1 PASS-with-metadata-filter

Findings:

- F-DIFY-003
- F-DIFY-004
- F-DIFY-005

### 13. Gaps vs target design

Status: recorded for cross-framework synthesis.

Evidence:

- Code audit and transcript evidence listed above.

Gaps:

- No native benchmark principal ACL in the exercised Service API hit-testing path.
- Economy keyword retrieval missed several required sources despite successful ingestion.
- CP06 does not establish generated answer citations, refusal wording, or native tool/MCP invocation.
- Langfuse/Phoenix hooks were identified in code but not live-export tested.

Findings:

- F-DIFY-003
- F-DIFY-004
- F-DIFY-005
- F-DIFY-006

## Seven-Dimension Benchmark Grid

| Dimension | Capability level | Earned maturity | Verdict | Transcript evidence | Finding ids |
| --- | --- | --- | --- | --- | --- |
| R retrieval+citation | Retrieval source selection works for some indexed docs; generation/citation not exercised | Partial | PARTIAL | `R1.md` through `R6.md`; R2 missing D02 and R4 missing D13 | F-DIFY-004, F-DIFY-005 |
| I tenant isolation | Dataset-token tenant check plus custom `source_id` metadata filter | Metadata-filter-only | PASS-with-metadata-filter | `I1.md`, `I2.md`, `I3.md` | F-DIFY-003 |
| P permission scope | Custom `source_id` metadata filter; no native principal/workspace/clearance ACL in hit-testing | Metadata-filter-only | PARTIAL | `P1.md` through `P5.md`; P3 missing D02 | F-DIFY-003, F-DIFY-004 |
| N no-answer | Source gate only; no generation refusal evaluated | Partial | PARTIAL | `N1.md`, `N2.md`, `N3.md`; N2 missing D03 | F-DIFY-005 |
| M multilingual | D14 returned for English and Chinese queries under metadata filter | Limited | PASS-with-metadata-filter | `M1.md`, `M2.md` | none |
| A multi-agent/tool | Retrieval of tool-related documents only; no native tool invocation | Metadata-filter-only | PASS-with-metadata-filter | `A1.md`, `A2.md` | F-DIFY-005 |
| F freshness | Active D14 returned and revoked D21 excluded under metadata filter | Metadata-filter-only | PASS-with-metadata-filter | `F1.md` | F-DIFY-003 |

## Findings View

Rows mirror `docs/ekb-research/findings/ledger.md`.

| finding_id | source_checkpoint | category | severity | subsystem | status |
| --- | --- | --- | --- | --- | --- |
| F-DIFY-001 | CP05 | deploy-friction | major | docker-compose | confirmed |
| F-DIFY-002 | CP05 | license-and-authorization | major | self-hosted-rbac | confirmed |
| F-DIFY-003 | CP06 | authorization | blocker | retrieval-acl | confirmed |
| F-DIFY-004 | CP06 | retrieval | major | economy-keyword-search | confirmed |
| F-DIFY-005 | CP06 | evaluation-surface | medium | generation-and-tools | confirmed |
| F-DIFY-006 | CP06 | observability | medium | tracing-hooks | confirmed |
