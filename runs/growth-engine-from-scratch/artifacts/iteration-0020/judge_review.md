## Iteration 20 vs Iteration 19

**KB body**: Tables (Q1 component, Q3 component, Q5-Q8 skill catalog, Q9-Q12 cognition, Q13 foundations, Q14 build sequence, Q15 failure modes) are byte-identical between candidate and retained best. Same row counts, same file:line anchors, same hook IDs.

**Q12 lock**: Candidate trims wording from `disjoint from`/two-sentence form to a single semicolon-joined `not X` form. Same anchors, same independence claim - cosmetic only.

**Benchmark answers**: This is the only meaningful delta.
- Candidate answers are more *concrete and operational*: q5 names the nine skills ("campaign console, keyword tracking, content optimization..."), q14 names actual deferrals ("no autopublish, no autonomous send, no budget mutation"), q12 explicitly states the disjoint-anchor independence claim in the answer text.
- Current-best answers are more *meta-descriptive* and carry inline file:line anchors directly in answer text (e.g., q1: ``getuai-plugin.md:11-20``, ``rankncompare.md:53-56``).
- The candidate trades inline file:line citations in benchmark answers for richer artifact-grounded content. The KB itself still carries every citation.

**Net**: Concrete artifact recap improves cross-model evaluability slightly (a verifier can check whether the nine skills/six milestones/nine failure modes are actually named). Removing inline file:line from answers is a citation-discipline regression at the answer surface but not at the KB surface.
