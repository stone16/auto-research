## Candidate vs Current Best

**Wins**
- **Q1 architecture trace lock**: candidate adds an explicit 6-row component table (crawler/search adapter → ranking signal source → GEO evaluator → content store → publisher → human-in-loop), each with input/state/output/citation columns, plus q1.trace8 (content optimization generator → human review). The current best stops at a 7-row trace.
- **Q3 architecture trace lock**: candidate adds q3.trace9 (cross-platform analyst → kill-vs-scale rec) and a 9-row component table that explicitly separates platform-bound (Google Ads adapter, credentialed mutations) from platform-agnostic (ResultEnvelope, anomaly detection, attribution, kill criteria). The current best lacks the boundary table.
- **Benchmark answers**: candidate writes substantive prose answers (e.g., q1 names the convergence + the three-way disagreement; q3 enumerates the data model and the boundary). The current best emits meta-pointers ("KB Q1 answers...") which are not directly evaluable by another model.
- **Architecture Trace Contract** preface: explicitly declares the read-grammar for traces, raising reproducibility for cross-model evaluators.

**Parity**
- Skill catalog (34 rows, margin audit), Q9–Q12 cognition pairs, Q13–Q15 tables are byte-equivalent.

**Gaps still present in candidate**
- Q9–Q12 remain dense prose; not yet a structured worked/failed table — this is the weakest dimension for cross-model evaluability of cognition.
- Q13/Q14/Q15 do not yet wire explicit `↔ Q#` cross-question hooks, so cross-domain integration discipline is implied rather than mechanical.
- Q2 and Q4 did not get the same component-level trace-lock table treatment as Q1/Q3 (asymmetric depth).
