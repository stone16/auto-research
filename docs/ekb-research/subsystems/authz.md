# Authorization Stack Audit

Status: CP13 static code-audit captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Scope | OpenFGA, OPA, Casbin authorization-engine audit |
| Design anchors | `docs/enterprise-knowledge-base-design.md:443` through `docs/enterprise-knowledge-base-design.md:477` |
| OpenFGA repo | https://github.com/openfga/openfga.git |
| OpenFGA pinned SHA | bccdbbd243ed519f21448ca84a0f31c5dbd23d68 |
| OPA repo | https://github.com/open-policy-agent/opa.git |
| OPA pinned SHA | 9c83b9948a643a9142986563c3863307e523493a |
| Casbin repo | https://github.com/casbin/casbin.git |
| Casbin pinned SHA | 1571e4f34fdad9106d05ab8d8ef59f5efc7fe987 |
| Recommendation | Use OpenFGA for relationship checks, OPA for contextual policy, and treat Casbin as a fallback RBAC/ABAC library rather than the relationship-sharing core. |

## Design Mapping

| Design need | Source lines | Audit interpretation |
| --- | --- | --- |
| Relationship tuples | `docs/enterprise-knowledge-base-design.md:443` through `docs/enterprise-knowledge-base-design.md:456` | Needs first-class object, relation, and user or userset tuple checks for tenant, workspace, KB, document, group, and tool objects. |
| Example checks | `docs/enterprise-knowledge-base-design.md:458` through `docs/enterprise-knowledge-base-design.md:464` | Needs read document, invoke tool, and grant KB decisions over nested relationships. |
| Contextual policy | `docs/enterprise-knowledge-base-design.md:466` through `docs/enterprise-knowledge-base-design.md:477` | Needs non-relationship predicates such as region, production write approval, restricted LLM use, MFA freshness, API key scopes, MCP redirect origins, and DLP redaction. |
| Retrieval gate | `docs/enterprise-knowledge-base-design.md:564` through `docs/enterprise-knowledge-base-design.md:568` | Requires permission filtering before and after ranking, not only route-level access. |

## Comparison

| Engine | Best fit | Relationship tuples | Contextual policy | Permission-before-ranking | Permission-after-ranking | Shared grant R5/P5 | Recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OpenFGA | ReBAC relationship graph | Strong: CheckRequest tuple key and graph resolver operate on object, relation, and user or userset. | Limited to contextual tuples and conditions; not a general policy language. | Strong if retrieval candidate IDs are filtered through batch Check/ListObjects before ranking. | Strong if ranked source IDs are rechecked before citation. | Strong: tuple-to-userset and computed userset support model shared grants. | Use as the relationship decision plane behind document, KB, workspace, group, tenant, and tool grants. |
| OPA | ABAC and contextual policy | Indirect: can encode relationships as data but has no native tuple graph semantics. | Strong: arbitrary input document and Rego evaluation support region, MFA, API-key, redirect-origin, DLP, and write-approval checks. | Strong when called as a policy filter over candidate metadata. | Strong when called again on ranked/cited candidates. | Medium: possible as policy/data, but model maintenance is harder than OpenFGA tuples. | Use beside OpenFGA for contextual denies and obligations. |
| Casbin | Embedded RBAC/ABAC library | Medium for simple roles/domains/resource roles; weak for nested relationship-heavy sharing. | Medium: matcher expressions and ABAC object attributes are flexible but app-owned. | Medium: possible as an in-process filter, but every relation must be flattened into policy/matchers. | Medium for the same reason. | Weak: shared grants require custom role/resource-role modeling, not native tuple-to-userset traversal. | Do not use as the core ReBAC engine; keep as a simple embedded-policy option where needed. |

## OpenFGA Audit

Verdict: strongest donor for the design's ReBAC relationship layer.

Evidence:

- API check entrypoint records store, object, relation, and user from the request tuple key, authorizes the API call, resolves the type system, and builds a CheckCommand: `.harness/ekb-research/workspace/openfga/pkg/server/check.go:37` through `.harness/ekb-research/workspace/openfga/pkg/server/check.go:180`
- The CheckCommand input carries `StoreID`, `TupleKey`, `ContextualTuples`, `Context`, and consistency: `.harness/ekb-research/workspace/openfga/pkg/server/commands/check_command.go:44` through `.harness/ekb-research/workspace/openfga/pkg/server/commands/check_command.go:50`
- CheckCommand validates tuple shape and contextual tuples, converts the request tuple, includes contextual tuples in request storage, and invokes `ResolveCheck`: `.harness/ekb-research/workspace/openfga/pkg/server/commands/check_command.go:102` through `.harness/ekb-research/workspace/openfga/pkg/server/commands/check_command.go:150`
- `ResolveCheckRequest` stores the model id, tuple key, contextual tuples, context, visited paths, and consistency: `.harness/ekb-research/workspace/openfga/internal/graph/resolve_check_request.go:18` through `.harness/ekb-research/workspace/openfga/internal/graph/resolve_check_request.go:42`
- The local resolver rejects cycles, loads relation rewrites from the type system, verifies a path exists from user to relation/object type, then evaluates the relation rewrite: `.harness/ekb-research/workspace/openfga/internal/graph/check.go:394` through `.harness/ekb-research/workspace/openfga/internal/graph/check.go:471`
- Direct tuple reads enforce object, relation, and user equality and filter tuple conditions against request context: `.harness/ekb-research/workspace/openfga/internal/graph/check.go:547` through `.harness/ekb-research/workspace/openfga/internal/graph/check.go:596`
- Relation rewrites include computed usersets and tuple-to-userset constructs: `.harness/ekb-research/workspace/openfga/pkg/typesystem/typesystem.go:98` through `.harness/ekb-research/workspace/openfga/pkg/typesystem/typesystem.go:123`
- The graph model names direct, computed-userset, and tuple-to-userset edges; tuple-to-userset records a tupleset relation such as a document parent relation: `.harness/ekb-research/workspace/openfga/internal/graph/graph.go:44` through `.harness/ekb-research/workspace/openfga/internal/graph/graph.go:95`, and `.harness/ekb-research/workspace/openfga/internal/graph/graph.go:233` through `.harness/ekb-research/workspace/openfga/internal/graph/graph.go:267`

Mapping:

- Design tuple `document:pricing-faq#parent@kb:sales-playbook` maps to OpenFGA object `document:pricing-faq`, relation `parent`, user/userset `kb:sales-playbook`; tuple-to-userset can express inherited document read through KB ownership or reader grants.
- Design tuple `tool:crm_lookup#invoker@group:sales-se` maps directly to the same object/relation/user tuple shape.
- Example check `can user:alice read document:pricing-faq?` maps to CheckRequest tuple key object `document:pricing-faq`, relation `read`, user `user:alice`.
- Example check `can service_account:mcp-sales invoke tool:crm_lookup?` maps to object `tool:crm_lookup`, relation `invoke`, user `service_account:mcp-sales`.
- Example check `can user:bob grant kb:sales-playbook to group:partner-users?` maps to object `kb:sales-playbook`, relation `grant`, user `user:bob`, with group targets represented as usersets or grant target tuples.

Limits:

- OpenFGA is not enough by itself for all contextual policy examples. Contextual tuples and conditions exist, but the design examples also require non-relationship obligations such as DLP redaction, MFA freshness, external LLM deny rules, and MCP redirect-origin checks. Those fit OPA more naturally.
- Permission-before-ranking and permission-after-ranking require the RAG application to call OpenFGA on candidate document IDs before ranking and again on the ranked citation set. OpenFGA supplies the check engine; the retrieval pipeline must enforce the call placement.

Findings:

- F-AUTHZ-001

## OPA Audit

Verdict: strongest donor for contextual ABAC and deny/obligation policy.

Evidence:

- The server data POST path reads request input, captures request metadata, starts a decision id, prepares a Rego query, passes parsed input and metrics into evaluation, and returns the result: `.harness/ekb-research/workspace/opa/v1/server/server.go:1741` through `.harness/ekb-research/workspace/opa/v1/server/server.go:1885`
- `makeRego` converts a data path into a query and attaches transaction, parsed query, parsed input, metrics, query tracer, instrumentation, runtime, unsafe builtin policy, print hook, and tracing options: `.harness/ekb-research/workspace/opa/v1/server/server.go:2644` through `.harness/ekb-research/workspace/opa/v1/server/server.go:2675`
- `readInputPostV1` accepts JSON or YAML input, rejects malformed bodies, carries request metadata, and converts `input` into an AST value: `.harness/ekb-research/workspace/opa/v1/server/server.go:2971` through `.harness/ekb-research/workspace/opa/v1/server/server.go:3012`
- `Rego` options expose query, parsed query, native input, and parsed input hooks: `.harness/ekb-research/workspace/opa/v1/rego/rego.go:921` through `.harness/ekb-research/workspace/opa/v1/rego/rego.go:979`
- `Rego.Eval` prepares the query and supplies transaction, metrics, instrumentation, time, cache, and seed options to evaluation: `.harness/ekb-research/workspace/opa/v1/rego/rego.go:1501` through `.harness/ekb-research/workspace/opa/v1/rego/rego.go:1525`
- `PreparedEvalQuery.Eval` builds a new evaluation context, selects the compiled eval query, and calls the Rego evaluator: `.harness/ekb-research/workspace/opa/v1/rego/rego.go:548` through `.harness/ekb-research/workspace/opa/v1/rego/rego.go:569`
- The topdown evaluator runs query expressions, handles cancellation, traces expressions, and dispatches evaluation steps and calls: `.harness/ekb-research/workspace/opa/v1/topdown/eval.go:181` through `.harness/ekb-research/workspace/opa/v1/topdown/eval.go:194`, `.harness/ekb-research/workspace/opa/v1/topdown/eval.go:404` through `.harness/ekb-research/workspace/opa/v1/topdown/eval.go:458`, and `.harness/ekb-research/workspace/opa/v1/topdown/eval.go:1035` through `.harness/ekb-research/workspace/opa/v1/topdown/eval.go:1075`
- Decision logging records decision id, path, query, input, results, error, metrics, bundles, request id, evaluated rules, and custom request/response metadata: `.harness/ekb-research/workspace/opa/v1/server/server.go:3107` through `.harness/ekb-research/workspace/opa/v1/server/server.go:3160`

Mapping:

- "Block export of confidential documents outside approved regions" maps to Rego over input fields such as action, document sensitivity, region, and tenant residency.
- "Require approval for write tools against production systems" maps to Rego over tool risk, target environment, and approval state.
- "Deny use of external LLMs for restricted documents" maps to Rego over document tags and model/provider metadata.
- "Require MFA freshness for admin actions" maps to Rego over principal session claims and action.
- "Block API keys without kb:read from retrieval endpoints" maps to Rego over API key scopes and endpoint/action.
- "Restrict MCP clients to explicitly registered redirect origins and scopes" maps to Rego over client registration, redirect origin, scopes, and tool id.
- "Require tenant-specific DLP redaction before traces leave the deployment" maps to Rego over trace destination, tenant policy, and redaction status.

Limits:

- OPA can encode relationships as data, but that is application-owned data modeling. It does not provide OpenFGA's tuple graph, tuple-to-userset resolver, or relationship-store APIs out of the box.
- The missing-dimension-scores-ZERO rule is not an OPA built-in. OPA can enforce it if the evaluation payload includes all expected dimensions and a Rego rule treats absent dimensions as zero, but the rule must be authored by the EKB evaluation layer.

Findings:

- F-AUTHZ-002

## Casbin Audit

Verdict: useful embedded RBAC/ABAC library, but weaker for the design's relationship-heavy shared grants.

Evidence:

- The main enforcer builds and evaluates govaluate matcher expressions, iterates policy rows, converts matcher results to allow/deny effects, and merges effects into the final decision: `.harness/ekb-research/workspace/casbin/enforcer.go:781` through `.harness/ekb-research/workspace/casbin/enforcer.go:917`
- Public `Enforce`, `EnforceWithMatcher`, `EnforceEx`, and `BatchEnforce` call the same enforcement path: `.harness/ekb-research/workspace/casbin/enforcer.go:936` through `.harness/ekb-research/workspace/casbin/enforcer.go:970`
- RBAC role APIs read and write roles through a role manager and grouping policies: `.harness/ekb-research/workspace/casbin/rbac_api.go:28` through `.harness/ekb-research/workspace/casbin/rbac_api.go:70`, and `.harness/ekb-research/workspace/casbin/management_api.go:367` through `.harness/ekb-research/workspace/casbin/management_api.go:390`
- Domain RBAC example models subject, domain, object, and action with a three-argument role function: `.harness/ekb-research/workspace/casbin/examples/rbac_with_domains_model.conf:1` through `.harness/ekb-research/workspace/casbin/examples/rbac_with_domains_model.conf:14`
- ABAC example shows attribute access through a matcher expression: `.harness/ekb-research/workspace/casbin/examples/abac_model.conf:1` through `.harness/ekb-research/workspace/casbin/examples/abac_model.conf:11`
- Resource-role example supports a second role graph for objects: `.harness/ekb-research/workspace/casbin/examples/rbac_with_resource_roles_model.conf:1` through `.harness/ekb-research/workspace/casbin/examples/rbac_with_resource_roles_model.conf:15`
- Conditional role manager can attach link condition functions to role edges: `.harness/ekb-research/workspace/casbin/rbac/default-role-manager/role_manager.go:1045` through `.harness/ekb-research/workspace/casbin/rbac/default-role-manager/role_manager.go:1056`

Mapping:

- RBAC baseline is straightforward: tenant/workspace roles can map to roles and domains.
- ABAC checks are possible through matcher expressions over request objects or attributes.
- Simple resource roles can model one object-role graph, but the design needs nested tenant -> workspace -> KB -> document inheritance and explicit shared grants that interact with groups and service accounts. Casbin can be made to represent this, but the application must flatten or duplicate relationships into grouping policies and matchers.

Limits:

- Casbin does not provide a native tuple-to-userset graph equivalent to OpenFGA for shared-grant traversal.
- Relationship-heavy sharing would require custom model files, role managers, policy storage, and explicit prefilter/recheck placement in retrieval.
- Because it is library-embedded, consistency, explanation, and multi-service policy administration would be owned by the EKB app rather than by a dedicated relationship service.

Findings:

- F-AUTHZ-003

## Recommendation For Contracts

| Contract area | Recommendation | Findings |
| --- | --- | --- |
| `authz.fga` | Encode tenant, workspace, group, knowledge_base, document, and tool relationships in OpenFGA form. | F-AUTHZ-001 |
| Contextual policy | Layer OPA decisions beside OpenFGA checks for region, MFA, LLM-provider, API-key scope, MCP redirect-origin, DLP, and approval semantics. | F-AUTHZ-002 |
| Casbin | Do not use as the first-choice relationship engine; keep as a simple embedded RBAC/ABAC option only if a service-local policy check is needed. | F-AUTHZ-003 |
| Retrieval enforcement | The RAG pipeline must call authz before candidate ranking and again before emitting citations/tool results; none of the authz engines enforces that placement without application integration. | F-AUTHZ-004 |

## Findings Summary

| finding_id | Summary |
| --- | --- |
| F-AUTHZ-001 | OpenFGA is the ReBAC donor for tuple relationship checks and shared grants. |
| F-AUTHZ-002 | OPA is the contextual policy donor for ABAC denies and obligations. |
| F-AUTHZ-003 | Casbin is weaker for relationship-heavy sharing despite useful RBAC/ABAC matchers. |
| F-AUTHZ-004 | Permission-before-ranking and permission-after-ranking are pipeline obligations, not automatic engine behavior. |
