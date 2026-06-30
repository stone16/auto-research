# RAGFlow Dossier

Status: CP04 ingest, query, and code audit captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Framework | RAGFlow |
| Repository | https://github.com/infiniflow/ragflow.git |
| Pinned SHA | f90be41eab4ccb9ad2c52031e6c5d3d89d998909 |
| INSTRUMENT_HASH | 1a2434beba68e3381d07a34c81babcc12e2b02caac4a56b58203fc55cc899f19 |
| CP04 dataset id | 2a24cb52729711f1b268f9a6a3b4685d |
| Security gate | PASS for I*/P*/P5/A2/F1 leak checks under CP04 external `document_ids` filtering; native principal/workspace/clearance ACL is N/A in the exercised REST retrieval path. |

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

Verdict: PARTIAL.

Evidence:

- Benchmark summary: `.harness/ekb-research/checkpoints/04/iter-1/evidence/cp04-benchmark-summary.json`
- Upload response: `.harness/ekb-research/checkpoints/04/iter-1/evidence/api-upload-documents.json`
- Final parse snapshot: `.harness/ekb-research/checkpoints/04/iter-1/evidence/api-parse-final.json`
- Benchmark runner log: `.harness/ekb-research/checkpoints/04/iter-1/evidence/cp04-run-benchmark-resume.log`

Observed behavior:

- CP04 uploaded all 21 corpus documents for the frozen instrument hash.
- RAGFlow marked all 21 documents `DONE`.
- Chunk coverage was incomplete: D01 produced 2 chunks, 19 documents produced 1 chunk each, and D02 produced 0 chunks. Total indexed chunks were 21 across 21 uploaded documents.
- D02 (`D02_acme_sales_pricing_matrix.pdf`) completed OCR/layout/table analysis but ended with `No chunk built from D02_acme_sales_pricing_matrix.pdf`. Queries requiring D02 could not retrieve that source.

Findings:

- F-RAGFLOW-003

### 3. Retrieval behavior

Verdict: PARTIAL.

Evidence:

- Query summary: `.harness/ekb-research/checkpoints/04/iter-1/evidence/cp04-query-results.json`
- Transcript directory: `docs/ekb-research/benchmark/runs/ragflow/`
- R2 transcript: `docs/ekb-research/benchmark/runs/ragflow/R2.md`
- P3 transcript: `docs/ekb-research/benchmark/runs/ragflow/P3.md`

Observed behavior:

- All 22 benchmark queries were attempted through RAGFlow REST retrieval.
- Retrieval dimension: 5 PASS, 1 PARTIAL. R2 was PARTIAL because the required D02 source had no indexed chunks.
- Permission dimension: 4 PASS-with-external-filter, 1 PARTIAL. P3 was PARTIAL for the same D02 ingestion gap.
- No-answer, multilingual, and freshness source-selection gates returned the expected required/forbidden source behavior within CP04 scope.
- CP04 used a deterministic TEI-compatible `/embed` sidecar to exercise RAGFlow ingestion and retrieval plumbing. These transcripts are source-selection evidence, not a claim about production semantic ranking quality.

Findings:

- F-RAGFLOW-003
- F-RAGFLOW-005

### 4. Tenant isolation mechanism

Verdict: EXTERNAL-FILTER-ONLY for benchmark principal isolation.

Evidence:

- Dataset search access check and retrieval call: `.harness/ekb-research/workspace/ragflow/api/apps/services/dataset_api_service.py:963` and `.harness/ekb-research/workspace/ragflow/api/apps/services/dataset_api_service.py:1056`
- Cross-dataset search access check and retrieval call: `.harness/ekb-research/workspace/ragflow/api/apps/services/dataset_api_service.py:1328` and `.harness/ekb-research/workspace/ragflow/api/apps/services/dataset_api_service.py:1428`
- Dataset accessibility model: `.harness/ekb-research/workspace/ragflow/api/db/services/knowledgebase_service.py:485` through `.harness/ekb-research/workspace/ragflow/api/db/services/knowledgebase_service.py:506`
- I* transcripts: `docs/ekb-research/benchmark/runs/ragflow/I1.md`, `docs/ekb-research/benchmark/runs/ragflow/I2.md`, and `docs/ekb-research/benchmark/runs/ragflow/I3.md`

Observed behavior:

- RAGFlow checks whether the API user can access the dataset. Dataset access is owner-or-team based.
- The exercised REST retrieval path does not accept benchmark principal attributes such as tenant, workspace, clearance, or explicit grants.
- CP04 enforced benchmark tenant/source boundaries by passing only the document ids permitted for each query. The I* leak gate passed under that external filter.

Findings:

- F-RAGFLOW-004

### 5. Permission/ACL model

Verdict: EXTERNAL-FILTER-ONLY for benchmark permission scope.

Evidence:

- Document accessibility defers to dataset accessibility: `.harness/ekb-research/workspace/ragflow/api/db/services/document_service.py:766` through `.harness/ekb-research/workspace/ragflow/api/db/services/document_service.py:770`
- Retrieval endpoint validates requested document ids belong to the dataset: `.harness/ekb-research/workspace/ragflow/api/apps/restful_apis/chunk_api.py:304` through `.harness/ekb-research/workspace/ragflow/api/apps/restful_apis/chunk_api.py:325`
- Retrieval call receives caller-supplied `document_ids`: `.harness/ekb-research/workspace/ragflow/api/apps/restful_apis/chunk_api.py:360` through `.harness/ekb-research/workspace/ragflow/api/apps/restful_apis/chunk_api.py:364`
- P* transcripts: `docs/ekb-research/benchmark/runs/ragflow/P1.md` through `docs/ekb-research/benchmark/runs/ragflow/P5.md`

Observed behavior:

- Native document access is not modeled as per-principal, per-workspace, or per-clearance policy in the exercised retrieval path.
- The API can restrict retrieval to specific `document_ids`; CP04 used that as an external enforcement shim.
- Forbidden sources were absent for P1, P2, P4, and P5 under the shim. P3 remained PARTIAL because D02 had no chunks, not because of a forbidden-source leak.

Findings:

- F-RAGFLOW-004

### 6. Data model reconstruction

Verdict: PARTIAL.

Evidence:

- Dataset and document access services cited in dimensions 4 and 5.
- Benchmark source id mapping in CP04 runner output: `.harness/ekb-research/checkpoints/04/iter-1/evidence/cp04-query-results.json`

Observed behavior:

- Dataset, document, and chunk identity are sufficient to run scoped retrieval with explicit `document_ids`.
- The audited path did not expose a native model matching the benchmark's tenant/workspace/group/grant/clearance rules.

Findings:

- F-RAGFLOW-004

### 7. Generation and citation

Verdict: NOT EXERCISED for answer generation.

Evidence:

- Retrieval transcripts: `docs/ekb-research/benchmark/runs/ragflow/`

Observed behavior:

- CP04 exercised retrieval endpoints and chunk/source evidence only.
- The generated transcripts record returned chunks and source ids. They do not prove generated answer correctness or citation assembly.
- No-answer queries are source-gate evidence only: no forbidden source was returned, but no generation refusal template was evaluated.

Findings:

- F-RAGFLOW-006

### 8. Tool/MCP surface

Verdict: NOT NATIVE in CP04 retrieval path.

Evidence:

- A1 transcript: `docs/ekb-research/benchmark/runs/ragflow/A1.md`
- A2 transcript: `docs/ekb-research/benchmark/runs/ragflow/A2.md`

Observed behavior:

- A1 and A2 were attempted through the same retrieval endpoint.
- A2 did not trigger a `tool.invoke:release_lookup` action and returned public release-note chunks instead. This is acceptable source-gate evidence but not a tool-invocation evaluation.

Findings:

- F-RAGFLOW-006

### 9. Observability and eval

Verdict: PARTIAL.

Evidence:

- CP04 compose up: `.harness/ekb-research/checkpoints/04/iter-1/evidence/compose-up.txt`
- CP04 ready status: `.harness/ekb-research/checkpoints/04/iter-1/evidence/compose-ps-ready.txt`
- Web smoke: `.harness/ekb-research/checkpoints/04/iter-1/evidence/smoke-ui-18080.txt`
- API smoke: `.harness/ekb-research/checkpoints/04/iter-1/evidence/smoke-api-19380.txt`
- Runtime logs: `.harness/ekb-research/checkpoints/04/iter-1/evidence/ragflow-logs-ready-tail.txt`
- Benchmark summary and query results listed above.

Observed behavior:

- CP04 captured API status, parse status, query responses, top chunks, and paired-control notes.
- The run required inserting a local API token and user access token into the fresh Docker database for automation; see `.harness/ekb-research/checkpoints/04/iter-1/evidence/mysql-create-api-token.txt` and `.harness/ekb-research/checkpoints/04/iter-1/evidence/mysql-fix-admin-access-token.txt`.

Findings:

- F-RAGFLOW-005

### 10. Extraction candidates

Status: preliminary.

Evidence:

- Retrieval pipeline and access-control code cited above.
- CP04 transcripts in `docs/ekb-research/benchmark/runs/ragflow/`.

Candidates:

- RAGFlow's retrieval endpoint can be used as a source-selection benchmark surface when explicit document scopes are supplied.
- Dataset-level access is simple and observable, but it is not a sufficient extraction candidate for enterprise principal/grant enforcement without an additional policy layer.
- Parser status is visible enough to catch zero-chunk ingestion failures and tie them back to retrieval misses.

Findings:

- F-RAGFLOW-003
- F-RAGFLOW-004

### 11. License posture

Status: not assessed in CP04.

Evidence:

- Planned for later synthesis.

Findings:

- none

### 12. Benchmark grid result

Verdict: 22/22 attempted; 7 dimensions filled.

Evidence:

- Query summary: `.harness/ekb-research/checkpoints/04/iter-1/evidence/cp04-query-results.json`
- Benchmark summary: `.harness/ekb-research/checkpoints/04/iter-1/evidence/cp04-benchmark-summary.json`
- Transcript directory: `docs/ekb-research/benchmark/runs/ragflow/`

Dimension counts:

- retrieval: 5 PASS, 1 PARTIAL
- tenant_isolation: 3 PASS-with-external-filter
- permission_scope: 4 PASS-with-external-filter, 1 PARTIAL
- no_answer: 3 PASS
- multilingual: 2 PASS
- multi_agent_tool: 2 PASS-with-external-filter
- freshness: 1 PASS-with-external-filter

Findings:

- F-RAGFLOW-003
- F-RAGFLOW-004
- F-RAGFLOW-005
- F-RAGFLOW-006

### 13. Gaps vs target design

Status: recorded for cross-framework synthesis.

Evidence:

- Code audit and transcript evidence listed above.

Gaps:

- No native benchmark principal ACL in the exercised retrieval path.
- PDF/table ingestion can silently produce a DONE document with zero chunks.
- CP04 does not establish answer-generation citation behavior.
- CP04 does not establish native tool/MCP invocation behavior.

Findings:

- F-RAGFLOW-003
- F-RAGFLOW-004
- F-RAGFLOW-006

## Seven-Dimension Benchmark Grid

| Dimension | Capability level | Earned maturity | Verdict | Transcript evidence | Finding ids |
| --- | --- | --- | --- | --- | --- |
| R retrieval+citation | Retrieval source selection works for indexed docs; generation/citation not exercised | Partial | PARTIAL | `R1.md` through `R6.md`; R2 missing D02 | F-RAGFLOW-003, F-RAGFLOW-006 |
| I tenant isolation | Dataset owner/team access plus caller-supplied document scope | External-filter-only | PASS-with-external-filter | `I1.md`, `I2.md`, `I3.md` | F-RAGFLOW-004 |
| P permission scope | Caller-supplied document scope; no native principal/workspace/clearance ACL | External-filter-only | PARTIAL | `P1.md` through `P5.md`; P3 missing D02 | F-RAGFLOW-003, F-RAGFLOW-004 |
| N no-answer | Source gate only; no generation refusal evaluated | Partial | PASS for source gate | `N1.md`, `N2.md`, `N3.md` | F-RAGFLOW-006 |
| M multilingual | D14 returned for English and Chinese queries | Limited | PASS | `M1.md`, `M2.md` | none |
| A multi-agent/tool | Retrieval of tool-related documents only; no native tool invocation | External-filter-only | PASS-with-external-filter | `A1.md`, `A2.md` | F-RAGFLOW-004, F-RAGFLOW-006 |
| F freshness | Active D14 returned and revoked D21 excluded under external filter | External-filter-only | PASS-with-external-filter | `F1.md` | F-RAGFLOW-004 |

## Findings View

Rows mirror `docs/ekb-research/findings/ledger.md`.

| finding_id | source_checkpoint | category | severity | subsystem | status |
| --- | --- | --- | --- | --- | --- |
| F-RAGFLOW-001 | CP03 | deploy-friction | major | docker-compose | confirmed |
| F-RAGFLOW-002 | CP03 | deploy-friction | medium | local-runtime | confirmed |
| F-RAGFLOW-003 | CP04 | ingestion | major | pdf-parser | confirmed |
| F-RAGFLOW-004 | CP04 | authorization | blocker | retrieval-acl | confirmed |
| F-RAGFLOW-005 | CP04 | deploy-friction | major | embedding-service | confirmed |
| F-RAGFLOW-006 | CP04 | evaluation-surface | medium | generation-and-tools | confirmed |
