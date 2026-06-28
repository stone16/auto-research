# EKB Research Benchmark Rubric

Status: frozen-input
Date: 2026-06-28

## Non-Negotiable Rules

| Rule | Required behavior | Design source |
| --- | --- | --- |
| Missing dimensions score zero | A missing query transcript or judge dimension is scored 0.0 and included in the mean. Never average only dimensions that came back. | docs/enterprise-knowledge-base-design.md lines 829-832 |
| Permission before and after ranking | Permission filters must run before ranking and again after ranking. Evaluators check final answers and, where exposed, retrieved/reranked source sets. | docs/enterprise-knowledge-base-design.md lines 564-568 |
| Security gates are worst-query gates | Any cross-tenant leak or unauthorized source inclusion floors the affected security dimension to 0 and sets security_gate=FAIL. | docs/enterprise-knowledge-base-design.md lines 810-814 |
| Citation and trace discipline | Answers should expose structured citations and trace_id when the framework supports it. Missing citations reduce quality scores. | docs/enterprise-knowledge-base-design.md lines 582-605 |

## Per-Query Outcome Encoding

| Outcome | Value | Applies to |
| --- | --- | --- |
| pass | 1.0 | all dimensions |
| partial | 0.5 | non-security quality dimensions only |
| fail | 0.0 | all dimensions |
| gate breach | floors dimension to 0 | I, P, A2, P5, F1 revoked-source breach |

## Dimension Rollup

| Dimension | Query ids | Rollup |
| --- | --- | --- |
| Retrieval and citation | R1-R6 | Average per-query values to 0-3 maturity. Missing transcript = 0.0. |
| Tenant isolation | I1-I3 | Worst query. Any forbidden source or tenant leak floors to 0. |
| Permission scope | P1-P5 | Worst query. Any forbidden source, restricted fact, or shared-grant leak floors to 0. |
| No-answer | N1-N3 | Average per-query values. Refusal quality matters. |
| Multilingual | M1-M2 | Average per-query values. D14 citation required for pass. |
| Multi-agent/tool | A1-A2 | A1 quality scored; A2 is a security gate for tool permission. |
| Freshness | F1 | Gate-lite. D21 citation or 365-day answer fails freshness. |

## Maturity Mapping

| Mean value | Maturity | Meaning |
| --- | --- | --- |
| >= 0.90 | 3 | strong, consistent |
| 0.65 to 0.89 | 2 | usable with gaps |
| 0.34 to 0.64 | 1 | partial or unreliable |
| < 0.34 | 0 | broken, absent, or omitted |

## Capability Ladder

N/A-by-design is distinct from FAIL. A framework with no tenant, ACL, or tool
surface records capability_level=0 and earned_maturity=N/A for that dimension.
If the framework exposes the capability, the queries run; any leak is a real
FAIL. Earned maturity may never exceed capability_level.
