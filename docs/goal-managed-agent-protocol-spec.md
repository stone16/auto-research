# Goal-Managed Agent Protocol Spec

## Purpose

This document turns the framework sketch into implementation-facing contracts.

The intent is not to freeze every storage or API detail.

The intent is to define:

- the owned object model,
- the runtime object model,
- the state transitions that matter,
- the event schema that acts as system truth,
- the subagent protocol,
- and the hook semantics that keep execution governable.

## Design Scope

This spec assumes:

- local-first execution,
- agent runtimes behind adapters,
- a goal-first control plane,
- evidence-backed completion,
- and typed governance surfaces.

This spec does not assume:

- dependence on a third-party orchestration framework,
- transcripts as source of truth,
- or full autonomy without human escalation.

## Object Model

### Owned objects

These are persisted control-plane objects.

```ts
type Goal = {
  id: string;
  title: string;
  status: "draft" | "active" | "completed" | "cancelled";
  owner_id: string;
  active_cycle_id?: string;
  linked_insight_ids: string[];
  created_at: string;
  updated_at: string;
};

type Cycle = {
  id: string;
  goal_id: string;
  kind: "weekly" | "sprint" | "monthly" | "quarterly" | "custom";
  starts_at: string;
  ends_at: string;
  checkpoint_dates: string[];
  review_cadence_id: string;
};

type ReviewCadence = {
  id: string;
  cycle_id: string;
  checkin_frequency: "daily" | "weekly" | "biweekly";
  owner_review_frequency: "weekly" | "monthly";
  escalation_sla_hours: number;
};

type Objective = {
  id: string;
  goal_id: string;
  title: string;
  description: string;
  status:
    | "draft"
    | "clarifying"
    | "planned"
    | "in_progress"
    | "blocked"
    | "verifying"
    | "completed"
    | "cancelled";
  progress_health: "unknown" | "off_track" | "at_risk" | "on_track" | "exceeded";
  version: number;
};

type KeyResult = {
  id: string;
  objective_id: string;
  parent_key_result_id?: string;
  title: string;
  specific: string;
  measurable_summary: string;
  attainable: string;
  relevant: string;
  time_bound: string;
  cycle_id?: string;
  review_cadence_id?: string;
  metric_ids: string[];
  baseline_ids: string[];
  target_ids: string[];
  leading_indicator_ids: string[];
  lagging_indicator_ids: string[];
  progress_health: "unknown" | "off_track" | "at_risk" | "on_track" | "exceeded";
  confidence_score: number;
  status:
    | "draft"
    | "proposed"
    | "approved"
    | "ready"
    | "running"
    | "blocked"
    | "verifying"
    | "done"
    | "failed"
    | "superseded";
  dependency_ids: string[];
  budget_policy_id?: string;
  notification_route_id?: string;
  evidence_contract_id?: string;
  version: number;
};

type MetricDefinition = {
  id: string;
  key_result_id: string;
  name: string;
  unit: "count" | "percent" | "currency" | "duration" | "score" | "custom";
  aggregation: "latest" | "sum" | "avg" | "p50" | "p95" | "ratio";
  direction: "higher_is_better" | "lower_is_better" | "range";
  leading_or_lagging: "leading" | "lagging";
  source_of_truth: string;
};

type Baseline = {
  id: string;
  metric_id: string;
  value: number;
  recorded_at: string;
  provenance: string;
};

type Target = {
  id: string;
  metric_id: string;
  target_value: number;
  due_at: string;
  tolerance?: number;
};

type MetricObservation = {
  id: string;
  metric_id: string;
  value: number;
  observed_at: string;
  source_ref: string;
  confidence: number;
};

type ForecastUpdate = {
  id: string;
  key_result_id: string;
  forecast_value: number;
  on_track: boolean;
  confidence_score: number;
  rationale: string;
  updated_at: string;
};

type EvidenceCheck = {
  id: string;
  key_result_id: string;
  type: "test" | "artifact" | "benchmark" | "human_review" | "policy_review";
  required: boolean;
  status: "pending" | "running" | "passed" | "failed" | "waived";
};

type DecisionRecord = {
  id: string;
  object_type: string;
  object_id: string;
  decision_type: string;
  actor_type: "user" | "agent" | "policy" | "system";
  actor_id: string;
  rationale: string;
  created_at: string;
};

type KnowledgeArtifact = {
  id: string;
  kind: "decision" | "playbook" | "postmortem" | "evidence_pack" | "metric_definition";
  source_goal_id: string;
  source_objective_id?: string;
  title: string;
  uri: string;
};

type Insight = {
  id: string;
  source_goal_id: string;
  statement: string;
  confidence: number;
  artifact_ids: string[];
};

type CrossGoalLink = {
  id: string;
  from_goal_id: string;
  to_goal_id: string;
  relation: "contributes_to" | "reuses" | "blocks" | "learned_from";
  evidence_ref?: string;
};

type BudgetPolicy = {
  id: string;
  scope: "goal" | "objective" | "key_result" | "workspace";
  scope_id: string;
  max_total_cost_usd?: number;
  max_cost_per_run_usd?: number;
  max_daily_cost_usd?: number;
  hard_stop: boolean;
};

type CostLedgerEntry = {
  id: string;
  scope_id: string;
  key_result_id?: string;
  task_execution_id?: string;
  cost_type: "model_tokens" | "tool_usage" | "workspace_runtime" | "human_review";
  amount_usd: number;
  quantity: number;
  recorded_at: string;
  provenance: string;
};

type NotificationRoute = {
  id: string;
  scope: "goal" | "objective" | "key_result" | "approval_request";
  scope_id: string;
  channels: Array<"ui" | "email" | "chat" | "push" | "webhook">;
  escalation_sla_hours: number;
  on_call_ref?: string;
};

type EscalationRoute = {
  id: string;
  notification_route_id: string;
  escalation_target: string;
  triggers_after_hours: number;
};

type EvalDataset = {
  id: string;
  name: string;
  version: string;
  case_ids: string[];
};

type HeldOutEvalSet = {
  id: string;
  dataset_id: string;
  purpose: "anti_gaming" | "release_gate" | "calibration";
  case_ids: string[];
};

type JudgeRotationPolicy = {
  id: string;
  enabled: boolean;
  primary_judges: string[];
  secondary_judges: string[];
  rotation_mode: "round_robin" | "randomized" | "disagreement_triggered";
  pairwise_required: boolean;
};

type CalibrationRun = {
  id: string;
  judge_id: string;
  eval_dataset_id: string;
  sampled_case_ids: string[];
  agreement_with_human: number;
  false_positive_rate: number;
  false_negative_rate: number;
  completed_at: string;
};

type GraderTrustScore = {
  judge_id: string;
  trust_score: number;
  status: "healthy" | "watch" | "demoted" | "disabled";
  last_calibrated_at: string;
};
```

### Runtime objects

These are created to execute or govern work against the owned model.

```ts
type TaskExecution = {
  id: string;
  key_result_id: string;
  protocol_id: string;
  status:
    | "queued"
    | "starting"
    | "running"
    | "blocked"
    | "completed_claimed"
    | "failed"
    | "cancelled"
    | "orphaned";
  assignee_type: "agent" | "human";
  assignee_id?: string;
  workspace_lease_id?: string;
  objective_version_at_spawn: number;
  key_result_version_at_spawn: number;
};

type AgentSession = {
  id: string;
  task_execution_id: string;
  runtime_adapter: string;
  status:
    | "starting"
    | "running"
    | "waiting_input"
    | "stalled"
    | "disconnected"
    | "completed"
    | "failed";
  started_at: string;
};

type ApprovalRequest = {
  id: string;
  object_type: string;
  object_id: string;
  scope: {
    workspace_id?: string;
    repo?: string;
    branch?: string;
    path?: string;
    action: string;
  };
  status: "pending" | "approved" | "denied" | "expired" | "superseded";
  reason_code: string;
  expires_at?: string;
};

type WorkspaceLease = {
  id: string;
  workspace_ref: string;
  mode: "shared" | "isolated" | "worktree" | "remote";
  status: "active" | "expired" | "released" | "invalid";
  holder_type: "task_execution" | "agent_session";
  holder_id: string;
};

type ExternalAction = {
  id: string;
  task_execution_id: string;
  action_type: "pr_comment" | "email" | "payment" | "ticket_update" | "deployment";
  status: "planned" | "dry_run_ready" | "awaiting_approval" | "committed" | "reversed" | "failed";
  dry_run_ref?: string;
  receipt_ref?: string;
  reversal_policy: "reversible" | "manual_reversal" | "irreversible";
};
```

## Ownership Rules

1. `Goal`, `Objective`, and `KeyResult` express intent.
2. `Cycle`, `MetricDefinition`, `Baseline`, `Target`, and `ForecastUpdate` express measurable progress.
3. `KnowledgeArtifact`, `Insight`, and `CrossGoalLink` express reusable learning across goals.
4. `BudgetPolicy`, `NotificationRoute`, and `JudgeRotationPolicy` are governance assets, not runtime side-effects.
5. `TaskExecution` exists only to satisfy a `KeyResult`.
6. `AgentSession` exists only to satisfy a `TaskExecution`.
7. `ApprovalRequest`, `CostLedgerEntry`, and `ExternalAction` may outlive a session, but never outlive their owning objective indefinitely.
8. `CalibrationRun` and `GraderTrustScore` are part of evaluator governance, not ad hoc operations metadata.
9. Transcripts may be stored, but they are never the primary state container.

## State Transition Rules

### Objective

- `draft -> clarifying`
- `clarifying -> planned`
- `planned -> in_progress`
- `in_progress -> blocked`
- `in_progress -> verifying`
- `verifying -> completed`
- `verifying -> in_progress`
- `* -> cancelled`

Rule:

- `Objective.completed` requires all required `KeyResult` objects to be `done`.

### KeyResult

- `draft -> proposed`
- `proposed -> approved`
- `approved -> ready`
- `ready -> running`
- `running -> blocked`
- `running -> verifying`
- `verifying -> done`
- `verifying -> failed`
- `* -> superseded`

Rules:

- only `approved` KRs may create `TaskExecution` records,
- `approved` KRs should normally carry cycle, metric, baseline, target, budget, and notification bindings before execution,
- only `verifying` KRs may be closed,
- and `superseded` is terminal for planning, but not for audit.

### KeyResult progress health

- `unknown -> off_track`
- `unknown -> on_track`
- `off_track -> at_risk`
- `at_risk -> on_track`
- `on_track -> exceeded`
- `* -> off_track`

Rule:

- progress health is orthogonal to lifecycle state.

### TaskExecution

- `queued -> starting`
- `starting -> running`
- `running -> blocked`
- `running -> completed_claimed`
- `running -> failed`
- `blocked -> running`
- `blocked -> cancelled`
- `completed_claimed -> orphaned`

Rules:

- `completed_claimed` is not accepted completion,
- `orphaned` means the result arrived after parent state moved on,
- and a task may not re-enter `running` after `failed`, `cancelled`, or `orphaned`.

### ExternalAction

- `planned -> dry_run_ready`
- `planned -> awaiting_approval`
- `dry_run_ready -> awaiting_approval`
- `awaiting_approval -> committed`
- `committed -> reversed`
- `* -> failed`

Rules:

- irreversible actions require explicit approval,
- committed actions should capture a receipt,
- and reversal semantics must be declared before commit.

## Event Log Schema

The append-only event log is the system of record for lifecycle behavior.

```ts
type EventEnvelope = {
  event_id: string;
  event_type: string;
  object_type: string;
  object_id: string;
  run_id?: string;
  causation_id?: string;
  correlation_id?: string;
  dedupe_key: string;
  actor: {
    type: "user" | "agent" | "system" | "policy" | "hook";
    id: string;
  };
  occurred_at: string;
  payload: Record<string, unknown>;
};
```

Minimum event families that must exist in addition to execution lifecycle events:

- `MetricObserved`
- `ForecastUpdated`
- `CheckpointDue`
- `CheckpointReviewed`
- `SpendRecorded`
- `BudgetThresholdCrossed`
- `BudgetExhausted`
- `NotificationRaised`
- `NotificationEscalated`
- `ExternalActionDryRunPrepared`
- `ExternalActionCommitted`
- `ExternalActionReceiptAttached`
- `CalibrationCompleted`
- `JudgeAssigned`
- `JudgeDemoted`

Protocol rules:

- cost and budget events are not optional telemetry; they can change control flow
- notification events are part of the truth model for `blocked_on_user`
- calibration and judge-assignment events are required to audit evaluator authority
- external action events must make irreversible side effects replay-visible even when reversal is impossible

Required event properties:

- every external side effect must emit an event,
- every resumable action must carry `correlation_id`,
- every retryable action must keep a stable `dedupe_key`,
- and every UI view must be reconstructable from objects plus events.

## Subagent Protocol

### Spawn request

```ts
type SpawnRequest = {
  protocol_id: string;
  task_execution_id: string;
  mode: "fork" | "fresh" | "worktree" | "remote" | "teammate";
  context_contract: ContextContract;
  capability_profile: string[];
  communication_contract: {
    channels: Array<"notification" | "message" | "approval" | "resume" | "event_stream">;
  };
  lifecycle_policy: {
    timeout_seconds?: number;
    max_retries?: number;
    stall_policy: "block" | "cancel" | "escalate";
    orphan_policy: "ignore" | "record" | "require_review";
  };
};
```

### Protocol actions

- `spawn`
- `ack`
- `block`
- `resume`
- `complete`
- `cancel`

### Protocol invariants

1. `protocol_id` is stable for the lifetime of the child execution.
2. `ack` must be emitted before the child is considered live.
3. `block` must include a structured reason and requested resolution.
4. `complete` is a completion claim only.
5. `resume` is valid only for blocked or disconnected child state.
6. `cancel` must be idempotent.
7. A late `complete` after KR supersession becomes an `orphaned` result.

## Hook Execution Model

### Registration

```ts
type HookRegistration = {
  id: string;
  scope: "session" | "agent" | "workflow" | "runtime" | "evaluator";
  event: string;
  order: number;
  timeout_ms: number;
  failure_policy: "fail_closed" | "fail_open" | "retry_once";
  mode: "sync" | "async";
  input_schema_ref: string;
  output_schema_ref: string;
};
```

### Allowed outputs

- `approve`
- `block`
- `updated_input`
- `additional_context`
- `updated_output`
- `retry`
- `escalation_request`
- `stop_continuation`

### Merge and precedence rules

1. Hooks execute in deterministic order within the same scope.
2. Narrower scope wins over broader scope when policies conflict.
3. `block` overrides `approve`.
4. `stop_continuation` is terminal for that lifecycle boundary.
5. `updated_input` is valid only before execution starts.
6. `updated_output` is valid only after a tool/runtime response exists.
7. Retries consume explicit retry budget and must emit an event.

## Failure Handling Rules

### Stale context

If the parent `Objective` or `KeyResult` version changes after spawn:

- mark the `TaskExecution` as `stale_context`,
- prevent auto-merge of child output,
- require revalidation before completion acceptance.

### Duplicate events

If the same `block` or `complete` is received twice:

- accept the first transition,
- record later duplicates,
- do not replay side effects.

### Late approvals

If approval arrives after timeout:

- keep the decision record,
- but require explicit reattachment to current state before resuming work.

### Evaluator disagreement

If automated evaluators pass but human review fails:

- keep the KR in `verifying` or move it to `failed`,
- never auto-close based on machine success alone.

### Restart recovery

If the daemon or runtime restarts:

- reconstruct work from objects plus event log,
- do not infer state from transcript tailing,
- and fail closed if lease or protocol state cannot be safely revalidated.

## UI Data Contracts

The UI should render structured state, not ad hoc log parsing.

### Plan preview

- objective summary
- KR list
- SMART gaps
- dependency warnings
- expected permissions
- expected evidence

### Approval inbox item

- request summary
- scope
- reason code
- requested action
- expiry
- related objective / KR / task execution

### Evidence review bundle

- KR summary
- completion claim
- evaluator outcomes
- artifacts
- decision history

### Session detail view

- task execution state
- agent session state
- current block reason
- recent events
- workspace lease status

## Implementation Order

1. Persist the owned object model and event log.
2. Implement objective/KR planning and approval transitions.
3. Implement `TaskExecution` plus `SubagentProtocol`.
4. Implement approval handling and workspace leases.
5. Implement evaluator registry.
6. Implement hook registry with deterministic semantics.
7. Build operator views from object and event contracts.
