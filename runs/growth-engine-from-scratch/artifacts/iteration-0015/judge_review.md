## Candidate vs Retained Best (iter 15 vs iter 14)

**Real gains**
- **Q1 disagreement evidence is now explicit.** Candidate adds `getuai-seo.md:52-83` (UI/MCP/AI three-runtime) and `growth-engine-legacy.md:45-49` (Browser→Core counter-position) both in-KB and in the q1 benchmark `citations` array. The retained best stated the disagreement in prose without anchoring the counter-position to a line range.
- **Q4 policy breakers grounded.** Candidate adds `openclaw-marketing.md:124-126` (`dmPolicy='pairing'`, explicit `allowFrom`) and `openclaw-marketing.md:158` (per-channel chunking) to both the Q4 prose and the q4 benchmark citations. Retained best had only the broader 122-158 range.
- **Evidence Policy now forbids source-ID-only citations.** New line: "Benchmark answers must carry explicit file:line anchors, not source IDs alone." This is a stated policy that matches the §6.3 Strong tier.

**Real losses**
- **Q3 second component table dropped.** Retained best carried a 9-row `order | component | input | state | output | citation` table for Ads after the trace table. Candidate keeps only the trace table. The Q1 equivalent table is retained. This is an architecture-grounding redundancy regression — the same information lives in `q3.trace1`-`q3.trace9`, but the structured second view that judges scored on Q1 is no longer parallel for Q3.
- **Q1 trade-off framing softened.** The retained best's closing sentence ("speed versus auditability… direct publishers ship quickly") is removed. Minor — the recommendation is still stated.

**Net**: the citation-discipline improvements target a stated quality dimension (§6.3 Strong) and the Q1/Q4 evidence anchors are concrete wins. The Q3 table loss is a structural regression but the underlying data is preserved row-by-row in the trace table.
