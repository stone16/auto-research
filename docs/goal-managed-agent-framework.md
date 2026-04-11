# Goal-Managed Agent Framework

## Purpose

This document sketches a framework for goal-managed, local-first agent orchestration inspired by Claude Code and other relevant open-source systems, but not dependent on any of them.

The goal is not "make a smarter chat tool."

The goal is to build a governed execution framework where:

- a human manages objectives,
- the system turns those objectives into executable Key Results,
- agents execute bounded work,
- hooks and policies constrain uncertainty,
- evaluation decides whether work is actually done,
- and the whole system remains extensible without becoming opaque.

## Research Posture

We should read broadly and implement narrowly.

That means:

- study current open-source agent runtimes, orchestration engines, policy systems, and eval stacks,
- extract the mechanism each one gets right,
- write our own clear specs for the control plane,
- and build the core system ourselves end to end.

Non-goals:

- directly embedding an external agent framework as our product core,
- inheriting another project's object model just because it already exists,
- hiding design uncertainty behind vague "multi-agent" language,
- or letting transcript history become the de facto source of truth.

## Core Thesis

The hard problem is not spawning more agents.

The hard problem is building the control surfaces that make multi-agent execution legible, governable, resumable, and extensible.

Claude Code is useful not because it proves one perfect design, but because its source shows a set of solved problems:

- context inheritance is not naive,
- subagents are not all the same,
- agent communication is explicit,
- hooks sit on real lifecycle boundaries,
- and permissions are modeled as policy, not as one-time access grants.

Our framework should adopt those lessons as abstractions, not as literal product mimicry.

The standard is:

- learn from existing systems,
- explain why a mechanism exists,
- decide whether our scenario is the same,
- write the spec,
- then implement our own version.

## Design Questions

This framework must answer these questions explicitly:

1. How does a vague goal become executable work?
2. What is the unit of execution: objective, key result, or task?
3. How is child-agent context constructed?
4. What state is shared, cloned, or isolated?
5. How do parent and child agents communicate?
6. How do hooks constrain uncertain LLM behavior?
7. How do plugins extend behavior without mutating global system state?
8. How does the system prove completion rather than merely report it?
9. Which mechanisms should be borrowed conceptually, but reimplemented from scratch?
10. Which user scenarios break a seemingly elegant design?
11. How is KR progress measured over time rather than only marked done?
12. How are cycle, cadence, checkpoint review, and time pressure represented?
13. How does cost governance constrain autonomy alongside permission governance?
14. How does `blocked_on_user` become a real notification and escalation path?
15. How do insights and artifacts from one goal improve the next goal?
16. How do we stop judges and graders from becoming a hidden single point of failure?

## Framework Layers

### 1. Goal Layer

This layer owns intent.

Core objects:

- `Goal`
- `Objective`
- `KeyResult`
- `Cycle`
- `ReviewCadence`
- `MetricDefinition`
- `Baseline`
- `Target`
- `ProgressSnapshot`
- `ForecastUpdate`
- `ConfidenceAssessment`
- `EvidenceCheck`
- `KnowledgeArtifact`
- `Insight`
- `CrossGoalLink`
- `DecisionRecord`

Responsibilities:

- collect clarifications,
- define success,
- define baselines, targets, and review cadence,
- distinguish leading and lagging indicators,
- track progress and forecast risk over time,
- establish ownership,
- model dependencies,
- connect prior lessons and reusable artifacts across goals,
- decide which work is ready to run.

Planning note:

- `TaskExecution` is not a peer-level planning object. It is a runtime artifact created to satisfy a `KeyResult`.
- A KR is not approval-ready until it either has a structured measurement model and cycle, or a justified exception explaining why it is milestone-only.

### 2. Planning Layer

This layer converts ambiguous user intent into structured execution plans.

Core abstractions:

- `PlanningSession`
- `ClarificationPrompt`
- `PlanPreview`
- `MetricPlan`
- `CyclePlan`
- `ReviewAgenda`
- `DependencyGraph`
- `ForecastPreview`
- `ExecutionReadinessCheck`

Responsibilities:

- ask clarifying questions,
- draft SMART Key Results through progressive disclosure,
- turn "measurable" from prose into a structured baseline/target/current model,
- choose cycle length and checkpoint cadence,
- separate leading indicators from lagging outcome metrics,
- detect dependency spaghetti,
- preview likely permissions and evidence,
- preview likely cost and escalation pressure,
- import relevant prior insights instead of treating every goal as an island,
- require approval before execution.

Additional planning constraints:

- KRs must be independent by default and dependency-bearing only by explicit exception.
- A parent KR may become a child Objective, but recursive decomposition must be capped and visualized.
- The system should ask for clarifications before forcing SMART precision when the user's intent is still fluid.
- Every approved KR should bind to a cycle, review cadence, and at least one progress signal unless explicitly marked as a one-shot milestone.

### 3. Runtime Layer

This layer runs work.

Core abstractions:

- `RuntimeAdapter`
- `AgentSession`
- `WorkspaceLease`
- `SubagentProtocol`
- `ExternalActionHandle`
- `ResumeHandle`

Responsibilities:

- launch local CLIs or SDK-backed agents,
- create isolated workspaces when needed,
- monitor liveness,
- record cost and runtime usage back into the ledger,
- pause and resume sessions,
- prepare dry-runs for irreversible external actions,
- collect execution artifacts.

Runtime constraints:

- no hidden child sessions,
- no silent workspace mutation without a decision record,
- no irreversible external action without either a dry-run or an explicit reason why dry-run is impossible,
- and no parent-child coordination that depends on transcript polling alone.

### 4. Governance Layer

This layer constrains behavior.

Core abstractions:

- `PolicyEngine`
- `PermissionRule`
- `BudgetPolicy`
- `CostLedgerEntry`
- `ApprovalRequest`
- `NotificationRoute`
- `EscalationRoute`
- `ExternalActionPolicy`
- `ReversalPolicy`
- `DecisionRecord`
- `HookRegistry`

Responsibilities:

- apply `allow` / `ask` / `deny` policy,
- apply `budget_warn` / `budget_block` policy,
- scope authority by workspace, repo, path, branch, action, or tool,
- intercept lifecycle events,
- route blocked and approval-required work to the right human channel,
- constrain irreversible external actions,
- block unsafe continuation,
- record decision provenance.

Governance constraints:

- authority should degrade gracefully from broad allowlists to narrow exception requests,
- budget should degrade gracefully from soft warnings to hard blocks,
- denial history should inform future UX,
- `blocked_on_user` is not complete unless it is attached to a notification route and escalation SLA,
- and irreversible actions must capture intent, approval, receipt, and reversal policy where possible.
- and policy explanations must be user-readable rather than only machine-readable.

### 5. Evaluation Layer

This layer decides whether work is actually complete.

Core abstractions:

- `EvaluatorRegistry`
- `EvidenceContract`
- `EvalDataset`
- `HeldOutEvalSet`
- `JudgeAssignment`
- `JudgeRotationPolicy`
- `VerificationRun`
- `CalibrationRun`
- `GraderTrustScore`
- `EvaluatorDemotionPolicy`
- `CompletionDecision`

Responsibilities:

- run tests, benchmarks, diff checks, artifact checks, or human review,
- separate execution success from business completion,
- rotate and calibrate graders,
- protect against eval gaming and self-referential scoring loops,
- route failed work back into clarification, approval, or retry states.

Evaluation constraints:

- every completion claim must map to explicit evidence,
- evidence must be reviewable in the UI,
- no single judge should retain indefinite promotion authority without calibration,
- held-out regression checks must exist outside the producer loop,
- and a successful shell/tool run must never be treated as completion by itself.

### 6. Operator Layer

This layer is the product surface.

Core surfaces:

- goal conversation,
- goal scorecard dashboard,
- KR scorecard,
- review agenda,
- plan approval,
- task board,
- session detail,
- approval inbox,
- budget view,
- evidence review,
- policy panel,
- evaluator health panel,
- cross-goal knowledge panel.

Responsibilities:

- make the system understandable,
- make blocked work actionable,
- make progress, confidence, and time pressure legible,
- make cost burn legible,
- make authority visible,
- make cross-goal learning reusable,
- make evaluator health auditable,
- make agent activity auditable.

Operator constraints:

- planning, approval, execution, and evaluation need distinct surfaces,
- blocked-on-user must be a first-class visible state,
- blocked-on-user must support both pull surfaces and push notifications,
- the dashboard must compose widgets such as countdown, trend, burndown, and confidence rather than only listing entities,
- and the operator should never need to reconstruct system state from raw logs.

## Framework Primitives

### SubagentProtocol

This is the most important primitive.

It should model child execution with explicit fields instead of a vague `spawn_agent()` call.

Suggested shape:

```ts
type SubagentProtocol = {
  mode: "fork" | "fresh" | "worktree" | "remote" | "teammate";
  context_contract: ContextContract;
  communication_contract: CommunicationContract;
  lifecycle_policy: LifecyclePolicy;
  capability_profile: CapabilityProfile;
};
```

Why:

- Claude Code clearly uses multiple execution modes because different tasks need different isolation and continuity semantics.
- A single spawn primitive hides the real design decisions.

### ContextContract

This defines what the child receives.

Suggested shape:

```ts
type ContextContract = {
  immutable_context: {
    goal_id: string;
    objective_id?: string;
    key_result_id?: string;
    scope: string[];
    constraints: string[];
    evidence_contract?: string;
  };
  inherited_messages_mode: "none" | "summary" | "filtered_history" | "cache_stable_fork";
  clone_runtime_state: boolean;
  shared_callbacks: Array<"none" | "metrics" | "ui" | "abort" | "state">;
};
```

Why:

- Claude Code does not simply dump full history into every child.
- It filters incomplete tool calls.
- It clones mutable runtime state by default.
- It shares only selected callbacks.

Our framework should keep the same discipline, even if we choose different defaults.

Spec rule:

- context transfer must be declared, not implied.

### CommunicationContract

This defines how agents talk.

Suggested channels:

- `task_notification_bus`
- `agent_message_bus`
- `approval_response_bus`
- `resume_bus`
- `event_stream`

Why:

- Claude Code uses notifications, direct messages, resume, and mailbox-style patterns.
- Transcript scraping is too implicit to be the main communication mechanism.

Spec rule:

- communication semantics must be typed enough that a UI can render them and a policy layer can reason about them.
- transcripts are presentation artifacts; the append-only event log is the source of truth.

Suggested protocol actions:

| Action | Sent by | Required fields | Invariant |
| --- | --- | --- | --- |
| `spawn` | parent/runtime | `protocol_id`, `mode`, `context_contract`, `capability_profile` | creates exactly one child execution intent |
| `ack` | child/runtime | `protocol_id`, `session_id`, `accepted_at` | confirms the child accepted the contract |
| `block` | child/runtime | `protocol_id`, `reason_code`, `details`, `requested_action` | child may not continue until the block is resolved or cancelled |
| `resume` | parent/runtime | `protocol_id`, `resume_token`, `resolution` | resumes a previously blocked or disconnected child |
| `complete` | child/runtime | `protocol_id`, `result_ref`, `evidence_refs` | completion is a claim, not final acceptance |
| `cancel` | parent/runtime | `protocol_id`, `reason_code` | child must stop or move to terminal cancellation |

Protocol rules:

- every action must be idempotent by `protocol_id` plus action-specific dedupe key,
- a late `complete` after parent rescope becomes `orphaned_completion` rather than silently mutating current state,
- and `resume` is valid only for blocked or disconnected child states.

### HookRegistry

This defines typed lifecycle interception.

Suggested events:

- `SessionStart`
- `PlanStart`
- `PlanApproved`
- `PreToolUse`
- `PostToolUse`
- `PostToolUseFailure`
- `PermissionRequest`
- `PermissionDenied`
- `SubagentStart`
- `SubagentStop`
- `TaskExecutionCreated`
- `TaskExecutionCompleted`
- `EvaluationStart`
- `EvaluationComplete`
- `SessionStop`

Suggested outputs:

- `approve`
- `block`
- `updated_input`
- `additional_context`
- `updated_output`
- `retry`
- `watch_registration`
- `escalation_request`
- `stop_continuation`

Why:

- Claude Code's hook system matters because it actively changes execution, not just logs it.
- Typed outputs are the difference between control surfaces and callback soup.

Spec rule:

- hooks may intercept control flow, but they may not become a second hidden planning system.

Execution semantics:

- hook order must be deterministic within a scope,
- hook handlers must declare sync or async execution,
- hooks must have timeouts and failure policies,
- and multiple hook outputs must merge by explicit precedence rules rather than arrival order.

Minimum merge rules:

- `block` wins over `approve`,
- `stop_continuation` is terminal for the current boundary,
- `updated_input` and `additional_context` merge only if schemas allow composition,
- and retries require a bounded retry budget with a recorded cause.

### ExtensionScope

Extensions must be scoped.

Suggested scopes:

- `session`
- `agent`
- `skill`
- `workflow`
- `runtime`
- `evaluator`

Why:

- Claude Code's session-scoped hook registration is a strong signal.
- Global extensions become un-debuggable quickly.

Spec rule:

- every extension must have an owner scope, lifecycle, cleanup path, and failure mode.

### ProgressModel

This defines how a KR moves from narrative intent to measurable progress.

Suggested shape:

```ts
type ProgressModel = {
  cycle_id: string;
  metric_ids: string[];
  baseline_ids: string[];
  target_ids: string[];
  leading_indicator_ids: string[];
  lagging_indicator_ids: string[];
  latest_forecast?: string;
  current_health: "unknown" | "off_track" | "at_risk" | "on_track" | "exceeded";
  current_confidence_score: number;
};
```

Why:

- OKR management is not binary completion.
- A dashboard needs baseline, target, current value, trend, and confidence.
- A KR that cannot be measured structurally is only partially planned.

Spec rule:

- no KR may enter `approved` without a `ProgressModel` or an explicit milestone-only exception.

### BudgetPolicy

This defines how autonomy is constrained by spend.

Suggested shape:

```ts
type BudgetPolicy = {
  scope: "goal" | "objective" | "key_result" | "workspace";
  scope_id: string;
  max_total_cost_usd?: number;
  max_cost_per_run_usd?: number;
  max_daily_cost_usd?: number;
  hard_stop: boolean;
};

type CostLedgerEntry = {
  scope_id: string;
  key_result_id?: string;
  task_execution_id?: string;
  cost_type: "model_tokens" | "tool_usage" | "workspace_runtime" | "human_review";
  amount_usd: number;
  recorded_at: string;
  provenance: string;
};
```

Why:

- unattended systems fail not only on bad permissions, but also on unbounded spend.
- budget must be governable at the same layer as authority.

Spec rule:

- permission approval does not override budget exhaustion.

### NotificationRoute

This defines how blocked or approval-required work reaches a human.

Suggested shape:

```ts
type NotificationRoute = {
  scope: "goal" | "objective" | "key_result" | "approval_request";
  scope_id: string;
  channels: Array<"ui" | "email" | "chat" | "push" | "webhook">;
  escalation_sla_hours: number;
  on_call_ref?: string;
};
```

Why:

- `blocked_on_user` is not useful if nobody is told.
- dashboard pull and asynchronous push are different primitives.

Spec rule:

- any long-lived blocked state must resolve to a `NotificationRoute`.

### KnowledgeGraph

This defines how knowledge compounds across goals.

Suggested shape:

```ts
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
  from_goal_id: string;
  to_goal_id: string;
  relation: "contributes_to" | "reuses" | "blocks" | "learned_from";
  evidence_ref?: string;
};
```

Why:

- otherwise every goal starts from zero even when the system just learned something expensive.

Spec rule:

- prior artifacts and insights must be eligible planning context, not only archived audit output.

### EvaluationCalibration

This defines how judges remain governable.

Suggested shape:

```ts
type JudgeRotationPolicy = {
  primary_judges: string[];
  secondary_judges: string[];
  rotation_mode: "round_robin" | "randomized" | "disagreement_triggered";
  pairwise_required: boolean;
};

type CalibrationRun = {
  judge_id: string;
  eval_dataset_id: string;
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

Why:

- one judge is still one model.
- calibration must become data, not advice.

Spec rule:

- no judge may keep automatic promotion authority without periodic calibration and a visible trust score.

### ExternalActionContract

This defines how irreversible external actions are governed.

Suggested shape:

```ts
type ExternalActionContract = {
  action_type: "pr_comment" | "email" | "payment" | "ticket_update" | "deployment";
  dry_run_supported: boolean;
  receipt_required: boolean;
  reversal_policy: "reversible" | "manual_reversal" | "irreversible";
};
```

Why:

- allow/ask/deny is a precondition, not a sufficient safety model for irreversible actions.

Spec rule:

- irreversible actions must capture dry-run intent, receipt, and reversal semantics explicitly.

## What We Lock In Spec

These are not implementation details. They are framework commitments.

1. `Goal`, `Objective`, `KeyResult`, `EvidenceCheck`, and `DecisionRecord` are explicit persisted objects.
2. `TaskExecution`, `AgentSession`, and `ApprovalRequest` are derived runtime objects with their own lifecycle.
3. Clarification is a product surface, not an ad hoc prompt pattern.
4. `spawn_agent()` is not enough; child execution must declare mode, context, communication, and lifecycle.
5. Shared mutable runtime state is opt-in, never implicit.
6. Hooks are typed and scoped.
7. Policy decisions are explainable and reviewable.
8. Completion is evidence-backed, not self-reported.
9. Human escalation is a designed state, not a crash path.
10. `KeyResult` progress requires structured measurement, cycle, and confidence primitives.
11. Budget governance is a peer of permission governance.
12. Blocked work must bind to explicit notification and escalation routes.
13. Cross-goal knowledge artifacts and insights are reusable planning inputs.
14. Judge calibration, rotation, and trust scoring are explicit evaluation objects.
15. Irreversible external actions require dry-run, receipt, and reversal semantics.

## System State Model

The framework needs an explicit state model before implementation starts.

### Objective states

- `draft`
- `clarifying`
- `planned`
- `in_progress`
- `blocked`
- `verifying`
- `completed`
- `cancelled`

### KeyResult states

- `draft`
- `proposed`
- `approved`
- `ready`
- `running`
- `blocked`
- `verifying`
- `done`
- `failed`
- `superseded`

### KeyResult progress health

- `unknown`
- `off_track`
- `at_risk`
- `on_track`
- `exceeded`

### TaskExecution states

- `queued`
- `starting`
- `running`
- `blocked`
- `completed_claimed`
- `failed`
- `cancelled`
- `orphaned`

### ApprovalRequest states

- `pending`
- `approved`
- `denied`
- `expired`
- `superseded`

### AgentSession states

- `starting`
- `running`
- `waiting_input`
- `stalled`
- `disconnected`
- `completed`
- `failed`

### ExternalAction states

- `planned`
- `dry_run_ready`
- `awaiting_approval`
- `committed`
- `reversed`
- `failed`

### GraderTrust states

- `healthy`
- `watch`
- `demoted`
- `disabled`

State rules:

- only approved KRs may materialize `TaskExecution` objects,
- approved KRs should normally carry baseline, target, cycle, and cadence before execution starts,
- lifecycle state and progress health are parallel dimensions, not one field,
- `completed_claimed` always requires evaluation before KR closure,
- budget exhaustion may block otherwise permission-valid work,
- long-lived blocked states must emit a notification through an explicit route,
- committed external actions must record a receipt or a documented reason why none exists,
- parent rescope may supersede a KR and orphan any attached task executions,
- and no state transition may be driven only by transcript text.

## Why Claude Code Likely Chose Its Design

### Multiple Subagent Modes

Likely reason:

- tasks differ in required isolation, cost, latency, and context continuity.

Simpler alternative:

- one generic subagent type with one context strategy.

Why that is weaker:

- either too much state leakage,
- or too much context loss,
- or no clean way to support worktree/remote/background semantics.

### Cloned Mutable Context By Default

Likely reason:

- shared mutable caches and state create interference between concurrent agents.

Simpler alternative:

- share parent runtime state wholesale.

Why that is weaker:

- races,
- transcript/result contamination,
- hard-to-debug permission and tool-result coupling.

### Explicit Notification And Resume Paths

Likely reason:

- background child completion must wake the parent without forcing transcript polling.

Simpler alternative:

- parent tails child output files or polls transcript logs.

Why that is weaker:

- implicit coupling,
- noisy context,
- poor UX,
- difficult recovery semantics.

### Session-Scoped Hooks

Likely reason:

- extension behavior should live and die with the scope that registered it.

Simpler alternative:

- global hook table.

Why that is weaker:

- hidden behavior accumulation,
- hard attribution,
- cleanup bugs,
- extension conflicts.

## Why Our Framework May Choose Different Defaults

We should borrow Claude Code's underlying logic, but not necessarily its exact defaults.

### Difference 1: Goal-First Instead Of Task-First

Claude Code is fundamentally a coding agent product.

Our framework is goal-governed orchestration.

So our default top-level object should be `Objective` and `KeyResult`, not only `Task`.

### Difference 2: Evaluation As A Core Layer

Claude Code includes verification surfaces, but our framework should elevate evaluation to a first-class subsystem.

Reason:

- our product promise depends on proving completion across many work types, not only code edits.

### Difference 3: Plugin Model Must Cover More Than Hooks

We need pluggability not only around lifecycle interception, but also around:

- runtime adapters,
- evaluators,
- context assemblers,
- policy providers,
- storage exporters.

Claude Code is a strong reference for hook scoping, but our system needs a broader plugin taxonomy.

### Difference 4: UI/UX Is Part Of The Runtime Contract

Our product is not "a daemon plus some logs."

Reason:

- vague goals need clarification dialogue,
- approvals need explainable authority requests,
- blocked work needs actionable recovery,
- and evidence needs human-readable review.

So operator UX is not a skin on top of the engine. It is part of how the engine stays governable.

### Difference 5: Goal Management Needs A Real Scorecard Layer

Claude Code is strong at task and session supervision.

Our framework also needs:

- cycles,
- baselines,
- targets,
- forecasts,
- confidence,
- and review cadence.

Otherwise it stays too close to a governed task tracker.

### Difference 6: Spend And Calibration Are Framework Problems

A local-first autonomous system needs two controls beyond permission rules:

- spend ceilings,
- and evaluator trust.

Those should not live only in operations docs. They need persisted objects and visible UI surfaces.

## Comparative Design Record

This is where we answer not only "what did Claude Code do?" but "why did it do that?" and "why might we choose differently?"

| Design dimension | Claude Code likely choice | Why that choice makes sense there | Our choice | Why our choice differs |
| --- | --- | --- | --- | --- |
| Top-level object model | task-centric with planning/task surfaces | coding work naturally collapses into bounded tasks quickly | `Goal -> Objective -> KeyResult -> Task` | our product promise starts higher than a task and must preserve intent hierarchy |
| Context transfer | filtered inheritance plus cloned mutable state, with special fork behavior | concurrent coding sessions are fragile if state leaks; fork mode also benefits from prompt-cache reuse | explicit `ContextContract` with declared inheritance modes | we need the same discipline, but tied to goal/KR semantics rather than only coding-session continuity |
| Child execution modes | multiple modes: fresh, fork, background, worktree, remote, teammate | execution constraints vary by cost, isolation, and continuity | `SubagentProtocol` as a first-class contract | we want the abstraction to be stable even if underlying runtimes change |
| Parent-child communication | notifications, resume, mailbox, direct messaging | polling transcripts is too implicit and brittle | typed buses for notifications, messages, approvals, and resume | our UI and policy layers need machine-readable communication semantics |
| Hooks | session-scoped typed lifecycle hooks | powerful enough to govern execution without becoming global callback soup | scoped hooks plus broader plugin taxonomy | our system must also let evaluators, context assemblers, and policy providers plug in |
| Permissions | rule-based local tool permissions and approval surfaces | coding agents need actionable authority without constant friction | rule-based policy engine covering workspace, repo, path, branch, action, and external authorities such as GitHub | our authority model is broader and more productized than a CLI tool's permission layer |
| Operator UX | coding cockpit with task/session/permission surfaces | the operator is supervising technical execution | goal control plane with clarification, KR approval, execution readiness, and evidence review | our user is governing objectives, not merely watching tool output |
| Completion model | execution and verification surfaces | good fit for coding tasks and tool loops | evaluation as a first-class subsystem | our system must judge business completion, not only tool/task completion |

## From-Scratch Implementation Outline

The core should be implemented as our own modules, even if adapters talk to external CLIs and services.

### Core modules

- `goal-service`: persists goals, objectives, KRs, tasks, dependencies, and decision records.
- `metric-service`: persists metric definitions, baselines, targets, observations, and forecasts.
- `cadence-service`: owns cycles, checkpoints, and review agendas.
- `planning-service`: runs clarification loops, SMART drafting, plan previews, and execution-readiness checks.
- `runtime-manager`: launches agent sessions, allocates workspaces, handles liveness, and owns resume handles.
- `subagent-engine`: validates and executes `SubagentProtocol` contracts.
- `policy-engine`: evaluates `allow` / `ask` / `deny` decisions and records justification.
- `budget-ledger`: records spend, forecasts burn, and raises budget alerts.
- `notification-service`: routes blocked work and approval requests through push and pull channels.
- `hook-registry`: registers scoped lifecycle hooks and enforces schemas.
- `evaluator-registry`: runs tests, artifact checks, benchmark checks, and human review workflows.
- `calibration-service`: runs held-out evals, judge rotation, trust scoring, and evaluator demotion.
- `knowledge-graph`: persists `Insight`, `KnowledgeArtifact`, and `CrossGoalLink`.
- `operator-api`: provides the UI-facing state model for goals, approvals, sessions, blockers, and evidence.
- `event-log`: append-only source of lifecycle events for audit, replay, and export.

### Adapter modules

- `runtime-adapter-codex-cli`
- `runtime-adapter-claude-cli`
- `runtime-adapter-sdk`
- `github-authority-adapter`
- `filesystem-authority-adapter`
- `notification-adapter-email`
- `notification-adapter-chat`
- `markdown-exporter`
- `obsidian-exporter`

### First implementation rule

Adapters may vary.

The core contracts may not.

## End-To-End User Scenarios

### Scenario A: Solo Builder Shipping An App Milestone

Flow:

1. User states: "Ship onboarding v1 for the app."
2. Planning layer asks clarifying questions.
3. System drafts 3 independent Key Results with baselines, targets, and a weekly review cadence.
4. User approves the KR plan and budget envelope.
5. Runtime launches bounded agent tasks in local workspaces.
6. One task blocks on a missing API credential.
7. Approval inbox requests human input and the notification route pushes an alert to the owner.
8. Work resumes in the same session.
9. Evaluation layer runs tests and UI verification.
10. Dashboard shows KR health, forecast, burn rate, and confidence before closure.
11. User reviews artifacts and marks the objective complete.

Likely failure modes:

- KRs too vague,
- no baseline or target,
- hidden dependencies,
- permission prompts too noisy,
- cost burn exceeds the value of the KR,
- evaluation contract underspecified.

Required product surfaces:

- goal conversation,
- KR preview with SMART gap highlights,
- KR scorecard with baseline, target, and forecast,
- execution readiness panel,
- approval inbox,
- notification feed,
- evidence review screen.

### Scenario B: Small Team With One Accountable Objective Owner

Flow:

1. Objective owner creates a goal and KRs.
2. Some KRs are delegated to human teammates, some to agents.
3. Agent work sends notifications and structured updates.
4. Task board shows blockers, dependencies, and budget burn.
5. Evidence checks and leading indicators feed into weekly review.
6. Cross-goal insights from prior launches are attached during replanning.

Likely failure modes:

- message routing ambiguity,
- duplicated ownership,
- stale context between human and agent work,
- weekly review happens without updated progress numbers,
- approvals becoming the bottleneck.

Required product surfaces:

- objective dashboard,
- review agenda,
- KPI and burndown views,
- dependency graph,
- cross-agent update feed,
- knowledge reuse panel,
- owner-specific review queue.

### Scenario C: Larger Organization With Policy Constraints

Flow:

1. Owner defines an objective in a governed workspace.
2. Planning layer previews likely authority requirements.
3. Policy engine denies certain actions by default and also checks budget pools.
4. Approval workflow escalates repo/path-specific exceptions and irreversible external actions.
5. Runtime uses constrained adapters, managed hooks, and dry-run receipts where possible.
6. Evaluation, calibration history, and audit logs support compliance review.

Likely failure modes:

- policy complexity overwhelms UX,
- too many immutable rules for fluid iteration,
- goal ownership fragmented across teams,
- cost limits become opaque or political,
- external action receipts are incomplete,
- evaluation artifacts not sufficient for compliance.

Required product surfaces:

- policy explainer,
- scope-aware approval requests,
- budget ledger view,
- evaluator trust panel,
- audit timeline,
- compliance export/evidence package.

## What To Learn From Open Source Without Depending On It

We are not trying to choose a winner and wire it in.

We are trying to extract durable mechanisms.

### Claude Code / Claude Code-adjacent patterns

Absorb:

- staged clarification UX,
- plan approval as a separate mode,
- multiple subagent execution modes,
- cloned mutable context,
- explicit notification and resume paths,
- scoped hooks,
- rule-based permissions,
- blocked-on-user as a first-class runtime state.

Do not copy blindly:

- product-specific object names,
- UI assumptions tied to a coding-only workflow,
- or any accidental complexity that exists because of Claude-specific runtime constraints.

### Workflow engines such as Temporal, Dagster, or Prefect

Absorb:

- durable state machines,
- retries and terminal-stop semantics,
- resumability,
- explicit workflow state instead of transcript inference.

Do not copy blindly:

- heavyweight operator models designed for data pipelines,
- or assumptions that the unit of work is deterministic code rather than uncertain agent execution.

### Agent graph frameworks such as LangGraph or similar orchestration stacks

Absorb:

- explicit node and edge definitions,
- checkpointed execution,
- structured handoffs between reasoning steps.

Do not copy blindly:

- graph-first design as the top-level product metaphor for users,
- or the assumption that graph nodes alone solve governance and operator UX.

### Coding-agent products such as OpenHands, Aider, Cline, Roo Code, and related systems

Absorb:

- practical repo/task execution loops,
- workspace awareness,
- tool affordance design,
- artifact-driven iteration,
- and lessons from where autonomy breaks down in real coding tasks.

Do not copy blindly:

- chat-centric or IDE-centric assumptions,
- or the idea that "tool access + loop" is enough to become a control plane.

### Policy systems such as OPA-style policy engines

Absorb:

- policy as explicit rules,
- separation between policy evaluation and business logic,
- auditable decisions,
- scoped exceptions.

Do not copy blindly:

- policy languages or embedding models that make operator UX worse than the risk they control.

### Eval and observability stacks such as promptfoo, Langfuse, Braintrust, or similar tools

Absorb:

- explicit eval datasets,
- experiment comparison,
- traceability from output back to evidence,
- and feedback loops that improve specs rather than only dashboards.

Do not copy blindly:

- evaluation models that reward eloquent summaries more than verified completion.

## Edge Cases The Spec Must Cover

### Goal Formation

- user intent is vague, contradictory, or unstable,
- user wants speed before SMART precision,
- user changes the goal after sub-work has already started.

### Measurement And Cadence

- KR has no baseline,
- target is not numerically or operationally testable,
- leading indicators improve while lagging indicators stall,
- checkpoint cadence is missing or unrealistic.

### Decomposition

- KRs are not independent,
- recursive KR to Objective decomposition never bottoms out,
- a later clarification invalidates already-approved child work.

### Context And Coordination

- child agent inherits stale or over-broad history,
- sibling agents mutate shared state,
- child finishes after parent has already moved on,
- child requires context the parent never formally declared.

### Authority

- one task needs GitHub write access but another should remain read-only,
- local-directory permissions differ by path or operation,
- the same action is allowed in one workspace and denied in another,
- user denies a request and the system needs graceful recovery.

### Budget And Spend

- a task is permission-allowed but budget-blocked,
- one KR burns the shared budget pool for the rest of the goal,
- human-review cost dominates agent-runtime cost,
- cost attribution is missing at KR closeout time.

### Liveness And Recovery

- local shell stalls on interactive prompts,
- remote agent disconnects,
- daemon restarts mid-run,
- human approval arrives after timeout or after a retry path already started.

### Notification And Escalation

- a KR is `blocked_on_user` but no one is notified,
- after-hours approvals route to the wrong person,
- the UI shows a blocker but no push channel exists,
- repeated alerts create operator blindness.

### Evaluation

- task "succeeds" mechanically but fails the KR,
- evidence is missing or ambiguous,
- human reviewer disagrees with automated completion,
- multiple evaluators return conflicting outcomes.

### Calibration And Anti-Gaming

- one judge begins rewarding stylistic changes over verified completion,
- the producer learns the judge's preferences and games them,
- held-out evals drift from live production failures,
- an evaluator should be demoted but no trust model exists.

### Knowledge Reuse

- a prior goal produced a reusable insight but the new planner never sees it,
- an old lesson is stale but still being injected as context,
- two goals should align through `contributes_to` but remain isolated.

### External Actions

- a PR comment is sent without a stored receipt,
- an email or payment cannot be dry-run and needs stronger approval,
- reversal policy is undefined when an external action partially succeeds.

### UX

- operator cannot tell what is blocked and why,
- too many approvals destroy flow,
- policy text is incomprehensible,
- evidence review is harder than redoing the work manually.

## Failure Matrix We Should Design For Early

| Failure | Required behavior |
| --- | --- |
| parent objective is edited after child spawn | mark affected child executions as `stale_context` and require revalidation before merge |
| duplicate `complete` or `block` events after reconnect | de-dupe by protocol/event key and preserve first accepted transition |
| approval arrives after timeout | record it, but require explicit reattachment or reject as stale depending on state |
| workspace lease path changed or repo branch renamed | revalidate authority and lease before further tool use |
| automated tests pass but evidence review fails | keep KR in `verifying` or move to `failed`, never auto-close |
| human and machine evaluators disagree | escalate to review queue with both decision records attached |
| daemon restarts with active background work | reconstruct from event log, not transcript, or fail closed |
| concurrent edits touch the same KR or policy rule | apply explicit optimistic concurrency control and surface conflict resolution in UI |
| budget is exhausted mid-run | move work to a budget-blocked state and surface spend attribution before any retry |
| `blocked_on_user` has no active notification route | fail the workflow setup or escalate to a default route instead of silently waiting |
| irreversible external action commits without receipt | mark the action as non-compliant and require manual remediation |
| one judge drifts from human reviewers | demote or rotate that judge according to calibration policy |
| a prior-goal lesson is stale or contradicted | mark the insight stale and require revalidation before reuse |

## Why Build From Scratch After Research

Because our main risk is not implementation speed. It is conceptual leakage.

If we adopt another framework's core abstractions too early, we inherit:

- its unit of work,
- its state model,
- its operator model,
- its failure semantics,
- and its blind spots.

That is acceptable for adapters.

It is dangerous for the control plane itself.

So the right sequence is:

1. read the strongest systems,
2. identify the underlying mechanisms,
3. write our own spec with explicit tradeoffs,
4. validate it against user scenarios and edge cases,
5. then implement from scratch.

## Evolution Path

### Phase 0: Research Artifact

Deliver:

- framework doc,
- scenario doc,
- benchmarked research loop,
- architecture critique.

### Phase 1: Local Control Plane Prototype

Deliver:

- objective/KR schema,
- metric, baseline, target, and cycle schema,
- planning conversation,
- task board,
- local runtime adapter,
- evidence contract abstraction.

### Phase 2: Subagent Protocol Prototype

Deliver:

- multiple spawn modes,
- context assembler,
- notification bus,
- resume handles,
- structured lifecycle events.

### Phase 3: Hook And Policy Engine

Deliver:

- typed hook registry,
- scoped extensions,
- permission rules,
- budget policy and spend ledger,
- approval inbox,
- audit records.

### Phase 4: Evaluator Registry

Deliver:

- tests evaluator,
- artifact evaluator,
- benchmark evaluator,
- held-out eval set,
- judge rotation and calibration,
- manual review evaluator.

### Phase 5: Multi-Workspace And Org Governance

Deliver:

- stronger policy scopes,
- managed rule layers,
- GitHub authority abstractions,
- notification routing,
- external action receipts and reversal rules,
- cross-goal knowledge graph,
- remote runtimes,
- richer audit/export paths.

## What Must Be True For This Framework To Work

1. Planning must reduce downstream coordination cost, not add theater.
2. Subagent protocol must make context inheritance predictable.
3. Hooks must be typed and scoped.
4. Evaluation must be separate from execution.
5. Policy must be legible in the UI.
6. Communication must be explicit.
7. Extensions must clean up with their scope.
8. Progress must be measured as a curve, not only a terminal state.
9. Spend must be governable as strictly as permissions.
10. Graders must be calibratable, replaceable, and visible.
11. Blocked work must reliably reach a human.
12. Knowledge learned in one goal must be reusable in the next.

If any one of these fails, the system will drift back into prompt babysitting with extra ceremony.
