# Observability And Evaluation Stack Audit

Status: CP14 static code-audit captured
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Scope | Langfuse, Ragas, and DeepEval observability/evaluation audit |
| Design anchors | `docs/enterprise-knowledge-base-design.md:776` through `docs/enterprise-knowledge-base-design.md:799`; `docs/enterprise-knowledge-base-design.md:829` through `docs/enterprise-knowledge-base-design.md:832`; `docs/enterprise-knowledge-base-design.md:913` through `docs/enterprise-knowledge-base-design.md:929` |
| Langfuse repo | https://github.com/langfuse/langfuse.git |
| Langfuse pinned SHA | 1a3aaee62946a4e4f10ed7327a7e9fab0f6a643b |
| Ragas repo | https://github.com/explodinggradients/ragas.git |
| Ragas pinned SHA | 298b68274234c060deacab3cf5fb52aa3a20e885 |
| DeepEval repo | https://github.com/confident-ai/deepeval.git |
| DeepEval pinned SHA | 8ebfa33d78db4cf81c0ae340b1a925e5406469c8 |
| Phoenix status | Not audited in CP14 because the acceptance criterion allows Langfuse and/or Phoenix; Langfuse was selected as the observability representative. |

## Design Mapping

| Design need | Source lines | Audit interpretation |
| --- | --- | --- |
| Offline RAG metrics | `docs/enterprise-knowledge-base-design.md:776` through `docs/enterprise-knowledge-base-design.md:799` | Needs retriever context precision/recall and generator faithfulness/factuality metrics. |
| Missing dimensions | `docs/enterprise-knowledge-base-design.md:829` through `docs/enterprise-knowledge-base-design.md:832` | Missing metric dimensions must become 0, never ignored, skipped, or averaged away. |
| Trace payload | `docs/enterprise-knowledge-base-design.md:913` through `docs/enterprise-knowledge-base-design.md:929` | Each answer trace needs tenant/workspace/principal, prompt/model/retriever/index/policy versions, chunks, context, answer, citations, cost, latency, tools, and labels. |
| Eval data model | `docs/enterprise-knowledge-base-design.md:342` through `docs/enterprise-knowledge-base-design.md:352` | Trace IDs must link messages, retrieval events, answer events, tool calls, eval datasets, eval cases, runs, and scores. |

## Comparison

| Tool | Best fit | Trace/span support | Prompt/dataset support | Metric support | Missing-dimension ZERO | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| Langfuse | Trace store and eval workbench | Strong for API ingestion of traces, observations, scores, and dataset run items. | Strong for prompt lookup by name/version and dataset run item enrichment. | Stores scores and datasets, but does not define RAG metric semantics. | Does not enforce; it records what callers send. | Use as observability store and trace-to-eval workbench, with EKB-owned zero-fill scoring. |
| Ragas | RAG metric vocabulary | Integrates with tracing, but CP14 treated it as metric library. | Not primary prompt/dataset system. | Strong for context precision, context recall, and faithfulness. | Does not enforce; some metrics return `np.nan` and aggregation uses `np.nanmean`. | Reuse metric implementations, but normalize missing/NaN dimensions to 0 before aggregation. |
| DeepEval | CI and span-level evaluation | Strong for trace, LLM span, retriever span, tool span, and attached metrics. | Supports prompts in spans and datasets through goldens/test runs. | Strong for contextual precision and faithfulness with strict thresholds. | Does not fully enforce; missing params can be skipped and score/success `None` is counted as error, not 0. | Use for span-level CI gates only behind an EKB wrapper that fails or zero-fills missing dimensions. |

## Langfuse Audit

Verdict: strongest donor for observability storage, prompt version linkage, and
trace-to-dataset workflow.

Evidence:

- The public ingestion API authenticates project-scoped ingestion keys, validates batch shape, rate-limits, and passes events to `processEventBatch`: `.harness/ekb-research/workspace/langfuse/web/src/pages/api/public/ingestion.ts:79` through `.harness/ekb-research/workspace/langfuse/web/src/pages/api/public/ingestion.ts:162`
- `processEventBatch` records ingestion counts and project/org span attributes, validates event schemas, authorizes events, sorts and groups the batch for async processing: `.harness/ekb-research/workspace/langfuse/packages/shared/src/server/ingestion/processEventBatch.ts:113` through `.harness/ekb-research/workspace/langfuse/packages/shared/src/server/ingestion/processEventBatch.ts:197`
- The worker merge path dispatches `trace`, `observation`, `score`, and `dataset_run_item` event types to dedicated processors: `.harness/ekb-research/workspace/langfuse/worker/src/services/IngestionService/index.ts:149` through `.harness/ekb-research/workspace/langfuse/worker/src/services/IngestionService/index.ts:194`
- Event records preserve `trace_id`, `span_id`, `parent_span_id`, prompt name/version/id, model, input/output, usage, cost, tool calls, experiment dataset id, experiment item id, and experiment item root span id: `.harness/ekb-research/workspace/langfuse/worker/src/services/IngestionService/index.ts:226` through `.harness/ekb-research/workspace/langfuse/worker/src/services/IngestionService/index.ts:380`
- Dataset run item processing joins run data and dataset item data, then writes `dataset_run_id`, `dataset_item_id`, `dataset_id`, `trace_id`, `observation_id`, input, expected output, metadata, and version into ClickHouse: `.harness/ekb-research/workspace/langfuse/worker/src/services/IngestionService/index.ts:396` through `.harness/ekb-research/workspace/langfuse/worker/src/services/IngestionService/index.ts:488`
- PromptService resolves prompts by project, name, explicit version or label, and caches by prompt name plus version/label: `.harness/ekb-research/workspace/langfuse/packages/shared/src/server/services/PromptService/index.ts:49` through `.harness/ekb-research/workspace/langfuse/packages/shared/src/server/services/PromptService/index.ts:130`, and `.harness/ekb-research/workspace/langfuse/packages/shared/src/server/services/PromptService/index.ts:194` through `.harness/ekb-research/workspace/langfuse/packages/shared/src/server/services/PromptService/index.ts:207`

Mapping:

- EKB `trace_id` propagation maps to Langfuse `trace_id` on observations, scores,
  and dataset run items.
- EKB prompt-version requirements map to Langfuse prompt name/version lookup and
  event-record prompt fields.
- EKB trace-to-eval conversion maps to dataset run item events that link dataset
  item input/expected output to trace and observation IDs.

Missing-dimension rule:

- Langfuse does not compute the full EKB score vector. It can store score events
  and dataset run items, but it does not make missing judge dimensions equal 0.
  The EKB eval runner must emit explicit zero-valued dimensions before sending
  scores or summaries to Langfuse.

Finding: F-OBS-001

## Ragas Audit

Verdict: useful metric donor, but unsafe as the final aggregator without a
zero-fill wrapper.

Evidence:

- Default `evaluate()` imports answer relevancy, context precision, faithfulness, and context recall when metrics are not supplied: `.harness/ekb-research/workspace/ragas/src/ragas/evaluation.py:137` through `.harness/ekb-research/workspace/ragas/src/ragas/evaluation.py:144`
- Context precision evaluates each retrieved context, ensembles binary verdicts, and computes average precision: `.harness/ekb-research/workspace/ragas/src/ragas/metrics/_context_precision.py:82` through `.harness/ekb-research/workspace/ragas/src/ragas/metrics/_context_precision.py:170`
- ID-based context precision compares retrieved context IDs with reference context IDs, but returns `np.nan` when no retrieved IDs are available: `.harness/ekb-research/workspace/ragas/src/ragas/metrics/_context_precision.py:251` through `.harness/ekb-research/workspace/ragas/src/ragas/metrics/_context_precision.py:307`
- Context recall classifies answer statements as attributable to retrieved context and computes attributed/total; ID-based recall compares reference IDs to retrieved IDs and returns `np.nan` when no references are present: `.harness/ekb-research/workspace/ragas/src/ragas/metrics/_context_recall.py:88` through `.harness/ekb-research/workspace/ragas/src/ragas/metrics/_context_recall.py:156`, and `.harness/ekb-research/workspace/ragas/src/ragas/metrics/_context_recall.py:227` through `.harness/ekb-research/workspace/ragas/src/ragas/metrics/_context_recall.py:279`
- Faithfulness generates answer statements, checks them against retrieved contexts, and computes faithful statements over total statements, but returns `np.nan` when no statements are generated: `.harness/ekb-research/workspace/ragas/src/ragas/metrics/_faithfulness.py:133` through `.harness/ekb-research/workspace/ragas/src/ragas/metrics/_faithfulness.py:214`
- EvaluationResult summarizes metric columns through `safe_nanmean`, and `safe_nanmean` uses `np.nanmean`, which ignores missing/NaN values when at least one value exists: `.harness/ekb-research/workspace/ragas/src/ragas/dataset_schema.py:436` through `.harness/ekb-research/workspace/ragas/src/ragas/dataset_schema.py:449`, and `.harness/ekb-research/workspace/ragas/src/ragas/utils.py:46` through `.harness/ekb-research/workspace/ragas/src/ragas/utils.py:55`

Missing-dimension rule:

- Ragas fails the EKB final-scoring rule if used directly for aggregation,
  because `np.nan` can be ignored instead of converted to 0. Ragas metrics can be
  used as raw metric producers only if the EKB runner converts absent, failed, or
  `NaN` dimensions to explicit zero before averaging.

Finding: F-OBS-002

## DeepEval Audit

Verdict: strong donor for CI-friendly and span-level evaluation, but missing
parameter behavior must be wrapped.

Evidence:

- Trace/span types include base spans with `trace_uuid`, parent UUID, input, output, metrics, metric collection, retrieval context, expected output, tools, LLM spans with prompt alias/version/commit hash, and retriever spans with embedder/top-k/chunk size: `.harness/ekb-research/workspace/deepeval/deepeval/tracing/types.py:87` through `.harness/ekb-research/workspace/deepeval/deepeval/tracing/types.py:175`
- Trace-scope execution walks live spans, separates LLM and retriever spans, builds an LLMTestCase from span input/output/retrieval context, executes each attached metric, and writes metric data back to the API span: `.harness/ekb-research/workspace/deepeval/deepeval/evaluate/execute/trace_scope.py:160` through `.harness/ekb-research/workspace/deepeval/deepeval/evaluate/execute/trace_scope.py:245`
- Trace-level metrics are also executed against the trace test case and attached to trace API metric data: `.harness/ekb-research/workspace/deepeval/deepeval/evaluate/execute/trace_scope.py:250` through `.harness/ekb-research/workspace/deepeval/deepeval/evaluate/execute/trace_scope.py:305`
- ContextualPrecisionMetric requires input, retrieval context, and expected output; strict mode sets threshold to 1, success is `score >= threshold`, and scores below threshold become 0 in strict mode: `.harness/ekb-research/workspace/deepeval/deepeval/metrics/contextual_precision/contextual_precision.py:45` through `.harness/ekb-research/workspace/deepeval/deepeval/metrics/contextual_precision/contextual_precision.py:67`, and `.harness/ekb-research/workspace/deepeval/deepeval/metrics/contextual_precision/contextual_precision.py:330` through `.harness/ekb-research/workspace/deepeval/deepeval/metrics/contextual_precision/contextual_precision.py:364`
- FaithfulnessMetric requires input, actual output, and retrieval context; strict mode sets threshold to 1, computes supported claims over total verdicts, and zeroes scores below threshold in strict mode: `.harness/ekb-research/workspace/deepeval/deepeval/metrics/faithfulness/faithfulness.py:51` through `.harness/ekb-research/workspace/deepeval/deepeval/metrics/faithfulness/faithfulness.py:80`, and `.harness/ekb-research/workspace/deepeval/deepeval/metrics/faithfulness/faithfulness.py:375` through `.harness/ekb-research/workspace/deepeval/deepeval/metrics/faithfulness/faithfulness.py:402`
- Missing required params can be skipped when `skip_on_missing_params` is enabled, setting score/success to no metric result; aggregate construction counts score/success `None` as error, not as zero: `.harness/ekb-research/workspace/deepeval/deepeval/evaluate/execute/_common.py:243` through `.harness/ekb-research/workspace/deepeval/deepeval/evaluate/execute/_common.py:295`, and `.harness/ekb-research/workspace/deepeval/deepeval/test_run/test_run.py:240` through `.harness/ekb-research/workspace/deepeval/deepeval/test_run/test_run.py:325`

Missing-dimension rule:

- DeepEval strict mode is useful for pass/fail gates, but it is not the full EKB
  missing-dimension contract. EKB must disable skip-on-missing for release gates
  or post-process skipped/error metrics into explicit zero-valued dimensions.

Findings: F-OBS-003, F-OBS-004

## Recommendation For Contracts

| Contract area | Recommendation | Findings |
| --- | --- | --- |
| Trace store | Use Langfuse-compatible trace/span and dataset run item export, preserving `trace_id` into eval cases and score rows. | F-OBS-001 |
| Metric producers | Use Ragas for raw context precision, context recall, and faithfulness, but never use its aggregate output as the final EKB score without zero-fill. | F-OBS-002 |
| Span-level gates | Use DeepEval for retriever/generator span-level CI gates with strict thresholds where appropriate. | F-OBS-003 |
| Zero contract | Add an EKB-owned score normalizer: expected dimension list in, raw metric results out, missing/NaN/skipped/error dimensions become 0 before averaging. | F-OBS-002, F-OBS-004 |

## Findings Summary

| finding_id | Summary |
| --- | --- |
| F-OBS-001 | Langfuse is the trace, prompt-version, and dataset-run donor, but not the final scorer. |
| F-OBS-002 | Ragas supplies core RAG metrics, but direct aggregation can ignore NaN instead of scoring missing dimensions as 0. |
| F-OBS-003 | DeepEval supplies span-level retriever/generator metrics and strict thresholds. |
| F-OBS-004 | DeepEval/Ragas need an EKB-owned zero-fill normalizer before release scoring. |
