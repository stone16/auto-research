## Judge Review (Stometa)

**Verdict:** candidate_better. The candidate's only substantive change vs the retained best is **Q13 promoted from a citation-stuffed paragraph to a structured 8-row table with stable IDs `q13.f1`–`q13.f8`**, each carrying shared_contract, corpus_evidence, domain_isolated_boundary, and hooks to Q14/Q15. This single change cascades into measurable improvements in two priority dimensions:

- **Cross-domain integration discipline:** Q14 milestones now name explicit `q13.f*` dependencies per row (e.g. `q14.m1` → `q13.f1,f2,f3,f4,f5,f7,f8`) instead of vague "Core credentials/artifacts." Q15 prophylactics replace "see Q13" with exact foundation IDs (e.g. `q15.fm1` → `q13.f1,f2,f4,f7`). Cross-question hooks are now machine-checkable.
- **Cross-model evaluability:** Eight new stable IDs make Q13 row-by-row scoreable, matching the discipline already established for traces, skills, cognition, milestones, and failure modes. The Stable Artifact ID Contract section was also updated to declare `q13.f*` as canonical.

**Minor flaws not blocking the verdict:**
- The Q13 markdown table header has 6 columns but the separator row has only 5 `---` segments. The data parses, but it is a cosmetic regression vs nothing.
- Q13 evidence introduces three new file references (`getuai-ui.md:18-32`, `openfang.md:39-70`, `optiminds-org-config.md:7-47`, `lawyer_finder.md:18-72`) that need to be corpus-verifiable. If any of these line ranges drift, citation discipline takes a hit — but on the candidate's face they look consistent with the corpus repos already cited elsewhere.
- Q1-Q12 are byte-identical to the retained best (good — no regression there).

**Why not a tie:** The retained best's Q13 prose makes the shared/isolated decision rule readable but not scoreable per foundation. The candidate makes each foundation independently auditable, which is exactly what the cross-model evaluability dimension asks for. This is a meaningful upgrade, not novelty.

**Priority dimension furthest from goal:** Architecture grounding. Q1–Q4 are already strong, but the architecture-trace contract still privileges component-granular cites; the *disagreement* claim in Q1 ("`getuai-seo` is a three-service product") could be tightened with a service-count file:line, and Q4's claim that the corpus rejects a universal social adapter would benefit from a direct counter-evidence cite where someone tried it and failed (rather than only the Gateway adapter cite).
