# EKB Evidence-Grounded Tech Spec

Status: CP21 final synthesis
Date: 2026-06-28

## Scope

This spec assembles the enterprise knowledge-base design from the CP15
comparison artifacts, CP16-CP19 contract artifacts, and CP20 wiring audit. The
harness stops at spec plus validated contract artifacts. It does not build a
running API service, MCP server, retriever, UI, or deployment.

## Source Index

| Artifact class | Path |
| --- | --- |
| Benchmark grid | `docs/ekb-research/benchmark/capability-grid.md` |
| Comparison matrix | `docs/ekb-research/comparison-matrix.md` |
| Extraction map | `docs/ekb-research/extraction-map.md` |
| Wiring audit | `docs/ekb-research/wiring-audit.md` |
| RAGFlow dossier | `docs/ekb-research/dossiers/ragflow.md` |
| Dify dossier | `docs/ekb-research/dossiers/dify.md` |
| WeKnora dossier | `docs/ekb-research/dossiers/weknora.md` |
| MaxKB dossier | `docs/ekb-research/dossiers/maxkb.md` |
| Open WebUI dossier | `docs/ekb-research/dossiers/open-webui.md` |
| Flowise dossier | `docs/ekb-research/dossiers/flowise.md` |
| AnythingLLM dossier | `docs/ekb-research/dossiers/anythingllm.md` |
| Postgres contract | `docs/ekb-research/contracts/schema.sql` |
| Authorization contract | `docs/ekb-research/contracts/authz.fga` |
| REST contract | `docs/ekb-research/contracts/openapi.yaml` |
| MCP contract | `docs/ekb-research/contracts/mcp-tools.md` |

## Non-Negotiables

| Rule | Governing artifact |
| --- | --- |
| `tenant_id` exists everywhere and RLS gates every table. | `docs/ekb-research/contracts/schema.sql` |
| Authorization is RBAC plus ReBAC plus ABAC: roles/groups, relationship tuples, and contextual OPA-style obligations. | `docs/ekb-research/contracts/authz.fga`, `docs/ekb-research/contracts/schema.sql` |
| Every answer carries structured citations and `trace_id`. | `docs/ekb-research/contracts/openapi.yaml` |
| Permission filters run before ranking and again after ranking/citation assembly. | `docs/ekb-research/extraction-map.md`, `docs/ekb-research/wiring-audit.md` |
| Missing, skipped, errored, or absent evaluation dimensions score as zero before aggregation. | `docs/ekb-research/extraction-map.md`, `docs/ekb-research/wiring-audit.md` |

## Subsystem Plan

| Subsystem | Decision | Extraction-map source | Governing contract |
| --- | --- | --- | --- |
| Local runtime and operator packaging | Build first-party runtime; lift Flowise CLI and route packaging patterns only. Docker sizing, port remaps, health probes, and cleanup remain operator guidance. | `docs/ekb-research/extraction-map.md:17` | No runtime contract in CP16-CP19; governed as an explicit runtime-wiring gap in `docs/ekb-research/wiring-audit.md`. |
| Corpus ingestion and source registry | Build first-party ingestion with chunk accounting, parser-completion checks, source hashes, and source-id registry; reuse AnythingLLM API/raw-text ergonomics. | `docs/ekb-research/extraction-map.md:18` | `docs/ekb-research/contracts/schema.sql` for source connectors, documents, document versions, chunks, and index versions. |
| Retrieval, ranking, and citation assembly | Build first-party retrieval pipeline with explicit pre-rank and post-rank policy call points; no framework retrieval ACL is sufficient as a donor. | `docs/ekb-research/extraction-map.md:19` | `docs/ekb-research/contracts/schema.sql`, `docs/ekb-research/contracts/authz.fga`, `docs/ekb-research/contracts/openapi.yaml`. |
| Relationship authorization (ReBAC) | Extract OpenFGA as the relationship decision-plane model for tenant, workspace, group, KB, document, and tool grants. | `docs/ekb-research/extraction-map.md:20` | `docs/ekb-research/contracts/authz.fga`; grant persistence in `docs/ekb-research/contracts/schema.sql`. |
| Contextual policy and obligations | Extract OPA-style request-input policy evaluation for region, MFA, DLP, LLM-provider, MCP redirect-origin, approval, and decision logging. | `docs/ekb-research/extraction-map.md:21` | `docs/ekb-research/contracts/schema.sql` for policy bindings and decision logs; `docs/ekb-research/contracts/authz.fga` delegates contextual ABAC to OPA. |
| Public API and OpenAI-compatible surface | Lift AnythingLLM developer/OpenAI-compatible API ergonomics and Flowise modular route organization, but bind every route to first-party tenant/principal/authz contracts. | `docs/ekb-research/extraction-map.md:22` | `docs/ekb-research/contracts/openapi.yaml`. |
| MCP and tool gateway | Lift Flowise custom-MCP hardening and AnythingLLM MCP-to-agent adapter patterns; build first-party source constraints and tool-permission checks. | `docs/ekb-research/extraction-map.md:23` | `docs/ekb-research/contracts/mcp-tools.md`, `docs/ekb-research/contracts/schema.sql`, `docs/ekb-research/contracts/authz.fga`. |
| Observability, prompts, and eval datasets | Extract Langfuse-compatible traces, observations, prompt versions, scores, datasets, and trace-to-dataset linkage; keep final scoring first-party. | `docs/ekb-research/extraction-map.md:24` | `docs/ekb-research/contracts/schema.sql`, `docs/ekb-research/contracts/openapi.yaml`. |
| Evaluation and release scoring | Use DeepEval for span-level CI metrics and Ragas only as raw metric producers; wrap both with an EKB zero-fill normalizer. | `docs/ekb-research/extraction-map.md:25` | `docs/ekb-research/contracts/schema.sql` for eval datasets, cases, runs, and scores. |

## Canonical Subsystem Crosswalk

The approved spec names nine canonical target subsystems: tenant, knowledge,
ingestion, retrieval, generation, tool-mcp, observability, authz, and eval. The
Subsystem Plan above re-decomposes those concerns into implementation rows, but
the canonical ownership remains:

| Canonical subsystem | Carrying plan row(s) | Verdict |
| --- | --- | --- |
| tenant | Relationship authorization (ReBAC); Contextual policy and obligations; Public API and OpenAI-compatible surface | Build first-party tenant propagation, RLS context, and tenant-scoped APIs; extract OpenFGA and OPA only as decision-plane donors. |
| knowledge | Corpus ingestion and source registry | Build first-party knowledge-base, source, document, chunk, hash, and index-version registry; lift only AnythingLLM raw-text/API ergonomics. |
| ingestion | Corpus ingestion and source registry | Build first-party parser completion, chunk accounting, and source-id registry; reuse AnythingLLM API shape where it fits. |
| retrieval | Retrieval, ranking, and citation assembly | Build first-party retrieval with pre-rank and post-rank policy checks; no framework retrieval ACL is a donor. |
| generation | Retrieval, ranking, and citation assembly; Public API and OpenAI-compatible surface | Build first-party answer assembly, refusal behavior, confidence, citations, and trace_id response semantics. |
| tool-mcp | MCP and tool gateway | Extract Flowise and AnythingLLM MCP hardening patterns, but keep source constraints and tool-permission checks first-party. |
| observability | Observability, prompts, and eval datasets | Extract Langfuse-compatible traces, observations, prompt versions, scores, datasets, and trace-to-dataset linkage. |
| authz | Relationship authorization (ReBAC); Contextual policy and obligations | Extract OpenFGA for relationship tuples and OPA-style policy obligations; wire both through first-party retrieval/API/tool paths. |
| eval | Evaluation and release scoring | Extract DeepEval span metrics and use Ragas only as raw metric producer behind a first-party zero-fill normalizer. |

## Donor Decisions

| Donor | Use | Evidence link |
| --- | --- | --- |
| Flowise | CLI/route packaging, API organization, hosted/custom MCP hardening patterns. | `docs/ekb-research/dossiers/flowise.md`, `docs/ekb-research/findings/ledger.md` F-FLOWISE-004 |
| AnythingLLM | Developer API ergonomics, OpenAI-compatible workspace-as-model shape, raw-text ingestion shape, MCP-to-agent adapter pattern. | `docs/ekb-research/dossiers/anythingllm.md`, `docs/ekb-research/findings/ledger.md` F-ANYTHINGLLM-004 |
| OpenFGA | Relationship tuple/check model for ReBAC. | `docs/ekb-research/subsystems/authz.md`, `docs/ekb-research/findings/ledger.md` F-AUTHZ-001 |
| OPA | Contextual ABAC/deny/obligation policy and decision logging pattern. | `docs/ekb-research/subsystems/authz.md`, `docs/ekb-research/findings/ledger.md` F-AUTHZ-002 |
| Langfuse | Trace, prompt-version, score, dataset, and trace-to-dataset plumbing. | `docs/ekb-research/subsystems/obs-eval.md`, `docs/ekb-research/findings/ledger.md` F-OBS-001 |
| DeepEval | Span-level retriever/generator CI metrics. | `docs/ekb-research/subsystems/obs-eval.md`, `docs/ekb-research/findings/ledger.md` F-OBS-003 |
| Ragas | Raw metric producer only; do not trust direct aggregation for release gates. | `docs/ekb-research/subsystems/obs-eval.md`, `docs/ekb-research/findings/ledger.md` F-OBS-002 |

Rejected or limited donor use:

| Framework | Boundary |
| --- | --- |
| RAGFlow | Useful parser/retrieval reference, but benchmark ACL and no-answer/tool maturity were source-gate scoped. |
| Dify | Useful app and tracing reference, but self-hosted RBAC and benchmark principal ACL were not proven. |
| WeKnora | Useful tenant/API-key and MCP management reference, but MCP search lacked source constraints. |
| MaxKB | Useful workspace/resource permission reference, but live benchmark used source gates and did not prove MCP/tool path. |
| Open WebUI | Useful group/resource ACL and permission-preview reference, but live tool behavior was scored ZERO. |

## Contract Coverage

| Contract | Responsibility |
| --- | --- |
| `docs/ekb-research/contracts/schema.sql` | Tenant-owned control plane, RLS, documents/chunks/indexes, grants, policies, audit, traces, tool calls, eval state. |
| `docs/ekb-research/contracts/authz.fga` | Relationship model for tenants, workspaces, groups, KBs, documents, and tools. |
| `docs/ekb-research/contracts/openapi.yaml` | REST API for tenants, workspaces, KBs, documents, sync, query/query-stream, traces, evals, tools, and audit. |
| `docs/ekb-research/contracts/mcp-tools.md` | MCP tool surface with scopes, risk, side effects, approval semantics, trace/audit, and A1/A2 no-bypass rules. |

## Open Questions And Known Gaps

These gaps are carried forward from `docs/ekb-research/wiring-audit.md`.

| Gap | Impact |
| --- | --- |
| No executable restricted-clearance policy artifact. | P4 is only partially covered: schema/authz provide metadata and OPA delegation hooks, but no Rego or equivalent `restricted_hr` policy exists. |
| No explicit language contract. | M1/M2 are only partially covered: OpenAPI/schema accept multilingual text and metadata, but there is no required language detection, language tag, or same-language answer behavior. |
| No explicit no-answer/refusal schema. | N1/N3 are only partially covered: `answer` and `confidence` exist, but there is no refusal reason enum or anti-fabrication rule in the contracts. |
| No runtime service wiring. | CP16-CP21 do not prove header-to-RLS propagation, OpenFGA/OPA calls, retrieval pre/post filters, MCP execution, or revoked-index enforcement in a running service. |

Follow-on harness work should implement the service and tests that close these
gaps. This harness intentionally stops before that implementation phase.
