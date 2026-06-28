# Cross-Framework Comparison Matrix

Status: CP15 synthesis captured
Date: 2026-06-28

## Scope

This matrix normalizes the seven framework dossiers across the frozen benchmark
dimensions in `docs/ekb-research/rubric.md`. Scores are earned maturity on the
0-3 rubric scale. `ZERO` is explicit where a dimension was not exercised or did
not earn maturity; it is not hidden as N/A.

The `donor_eligible` column is a leak pre-filter derived from each framework's
security gate. All seven framework dossiers recorded `security_gate=PASS` for
the exercised leak checks, so this column is `PASS` for every row. That is only
a pre-filter. The donor decision still rejects source-filter-only ACL evidence,
retrieval-quality gaps, and unexercised generation/tool behavior.

## Matrix

| Framework | Dimension | Score | Verdict | donor_eligible | Donor decision |
| --- | --- | --- | --- | --- | --- |
| RAGFlow | R retrieval+citation | 1/3 (F-RAGFLOW-003, F-RAGFLOW-006) | PARTIAL: D02-related misses and no generated citations (F-RAGFLOW-003, F-RAGFLOW-006) | PASS from security_gate=PASS (F-RAGFLOW-004) | NO: retrieval parser gap and citation surface not proven (F-RAGFLOW-003, F-RAGFLOW-006) |
| RAGFlow | I tenant isolation | 1/3 (F-RAGFLOW-004) | PASS-with-external-filter, not native benchmark principal policy (F-RAGFLOW-004) | PASS from security_gate=PASS (F-RAGFLOW-004) | NO: external `document_ids` filter only (F-RAGFLOW-004) |
| RAGFlow | P permission scope | 1/3 (F-RAGFLOW-003, F-RAGFLOW-004) | PARTIAL: source filter plus D02/P3 gap (F-RAGFLOW-003, F-RAGFLOW-004) | PASS from security_gate=PASS (F-RAGFLOW-004) | NO: no native principal/workspace/clearance ACL (F-RAGFLOW-004) |
| RAGFlow | N no-answer | 1/3 (F-RAGFLOW-006) | PASS for source gate only; refusal text not evaluated (F-RAGFLOW-006) | PASS from security_gate=PASS (F-RAGFLOW-004) | NO: no generated refusal harness (F-RAGFLOW-006) |
| RAGFlow | M multilingual | 1/3 (F-RAGFLOW-004) | PASS under externally scoped retrieval (F-RAGFLOW-004) | PASS from security_gate=PASS (F-RAGFLOW-004) | NO: result depends on external source filter (F-RAGFLOW-004) |
| RAGFlow | A multi-agent/tool | 1/3 (F-RAGFLOW-004, F-RAGFLOW-006) | PASS-with-external-filter for source selection only; no native tool trace (F-RAGFLOW-006) | PASS from security_gate=PASS (F-RAGFLOW-004) | NO: tool execution and tool ACL not proven (F-RAGFLOW-004, F-RAGFLOW-006) |
| RAGFlow | F freshness | 1/3 (F-RAGFLOW-004) | PASS-with-external-filter; revoked D21 excluded by caller scope (F-RAGFLOW-004) | PASS from security_gate=PASS (F-RAGFLOW-004) | NO: freshness gate depends on caller-supplied scope (F-RAGFLOW-004) |
| Dify | R retrieval+citation | 1/3 (F-DIFY-004, F-DIFY-005) | PARTIAL: economy keyword misses and no generated citations (F-DIFY-004, F-DIFY-005) | PASS from security_gate=PASS (F-DIFY-003) | NO: production retrieval and answer path not proven (F-DIFY-004, F-DIFY-005) |
| Dify | I tenant isolation | 1/3 (F-DIFY-003) | PASS-with-metadata-filter, not native benchmark principal policy (F-DIFY-003) | PASS from security_gate=PASS (F-DIFY-003) | NO: custom `source_id` filter only (F-DIFY-003) |
| Dify | P permission scope | 1/3 (F-DIFY-003, F-DIFY-004) | PARTIAL: metadata filter plus P3 miss (F-DIFY-003, F-DIFY-004) | PASS from security_gate=PASS (F-DIFY-003) | NO: no native principal/workspace/clearance ACL in hit testing (F-DIFY-003) |
| Dify | N no-answer | 1/3 (F-DIFY-005) | PARTIAL: source gate only and no generated refusal evaluated (F-DIFY-005) | PASS from security_gate=PASS (F-DIFY-003) | NO: no answer/refusal harness (F-DIFY-005) |
| Dify | M multilingual | 1/3 (F-DIFY-003, F-DIFY-004) | PASS-with-metadata-filter for D14 retrieval (F-DIFY-003, F-DIFY-004) | PASS from security_gate=PASS (F-DIFY-003) | NO: metadata-filter-only maturity (F-DIFY-003) |
| Dify | A multi-agent/tool | 1/3 (F-DIFY-005) | PASS-with-metadata-filter for retrieval only; no native tool invocation (F-DIFY-005) | PASS from security_gate=PASS (F-DIFY-003) | NO: app/workflow tool trace not exercised (F-DIFY-005) |
| Dify | F freshness | 1/3 (F-DIFY-003) | PASS-with-metadata-filter; revoked source exclusion externalized (F-DIFY-003) | PASS from security_gate=PASS (F-DIFY-003) | NO: freshness gate depends on custom metadata filter (F-DIFY-003) |
| WeKnora | R retrieval+citation | 2/3 (F-WEKNORA-003) | PASS for source selection with generated citations not evaluated (F-WEKNORA-003) | PASS from security_gate=PASS (F-WEKNORA-003) | NO: citation and generated-answer path not proven (F-WEKNORA-003) |
| WeKnora | I tenant isolation | 1/3 (F-WEKNORA-003) | PASS-with-source-filter using tenant/API-key plus `knowledge_ids` gate (F-WEKNORA-003) | PASS from security_gate=PASS (F-WEKNORA-003) | NO: benchmark document ACL remained external (F-WEKNORA-003) |
| WeKnora | P permission scope | 1/3 (F-WEKNORA-003) | PASS-with-source-filter; document policy externalized (F-WEKNORA-003) | PASS from security_gate=PASS (F-WEKNORA-003) | NO: source gate extension needed before donor use (F-WEKNORA-003) |
| WeKnora | N no-answer | 1/3 (F-WEKNORA-004) | PARTIAL: N2 missed D03 under keyword retrieval (F-WEKNORA-004) | PASS from security_gate=PASS (F-WEKNORA-003) | NO: no-answer quality unreliable without production ranking (F-WEKNORA-004) |
| WeKnora | M multilingual | 1/3 (F-WEKNORA-003) | PASS-with-source-filter under multilingual prompts (F-WEKNORA-003) | PASS from security_gate=PASS (F-WEKNORA-003) | NO: source-filter-only maturity (F-WEKNORA-003) |
| WeKnora | A multi-agent/tool | 1/3 (F-WEKNORA-005) | PASS-with-source-filter for transcripts; MCP search cannot carry `knowledge_ids` (F-WEKNORA-005) | PASS from security_gate=PASS (F-WEKNORA-003) | NO: MCP search is not benchmark-safe until source constraints are carried (F-WEKNORA-005) |
| WeKnora | F freshness | 1/3 (F-WEKNORA-003) | PASS-with-source-filter; revoked source excluded externally (F-WEKNORA-003) | PASS from security_gate=PASS (F-WEKNORA-003) | NO: freshness policy not native to retrieval path (F-WEKNORA-003) |
| MaxKB | R retrieval+citation | 2/3 (F-MAXKB-004) | PASS/PARTIAL source selection with generated citations not evaluated (F-MAXKB-004) | PASS from security_gate=PASS (F-MAXKB-003) | NO: answer and citation assembly not exercised (F-MAXKB-004) |
| MaxKB | I tenant isolation | 1/3 (F-MAXKB-003) | PASS-with-source-filter; default workspace/admin run (F-MAXKB-003) | PASS from security_gate=PASS (F-MAXKB-003) | NO: benchmark tenant policy externalized (F-MAXKB-003) |
| MaxKB | P permission scope | 1/3 (F-MAXKB-003, F-MAXKB-004) | PARTIAL: P3 miss and source-filter-only permission gate (F-MAXKB-003, F-MAXKB-004) | PASS from security_gate=PASS (F-MAXKB-003) | NO: workspace resource grants are not document ACL proof (F-MAXKB-003) |
| MaxKB | N no-answer | 1/3 (F-MAXKB-004) | PARTIAL: N2 missed D03; refusal not evaluated (F-MAXKB-004) | PASS from security_gate=PASS (F-MAXKB-003) | NO: no generated no-answer behavior proven (F-MAXKB-004) |
| MaxKB | M multilingual | 1/3 (F-MAXKB-003) | PASS-with-source-filter for M1/M2 (F-MAXKB-003) | PASS from security_gate=PASS (F-MAXKB-003) | NO: source-filter-only maturity (F-MAXKB-003) |
| MaxKB | A multi-agent/tool | 1/3 (F-MAXKB-004) | PARTIAL: A1 missed D17 and MCP not executed (F-MAXKB-004) | PASS from security_gate=PASS (F-MAXKB-003) | NO: live MCP/tool path not proven (F-MAXKB-004) |
| MaxKB | F freshness | 1/3 (F-MAXKB-003, F-MAXKB-004) | PARTIAL: F1 missed D14 while revoked D21 excluded externally (F-MAXKB-003, F-MAXKB-004) | PASS from security_gate=PASS (F-MAXKB-003) | NO: source gate and freshness answer quality not native/proven (F-MAXKB-003, F-MAXKB-004) |
| Open WebUI | R retrieval+citation | 1/3 (F-OPENWEBUI-002, F-OPENWEBUI-003) | PARTIAL: multiple required-source misses and no generated citations (F-OPENWEBUI-003) | PASS from security_gate=PASS (F-OPENWEBUI-002) | NO: retrieval quality and citation path not proven (F-OPENWEBUI-003) |
| Open WebUI | I tenant isolation | 1/3 (F-OPENWEBUI-002) | PASS-with-source-filter; collection IDs selected externally (F-OPENWEBUI-002) | PASS from security_gate=PASS (F-OPENWEBUI-002) | NO: native grant model not exercised as benchmark principal resolver (F-OPENWEBUI-002) |
| Open WebUI | P permission scope | 1/3 (F-OPENWEBUI-002) | PASS for code-audited grants; live benchmark ACL externalized (F-OPENWEBUI-002) | PASS from security_gate=PASS (F-OPENWEBUI-002) | NO: group/document grant matrix not live-tested (F-OPENWEBUI-002) |
| Open WebUI | N no-answer | 1/3 (F-OPENWEBUI-003) | PARTIAL: N2 missed D03 and generated refusal not evaluated (F-OPENWEBUI-003) | PASS from security_gate=PASS (F-OPENWEBUI-002) | NO: no generated no-answer behavior proven (F-OPENWEBUI-003) |
| Open WebUI | M multilingual | 1/3 (F-OPENWEBUI-003) | PARTIAL: M1/M2 missed D14 (F-OPENWEBUI-003) | PASS from security_gate=PASS (F-OPENWEBUI-002) | NO: multilingual retrieval quality insufficient (F-OPENWEBUI-003) |
| Open WebUI | A multi-agent/tool | ZERO/3 (F-OPENWEBUI-003) | ZERO: tool behavior not evaluated live (F-OPENWEBUI-003) | PASS from security_gate=PASS (F-OPENWEBUI-002) | NO: tool-agent maturity absent in benchmark (F-OPENWEBUI-003) |
| Open WebUI | F freshness | 1/3 (F-OPENWEBUI-002) | PASS-with-source-filter; revoked-source gate externalized (F-OPENWEBUI-002) | PASS from security_gate=PASS (F-OPENWEBUI-002) | NO: freshness policy not native to retrieval path (F-OPENWEBUI-002) |
| Flowise | R retrieval+citation | 1/3 (F-FLOWISE-003) | PARTIAL: deterministic chunk scan only, no citations/generation (F-FLOWISE-003) | PASS from security_gate=PASS (F-FLOWISE-002) | NO: document-store plumbing is not answer quality (F-FLOWISE-003) |
| Flowise | I tenant isolation | 1/3 (F-FLOWISE-002) | PASS-with-source-filter; API-key/workspace checks not benchmark document ACL (F-FLOWISE-002) | PASS from security_gate=PASS (F-FLOWISE-002) | NO: document-level policy remains first-party (F-FLOWISE-002) |
| Flowise | P permission scope | 1/3 (F-FLOWISE-002, F-FLOWISE-004) | PASS for workspace/API-key RBAC code audit; benchmark ACL externalized (F-FLOWISE-002, F-FLOWISE-004) | PASS from security_gate=PASS (F-FLOWISE-002) | NO for ACL donor; YES only for integration controls (F-FLOWISE-004) |
| Flowise | N no-answer | 1/3 (F-FLOWISE-003) | PARTIAL: N2 miss and no generated refusal (F-FLOWISE-003) | PASS from security_gate=PASS (F-FLOWISE-002) | NO: no answer/refusal path exercised (F-FLOWISE-003) |
| Flowise | M multilingual | 1/3 (F-FLOWISE-002) | PASS-with-source-filter under source-scoped stores (F-FLOWISE-002) | PASS from security_gate=PASS (F-FLOWISE-002) | NO: source-filter-only maturity (F-FLOWISE-002) |
| Flowise | A multi-agent/tool | 1/3 (F-FLOWISE-003, F-FLOWISE-004) | PARTIAL: MCP/API surfaces exist but live tool trace not run (F-FLOWISE-003, F-FLOWISE-004) | PASS from security_gate=PASS (F-FLOWISE-002) | YES for API/CLI/MCP hardening only; NO for tool ACL (F-FLOWISE-004) |
| Flowise | F freshness | 1/3 (F-FLOWISE-002) | PASS-with-source-filter; revoked-source gate externalized (F-FLOWISE-002) | PASS from security_gate=PASS (F-FLOWISE-002) | NO: freshness policy remains first-party (F-FLOWISE-002) |
| AnythingLLM | R retrieval+citation | 1/3 (F-ANYTHINGLLM-003) | PARTIAL: deterministic chunk scan only, no citations/generation (F-ANYTHINGLLM-003) | PASS from security_gate=PASS (F-ANYTHINGLLM-002) | NO: workspace-document plumbing is not answer quality (F-ANYTHINGLLM-003) |
| AnythingLLM | I tenant isolation | 1/3 (F-ANYTHINGLLM-002) | PASS-with-source-filter; workspace selection externalized (F-ANYTHINGLLM-002) | PASS from security_gate=PASS (F-ANYTHINGLLM-002) | NO: developer API key is not benchmark principal ACL (F-ANYTHINGLLM-002) |
| AnythingLLM | P permission scope | 1/3 (F-ANYTHINGLLM-002, F-ANYTHINGLLM-004) | PASS for role/membership surfaces; document ACL not proven (F-ANYTHINGLLM-002, F-ANYTHINGLLM-004) | PASS from security_gate=PASS (F-ANYTHINGLLM-002) | NO for ACL donor; YES only for API ergonomics (F-ANYTHINGLLM-004) |
| AnythingLLM | N no-answer | 1/3 (F-ANYTHINGLLM-003) | PARTIAL: N2 miss and no generated refusal (F-ANYTHINGLLM-003) | PASS from security_gate=PASS (F-ANYTHINGLLM-002) | NO: no generated no-answer behavior proven (F-ANYTHINGLLM-003) |
| AnythingLLM | M multilingual | 1/3 (F-ANYTHINGLLM-002) | PASS-with-source-filter under source-scoped workspaces (F-ANYTHINGLLM-002) | PASS from security_gate=PASS (F-ANYTHINGLLM-002) | NO: source-filter-only maturity (F-ANYTHINGLLM-002) |
| AnythingLLM | A multi-agent/tool | 1/3 (F-ANYTHINGLLM-003, F-ANYTHINGLLM-004) | PARTIAL: MCP/agent surfaces exist but live tool trace not run (F-ANYTHINGLLM-003, F-ANYTHINGLLM-004) | PASS from security_gate=PASS (F-ANYTHINGLLM-002) | YES for OpenAI/API/MCP adapter patterns only; NO for tool ACL (F-ANYTHINGLLM-004) |
| AnythingLLM | F freshness | 1/3 (F-ANYTHINGLLM-002) | PASS-with-source-filter; revoked-source gate externalized (F-ANYTHINGLLM-002) | PASS from security_gate=PASS (F-ANYTHINGLLM-002) | NO: freshness policy remains first-party (F-ANYTHINGLLM-002) |

## Donor Filter Result

No row has `donor_eligible=FAIL`, so the leak pre-filter excludes no framework
solely by security gate. The extraction map still recommends no donor for the
core retrieval ACL path because the relevant findings show external source
filters or metadata filters rather than native benchmark-equivalent policy
enforcement.
