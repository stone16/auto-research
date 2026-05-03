## Review of Candidate (iter 9) vs Retained Best (iter 13)

### Strengths
- **Q13 is now a structured table** (`q13.f1`–`q13.f8`) with `shared contract`, `corpus evidence`, `domain-isolated boundary`, and an explicit `hooks_to_q14_q15` column. Retained best leaves Q13 as a prose paragraph, so the candidate is materially better here for cross-domain integration discipline.
- **Q14 dependencies and Q15 prophylactics now cite `q13.f*` IDs** (e.g., `q15.fm1` cites `q13.f1`/`q13.f2`/`q13.f4`/`q13.f7`; `q14.m1` cites the f-set explicitly). This fulfills the cross-question hook requirement more rigorously than retained.
- **Benchmark answer citation arrays are richer**: q1, q2, q3, q4, q11, q13, q14, q15 all carry more `file:line` anchors than retained. Retained dropped to ~3–6 citations per answer; candidate restores 8–17.
- Stable ID contract is extended to include `q13.f1`–`q13.f8`, improving cross-model evaluability.

### Regressions
- **Q1–Q4 architecture trace tables are collapsed from per-component rows (8/7/9/7 trace rows in retained) to a single row per domain.** Retained's `q1.trace1`–`q1.trace8` and `q3.trace1`–`q3.trace9`, plus the Q1/Q3 component-order tables, are the load-bearing mechanism for architecture grounding — every step had its own citation. Candidate compresses all anchors into one cell per domain, which sacrifices auditability.
- Lost Q1 component-order table (6 rows) and Q3 component-order table (9 rows) plus the prose 'trace lock' commentary that justifies the boundary.
- Q2 and Q4 trace tables (7 rows each in retained) are also collapsed.

### Net
Candidate trades architecture-grounding granularity for Q13 structure and citation breadth. The Q13 + cross-question hook gains are real, but the Q1–Q4 trace-row collapse is a meaningful regression on the dimension most central to the goal state ('State the from-scratch architecture of each domain subsystem … grounded in repo evidence'). Retain the iter-13 trace tables and merge candidate's Q13 table + answer citation expansions into the retained.
