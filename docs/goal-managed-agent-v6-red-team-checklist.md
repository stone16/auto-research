# Goal-Managed Agent v6: Red-Team Checklist

## Purpose

This document turns the filtered foundations into a falsification checklist.

The goal is not to defend the current architecture. The goal is to find which
claims survive contact with a minimal real prototype, and which claims should be
downgraded, simplified, or removed before tech-spec freeze.

Use this alongside:

- `docs/goal-managed-agent-v6-foundations.md`
- `docs/goal-managed-agent-v6-wireframes.html`
- `runs/goal-managed-agent-orchestration-v6/`

## How to use this checklist

For each item:

1. Start from the current evidence class in the foundations doc.
2. Run the minimum falsification experiment.
3. Record the failure signal or pass condition.
4. Re-label the claim as one of:
   - `kept`
   - `downgraded`
   - `split`
   - `removed`
   - `still open`

Hard rule: discussion-backed claims do not become product invariants just because
they are elegant.

## P0: Resolve before tech-spec freeze

### RT-01: Single-KR lifecycle proof

- Claim: one governed KR can survive clarification, approval, launch, denial,
  replan, resume, verification, and acceptance without state ambiguity.
- Current evidence: run-backed as the next proof burden, but not yet built.
- Why this matters: this is the shortest path from research prose to product truth.
- Minimum falsification experiment:
  build one instrumented OAuth2-style KR prototype that exercises the full path,
  including one denied permission and one resume.
- Failure signal:
  any step depends on transcript reconstruction, manual hidden state, or human
  memory instead of explicit objects and events.
- If it fails:
  simplify the object model before writing more architecture prose.

### RT-02: Source-of-truth status really works

- Claim: the state layer can keep user-visible status coherent from durable state.
- Current evidence: partially contradicted by the real v6 run, which ended with
  stale `loop_status.json` while `state.json` and `results.tsv` had advanced.
- Minimum falsification experiment:
  kill and restart the prototype during active work, then verify that every
  status surface derives the same answer from one durable source of truth.
- Failure signal:
  any two status surfaces disagree after restart.
- If it fails:
  block UI spec freeze until status derivation is unified.

### RT-03: Judge can be bounded tightly enough

- Claim: rubric judging is useful if wrapped by invariants, calibration, and
  human review.
- Current evidence: mixed. Real v6 run persisted `dimension_scores`, but also
  emitted 10 invariant artifacts, with 6 `verdict_score_mismatch` hits.
- Minimum falsification experiment:
  replay a calibration set plus several real v6 contradiction cases, measure
  contradiction rate, human agreement, and escalation behavior.
- Failure signal:
  the judge still changes product state in ways that contradict score math or
  hides regressions without being caught and contained.
- If it fails:
  downgrade the judge to advisory status for more of the lifecycle.

### RT-04: Hybrid acceptance really needs three layers

- Claim: assertions + metrics + rubric is the right acceptance model.
- Current evidence: partial analogue only. The v6 run clearly exercised the
  rubric layer, but not an independent metrics layer.
- Minimum falsification experiment:
  prototype the same KR in three variants:
  - assertions + rubric
  - metrics + rubric
  - assertions + metrics + rubric
  and compare whether the metrics layer changes real decisions.
- Failure signal:
  the metrics layer duplicates assertions or never changes acceptance decisions.
- If it fails:
  cut or defer the metrics layer from MVP.

### RT-05: Node/Run split is worth the complexity

- Claim: user-visible Node plus mostly-hidden Run is better than a flatter
  objective/execution attempt model.
- Current evidence: discussion-backed.
- Minimum falsification experiment:
  model one workflow in two versions:
  - Node/Run
  - simpler Objective/ExecutionAttempt
  then test whether operators can understand progress, failure, and review
  without digging through internals.
- Failure signal:
  users repeatedly need run-level details to understand normal progress.
- If it fails:
  flatten the model before freezing schemas.

### RT-06: No-orphan invariant does not create fake goals

- Claim: exploratory work should always attach to a real or explicit exploratory
  objective; no orphan lane is needed.
- Current evidence: discussion-backed.
- Minimum falsification experiment:
  test ambiguous exploratory work such as market scan, compliance discovery, or
  architecture spike, and observe whether users can parent it honestly.
- Failure signal:
  users create low-quality placeholder goals just to satisfy the schema.
- If it fails:
  introduce a bounded orphan or inbox lane with audit semantics.

## P1: Resolve before broad prototype expansion

### RT-07: Contract-change reconcile is better than hard block or auto-fork

- Claim: when intent, acceptance, or policy changes mid-run, the right response
  is reconcile with continue/abort/restart, not hard block or silent version fork.
- Current evidence: discussion-backed.
- Minimum falsification experiment:
  edit parent acceptance and local policy while child work is running, then test
  whether reconcile stays understandable and auditable.
- Failure signal:
  budget semantics become unintelligible, or users cannot predict what survives.
- If it fails:
  narrow the editable surface or adopt explicit version branching.

### RT-08: Escalation can stay agent-driven

- Claim: `needs_human_review` and similar escalation can be decided by parent or
  child agent reasoning instead of structural rules.
- Current evidence: discussion-backed.
- Minimum falsification experiment:
  run adversarial cases where the child sees a real problem but the parent is
  tempted to suppress it for flow or score reasons.
- Failure signal:
  important human-review flags are suppressed, or noisy escalation overwhelms the
  operator because there is no deterministic floor.
- If it fails:
  add structural escalation rules for named event classes.

### RT-09: Progressive disclosure model matches actual operator workflows

- Claim: the three-layer render model is the right UI abstraction.
- Current evidence: discussion-backed, with an internal mismatch already noted by
  the wireframes: foundations "Layer 0" appears to split into Workspace Overview
  and Objective Tree in the actual UI exploration.
- Minimum falsification experiment:
  walk five common flows end to end in the wireframes or prototype:
  scan portfolio, inspect one objective, approve a risky action, compare two
  sibling runs, and repair blocked work after restart.
- Failure signal:
  common work requires jumping layers in unnatural ways, or the foundations and
  wireframes keep drifting apart.
- If it fails:
  rewrite the UI model before tech-spec freeze instead of forcing the UI to obey
  the old abstraction.

### RT-10: "One accountable owner" survives team reality

- Claim: one accountable owner per objective is the invariant across solo, small
  team, and larger-organization use.
- Current evidence: run-backed directionally, but not product-validated.
- Minimum falsification experiment:
  model a workflow with compliance reviewer, engineering owner, and operations
  approver, then test whether a single owner still reflects reality.
- Failure signal:
  important decisions are routinely owned by different people at different stages.
- If it fails:
  keep one primary owner but add explicit secondary approval roles to the model.

## P2: Resolve before org-scale claims

### RT-11: Same lifecycle skeleton for runtime and evaluator plugins

- Claim: runtime adapters and evaluator providers should share one plugin
  lifecycle skeleton.
- Current evidence: discussion-backed plus research support from the retained
  best v6 knowledge base.
- Minimum falsification experiment:
  implement one runtime adapter and one evaluator provider against the same
  manifest, activation, cleanup, and scope rules.
- Failure signal:
  one side needs a materially different lifecycle or permission contract.
- If it fails:
  split plugin families instead of preserving symmetry for elegance.

### RT-12: Single-sentence Node is expressive enough

- Claim: a Node can be expressed as a single sentence, with the rest delegated to
  acceptance, docs, and artifacts.
- Current evidence: discussion-backed.
- Minimum falsification experiment:
  create Nodes for three very different domains:
  coding, content migration, and policy/compliance review.
- Failure signal:
  the sentence becomes a label while the real intent repeatedly leaks into
  side documents or chat context.
- If it fails:
  relax the field contract before schemas harden.

## Evidence-driven housekeeping discovered during filtering

These are not red-team hypotheses; they are factual sync tasks already exposed by
the current docs:

- `docs/goal-managed-agent-v6-wireframes.html` had a stale plateau number
  `0.86`; this pass corrects the displayed values to v5 best `0.89` and v6 best
  `0.90`, and future doc sync should preserve those numbers.
- The wireframes already note that foundations §14 and the explored UI split are
  not fully aligned; that mismatch should stay visible until the UI model is
  either updated or explicitly rejected.
- The real v6 run proved the value of invariant guards and judge contradiction
  capture, but it did not prove that the full future ontology is implementation-ready.

## Exit criterion

This checklist is "done" only when every P0 item is labeled `kept`, `downgraded`,
`split`, or `removed` with written reasoning.

If most P0 items remain `still open`, the correct next move is not broader tech
spec prose. It is a smaller prototype.
