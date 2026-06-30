# Framework Dossier Template

Status: template
Date: 2026-06-28

## Header

| Field | Value |
| --- | --- |
| Framework | <name> |
| Repository | <url> |
| Pinned SHA | <sha> |
| INSTRUMENT_HASH | <hash> |
| Security gate | PASS/FAIL/N/A |

## Dossier Dimensions

### 1. Boot outcome

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 2. Ingestion behavior

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 3. Retrieval behavior

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 4. Tenant isolation mechanism

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 5. Permission/ACL model

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 6. Data model reconstruction

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 7. Generation and citation

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 8. Tool/MCP surface

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 9. Observability and eval

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 10. Extraction candidates

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 11. License posture

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 12. Benchmark grid result

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

### 13. Gaps vs target design

Evidence:

- repo/file:line: <required where code claim is made>
- transcript: <path where runtime claim is made>

Findings:

- <finding_id or none>

## Seven-Dimension Benchmark Grid

| Dimension | Capability level | Earned maturity | Verdict | Transcript evidence | Finding ids |
| --- | --- | --- | --- | --- | --- |
| R retrieval+citation | <0-3> | <0-3> | PASS/PARTIAL/FAIL | benchmark/runs/<framework>/ | <ids> |
| I tenant isolation | <0-3> | <0-3 or N/A> | PASS/FAIL/N/A | benchmark/runs/<framework>/ | <ids> |
| P permission scope | <0-3> | <0-3 or N/A> | PASS/FAIL/N/A | benchmark/runs/<framework>/ | <ids> |
| N no-answer | <0-3> | <0-3> | PASS/PARTIAL/FAIL | benchmark/runs/<framework>/ | <ids> |
| M multilingual | <0-3> | <0-3 or N/A> | PASS/PARTIAL/FAIL/N/A | benchmark/runs/<framework>/ | <ids> |
| A multi-agent/tool | <0-3> | <0-3 or N/A> | PASS/FAIL/N/A | benchmark/runs/<framework>/ | <ids> |
| F freshness | <0-3> | <0-3> | PASS/FAIL | benchmark/runs/<framework>/ | <ids> |

## Findings View

Rows here mirror docs/ekb-research/findings/ledger.md. Do not create dossier-only findings.
