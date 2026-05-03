## Review

**What changed vs. retained best:** Q9-Q12 cognition is converted from four prose paragraphs into a single 20-row structured table with columns `domain | model_name | trigger | worked_here | failed_here | anti_pattern | hook_to_skill_or_failure_mode`. Q1-Q8 and Q13-Q15 are unchanged.

**Strengths:**
- Every cognitive model now has an explicit trigger column, removing ambiguity about when to apply each model.
- Worked-here and failed-here citations are in dedicated columns — no narrative reconstruction needed by reviewers.
- The `hook_to_skill_or_failure_mode` column enforces cross-question discipline mechanically, naming Q1/Q5/Q7/Q14/Q15 references per row.
- 20 cognition rows vs ~24 named models in the old prose; coverage is preserved while every row meets the worked/failed pairing rule. Unsupported claims are explicitly excluded (stated in preamble).
- The cognition synthesis paragraph at the bottom of the table reframes the discipline correctly: trigger → evidence pair → control hook.

**Weaknesses / unchanged gaps:**
- Cognition rows lack stable IDs (e.g., `q9.cog1`, `q11.cog3`) which would lift Cross-model evaluability further. Q1-Q4 trace rows already use `qN.traceK`; cognition table should follow.
- The benchmark answer summary text changed only slightly ("row-scored" / "unified cognition table") — answers could explicitly cite row IDs once they exist.
- Q9 row for E-E-A-T cites `growth-engine.md:8` which is a single line, weaker than other rows that cite ranges.

**Net:** Real structural win on cognition with no regressions elsewhere.
