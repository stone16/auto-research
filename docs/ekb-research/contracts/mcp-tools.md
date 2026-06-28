# EKB MCP Tool Contract

Status: CP19 contract artifact
Date: 2026-06-28

## Scope

This contract fixes the first-party MCP tool surface from
`docs/enterprise-knowledge-base-design.md:707-717` and applies the security
rules from `docs/enterprise-knowledge-base-design.md:727-735`. Scope names use
the resource-level permission vocabulary in
`docs/enterprise-knowledge-base-design.md:426-441`.

MCP is an alternate client protocol, not a permission bypass. Every MCP request
must authenticate through OAuth/OIDC or a scoped service account, map to the same
principal model as REST, run the same OpenFGA/OPA checks as REST, and emit
trace/audit records. This rule is mandatory because benchmark A1 requires an
authorized `kb.search` tool call with trace proof, while benchmark A2 requires
`tool.invoke` denial when `rep@acme/sales` lacks a `tool:invoke` grant
(`docs/ekb-research/benchmark/query-suite.md:232-250`).

## Common Envelope

| Field | Requirement |
| --- | --- |
| Authentication | OAuth/OIDC user token or scoped service account token. |
| Tenant context | `tenant_id`, `workspace_id`, and principal id resolved before tool dispatch. |
| Authorization | Same relationship and contextual policy decision path as REST; no MCP-only allow path. |
| Trace | Every call receives or creates a `trace_id` and records tool name, principal, tenant, workspace, decision, latency, and policy versions. |
| Audit | Every allow, deny, approval request, and approval result writes an audit event. |
| Sensitivity metadata | Tool schemas declare input sensitivity, output sensitivity, and whether output may include source text. |
| Side-effect metadata | Tool schemas declare `side_effect: none`, `write_internal`, or `external_action`. |

Risk levels:

| Risk | Meaning |
| --- | --- |
| Low | Read-only metadata or bounded retrieval of already permitted material. |
| Medium | Reads raw source content, runs generation, writes internal feedback/eval state, or may reveal sensitive context. |
| High | Can invoke external tools or produce side effects outside the KB control plane. |

## Tool Surface

| Tool | Purpose | Required scopes | Risk | Side effect | Approval and audit semantics |
| --- | --- | --- | --- | --- | --- |
| `kb.search` | Retrieve permitted chunks and source metadata from selected knowledge bases. | `kb:read`, `document:read`, `chunk:read` on each selected KB/document after tenant/workspace resolution. | Low | `none` | No approval for read-only retrieval. Must recheck permissions before and after ranking, return only permitted citations, trace the retrieval event, and audit allow/deny. |
| `kb.ask` | Answer a question using permitted retrieval results and structured citations. | `app:run`, `kb:read`, `document:read`, `chunk:read` on selected sources. | Medium | `none` | No approval for ordinary reads. Must call retrieval through the same permission path as `kb.search`, emit answer trace with citations and confidence, and audit allow/deny. |
| `kb.get_source` | Return a permitted source document, chunk, or cited span for inspection. | `kb:read`, `document:read`; `chunk:read` when returning chunk/span bodies. | Medium | `none` | No approval for read-only access. Must enforce document/span permission, redact by tenant DLP policy when required, trace source access, and audit allow/deny. |
| `kb.list_knowledge_bases` | List knowledge bases visible to the principal in a workspace. | `kb:read` for each returned KB or workspace membership that implies KB read visibility. | Low | `none` | No approval. Must filter the list before response construction and audit the list operation without leaking hidden KB ids. |
| `kb.list_documents` | List visible documents and ingestion status for a knowledge base. | `kb:read`, `document:read` for returned documents. | Low | `none` | No approval. Must filter per document before response construction, omit hidden document ids, trace list pagination, and audit allow/deny. |
| `kb.explain_answer` | Explain answer provenance, retrieval scores, policy filters, and citation decisions for an existing trace. | `trace:read` for the trace plus `kb:read`, `document:read`, and `chunk:read` for any cited evidence returned. | Medium | `none` | No approval unless tenant trace policy requires break-glass for sensitive bodies. Must hide evidence the principal cannot currently read and audit trace inspection. |
| `kb.create_feedback` | Attach user or operator feedback to an answer, citation, or trace. | `app:run`; `trace:read` when feedback references an existing trace. | Medium | `write_internal` | Write tool. Requires explicit grant through the authenticated principal; optional approval is not required by default because it writes only feedback metadata. Must audit creation and include the target `trace_id` when present. |
| `kb.run_eval` | Start an evaluation run over an approved dataset, trace sample, or query suite. | `eval:run`; `trace:read` when sampling traces; `kb:read`, `document:read`, and `chunk:read` for evaluated sources. | Medium | `write_internal` | Write tool. Requires explicit `eval:run` grant. Approval is optional for scheduled or high-cost production evals. Must write eval-run, score, and dataset audit records with missing dimensions scored as zero downstream. |
| `tool.invoke` | Invoke a registered external or internal tool through the EKB tool gateway. | `tool:invoke` on the target tool plus any tool-declared downstream scopes such as `kb:read`, `document:read`, `audit:read`, or connector-specific grants. | High | `external_action` unless the tool schema proves read-only behavior. | Tool-invoke path. Requires explicit tool grant, contextual OPA checks, sensitivity and side-effect metadata, and approval workflow whenever policy marks the tool high-risk, write-capable, production-impacting, or external. Must deny and audit missing grants instead of falling back to best-effort execution. |

## Permission And Trace Contract

1. MCP and REST share one principal resolver. A service account such as
   `service_account:mcp-sales` is authorized through the same group, tenant,
   workspace, KB, document, and tool relations as REST
   (`docs/ekb-research/contracts/authz.fga`).
2. MCP tools cannot return a citation, source body, trace body, eval row, or tool
   result that the same principal could not obtain through the REST API.
3. Retrieval tools must filter before ranking and recheck after ranking, matching
   the first-party retrieval guardrail in
   `docs/ekb-research/extraction-map.md`.
4. `tool.invoke` must never fabricate fixture output or convert a denied tool
   invocation into an implied success. The A2 benchmark gate is PASS only when
   the tool is not invoked and no forbidden fixture output is returned.
5. Every call writes a trace/audit record even on deny. Minimum fields are
   `trace_id`, `tenant_id`, `workspace_id`, `principal_id`, `tool_name`,
   `resource_ids`, `decision`, `policy_version`, `input_hash`, `output_hash`
   when output exists, `latency_ms`, and `created_at`.

## A1/A2 Benchmark Tie

| Benchmark | Contract requirement |
| --- | --- |
| A1 authorized MCP/tool retrieval | `svc-mcp@acme/sales` may call `kb.search` only if its service-account principal has the required KB/document/chunk grants. The result must cite D17 and include a traced tool call for PASS. |
| A2 tool permission gate | `rep@acme/sales` lacks `tool:invoke`; `tool.invoke` for `release_lookup` must be denied, traced, and audited. The answer path may cite permitted D18 without tool output, but must not return or fabricate `tool.invoke:release_lookup` output. |

## Coverage Table

| Design tool | Design source | Documented tool row | Missing? |
| --- | --- | --- | --- |
| `kb.search` | `docs/enterprise-knowledge-base-design.md:708` | `kb.search` | no |
| `kb.ask` | `docs/enterprise-knowledge-base-design.md:709` | `kb.ask` | no |
| `kb.get_source` | `docs/enterprise-knowledge-base-design.md:710` | `kb.get_source` | no |
| `kb.list_knowledge_bases` | `docs/enterprise-knowledge-base-design.md:711` | `kb.list_knowledge_bases` | no |
| `kb.list_documents` | `docs/enterprise-knowledge-base-design.md:712` | `kb.list_documents` | no |
| `kb.explain_answer` | `docs/enterprise-knowledge-base-design.md:713` | `kb.explain_answer` | no |
| `kb.create_feedback` | `docs/enterprise-knowledge-base-design.md:714` | `kb.create_feedback` | no |
| `kb.run_eval` | `docs/enterprise-knowledge-base-design.md:715` | `kb.run_eval` | no |
| `tool.invoke` | `docs/enterprise-knowledge-base-design.md:716` | `tool.invoke` | no |

Missing design tools: 0.
