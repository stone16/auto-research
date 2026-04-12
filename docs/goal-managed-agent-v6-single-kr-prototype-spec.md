# Goal-Managed Agent v6: Single-KR Prototype Spec

## Purpose

This document specifies the smallest prototype that can answer RT-01 from
`docs/goal-managed-agent-v6-red-team-checklist.md`:

> Can one governed KR survive clarification, approval, launch, denial, replan,
> resume, verification, and acceptance without state ambiguity?

This is not the full product tech spec. It is a proof artifact for one narrow
workflow.

## Prototype question

The prototype succeeds only if it proves all three:

1. One KR can move through the full governed lifecycle without relying on
   transcript memory.
2. Every user-visible status is reconstructable from one durable source of
   truth after restart.
3. Completion requires explicit evidence and operator acceptance, not agent
   self-report or judge score alone.

## Non-goals

Do not solve these in this prototype:

- full recursive Node tree
- portfolio views across many objectives
- org-scale policy layers
- remote runtimes
- general plugin marketplace
- calibrated judge automation that can directly close work
- the full three-layer acceptance model if the metrics layer is still unproven

If a design decision does not help answer RT-01 or RT-02, defer it.

## Prototype scenario

Use one concrete scenario:

- Objective: ship OAuth2-based authentication for API and admin routes before
  launch review.
- Prototype KR: staging auth flow passes contract tests, required secrets and
  callback URLs exist with rollback notes, and an operator accepts the evidence
  bundle before promotion.

The scenario is intentionally code-heavy because it gives deterministic evidence
and an easy permission-denial path.

## Evidence posture

This spec follows the filtered foundations:

- keep run-backed findings
- treat discussion-backed elegance as optional until proven
- prefer smaller object sets over architectural symmetry

Concretely:

- keep `completed_claimed` vs accepted completion
- keep append-only event logging
- keep explicit approval and denial handling
- keep resume and stale-context handling
- keep evaluator and operator acceptance separate
- defer the independent metrics layer from product truth in this prototype

## In-scope objects

Only persist the minimum objects needed to prove the lifecycle:

### Objective

Fields:

- `objective_id`
- `intent`
- `owner`
- `status`

The Objective exists only as parent context for the KR.

### KeyResult

Fields:

- `kr_id`
- `objective_id`
- `intent`
- `acceptance`
- `status`
- `version`
- `owner`

`acceptance` for this prototype uses:

- deterministic assertions
- optional rubric notes for human review

Do not require a separate metrics layer in order to close the KR.

### TaskExecution

Fields:

- `task_execution_id`
- `kr_id`
- `status`
- `version_snapshot`
- `runtime`
- `workspace_lease_id`
- `resume_handle`
- `current_block_reason`
- `artifacts`

### ApprovalRequest

Fields:

- `approval_request_id`
- `task_execution_id`
- `scope`
- `requested_action`
- `reason_code`
- `status`
- `created_at`
- `resolved_at`

### EvidenceCheck

Fields:

- `evidence_check_id`
- `kr_id`
- `kind`
- `status`
- `artifact_refs`
- `notes`

Kinds in scope:

- `test`
- `artifact`
- `human_review`
- `policy_review`

### DecisionRecord

Fields:

- `decision_record_id`
- `object_type`
- `object_id`
- `decision`
- `actor`
- `reason`
- `created_at`

### EventEnvelope

This is the source of truth for lifecycle reconstruction.

Fields:

- `event_id`
- `event_type`
- `object_type`
- `object_id`
- `correlation_id`
- `dedupe_key`
- `actor`
- `occurred_at`
- `payload`

## Explicitly deferred objects

These are intentionally out of scope for the first prototype:

- full Node/Run recursive ontology
- sub-Run synthesis trees
- general `local_policy` inheritance engine
- generalized plugin registry
- org-wide approval routing

If the prototype cannot prove the single-KR lifecycle without these, that is a
signal that the architecture is still too abstract.

## Minimal status model

### KeyResult statuses

- `draft`
- `ready_for_approval`
- `approved`
- `running`
- `blocked`
- `verifying`
- `accepted`
- `failed`
- `superseded`

Rules:

- only `approved` KRs may create a `TaskExecution`
- only `verifying` KRs may move to `accepted`
- `accepted` is terminal for this prototype
- if the KR contract changes after launch, the old path becomes stale and must
  not auto-merge

### TaskExecution statuses

- `queued`
- `running`
- `blocked`
- `completed_claimed`
- `failed`
- `cancelled`
- `orphaned`

Rules:

- `completed_claimed` is never treated as done
- `blocked -> running` is allowed only through explicit resume
- late completion after KR supersession becomes `orphaned`

## Acceptance model for this prototype

Use a deliberately narrow acceptance contract.

### Assertions

Required:

1. contract tests for staging auth flow pass
2. required secret and callback configuration artifacts exist
3. rollback note exists
4. operator has reviewed the evidence bundle

### Rubric

Allowed only for advisory review:

- evidence sufficiency
- rollout readiness notes
- residual risk notes

The rubric must not close the KR on its own.

### Done condition

The KR is `accepted` only when:

- all required assertions pass
- required `EvidenceCheck` items are passed or explicitly waived
- operator acceptance is recorded in a `DecisionRecord`

## Lifecycle script to prove

The prototype must support this exact path:

1. User drafts the KR.
2. System asks clarifying questions until the KR is specific enough.
3. User approves launch.
4. System creates `TaskExecution` and a workspace lease.
5. Runtime requests a blocked permission or missing credential.
6. User denies the request.
7. System records denial and moves work to `blocked`.
8. User or system replans the KR or narrows the action.
9. User provides the missing approval or input.
10. System resumes the same logical execution through `resume_handle`.
11. Runtime claims completion and uploads artifacts.
12. System moves to `completed_claimed`, not `accepted`.
13. Evaluator checks run.
14. Operator reviews evidence and accepts or rejects.
15. Restart the app and prove the same state can be reconstructed.

If any one of these steps cannot be made explicit in object and event form, the
prototype has failed its purpose.

## Required events

At minimum, emit these event types:

- `kr.created`
- `kr.clarification_requested`
- `kr.updated`
- `kr.approved`
- `task_execution.created`
- `task_execution.started`
- `approval_request.created`
- `approval_request.denied`
- `task_execution.blocked`
- `kr.replanned`
- `approval_request.approved`
- `task_execution.resumed`
- `task_execution.completed_claimed`
- `evidence_check.started`
- `evidence_check.passed`
- `evidence_check.failed`
- `operator.accepted`
- `operator.rejected`
- `task_execution.orphaned`

Every visible state change must be derivable from these events plus the current
object snapshots.

## Required UI surfaces

Only build the surfaces needed to prove the lifecycle:

### 1. KR planning view

Shows:

- KR intent
- open clarification questions
- current acceptance assertions
- launch readiness summary

Actions:

- answer clarification
- edit KR
- approve launch

### 2. Execution status view

Shows:

- KR status
- TaskExecution status
- current block reason
- latest approval request
- latest event timeline

Actions:

- deny or approve request
- trigger replan
- resume work

### 3. Evidence review view

Shows:

- completion claim
- artifacts
- EvidenceCheck results
- decision history

Actions:

- accept KR
- reject KR

### 4. Recovery debug view

Shows:

- object snapshots
- append-only event timeline
- reconstructed current state

This view exists to prove RT-02, not because it is the final UX.

## Source-of-truth rule

The prototype must choose one durable state source and commit to it.

Preferred rule:

- append-only event log is the durable truth
- object tables are materialized current-state projections
- UI reads projections, but recovery can always recompute them from events

Failure condition:

- any UI view depends on transcript tailing, in-memory process state, or ad hoc
  log scraping that cannot be reconstructed after restart

## Runtime assumptions

Keep runtime narrow:

- one local runtime adapter
- one local workspace lease
- one resume path
- one blocked permission flow

This prototype does not need multiple runtimes, multiple simultaneous child
agents, or generalized plugin activation.

## Verification plan

### Deterministic checks

- forbidden transition tests
- duplicate event dedupe tests
- late completion becomes `orphaned`
- denied approval cannot silently resume work
- restart reconstructs the same visible status

### Scenario test

Run one end-to-end scripted scenario that includes:

- one denial
- one replan
- one resume
- one completion claim
- one operator decision
- one restart in the middle of the flow

### Human review check

A reviewer should be able to answer these without reading transcripts:

1. What is blocked right now?
2. Why is it blocked?
3. What changed at replan?
4. What evidence exists?
5. Why is the KR not yet accepted?
6. After restart, did the system recover the same answer?

If the reviewer cannot answer these from the prototype surfaces, the model is
still too implicit.

## Exit criteria

The single-KR prototype is successful only if:

1. the full lifecycle script runs end to end
2. restart does not produce conflicting statuses
3. completion cannot bypass evaluator and operator review
4. denial and resume are explicit, reviewable transitions
5. the operator can understand the state without transcript archaeology

## Failure interpretations

If the prototype fails, use these interpretations:

- if state is unclear after restart: the source-of-truth model is wrong or not
  consistently applied
- if denial and resume are awkward: the runtime or approval model is too implicit
- if completion logic is confusing: the acceptance contract is too abstract
- if operators need raw run detail all the time: the Node/Run split may be too
  complex for MVP
- if metrics are unused: remove them from MVP instead of preserving symmetry

## Next document after this

If this prototype succeeds, the next document should be a true implementation
tech spec for:

- object schemas
- event schemas
- projection/recovery rules
- UI contracts
- scenario tests

If this prototype fails, the next document should be a simplification memo, not
the full tech spec.
