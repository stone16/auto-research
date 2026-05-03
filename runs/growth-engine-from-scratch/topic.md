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

---

## Run Outcome (v1.0, 2026-05-03)

- ✅ **Iteration 6 is the kept best at score 0.98** — `last_kept_experiment: embed evaluation rubric and upgrade cognition pair clauses`
- ✅ KB at 51,533 chars (309 lines): all 15 questions answered with structured artifacts (32-row skill-catalog across Q5-Q8, 6-row build-sequence in Q14, 9-row failure-modes table in Q15) and tier:file:line citations throughout
- ✅ Embedded **Evaluation Rubric Contract** (KB §"Evaluation Rubric Contract") — producer engineered cross-model evaluability per §6.2 directly into the KB so different judges compare at the same clause level
- ✅ 10 iterations attempted; framework kept iters 1 (0.85), 2 (0.90), 6 (0.98) and discarded 3-5, 7-10 — cybernetic keep/discard gate worked as designed
- ✅ Judge invariant guard caught real regressions: iter-2 `unacknowledged_regressions`, iter-9 `verdict_score_mismatch` (auto-demoted to tie)
- ✅ Source payload trimmed from 1.9 MB to 176 KB via `--max-bytes-per-repo 2500` (PR #6); fits codex's 1 MB input cap with margin

### Known v2 candidates (carried forward from iter-2 judge feedback, not fully closed at iter-6)

- **Vertical-case repos under-represented**: `lawyer_finder`, `cuilawgroup`, `law-intake` are listed in `source-vertical-cases.md` but rarely cited in the KB body (only `lawyer_marketing` is). A v2 run could pull these in for richer industry-pack evidence.
- **Citation reuse**: a few line ranges (e.g., `getuai-seo.md:101-106`) are cited multiple times across questions. Deeper sections of the raw extracts could be mined.
- **Per-criterion stable-ID rubric**: spec §6.2 introduced `q<N>.r<M>` IDs in `benchmark.json`, but the KB's Q1-Q4 architecture answers don't carry inline rubric anchor IDs the way the embedded Evaluation Rubric Contract table does. Cleanup opportunity for v2.
- **Loop convergence at iter-6**: producer plateaued; iters 7-10 all regressed below the 0.98 baseline. Increasing source diversity (e.g., adding a small LLM-driven re-composition pass on top of the digests) could unstick the producer.

### Status

- Tag: `growth-v1.0` on branch `autoresearch/growth-v1-dryrun`
- Stop reason: `max_total_iterations` cap (10); `dimension_threshold` 0.95 was not fully met across all dimensions despite best_score 0.98
- Total cost: ~10-11 codex producer calls + ~10 claude judge calls; ~4 hours wall clock

---

## Run Outcome (v2.0, 2026-05-03)

- ✅ **Iteration 19 is the kept best at score 1.0000** — `last_kept_experiment: shorten Q12 failed-anchor lock`
- ✅ **Broke past v1's 0.98 plateau**: trajectory 0.485 → 0.87 → 0.88 → 0.92 → 0.93 → discards → 0.95 (iter-11) → discards → 0.95 (iter-15) → discards → **1.0000 (iter-17, 18, 19)**
- ✅ **9 of 19 post-iter-1 iterations kept** (~47% keep rate vs v1's 37%); 10 discarded by the cybernetic gate
- ✅ KB consolidated, didn't bloat: v1 iter-6 = 51 KB → v2 iter-19 = 28 KB. Producer found an information-density optimum.
- ✅ Judge invariant guard caught 3 `verdict_score_mismatch` violations (auto-demoted to ties); 3 judge fallbacks to deterministic scoring (judge CLI exited code 1 on those iters)

### How v2 fixed v1's documented gaps

- ✅ **Per-criterion stable IDs in body**: q9.cog1..q12.cog5 (cognition rows), q13.f1..q13.f8 (foundations), q14.m1..q14.m6 (milestones), q15.fm1..q15.fm9 (failure modes), plus per-skill IDs in Q5-Q8. The spec §6.2 stable-ID vision is now baked into the KB body, not just the embedded Evaluation Rubric Contract.
- ✅ **Vertical-case coverage**: `lawyer_finder` cited 2x (was 0 in v1), `cuilawgroup` cited 1x (was 0), `lawyer_marketing` 7x (anchor case). `law-intake` still uncited (small repo, thin even at 5K budget).
- ✅ **Citation depth**: iters 13/14/18 narrowed file:line ranges to specific worked-vs-failed contrasts on independent code regions (e.g., q12.cog2 worked-here at `reddit-scount.md:124-181` vs failed-here narrowed from `:141-181` to `:145-162`).
- ✅ **Q1/Q4 architecture asymmetry**: explicit component-by-component trace tables added in iters 2/6/16; Q3 also got a 9-row order/component/state/output/citation table.

### v2 setup that enabled the breakthrough

- Source budget bumped 2500 → 5000 bytes/repo (`scripts/compose_sources.py --max-bytes-per-repo 5000`); total source payload 176 KB → 300 KB, well under codex's 1 MB cap.
- State.json reset to `iteration=0, best_score=0.0` to let producer climb from a fresh score gate.
- Live KB started at v1's iter-6 content (51 KB) as producer's baseline; v2 builds on v1, doesn't restart.
- Mid-run framework patch landed (PR #8): `models.py` now accepts `experiment` as alias for `experiment_title` (codex returned shorthand on iters 2-4 of v2's first attempt, halting the loop after 3 consecutive crashes).

### Known v3 candidates (carried forward from v2 judge feedback)

- **`law-intake` still uncited**: small repo, 5K budget didn't help. Either drop from source-vertical-cases or pull a different excerpt that's substantive.
- **`growth-engine` cited 30+ times in cognition; some other repos under 3 citations**: distribution skew. Could be a feature (rich repo gets more attention) or bug (other repos under-mined).
- **Iter-20 attempted compression and was rejected**: producer was probing an information-density limit. A v3 with a higher iteration budget AND tighter rubrics might find further compression without losing structure.
- **3 `judge_review.md` fallbacks to deterministic scoring**: Claude CLI exited code 1 on iters 12 (post-discard), 13, 14. Investigate whether claude is hitting timeout/rate-limit, or whether the judge prompt got too large.

### Status

- Tag: `growth-v2.0` on branch `autoresearch/growth-v2`
- Stop reason: `max_total_iterations` cap (20); 3 consecutive iterations at 1.0000 (iters 17/18/19) effectively saturated the producer-judge agreement
- Total cost: ~20 codex producer calls + ~20 claude judge calls + 3 deterministic judge fallbacks; ~3.5 hours wall clock for the resumed run + ~12 minutes for v2's first crashed attempt
