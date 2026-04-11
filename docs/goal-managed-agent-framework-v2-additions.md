# Goal-Managed Agent Framework v2 Additions

## Purpose

This document patches the current framework sketch where it is still too close to a governed task runner and not yet fully qualified as a goal-managed dashboard.

The three highest-priority additions are:

1. a progress and measurement model
2. cost and budget primitives in the governance layer
3. calibration and judge-rotation objects in the evaluation layer

These are the minimum changes required to move from:

- "goal-shaped task orchestration"

to:

- "a governed OKR and execution control plane with a real dashboard"

## Accepted Diagnosis

The current framework already gets several hard things right:

- owned vs runtime object separation
- explicit state machines
- typed subagent context contracts
- hooks as lifecycle-scoped control surfaces
- evaluation as a first-class layer
- a testing strategy that rejects "just use another model as the judge"

The biggest remaining weakness is that the framework still treats `KeyResult` as too binary.

Without explicit progress, cadence, budget, and calibration objects, it risks collapsing back into a sophisticated task tracker.

## Patch Map

This draft extends the existing sections in [goal-managed-agent-framework.md](/Users/stometa/dev/auto-research/docs/goal-managed-agent-framework.md):

- Goal Layer
- Planning Layer
- Governance Layer
- Evaluation Layer
- Operator Layer
- System State Model

It does not replace the current spec. It adds missing framework commitments.

## Patch 1: Progress, Measurement, and Cycle Model

### Why

An OKR system is not defined by whether a KR is `done`.

It is defined by whether the system can answer:

- what the baseline was
- what the target is
- what the current value is
- whether confidence is rising or falling
- whether the team is ahead or behind forecast
- which signals are leading and which are lagging

Without this layer, `KeyResult` is only a dressed-up task.

### New Objects

Add these owned objects:

- `Cycle`
- `ReviewCadence`
- `MetricDefinition`
- `MetricSeries`
- `MetricObservation`
- `Baseline`
- `Target`
- `ProgressSnapshot`
- `ForecastUpdate`
- `ConfidenceAssessment`
- `IndicatorDefinition`

Suggested shapes:

```ts
type Cycle = {
  id: string;
  goal_id: string;
  kind: "weekly" | "sprint" | "monthly" | "quarterly" | "custom";
  starts_at: string;
  ends_at: string;
  checkpoint_dates: string[];
  review_cadence_id: string;
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
  metric_id: string;
  value: number;
  recorded_at: string;
  provenance: string;
};

type Target = {
  metric_id: string;
  target_value: number;
  due_at: string;
  tolerance?: number;
};

type MetricObservation = {
  metric_id: string;
  value: number;
  observed_at: string;
  source_ref: string;
  confidence: number;
};

type ForecastUpdate = {
  key_result_id: string;
  forecast_value: number;
  on_track: boolean;
  confidence_score: number;
  rationale: string;
  updated_at: string;
};
```

### KeyResult Changes

Replace the current text-only `measurable` field as the main source of truth.

`KeyResult` should keep a human-readable statement, but it also needs structured measurement references:

```ts
type KeyResult = {
  id: string;
  objective_id: string;
  title: string;
  measurable_summary: string;
  metric_ids: string[];
  cycle_id: string;
  baseline_ids: string[];
  target_ids: string[];
  current_progress_status: "off_track" | "at_risk" | "on_track" | "exceeded";
  current_confidence_score: number;
};
```

### Review and Cadence Objects

Time must become an explicit planning primitive, not a free-text deadline.

Add:

```ts
type ReviewCadence = {
  id: string;
  cycle_id: string;
  checkin_frequency: "daily" | "weekly" | "biweekly";
  owner_review_frequency: "weekly" | "monthly";
  escalation_sla_hours: number;
};

type CheckpointReview = {
  id: string;
  key_result_id: string;
  checkpoint_at: string;
  summary: string;
  progress_delta: number;
  confidence_delta: number;
  decision: "stay_course" | "replan" | "de-scope" | "escalate";
};
```

### State Model Changes

The current KR states are operationally useful, but too binary for OKR management.

Keep the execution states, but add progress health as a parallel dimension:

- lifecycle state: `draft -> approved -> running -> blocked -> verifying -> done`
- progress health: `unknown -> off_track -> at_risk -> on_track -> exceeded`

Spec rule:

- a KR may be `running` and still be `off_track`
- a KR may be `blocked` but still have improving leading indicators
- completion is terminal for lifecycle, not for forecasting history

### Operator Layer Changes

The dashboard cannot just show queues and approvals.

It needs composition primitives:

- `KRProgressCard`
- `KPIChart`
- `TrendLine`
- `ForecastBadge`
- `ConfidenceRibbon`
- `CycleCountdown`
- `BurndownView`
- `ReviewAgenda`

Minimum dashboard views:

1. Goal overview: objectives, KR health, cycle countdown
2. KR scorecard: baseline, target, current, forecast, confidence
3. Review agenda: what must be reviewed this week
4. Leading indicators view: early-warning metrics before hard failure

### Framework Rule

No `KeyResult` may enter `approved` without:

- a structured metric definition or a justified exception
- a baseline
- a target
- a cycle
- a review cadence

That is the threshold between "task planning" and "goal management."

## Patch 2: Cost and Budget Primitives in Governance

### Why

Permissions are not the only hard limit on unattended agents.

Cost is a first-class control surface:

- token spend
- model choice
- tool/API spend
- workspace minutes
- human-review cost

If the framework can block on path access but not on budget exhaustion, governance is incomplete.

### New Objects

Add these governance objects:

- `BudgetPolicy`
- `QuotaPool`
- `CostLedgerEntry`
- `CostAttribution`
- `SpendForecast`
- `BurnAlert`

Suggested shapes:

```ts
type BudgetPolicy = {
  id: string;
  scope: "goal" | "objective" | "key_result" | "workspace" | "org";
  scope_id: string;
  max_total_cost_usd?: number;
  max_cost_per_run_usd?: number;
  max_daily_cost_usd?: number;
  max_human_review_minutes?: number;
  hard_stop: boolean;
};

type CostLedgerEntry = {
  id: string;
  scope_id: string;
  key_result_id?: string;
  task_execution_id?: string;
  session_id?: string;
  cost_type: "model_tokens" | "tool_usage" | "human_review" | "workspace_runtime";
  amount_usd: number;
  quantity: number;
  recorded_at: string;
  provenance: string;
};

type CostAttribution = {
  key_result_id: string;
  direct_cost_usd: number;
  shared_cost_usd: number;
  cumulative_cost_usd: number;
  budget_remaining_usd?: number;
};
```

### Policy Engine Changes

`PolicyEngine` should not only answer `allow / ask / deny`.

It should answer:

- `allow`
- `ask`
- `deny`
- `budget_block`
- `budget_warn`

Spec rule:

- a request may be path-allowed but budget-denied
- a request may be permission-approved but still require human approval if it would cross a spend threshold
- every `ExecutionEnvelope` must carry a budget snapshot

### Runtime Changes

`RuntimeAdapter.start` and `RuntimeAdapter.resume` must report spend back into the ledger.

That means runtime events need explicit cost hooks:

- `SpendRecorded`
- `BudgetThresholdCrossed`
- `BudgetExhausted`

### Run Control Changes

The loop-level stop model should grow beyond iteration counts.

Add stop conditions such as:

- `max_total_cost_usd`
- `max_cost_per_iteration_usd`
- `max_consecutive_no_dimension_progress`
- `max_budget_burn_rate`

`max_consecutive_no_dimension_progress` matters because the live `v5` pattern already showed a judge-loop plateau where the system kept iterating without materially breaking through.

### Operator Layer Changes

The dashboard needs budget views:

- `BudgetBar`
- `SpendByKR`
- `CostTrend`
- `QuotaWarning`
- `BudgetBlockInbox`

Minimum budget questions the UI must answer:

1. what did this KR cost so far
2. what is forecast to finish
3. which model/tool is driving spend
4. which blocked tasks are blocked by authority vs budget

### Framework Rule

No unattended mode may be enabled without:

- an explicit `BudgetPolicy`
- cost attribution at least to the KR level
- visible cost alerts in the operator layer

## Patch 3: Calibration, Judge Rotation, and Anti-Gaming Objects

### Why

The testing strategy already says the right thing:

- do not trust one judge blindly
- use deterministic assertions first
- calibrate graders against human review
- protect against eval gaming

But today those are principles, not objects.

Without first-class calibration objects, anti-Goodhart behavior remains advisory text.

### New Objects

Add these evaluation objects:

- `EvalDataset`
- `HeldOutEvalSet`
- `JudgeAssignment`
- `CalibrationRun`
- `DisagreementCase`
- `GraderTrustScore`
- `JudgeRotationPolicy`
- `EvaluatorDemotionPolicy`

Suggested shapes:

```ts
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
  last_calibrated_at: string;
  status: "healthy" | "watch" | "demoted" | "disabled";
};
```

### Evaluation Flow Changes

The framework should support:

1. deterministic checks
2. pairwise LLM judgment
3. cross-family disagreement checks
4. held-out regression checks
5. human arbitration when disagreement crosses threshold

That implies explicit evaluation routing:

```ts
type EvaluationRoute = {
  deterministic_required: boolean;
  pairwise_judge_required: boolean;
  heldout_eval_required: boolean;
  human_review_threshold: number;
};
```

### Anti-Gaming Rules

Add framework commitments:

- keep at least one held-out eval set outside the producer loop
- rotate judges by policy, not ad hoc operator intuition
- log which judge evaluated which candidate
- track judge-human agreement over time
- demote a judge when calibration quality drops below threshold

### Pairwise Reviewer Generalization

The current pairwise upgrade in the live framework is directionally right.

The next step is to make it a formal object model:

- `PairwiseComparison`
- `JudgeAssignment`
- `ComparisonOutcome`
- `MergeableImprovement`
- `RegressionNotice`

This allows the system to say:

- candidate is not globally better
- but here are two local wins worth absorbing
- and here are the regressions to avoid reintroducing

That is a much stronger anti-Goodhart mechanism than scalar score alone.

### Operator Layer Changes

The operator UI needs evaluator health surfaces:

- `JudgeAgreementPanel`
- `CalibrationHistory`
- `HeldOutEvalHealth`
- `DisagreementQueue`
- `EvaluatorTrustBadge`

Minimum evaluator questions the UI must answer:

1. which judge scored this result
2. whether that judge is currently trusted
3. whether another judge disagreed
4. whether the result passed held-out checks
5. whether human review overruled the automated verdict

### Framework Rule

No judge may remain in automatic promotion authority indefinitely without:

- periodic `CalibrationRun`
- recorded `GraderTrustScore`
- a defined `EvaluatorDemotionPolicy`

## Other Accepted Gaps, Not Yet in the Top 3

These should remain in backlog, not be forgotten:

1. `NotificationChannel`, `EscalationRoute`, and after-hours routing for `blocked_on_user`
2. cross-goal knowledge objects such as `Insight`, `LessonLearned`, `KnowledgeArtifact`, and `CrossGoalLink`
3. dashboard composition objects beyond named surfaces
4. irreversible external action objects such as `ExternalAction`, `Receipt`, `DryRunMode`, and `ReversalPolicy`
5. cross-goal alignment edges such as `ContributesTo`

These are important. They are just not as foundational as measurement, budget, and calibration.

## Proposed Spec Commitments for v2

If the framework adopts only three new commitments in the next revision, they should be:

1. `KeyResult` must have structured measurement and cycle references
2. `PolicyEngine` must reason about spend as well as permission
3. `EvaluationLayer` must own calibration and judge-rotation objects

Those three changes would materially raise the ceiling of the whole framework.

## Recommendation

Do not fold these changes into the main spec piecemeal.

Use this document as the patch set for the next framework revision, then update:

- [goal-managed-agent-framework.md](/Users/stometa/dev/auto-research/docs/goal-managed-agent-framework.md)
- [goal-managed-agent-protocol-spec.md](/Users/stometa/dev/auto-research/docs/goal-managed-agent-protocol-spec.md)
- [goal-managed-agent-testing-strategy.md](/Users/stometa/dev/auto-research/docs/goal-managed-agent-testing-strategy.md)

in one coordinated pass so the object model, protocol, and assurance model stay aligned.
