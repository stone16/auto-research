# EKB Wiring Audit

Status: CP20 wiring gate captured
Date: 2026-06-28

## Scope

This audit verifies wiring across CP15 through CP19. It does not author new
findings, schema, authz, OpenAPI, or MCP contract content. It checks two things:

1. Every extraction-map subsystem row traces to real findings-ledger rows.
2. The four contract artifacts cover, partially cover, or explicitly gap the
   benchmark requirements named in the CP20 acceptance criteria.

Mechanical evidence:
`.harness/ekb-research/checkpoints/20/iter-1/evidence/wiring-mechanical-check.txt`.

## Mechanical Gate Summary

| Check | Result |
| --- | --- |
| Findings ledger rows parsed | 42 |
| Extraction-map subsystem rows parsed | 9 |
| Extraction-map finding references parsed | 23 |
| Dangling finding_id references | 0 |
| Findings with `status=open` | 0 |
| Extraction-map rows without a ledger-backed finding | 0 |
| Query shortfalls from benchmark result JSON | 23 |
| Ledger rows citing those shortfall query IDs | 34 |
| Append-shortfall check | PASS: 23 shortfalls <= 34 ledger query citations |

Shortfall query IDs covered by ledger citations:
`A1`, `F1`, `M1`, `M2`, `N2`, `P3`, `P4`, `R1`, `R2`, `R4`, `R5`.

## Extraction To Findings Trace

| Extraction-map row | Target subsystem | Findings-ledger backing | Result |
| --- | --- | --- | --- |
| `docs/ekb-research/extraction-map.md:31` | Local runtime and operator packaging | F-FLOWISE-004 at `docs/ekb-research/findings/ledger.md:37`; guardrails F-RAGFLOW-002 at line 9, F-MAXKB-001 at line 26, F-OPENWEBUI-001 at line 30, F-FLOWISE-001 at line 34, F-ANYTHINGLLM-001 at line 38 | Backed; donor is extract, Docker/runtime limits are confirmed guardrails. |
| `docs/ekb-research/extraction-map.md:32` | Corpus ingestion and source registry | F-ANYTHINGLLM-004 at `docs/ekb-research/findings/ledger.md:41`; guardrail F-RAGFLOW-003 at line 10 | Backed; raw-text/API ergonomics are extract, parser-completion warning is confirmed. |
| `docs/ekb-research/extraction-map.md:33` | Retrieval, ranking, and citation assembly | F-AUTHZ-001 at `docs/ekb-research/findings/ledger.md:42`; F-AUTHZ-002 at line 43; guardrails F-RAGFLOW-004 at line 11, F-DIFY-003 at line 16, F-WEKNORA-003 at line 22, F-MAXKB-003 at line 28, F-OPENWEBUI-002 at line 31, F-FLOWISE-002 at line 35, F-ANYTHINGLLM-002 at line 39 | Backed; first-party pipeline boundary is justified by multiple source-filter-only ACL findings. |
| `docs/ekb-research/extraction-map.md:34` | Relationship authorization (ReBAC) | F-AUTHZ-001 at `docs/ekb-research/findings/ledger.md:42`; guardrail F-AUTHZ-004 at line 45 | Backed; OpenFGA is extract for decisions, not automatic retrieval insertion. |
| `docs/ekb-research/extraction-map.md:35` | Contextual policy and obligations | F-AUTHZ-002 at `docs/ekb-research/findings/ledger.md:43`; paired ReBAC boundary F-AUTHZ-001 at line 42 | Backed; OPA is extract for contextual decisions and obligations. |
| `docs/ekb-research/extraction-map.md:36` | Public API and OpenAI-compatible surface | F-ANYTHINGLLM-004 at `docs/ekb-research/findings/ledger.md:41`; F-FLOWISE-004 at line 37; guardrails F-ANYTHINGLLM-002 at line 39 and F-FLOWISE-002 at line 35 | Backed; API ergonomics are extract but authz remains first-party. |
| `docs/ekb-research/extraction-map.md:37` | MCP and tool gateway | F-FLOWISE-004 at `docs/ekb-research/findings/ledger.md:37`; F-ANYTHINGLLM-004 at line 41; guardrail F-WEKNORA-005 at line 24 | Backed; MCP hardening patterns are extract, source constraints and tool permission checks remain first-party. |
| `docs/ekb-research/extraction-map.md:38` | Observability, prompts, and eval datasets | F-OBS-001 at `docs/ekb-research/findings/ledger.md:46`; guardrail F-OBS-004 at line 49 | Backed; Langfuse-compatible plumbing is extract, scoring policy is not delegated to it. |
| `docs/ekb-research/extraction-map.md:39` | Evaluation and release scoring | F-OBS-003 at `docs/ekb-research/findings/ledger.md:48`; guardrails F-OBS-002 at line 47 and F-OBS-004 at line 49 | Backed; DeepEval/Ragas are metric producers, zero-fill scoring remains first-party. |

Unbacked extraction-map entries: none.

Dangling finding references: none.

Open findings: none.

## Data-Flow Audit

| Benchmark requirement | Dimension | Contract artifact lines | Coverage verdict | Boundary |
| --- | --- | --- | --- | --- |
| I2 tenant isolation with paired Globex/Acme behavior (`docs/ekb-research/benchmark/query-suite.md:112-120`) | I tenant isolation | `docs/ekb-research/contracts/schema.sql:53-63` defines tenant ownership and `current_tenant_id`; `docs/ekb-research/contracts/schema.sql:456-519` enables RLS policies; `docs/ekb-research/contracts/openapi.yaml:363-369` requires `X-Tenant-Id` tenant context | Covered at contract level | Real-traced to schema and OpenAPI contracts; runtime propagation from HTTP header to Postgres setting is assumed because no service implementation exists. |
| P4 restricted clearance (`docs/ekb-research/benchmark/query-suite.md:162-170`) | P permission scope | `docs/ekb-research/contracts/schema.sql:205-224` provides document/chunk metadata slots for sensitivity; `docs/ekb-research/contracts/schema.sql:262-270` defines policy bindings; `docs/ekb-research/contracts/authz.fga:11-12` delegates contextual ABAC/DLP to OPA | Partial with explicit gap | Assumed boundary: no executable OPA/Rego clearance policy is present in the CP16-CP19 contracts. |
| R5 shared-grant positive and P5 shared-grant negative (`docs/ekb-research/benchmark/query-suite.md:82-90`, `docs/ekb-research/benchmark/query-suite.md:172-180`) | R retrieval and P permission scope | `docs/ekb-research/contracts/schema.sql:249-260` stores resource grants; `docs/ekb-research/contracts/authz.fga:65-78` models grant inheritance into KB/document read; `docs/ekb-research/contracts/openapi.yaml:625-641` requires source citation fields | Covered at contract level | Real-traced to schema/authz/OpenAPI contracts; enforcement inside retrieval candidate generation is assumed pending service implementation. |
| R1/R6 citations and trace_id (`docs/ekb-research/benchmark/query-suite.md:42-50`, `docs/ekb-research/benchmark/query-suite.md:92-100`) | R retrieval and citation | `docs/ekb-research/contracts/openapi.yaml:607-624` requires answer, non-empty citations, confidence, retrieval, and trace_id; `docs/ekb-research/contracts/openapi.yaml:625-641` defines citation fields; `docs/ekb-research/contracts/schema.sql:315-338` stores retrieval and answer events with trace_id | Covered at contract level | Real-traced to OpenAPI/schema contracts; citation correctness is an implementation/eval boundary. |
| A1 authorized MCP/tool retrieval (`docs/ekb-research/benchmark/query-suite.md:232-240`) | A multi-agent/tool | `docs/ekb-research/contracts/mcp-tools.md:46` scopes `kb.search`; `docs/ekb-research/contracts/mcp-tools.md:79` ties A1 to D17 plus traced tool call; `docs/ekb-research/contracts/schema.sql:340-374` stores tool grants and tool calls; `docs/ekb-research/contracts/authz.fga:80-86` models tool invoke | Covered at contract level | Real-traced to MCP/schema/authz contracts; live MCP invocation is assumed pending service implementation. |
| A2 tool permission gate (`docs/ekb-research/benchmark/query-suite.md:242-250`) | A multi-agent/tool | `docs/ekb-research/contracts/mcp-tools.md:54` requires `tool:invoke`; `docs/ekb-research/contracts/mcp-tools.md:67-73` forbids denied-tool fallback and requires trace/audit; `docs/ekb-research/contracts/mcp-tools.md:80` ties A2 to deny/no fixture output; `docs/ekb-research/contracts/schema.sql:364-374` records allow/deny/error tool call decisions | Covered at contract level | Real-traced to MCP/schema contracts; live denial path is assumed pending service implementation. |
| M1/M2 language (`docs/ekb-research/benchmark/query-suite.md:212-230`) | M multilingual | `docs/ekb-research/contracts/openapi.yaml:555-572` accepts arbitrary query text and response options; `docs/ekb-research/contracts/openapi.yaml:607-624` returns answer/confidence/trace; `docs/ekb-research/contracts/schema.sql:205-224` provides metadata slots that can carry language tags | Partial with explicit gap | Assumed boundary: no contract artifact defines `language`, `locale`, language detection, or answer-language preservation semantics. |
| F1 freshness with revoked source and index version (`docs/ekb-research/benchmark/query-suite.md:252-260`) | F freshness | `docs/ekb-research/contracts/schema.sql:189-202` gives documents `status` including revoked; `docs/ekb-research/contracts/schema.sql:227-246` defines immutable index version references for embeddings; `docs/ekb-research/contracts/schema.sql:315-325` links retrieval events to `index_version_id`; `docs/ekb-research/contracts/openapi.yaml:652-667` requires response `index_version` | Covered at contract level | Real-traced to schema/OpenAPI contracts; runtime rule "revoked source cannot be cited after new index_version" is assumed. |
| N1/N3 no-answer and leak-free refusal (`docs/ekb-research/benchmark/query-suite.md:182-190`, `docs/ekb-research/benchmark/query-suite.md:202-210`) | N no-answer | `docs/ekb-research/contracts/openapi.yaml:586-597` models mandatory citation requirements; `docs/ekb-research/contracts/openapi.yaml:607-624` requires `answer`, non-empty `citations`, `confidence`, and `trace_id`; `docs/ekb-research/contracts/schema.sql:387-443` stores eval cases, expected metrics, scores, and zero-fill facts for release checks | Partial with explicit gap | Assumed boundary: OpenAPI provides answer/confidence fields, but no contract artifact defines a no-answer enum, refusal reason schema, or executable anti-fabrication policy. |

## Contract Artifact Coverage

| Contract artifact | Appears in Data-Flow Audit rows |
| --- | --- |
| `docs/ekb-research/contracts/schema.sql` | I2, P4, R5/P5, R1/R6, A1, A2, M1/M2, F1, N1/N3 |
| `docs/ekb-research/contracts/authz.fga` | P4, R5/P5, A1 |
| `docs/ekb-research/contracts/openapi.yaml` | I2, R5/P5, R1/R6, M1/M2, F1, N1/N3 |
| `docs/ekb-research/contracts/mcp-tools.md` | A1, A2 |

Every contract artifact appears in at least one Data-Flow Audit row. Every
benchmark dimension appears in at least one row: R, I, P, N, M, A, and F.

## Explicit Gaps

| Gap | Affected requirement | Why it remains a gap |
| --- | --- | --- |
| No executable restricted-clearance policy artifact | P4 | Schema and authz contracts provide metadata/policy-binding/delegation hooks, but no Rego or equivalent policy file defines `restricted_hr` clearance. |
| No explicit language contract | M1/M2 | OpenAPI and schema accept multilingual text and metadata, but no artifact requires language detection, language tags, or same-language answer behavior. |
| No explicit no-answer/refusal schema | N1/N3 | `answer` and `confidence` exist, but no enum, refusal reason, or anti-fabrication rule is encoded in OpenAPI/schema. |
| No runtime service wiring | I2, P4, R5/P5, R1/R6, A1/A2, F1 | CP16-CP19 are contract artifacts only; there is no implemented API service to prove header-to-RLS propagation, OpenFGA/OPA calls, retrieval pre/post filters, MCP execution, or revoked-index enforcement. |

## Boundary Classification

| Boundary | Classification | Reason |
| --- | --- | --- |
| Extraction-map row to findings-ledger row | Real-traced | Mechanical check parsed 9 extraction rows, 23 finding references, 42 ledger rows, zero dangling references, and zero open findings. |
| Query shortfall to ledger citation | Real-traced | Mechanical check counted 23 non-PASS query shortfalls and 34 ledger query-id citations. |
| `schema.sql` syntax and RLS presence | Real-traced | CP16 validated the schema in Postgres and this audit cites line-level tenant/RLS artifacts. |
| `authz.fga` tuple model | Real-traced | CP17 validated the model and this audit cites line-level grant/tool relations. |
| `openapi.yaml` response and tenant contract | Real-traced | CP18 validated the OpenAPI document and this audit cites line-level response/tenant fields. |
| `mcp-tools.md` tool surface | Real-traced | CP19 validated 9 design tools, zero missing, and this audit cites line-level A1/A2 tool rules. |
| HTTP `X-Tenant-Id` to Postgres `app.tenant_id` | Assumed | No service implementation exists in this harness scope. |
| Retrieval pre-rank and post-rank authz calls | Assumed | Contracts require the boundary, but no retriever implementation exists. |
| Restricted clearance evaluation | Assumed gap | Delegated to OPA/policy bindings, but no executable policy artifact exists. |
| Language handling for multilingual answers | Assumed gap | Contracts allow strings/metadata, but no language field or policy exists. |
| No-answer/refusal behavior | Assumed gap | OpenAPI can carry the answer and confidence, but refusal semantics require implementation and eval policy. |
| MCP live invocation and denial | Assumed | MCP contract and tool-call table exist, but no server path is implemented. |

## Conclusion

Extraction claims are fully backed by ledger rows, with zero dangling references
and zero open findings. The contracts cover the named benchmark requirements at
the contract level, except the explicit gaps above. Those gaps must be carried
into the final tech spec rather than treated as completed runtime behavior.
