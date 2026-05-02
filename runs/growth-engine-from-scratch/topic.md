# Topic Brief

Topic: Growth Engine From Scratch — Architecture, Reusable Skills, and Practitioner Cognition Synthesized from the getuai/ Corpus

## Scope

This run synthesizes from the ~64 repositories under `~/dev/getuai/` a from-scratch
playbook for building a growth engine: the architecture (how the system is wired),
the reusable skills (what units of work exist, how they are invoked and maintained),
and the practitioner cognitive models (what mental frames the people who built these
repos applied).

The deliverable is a `knowledge_base.md` that gives a small team starting Day 1 a
defensible build sequence and decision frame across four growth domains — SEO/GEO,
Content Writing, Ads management, Social media — plus the cross-cutting infrastructure
and failure-mode discipline that ties them together.

## Goal State

"Good understanding" means being able to:

- State the from-scratch architecture of each domain subsystem (SEO/GEO, Content,
  Ads, Social), grounded in repo evidence and acknowledging where repos disagree.
- Enumerate the reusable skills per domain with their invocation surface, input/output
  contract, state persistence, and maintenance signals.
- Name the practitioner cognitive models per domain with worked-here / failed-here
  evidence pairs.
- Specify the cross-domain shared infrastructure (identity, data, queue, observability,
  LLM gateway, human-in-loop) with explicit decision rule for shared-vs-isolated.
- Produce a Day-1 → Month-3 build sequence with explicit deferrals.
- Catalog cross-domain failure modes with per-domain evidence and prophylactic measures.
- Carry three structured artifacts embedded in `knowledge_base.md`:
  - `skill-catalog` table (≥32 rows, 8 columns) split across Q5/Q6/Q7/Q8 answers
  - `build-sequence` table (≥6 rows, 6 columns) embedded in Q14 answer
  - `failure-modes` table (≥8 rows, 7 columns) embedded in Q15 answer

## Non-Goals

- Code-from-scratch implementation. The KB is design knowledge, not code.
- Coverage of repos outside `~/dev/getuai/`.
- Treating any single existing project (including `getuai/growth-engine` and
  `getuai/growth-engine-legacy`) as the canonical answer. They are peer evidence
  among 64.
- Generic growth-marketing advice not grounded in the corpus.
- Live experimentation. The corpus IS the empirical evidence; this run does not run
  campaigns or A/B tests.

## Quality Dimensions

- **Architecture grounding**: Every architectural claim cites repo:file:line per §6.3
  citation tier.
- **Skill enumeration completeness**: ≥8 skills per domain in the embedded skill-catalog
  with all 8 columns populated.
- **Cognition evidence pairing**: Every named mental model has a worked-here AND a
  failed-here citation; unsupported models score 0.0 per §6.7.
- **Cross-domain integration discipline**: Q13/Q14/Q15 use cross-question hooks to
  Q1-Q12; Q15 cross-domain claims have per-domain evidence.
- **Citation discipline**: Tiered per §6.3 — Strong (file:line), Acceptable for B/A
  (digest with transitive file:line), Required for S band (direct file:line).
- **Cross-model evaluability**: Per-criterion scoring (§6.2) with stable IDs makes
  judge divergence diagnosable at the clause level.

## Ambiguities Resolved (Per Spec §8)

- §8.1: single 15-question run (cross-question consistency requires it).
- §8.2: Content Writing kept as separate domain.
- §8.3: three artifacts EMBEDDED in `knowledge_base.md`.
- §8.4: provisional anchors deferred for Path B; progressive crystallization per §6.10.
- §8.5: `growth-engine-legacy` stays in `source-failure-modes.md`, origin-tagged.
- §8.6 (deferred for Path B): OS sandbox + point-verify tool; honor-system risk accepted
  for early iterations until the harness lands the wrapper.

## Research Frame

Every iteration should improve `knowledge_base.md` along the 15-question matrix:

```
Architecture (Q1-Q4) → Skills (Q5-Q8) → Cognition (Q9-Q12) → Integration (Q13-Q15)
```

Per §7 layer-iteration grouping, iter-1 to iter-10 prioritize architecture; iter-11
to iter-20 prioritize skills; iter-21 to iter-30 prioritize cognition; iter-31 to
iter-40 prioritize integration. Producer is free to revise earlier-layer answers
when integration questions reveal contradictions (§6.6).

## Control Frame

The control loop: producer proposes a `knowledge_base.md` revision, judge scores
against §5 benchmark using §6 calibration rules, only score-improving changes are
kept. Per §7, cross-model validation runs at iter-1 anchor crystallization, every
threshold crossing, iters 5/15/30, and the final iteration.

---

## Run-Init Verification (Path B, 2026-05-02)

- ✅ All 10 `sources/source-*.md` digests composed from 64-repo `_raw/` extracts
- ✅ `benchmark.json` contains 15 questions extracted from spec §5
- ✅ `topic.md`, `program.md`, `run.json`, `knowledge_base.md` seeded
- ✅ Mock iteration completed; framework reads run cleanly
- ⏸ DEFERRED: provisional anchors (§6.10 — progressive crystallization)
- ⏸ DEFERRED: §8.6 OS sandbox + point-verify tool (honor-system risk accepted for early iters)
- ⏭ NEXT: trigger iter-1 with real producer/judge:

  ```bash
  uv run autoresearch loop runs/growth-engine-from-scratch \
    --producer codex --judge claude \
    --tag growth-v1 \
    --max-total-iterations 40 \
    --dimension-threshold 0.80
  ```
