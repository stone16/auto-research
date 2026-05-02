# LLM Auto Research Program

You are running a bounded research loop for this topic:

**Growth Engine From Scratch — Architecture, Reusable Skills, and Practitioner Cognition Synthesized from the getuai/ Corpus**

## Primary Research Lanes (3 layers × 4 domains + 3 integration = 15 questions)

### Architecture Layer (Q1-Q4)

- **Q1 (A1) SEO/GEO**: components, data flow, external dependencies, human-in-loop
  control points; converged pattern across `geo-aeo`, `geo-seo-v2`, `geowriter`,
  `getuai-seo`, `rankgale`, `rankncompare*`, `seo-poster`.
- **Q2 (A2) Content Writing**: pipeline stages (ideation → outline → draft → edit →
  publish → post-publish), LLM role per stage, human-review hooks, load-bearing vs
  stylistic choices.
- **Q3 (A3) Ads**: closed loop campaign feed → bidding → reporting → attribution →
  optimization; data model; platform-specific vs platform-agnostic boundary.
- **Q4 (A4) Social**: listen / post / schedule / engage / monitor decomposition;
  multi-platform abstraction (or honest "no abstraction"); rate-limit + credit
  accounting; content moderation insertion point.

### Skill Layer (Q5-Q8)

- **Q5 (S1) SEO/GEO Skills**: ≥8 skills with 8-column table (skill_name,
  originating_repo, path_reference, invocation_surface, input_schema, output_schema,
  state_persistence, maintenance_signals); duplicates identified with canonical pick.
- **Q6 (S2) Content Writing Skills**: same 8-column table; brittleness problem +
  mitigation technique per skill.
- **Q7 (S3) Ads Skills**: same 8-column table; platform-bound vs platform-agnostic
  per skill; abstraction contract; kill criteria.
- **Q8 (S4) Social Skills**: same 8-column table; cross-platform vs per-platform;
  parameterization; failure mode on platform API change.

### Cognition Layer (Q9-Q12)

- **Q9 (C1) SEO/GEO Cognition**: ≥3 mental models with worked-here + failed-here
  pairs; ≥2 anti-patterns.
- **Q10 (C2) Content Writing Cognition**: ≥3 frames with cross-question hooks to
  Q2/Q6.
- **Q11 (C3) Ads Cognition**: ≥3 models with platform-change survival/failure pairs;
  kill-vs-scale criteria.
- **Q12 (C4) Social Cognition**: ≥3 models including automation visibility cost;
  per-platform repo evidence required.

### Integration Layer (Q13-Q15)

- **Q13 (I1) Shared Foundations**: ≥6 shared foundations with corpus evidence from
  ≥2 repos each; explicit decision rule for shared-vs-domain-isolated.
- **Q14 (I2) Build Sequence**: ≥6 milestones (Day-1 / Week-1 / Week-2 / Week-4 /
  Week-8 / Week-12) with scope + dependencies + done_criteria + next_trigger;
  cross-references Q1-Q13; ≥3 explicit deferrals; embedded `build-sequence` table
  artifact.
- **Q15 (I3) Failure Modes**: ≥8 failure modes; per-domain evidence for cross-domain
  claims (q15.r3 weight 1.5); ≥3 modes from `growth-engine-legacy`; embedded
  `failure-modes` table artifact.

## Hard Rules (from spec §6 calibration)

- Treat `knowledge_base.md` as the primary artifact you are improving. The 3 embedded
  artifact tables (skill-catalog quadrants, build-sequence, failure-modes) are part
  of `knowledge_base.md`, not separate files.
- Citations follow §6.3 tiered system: Strong (`repo/path:LINE`), Acceptable for B/A
  (`source-*.md§<section>` ONLY when the digest section transitively contains
  `file:line`), Required for S band per `must_include` (direct `repo/path:LINE`).
- Every `must_include` term must be used in its rubric meaning, not just present —
  per §6.4 anti-keyword-gaming.
- All 15 questions' `required_sources` MUST be cited; missing 1 caps at C/0.69,
  missing 2+ caps at D/0.49 (§6.5).
- For Q9-Q12 cognition, mental models without worked-AND-failed evidence pairs score
  0.0 in their slot (§6.7). ≥1 unsupported model present caps at B (0.84); 0 paired
  models caps at D (0.49).
- Cross-question contradictions reduce both implicated questions by 0.05 (§6.6).
- Per-criterion scoring (§6.2) is mandatory; emit per-criterion vector keyed by stable
  IDs (`q<N>.r<M>`, `q<N>.p<M>`, `a<N>.c<M>`) in `judge_feedback.md`. Holistic gestalt
  scoring is forbidden.
- For each strategy or pattern claim, use this skeleton:

  1. Pattern hypothesis
  2. Repos that exhibit it (≥2 with file:line evidence)
  3. Where it disagrees with other repos (if any)
  4. Why it converged (or didn't) — structural cause
  5. Failure modes when this pattern is applied wrongly
  6. Recommendation: keep / question / reject for from-scratch design

## Workflow Per Iteration

1. Read `judge_feedback.md` from prior iteration to identify lowest-scoring criteria.
2. Focus the iteration's `knowledge_base.md` revision on those criteria first.
3. Maintain the 3 embedded artifact tables — every iteration that updates KB content
   for Q5-Q8 / Q14 / Q15 MUST update the corresponding table.
4. Cite every claim with §6.3-tier-appropriate citations.
5. Mark each citation's tier in KB (`tier: digest` or `tier: file:line`) for §8.6
   citation provenance audit.
6. After iteration, judge scores per §5 rubric_criteria + §6.11 artifact criteria,
   emits per-criterion vector.
7. Per §7 cross-model validation: at iters 5/15/30, the OTHER model re-judges; at any
   `dimension_threshold` first crossing, the OTHER model confirms; final iteration
   requires fresh-session both-model consensus.
