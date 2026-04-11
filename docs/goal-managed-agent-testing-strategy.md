# Goal-Managed Agent Testing Strategy

## Core Position

We cannot prove an agentic system is "correct" with one kind of test.

We need a layered assurance stack:

1. deterministic software tests for the control plane,
2. protocol and recovery tests for runtime behavior,
3. offline agent evals for task success,
4. adversarial and fault-injection tests for robustness,
5. online monitoring and human review for real-world drift.

If any one layer becomes the whole strategy, we will get false confidence.

## The Main Mistake To Avoid

Do not treat "ask another model to judge it" as the primary safety mechanism.

That only adds another probabilistic component.

A second model can help as one evaluator, but it cannot replace:

- deterministic invariants,
- explicit success criteria,
- replayable datasets,
- trace review,
- and operational guardrails.

## What We Are Actually Testing

There are two different correctness problems:

### 1. System correctness

Questions:

- Did the state machine transition correctly?
- Did the permission policy behave correctly?
- Did the hook system apply the right precedence?
- Did resume/dedupe/orphan handling work?

These should be tested mostly with normal software tests.

### 2. Agent effectiveness

Questions:

- Did the agent solve the task?
- Did it solve it for the right reason?
- Did it use tools correctly?
- Did it remain consistent across repeated trials?

These require agent evals, traces, and human calibration.

### 3. Evaluator correctness

Questions:

- Did the judge reward the right thing?
- Is the grader still aligned with human review?
- Did a held-out eval catch gaming that the main loop missed?
- Should a judge be rotated, demoted, or disabled?

These require calibration runs, held-out datasets, disagreement review, and trust scoring.

## The Assurance Stack

## Layer 1: Deterministic Control-Plane Tests

These should be the strictest tests in the system.

Targets:

- object lifecycle tests for `Goal`, `Objective`, `KeyResult`, `EvidenceCheck`, `DecisionRecord`
- metric, baseline, target, and cycle rules
- state machine tests
- optimistic concurrency tests
- permission rule evaluation tests
- budget policy evaluation tests
- notification route and escalation resolution tests
- hook merge/precedence tests
- event-log append and replay tests

Best practice:

- every state transition should have positive tests and forbidden-transition tests
- every policy rule should be testable without an LLM
- every bug in this layer should become a regression test

Examples:

- `approved -> ready` allowed, `draft -> running` forbidden
- KR approval rejected when no baseline/target/cycle exists and no exception is recorded
- duplicate `complete` event does not double-close a KR
- late approval cannot silently resume superseded work
- permission-allowed but budget-exhausted work still blocks
- `block` overrides `approve` when hook outputs conflict

## Layer 2: Protocol And Recovery Tests

This layer proves the runtime behaves sanely under failure.

Targets:

- `spawn/ack/block/resume/complete/cancel` protocol
- workspace lease behavior
- daemon restart recovery
- stale context handling
- disconnected child agent recovery
- blocked notification routing
- external action dry-run / receipt / reversal behavior
- budget threshold crossings during a live run

Best practice:

- use simulation and fault injection, not only happy-path integration tests
- assert idempotency and dedupe behavior explicitly
- replay event logs to reconstruct state and compare with expected state

Examples:

- child emits `complete` twice after reconnect
- daemon restarts between `block` and `resume`
- parent objective changes while child is running
- branch/path/workspace lease changes mid-session
- `blocked_on_user` event is raised but notification route is missing
- deployment action commits without a receipt attachment

## Layer 3: Offline Agent Evals

This layer tests whether the agent can actually do the work.

Targets:

- planning and clarification
- KR drafting quality
- metric and cadence drafting quality
- permission-request behavior
- budget-request behavior
- coding/execution tasks
- evidence collection
- cross-goal knowledge reuse
- cross-agent coordination

Best practice:

- start early with a small but high-signal eval set
- use tasks drawn from real failures and real manual checks
- keep tasks unambiguous and reference-solvable
- version datasets
- run the same eval suite on every meaningful change

For our system, the eval suite should include:

- happy paths
- edge cases
- adversarial cases
- recovery cases
- policy-boundary cases
- budget-boundary cases
- evaluator-disagreement cases
- long-running coordination cases

## Layer 4: Adversarial And Robustness Tests

This layer tests whether the system breaks in dangerous ways.

Targets:

- prompt injection into planning
- permission escalation attempts
- eval gaming
- held-out overfitting
- dependency-spaghetti plans
- infinite recursive decomposition
- message spoofing or malformed protocol events
- hook abuse
- budget bypass attempts

Best practice:

- treat this like red teaming, not just regression testing
- test both malicious and accidental failure modes
- verify that unsafe behavior is blocked, escalated, or contained

## Layer 5: Online Monitoring And Human Review

This layer catches what offline evals miss.

Targets:

- production drift
- real user failure patterns
- grader misalignment
- operator UX confusion
- pathological long-tail failures
- cost drift
- no-dimension-progress plateaus

Best practice:

- ship with tracing
- sample transcripts and event histories regularly
- mine failures into future offline eval cases
- do not rely on user complaints as the main signal

## Dataset Best Practices

The dataset is the heart of the eval system.

### How to build it

Start with:

- manual release checks,
- bug reports,
- support issues,
- observed production failures,
- and domain-expert-crafted scenarios.

### How big it should be at the start

Small is fine if it is real.

An initial set of 20-50 high-signal tasks is enough to start if they come from real failures or core workflows.

### How to structure each task

Each task should include:

- input context
- exact goal
- explicit success conditions
- known constraints
- expected evidence
- grader instructions
- reference solution when possible

A task is bad if two informed reviewers would disagree on pass/fail.

### Versioning

Dataset versions must be explicit.

We should be able to answer:

- which dataset version produced this score?
- what changed between dataset versions?
- did the system improve, or did the dataset get easier?
- which cases were held out from the producer loop?

## Grader Best Practices

Graders are part of the system under test.

### Order of preference

1. deterministic assertions first
2. structural assertions second
3. model-graded rubrics only when necessary
4. human review for ambiguous cases

Examples of deterministic checks:

- file exists
- JSON schema matches
- command exit code is correct
- expected diff present
- required artifact attached
- forbidden tool not used

Examples of structural checks:

- event stream contains `block -> resume -> complete`
- permission request includes correct scope
- KR has all SMART fields filled

Examples of model-graded checks:

- clarification quality
- plan coherence
- explanation quality
- evidence sufficiency when not fully capturable deterministically

### Rules for model graders

- pin the grader model/version when possible
- keep rubrics narrow and criterion-based
- prefer pairwise comparison, classification, or structured scoring over open-ended judging
- calibrate graders against human review regularly
- review transcripts when the grader says pass/fail for surprising reasons

## Calibration And Held-Out Best Practices

Calibration should be treated as a repeating system process, not a manual reminder.

Required objects and workflows:

- `HeldOutEvalSet`
- `JudgeRotationPolicy`
- `CalibrationRun`
- `GraderTrustScore`
- `EvaluatorDemotionPolicy`

Best practices:

- keep at least one held-out eval set outside the producer optimization loop
- rotate judges by policy when enough disagreement or drift accumulates
- record judge-human agreement over time instead of trusting intuition
- demote or disable judges whose trust scores fall below threshold
- require human arbitration on high-impact disagreement cases

Anti-patterns:

- one judge family scoring every release indefinitely
- tuning directly against the same public eval subset until it becomes predictable
- treating "0.89 looks good" as evidence that the judge itself is healthy

## Metrics That Matter

A single score is not enough.

We should track:

- task success rate
- critical-path success rate
- KR on-track rate
- forecast accuracy
- review-on-time rate
- consistency across reruns
- false-approve rate
- false-block rate
- permission-request precision
- budget-block precision
- retry rate
- orphaned-completion rate
- resume success rate
- evaluator disagreement rate
- judge-human agreement rate
- held-out eval pass rate
- consecutive-no-dimension-progress streak length
- cost per successful task
- latency to successful task

### For agents, track consistency explicitly

One-off success is not enough for a real product.

Track both:

- `pass@k`: can the system succeed in any of k tries?
- consistency-style metrics: how often does it succeed reliably on repeated runs?

For our product, consistency matters more than hero runs.

## Harness Best Practices

The harness must make tasks reproducible.

Requirements:

- fixed repo snapshot or controlled fixture
- fixed tool availability
- explicit permission policy for the test
- explicit budget policy for the test
- trace capture
- event-log capture
- notification capture
- time budget
- cost budget
- cleanup after run

Anti-pattern:

- testing only the final text response

For coding and execution agents, behavior must be verified through traces, artifacts, file outputs, and event logs.

## Recommended Test Pyramid For This Product

### Per-commit

- unit tests for control-plane logic
- protocol contract tests
- hook precedence tests
- policy-engine tests
- a very small smoke eval suite

### Nightly

- full offline eval suite
- rerun critical evals multiple times for consistency
- adversarial eval subset
- restart/recovery chaos tests

### Pre-release

- full scenario suite
- long-running soak tests
- human transcript review sample
- policy/audit export verification

### Post-release

- production monitoring
- shadow mode on risky changes
- canary rollout for new runtime or model changes
- continuous failure harvesting into datasets

## Best Practices We Should Adopt

1. Evaluate early, not after the system feels complex.
2. Start from real failures, not imagined benchmark theater.
3. Keep early suites small but high-signal.
4. Make tasks and graders unambiguous.
5. Prefer deterministic checks wherever possible.
6. Treat transcripts as evidence for review, not truth for state.
7. Version datasets and graders.
8. Re-run critical cases multiple times to measure consistency.
9. Combine automated evals with regular human calibration.
10. Keep held-out cases outside the producer loop.
11. Track evaluator trust, not just candidate score.
12. Turn every escaped production failure into a new test.

## What We Should Build First

If we want a serious testing foundation, the first implementation slice should be:

1. deterministic tests for the control plane and state machine
2. an append-only event log with replay tests
3. a small versioned eval dataset for the top 20-50 workflows/failures
4. a reproducible agent-eval harness with trace capture
5. a calibration harness with held-out evals and judge trust scoring
6. an operator review screen for inspecting failures and grading disagreements

If we skip those and jump straight to "more agents" or "better prompts," we will not know whether the system is improving or just changing shape.
