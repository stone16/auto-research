## Pairwise Review (iter 14 vs iter 13)

**Net change: candidate strictly improves on three axes with no regressions.**

### Concrete deltas vs retained best
1. **Q13 promoted from prose to stable-ID table** (`q13.f1`-`q13.f8`) with six columns including an explicit `hooks_to_q14_q15` column. The retained best Q13 is a single dense paragraph — judges cannot score row-by-row.
2. **Q2 and Q4 gain component-order tables** (8-row content workspace; 7-row social control plane) matching the schema already used for Q1/Q3. Architecture grounding is now symmetric across all four domains.
3. **Q14 milestones now name `q13.f*` dependencies** explicitly (e.g., `q14.m1` cites `q13.f1`/`q13.f3`/`q13.f7`/`q13.f8`; `q14.m3` cites `q13.f6`). Retained best uses only generic phrases like "Core + LLM gateway."
4. **Q15 prophylactics cite Q13 rows** (e.g., `q15.fm1` -> `q13.f1`/`q13.f2`/`q13.f4`/`q13.f7`; `q15.fm5` -> `q13.f1`/`q13.f3`). Retained best says "see Q13" generically.
5. **Stable Artifact ID Contract** updated to enumerate `q13.f1`-`q13.f8` alongside the other ID families.
6. Minor: `content.skill1` input schema widened to `placeholders/style variables`; cognition synthesis explicitly adds observability and LLM routing to shared infra.

### What still ranks lowest
Cross-domain integration discipline is now the strongest axis but still has slack: not every Q14 row enumerates *all* Q13 dependencies (e.g., `q14.m2` mentions `q13.f2`/`q13.f3` but omits `q13.f5` observability and `q13.f7` approval, both of which the artifact would touch). Tightening Q14 dependency completeness would be the next move.

### No regressions
All IDs from iter 13 are preserved. Skill catalog row counts unchanged (9/8/9/8). Cognition table unchanged. Q15 row count unchanged.
