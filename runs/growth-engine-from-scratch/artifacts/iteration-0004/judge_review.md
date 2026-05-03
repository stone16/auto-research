## Candidate vs Current Best

**Net improvements in candidate:**
- Cognition table now carries stable row IDs `q9.cog1`-`q12.cog5` as a first column, mirroring the `q1.trace*`/`q3.trace*` pattern. This is a direct lift for cross-model evaluability — judges can score row-by-row instead of by free-text matching.
- Q15 benchmark answer now invokes a specific cognition row by ID (`q12.cog1 "Universal social adapter without per-channel policy/gating"`) as an explicit cross-question hook, strengthening Q15 ↔ Q12 integration.
- `q9.cog3` failed-here citations widened from single lines (`growth-engine.md:8`, `:27`) to ranges (`:7-13`, `:23-30`), which is more defensible under the citation policy.
- Q6 benchmark answer flags multilingual handling and evaluation-rubric discipline as required contract gaps; Q7 explicitly defers A/B test orchestration; Q8 adds hashtag/mention/length policy parameterization. These tighten the answer-side specification without inflating the catalog.
- Q13 benchmark answer adds `approval` to the boundary list in the decision rule, matching the prose section.

**Regressions in candidate:**
- Q13 prose contains a typo `getu-ads.md:21-28` (current best uses correct `getuai-ads.md:21-28`). This is a broken citation under the file:line policy.

**Unchanged surfaces:** Q1-Q4 traces, Q5-Q8 skill catalog (still 34 rows / 8 columns / margin audit), Q14 build sequence, Q15 failure modes table, Q2/Q4 trace tables.

The stable-ID upgrade plus the explicit cross-question hook in Q15 are meaningful gains against named dimensions. The Q13 citation typo is a real but local regression that should be folded back rather than blocking the swap.
