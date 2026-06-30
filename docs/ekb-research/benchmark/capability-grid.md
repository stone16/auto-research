# Capability Grid

Status: CP15 synthesis captured
Date: 2026-06-28

## Scope

This file aggregates per-framework capability ladders for the seven benchmark
dimensions. `Capability level` records the highest observed surface in the
dossier. `Earned maturity` records the benchmark-earned maturity and never
exceeds capability level. `ZERO` is distinct from `FAIL`; `N/A-by-design` would
mean the framework has no relevant surface, while `FAIL` would mean a surfaced
capability leaked or failed a gate. CP15 has no `N/A-by-design` rows and no
security `FAIL` rows.

## Grid

| Framework | Dimension | Capability level | Earned maturity | Ladder state | Evidence |
| --- | --- | --- | --- | --- | --- |
| RAGFlow | R retrieval+citation | 2 (F-RAGFLOW-003, F-RAGFLOW-006) | 1 (F-RAGFLOW-003, F-RAGFLOW-006) | PARTIAL, not N/A-by-design (F-RAGFLOW-003) | D02 zero chunks and no generation/citation evaluation (F-RAGFLOW-003, F-RAGFLOW-006) |
| RAGFlow | I tenant isolation | 1 (F-RAGFLOW-004) | 1 (F-RAGFLOW-004) | PASS-with-external-filter, not FAIL (F-RAGFLOW-004) | Dataset owner/team plus caller `document_ids`, no benchmark principal ACL (F-RAGFLOW-004) |
| RAGFlow | P permission scope | 1 (F-RAGFLOW-004) | 1 (F-RAGFLOW-003, F-RAGFLOW-004) | PARTIAL, not FAIL (F-RAGFLOW-004) | External document scope and P3 miss (F-RAGFLOW-003, F-RAGFLOW-004) |
| RAGFlow | N no-answer | 1 (F-RAGFLOW-006) | 1 (F-RAGFLOW-006) | PARTIAL source-gate maturity, not N/A-by-design (F-RAGFLOW-006) | Refusal text omitted from CP04 (F-RAGFLOW-006) |
| RAGFlow | M multilingual | 1 (F-RAGFLOW-004) | 1 (F-RAGFLOW-004) | PASS under external filter, not FAIL (F-RAGFLOW-004) | D14 source selection under caller scope (F-RAGFLOW-004) |
| RAGFlow | A multi-agent/tool | 1 (F-RAGFLOW-006) | 1 (F-RAGFLOW-004, F-RAGFLOW-006) | PARTIAL source-gate maturity, not N/A-by-design (F-RAGFLOW-006) | No native tool/MCP invocation evaluated (F-RAGFLOW-006) |
| RAGFlow | F freshness | 1 (F-RAGFLOW-004) | 1 (F-RAGFLOW-004) | PASS-with-external-filter, not FAIL (F-RAGFLOW-004) | Revoked source excluded by caller scope (F-RAGFLOW-004) |
| Dify | R retrieval+citation | 2 (F-DIFY-004, F-DIFY-005) | 1 (F-DIFY-004, F-DIFY-005) | PARTIAL, not N/A-by-design (F-DIFY-004) | Economy keyword misses and no generation/citation evaluation (F-DIFY-004, F-DIFY-005) |
| Dify | I tenant isolation | 1 (F-DIFY-003) | 1 (F-DIFY-003) | PASS-with-metadata-filter, not FAIL (F-DIFY-003) | Dataset token plus custom `source_id` filter (F-DIFY-003) |
| Dify | P permission scope | 1 (F-DIFY-003) | 1 (F-DIFY-003, F-DIFY-004) | PARTIAL, not FAIL (F-DIFY-003) | Metadata filter and P3 miss (F-DIFY-003, F-DIFY-004) |
| Dify | N no-answer | 1 (F-DIFY-005) | 1 (F-DIFY-005) | PARTIAL source-gate maturity, not N/A-by-design (F-DIFY-005) | No generated refusal evaluated (F-DIFY-005) |
| Dify | M multilingual | 1 (F-DIFY-003, F-DIFY-004) | 1 (F-DIFY-003, F-DIFY-004) | PASS-with-metadata-filter, not FAIL (F-DIFY-003) | D14 returned under custom metadata filter (F-DIFY-003, F-DIFY-004) |
| Dify | A multi-agent/tool | 1 (F-DIFY-005) | 1 (F-DIFY-005) | PARTIAL retrieval-only maturity, not N/A-by-design (F-DIFY-005) | No native tool invocation in CP06 (F-DIFY-005) |
| Dify | F freshness | 1 (F-DIFY-003) | 1 (F-DIFY-003) | PASS-with-metadata-filter, not FAIL (F-DIFY-003) | Revoked source excluded by custom metadata filter (F-DIFY-003) |
| WeKnora | R retrieval+citation | 2 (F-WEKNORA-003) | 2 (F-WEKNORA-003) | PASS source-selection maturity, citation unproven (F-WEKNORA-003) | Source chunks returned; generated citations not evaluated (F-WEKNORA-003) |
| WeKnora | I tenant isolation | 2 (F-WEKNORA-003) | 1 (F-WEKNORA-003) | PASS-with-source-filter, not FAIL (F-WEKNORA-003) | Tenant/API-key boundary plus `knowledge_ids` gate (F-WEKNORA-003) |
| WeKnora | P permission scope | 2 (F-WEKNORA-003) | 1 (F-WEKNORA-003) | PASS-with-source-filter, not FAIL (F-WEKNORA-003) | Document-level benchmark policy externalized (F-WEKNORA-003) |
| WeKnora | N no-answer | 1 (F-WEKNORA-004) | 1 (F-WEKNORA-004) | PARTIAL, not FAIL (F-WEKNORA-004) | N2 missed D03 under keyword retrieval (F-WEKNORA-004) |
| WeKnora | M multilingual | 1 (F-WEKNORA-003) | 1 (F-WEKNORA-003) | PASS-with-source-filter, not FAIL (F-WEKNORA-003) | Multilingual prompts used source gate (F-WEKNORA-003) |
| WeKnora | A multi-agent/tool | 1 (F-WEKNORA-005) | 1 (F-WEKNORA-005) | PARTIAL, not FAIL (F-WEKNORA-005) | MCP search lacks `knowledge_ids` source constraint (F-WEKNORA-005) |
| WeKnora | F freshness | 1 (F-WEKNORA-003) | 1 (F-WEKNORA-003) | PASS-with-source-filter, not FAIL (F-WEKNORA-003) | Revoked source avoided through source gate (F-WEKNORA-003) |
| MaxKB | R retrieval+citation | 2 (F-MAXKB-004) | 2 (F-MAXKB-004) | PASS/PARTIAL source-selection maturity, citation unproven (F-MAXKB-004) | Hit-test chunks scored; final answers not evaluated (F-MAXKB-004) |
| MaxKB | I tenant isolation | 2 (F-MAXKB-003) | 1 (F-MAXKB-003) | PASS-with-source-filter, not FAIL (F-MAXKB-003) | Default workspace/admin run with external source gate (F-MAXKB-003) |
| MaxKB | P permission scope | 2 (F-MAXKB-003) | 1 (F-MAXKB-003, F-MAXKB-004) | PARTIAL, not FAIL (F-MAXKB-003) | Workspace resource permissions plus external document gate (F-MAXKB-003) |
| MaxKB | N no-answer | 1 (F-MAXKB-004) | 1 (F-MAXKB-004) | PARTIAL, not FAIL (F-MAXKB-004) | N2 missed D03 and refusal omitted (F-MAXKB-004) |
| MaxKB | M multilingual | 2 (F-MAXKB-003) | 1 (F-MAXKB-003) | PASS-with-source-filter, not FAIL (F-MAXKB-003) | M1/M2 passed under source filter (F-MAXKB-003) |
| MaxKB | A multi-agent/tool | 1 (F-MAXKB-004) | 1 (F-MAXKB-004) | PARTIAL, not FAIL (F-MAXKB-004) | MCP path exists but was not executed (F-MAXKB-004) |
| MaxKB | F freshness | 1 (F-MAXKB-003, F-MAXKB-004) | 1 (F-MAXKB-003, F-MAXKB-004) | PARTIAL, not FAIL (F-MAXKB-004) | F1 missed D14; revoked source excluded externally (F-MAXKB-003, F-MAXKB-004) |
| Open WebUI | R retrieval+citation | 2 (F-OPENWEBUI-002, F-OPENWEBUI-003) | 1 (F-OPENWEBUI-003) | PARTIAL, not N/A-by-design (F-OPENWEBUI-003) | Required-source misses and no generation/citation evaluation (F-OPENWEBUI-003) |
| Open WebUI | I tenant isolation | 2 (F-OPENWEBUI-002) | 1 (F-OPENWEBUI-002) | PASS-with-source-filter, not FAIL (F-OPENWEBUI-002) | AccessGrant model exists; live gate externalized (F-OPENWEBUI-002) |
| Open WebUI | P permission scope | 2 (F-OPENWEBUI-002) | 1 (F-OPENWEBUI-002) | PASS code-audit, live source-filter-only (F-OPENWEBUI-002) | User/group grants not live benchmark principal resolver (F-OPENWEBUI-002) |
| Open WebUI | N no-answer | 1 (F-OPENWEBUI-003) | 1 (F-OPENWEBUI-003) | PARTIAL, not FAIL (F-OPENWEBUI-003) | N2 missed D03 and refusal omitted (F-OPENWEBUI-003) |
| Open WebUI | M multilingual | 1 (F-OPENWEBUI-003) | 1 (F-OPENWEBUI-003) | PARTIAL, not FAIL (F-OPENWEBUI-003) | M1/M2 missed D14 (F-OPENWEBUI-003) |
| Open WebUI | A multi-agent/tool | 1 (F-OPENWEBUI-003) | ZERO (F-OPENWEBUI-003) | ZERO-not-evaluated, not N/A-by-design and not security FAIL (F-OPENWEBUI-003) | Tool behavior omitted from CP10 benchmark (F-OPENWEBUI-003) |
| Open WebUI | F freshness | 1 (F-OPENWEBUI-002) | 1 (F-OPENWEBUI-002) | PASS-with-source-filter, not FAIL (F-OPENWEBUI-002) | Revoked source avoided through external collection scope (F-OPENWEBUI-002) |
| Flowise | R retrieval+citation | 2 (F-FLOWISE-003) | 1 (F-FLOWISE-003) | PARTIAL, not N/A-by-design (F-FLOWISE-003) | Stored chunks scanned; answer/citation not evaluated (F-FLOWISE-003) |
| Flowise | I tenant isolation | 2 (F-FLOWISE-002) | 1 (F-FLOWISE-002) | PASS-with-source-filter, not FAIL (F-FLOWISE-002) | API-key/workspace checks plus external source gate (F-FLOWISE-002) |
| Flowise | P permission scope | 2 (F-FLOWISE-002, F-FLOWISE-004) | 1 (F-FLOWISE-002) | PASS code-audit, live source-filter-only (F-FLOWISE-002) | Workspace RBAC exists; document ACL not proven (F-FLOWISE-002) |
| Flowise | N no-answer | 1 (F-FLOWISE-003) | 1 (F-FLOWISE-003) | PARTIAL, not FAIL (F-FLOWISE-003) | N2 missed D03 and refusal omitted (F-FLOWISE-003) |
| Flowise | M multilingual | 1 (F-FLOWISE-002) | 1 (F-FLOWISE-002) | PASS-with-source-filter, not FAIL (F-FLOWISE-002) | Source-scoped stores only (F-FLOWISE-002) |
| Flowise | A multi-agent/tool | 2 (F-FLOWISE-004) | 1 (F-FLOWISE-003, F-FLOWISE-004) | PARTIAL, not FAIL (F-FLOWISE-004) | MCP/API surfaces code-audited; no live tool trace (F-FLOWISE-003, F-FLOWISE-004) |
| Flowise | F freshness | 1 (F-FLOWISE-002) | 1 (F-FLOWISE-002) | PASS-with-source-filter, not FAIL (F-FLOWISE-002) | Revoked source avoided through external source gate (F-FLOWISE-002) |
| AnythingLLM | R retrieval+citation | 2 (F-ANYTHINGLLM-003) | 1 (F-ANYTHINGLLM-003) | PARTIAL, not N/A-by-design (F-ANYTHINGLLM-003) | Stored chunks scanned; answer/citation not evaluated (F-ANYTHINGLLM-003) |
| AnythingLLM | I tenant isolation | 2 (F-ANYTHINGLLM-002) | 1 (F-ANYTHINGLLM-002) | PASS-with-source-filter, not FAIL (F-ANYTHINGLLM-002) | Workspace membership exists; benchmark source gate externalized (F-ANYTHINGLLM-002) |
| AnythingLLM | P permission scope | 2 (F-ANYTHINGLLM-002, F-ANYTHINGLLM-004) | 1 (F-ANYTHINGLLM-002) | PASS code-audit, live source-filter-only (F-ANYTHINGLLM-002) | Developer API not bound to benchmark principal ACL (F-ANYTHINGLLM-002) |
| AnythingLLM | N no-answer | 1 (F-ANYTHINGLLM-003) | 1 (F-ANYTHINGLLM-003) | PARTIAL, not FAIL (F-ANYTHINGLLM-003) | N2 missed D03 and refusal omitted (F-ANYTHINGLLM-003) |
| AnythingLLM | M multilingual | 1 (F-ANYTHINGLLM-002) | 1 (F-ANYTHINGLLM-002) | PASS-with-source-filter, not FAIL (F-ANYTHINGLLM-002) | Source-scoped workspaces only (F-ANYTHINGLLM-002) |
| AnythingLLM | A multi-agent/tool | 2 (F-ANYTHINGLLM-004) | 1 (F-ANYTHINGLLM-003, F-ANYTHINGLLM-004) | PARTIAL, not FAIL (F-ANYTHINGLLM-004) | MCP/agent surfaces code-audited; no live tool trace (F-ANYTHINGLLM-003, F-ANYTHINGLLM-004) |
| AnythingLLM | F freshness | 1 (F-ANYTHINGLLM-002) | 1 (F-ANYTHINGLLM-002) | PASS-with-source-filter, not FAIL (F-ANYTHINGLLM-002) | Revoked source avoided through external source gate (F-ANYTHINGLLM-002) |

## N/A And FAIL Accounting

`N/A-by-design`: zero rows. Every reviewed framework exposed at least a partial
or adjacent surface for each benchmark dimension.

`FAIL`: zero rows. The exercised leak gates did not observe forbidden-source
leaks. Source-filter-only rows remain low-maturity passes or partials, not FAIL.

`ZERO`: one row. Open WebUI tool behavior is scored `ZERO` because the benchmark
did not exercise live tool or agent behavior; it is not hidden as N/A.
