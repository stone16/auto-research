## Iteration 7 Review

**Wins**
- Adds an explicit `Clause-Level Evaluation Anchors` table with stable IDs (`q1.r1`, `q9.c1`, etc.) plus a `source vector` per row. This is the single biggest cross-model evaluability gain in the artifact's history — different judges can now score the same anchor.
- Embeds rubric contract in compact form alongside the new clause-anchor table.
- Benchmark answers now lead with `[q1] Answer:` style prefixes which trace cleanly back to anchors.

**Regressions**
- **Q5 SEO skill catalog dropped from 9 → 8 rows**: `sitemap-robots-generator` (rankncompare publisher row) was deleted. The catalog now exactly meets the >=8 threshold with zero margin and loses the canonical static-publisher evidence that anchors Q1's content store claim and Q15's static-publisher-vs-GEO failure mode.
- **Q7 Ads skill catalog dropped from 9 → 8 rows**: `composite-campaign-build` was deleted. This skill demonstrated the partial-failure preservation pattern (campaigns/groups persist if ad creation fails) — a meaningful kill-criteria signal lost.
- **Q1–Q4 prose compressed** in a way that drops some hedging language (e.g., `getuai-seo` three-service framing, OpenClaw multi-platform abstraction nuance, `lawyer_marketing` read/write split detail). Same evidence, less argumentation.
- **Citation paths shortened** via an Evidence Policy that requires the reader to mentally prepend the `runs/growth-engine-from-scratch/sources/_raw/` prefix. Still file:line tier per §6.3, but reduces auditability — the current best's full paths are easier to grep against the repo.
- **Q9–Q12 cognition condensed to one-line entries**: the `- Decision shaped:` / `- Trigger condition:` / `- Worked here:` / `- Failed here:` bullet structure was collapsed into prose. All four clauses still appear but parsing is harder for a judge.

**Net**
The clause-anchor table is a real contribution. But the skill-row deletions and prose compression cost more than the anchor table adds. The retained best should absorb the anchor table without accepting the regressions.
