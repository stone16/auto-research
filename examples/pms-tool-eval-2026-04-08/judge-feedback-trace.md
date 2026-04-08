## Iteration 1

**Priority dimension**: Freshness
**Improvement suggestion**: Run a single batched live-verification pass that resolves every `needs-live-check` field for the top candidates by hitting GitHub's API for repo metadata (default branch, last commit SHA + date, stargazers_count, license, open issues, latest release tag) and the registry APIs (npm/PyPI/crates.io) for current install commands and latest published versions. Prioritize the 10 first-choice + 10 backup tools (20 repos total), then propagate the verified data into both the candidate entries and the `last_updated`/`stars`/`install` fields. This single pass would simultaneously raise Freshness, Candidate Depth, and Benchmark Testability scores.

### Review
## Catalog Review

**Strengths**
- All 10 modules have ≥3 candidates listed, with risk_manager and embedding_engine appropriately flagged as ecosystem gaps with documented evidence.
- Cross-module tools section is well-structured: pmxt, nautilus_trader, polybot, Polymarket/agents, and caiovicentino/polymarket-mcp-server each have explicit coverage boundaries.
- First-choice/backup recommendations exist for every module with clear rationales tied to the source corpus.
- Known gaps (kalshi-python, OSS risk library, embedding metadata, correlation detector sparsity) are explicitly enumerated.

**Weaknesses**
- **Pervasive `needs-live-check` placeholders**: install commands, last_updated, stars, and api_docs are unverified for the majority of candidates. Only py-clob-client (2026-03-29) and rs-clob-client (2026-03-30) have verified recency.
- **Embedding engine entries are skeletal**: sentence-transformers, FinBERT, and spaCy all have `repo: needs-live-check` — these are well-known projects whose metadata could be verified trivially.
- **Test coverage is `unknown` everywhere** — no candidate has been profiled for CI status, license, or auth requirements needed for harness automation.
- **Freshness signals are weak**: catalog dates from 2026-04-07 but only 2 of ~25 candidates have 2026 timestamps. The rest are frozen-corpus assertions without live verification of repo activity, breaking changes, or API versions.
- The frozen-corpus boundary is honest but limiting — the catalog reads more as a literature survey than a benchmark-ready evaluation matrix.

## Iteration 2

**Priority dimension**: Benchmark Testability
**Improvement suggestion**: Add two structured fields to every candidate: (1) `auth_model` capturing the concrete authentication mechanism (e.g., 'EIP-712 signed orders + API key/secret/passphrase' for py-clob-client, 'RSA private key + API key ID' for kalshi_python_sync, 'none' for sentence-transformers), and (2) `primary_endpoints` listing the 2-3 critical REST/WebSocket URLs the harness will hit (e.g., 'https://clob.polymarket.com', 'wss://ws-subscriptions-clob.polymarket.com/ws/'). Also promote `kalshi_python_sync==3.11.0` and `kalshi_python_async==3.11.0` to full candidate entries under data_connector and order_executor with their own repo URLs and verification timestamps, since the deprecated kalshi-python should not remain the only Kalshi-side SDK in the catalog.

### Review
## Judge Review — Prediction Market Tool Catalog (2026-04-07)

**Strengths**
- All 10 modules have ≥3 candidates with first_choice/backup designations and rationale.
- Live verification (commit SHAs, release tags, open issues, PyPI/npm/cargo versions) is consistently captured as of 2026-04-07, giving strong freshness signals.
- Cross-module mapping is explicit (6 tools) with clear coverage boundaries, including pmxt, nautilus_trader, and the MCP server.
- Known gaps are documented with concrete build-vs-adapt implications (risk library gap, kalshi-python deprecation, correlation tooling sparsity).

**Weaknesses**
- `test_coverage` is `unknown` for every single candidate — a required field that is never populated, even where tests demonstrably exist (e.g., poly-websockets Vitest, nautilus_trader, sentence-transformers).
- Authentication requirements and API endpoint specifics are not captured as structured fields. py-clob-client notes "auth and signing setup is non-trivial" but no concrete auth model (EIP-712, API key + secret, OAuth) is recorded for automated harness wiring.
- kalshi-python is included as a Kalshi data_connector candidate despite being officially deprecated; the successor packages `kalshi_python_sync==3.11.0` / `kalshi_python_async==3.11.0` are mentioned in notes but not promoted to first-class candidate entries with their own repo, install, and verification fields.
- Embedding engine module leans heavily on general-purpose NLP tools; no prediction-market-specific embedding work or recent BGE/E5/Voyage-class models are evaluated.

**Verdict:** Catalog is benchmark-ready for a Phase 1 harness but the missing auth/test-coverage detail will cost time during automated wiring.

## Iteration 3

**Priority dimension**: Candidate Depth
**Improvement suggestion**: Resolve the universal `test_coverage: unknown` field by running each candidate's test suite (or scraping coverage badges/CI artifacts) and recording either a numeric percentage or a structured status like `tests_present: true, coverage_pct: null, ci_status: passing`. As a parallel pass, replace `last_updated: unknown` for kalshi_python_sync/async with the verified PyPI release date (2026-03-31) and `language: other` entries with their actual primary language detected from the repo's file mix.

### Review
## Catalog Review

**Strengths**
- All 10 modules have ≥3 candidates with first_choice/backup designations and rationales.
- Cross-module mapping section is explicit and includes coverage boundaries (e.g., pmxt has no risk layer, Kalshi SDKs are venue-native).
- Install commands, primary endpoints, and auth models are populated for nearly every candidate — directly supporting automated benchmark harness construction.
- Freshness is strong: most `last_updated` values fall within the last 60 days of 2026-04-07, and deprecated tools (kalshi-python, 0xalberto bot) are flagged.
- Known gaps section honestly documents the risk-library, correlation-detector, and test-coverage shortfalls.

**Weaknesses**
- `test_coverage` is `unknown` for **every** candidate — even where tests demonstrably exist (pmxt jest, poly-websockets vitest). This is the most consistent depth gap.
- `kalshi_python_sync` and `kalshi_python_async` have `last_updated: unknown` and `stars: unknown` because the declared `exchange-infra` repo is not browsable. No alternative freshness signal (PyPI release date, download counts) has been promoted into the structured fields.
- Several `language: other` entries (ent0n29/polybot, PaulieB14/polymarket-subgraph-analytics) leave the primary implementation language unspecified, weakening harness selection.
- A few candidate `notes` repeat boilerplate from cross-module reuse rather than module-specific justification (pmxt appears verbatim across data_connector, normalizer, arbitrage, executor).

## Iteration 4

**Priority dimension**: Candidate Depth
**Improvement suggestion**: Resolve the opaque repo-health signals for `kalshi_python_sync` and `kalshi_python_async` by (a) downloading the PyPI sdist/wheel and inspecting the bundled `tests/` directory and any embedded CI config to populate `tests_present` and `test_harness` from package contents, and (b) checking PyPI 'Project links', the docs.kalshi.com SDK page, and `pyproject.toml` metadata for the true source-repo URL — then update the `repo` field, stars, and `ci_status` accordingly. This converts the catalog's two highest-stakes Kalshi executor entries from partially-verified to fully-verified, closing the largest remaining Candidate Depth gap.

### Review
## Catalog Review

**Strengths**
- All 10 modules have ≥3 candidates with explicit first-choice/backup picks and rationales.
- Cross-module mapping is comprehensive (7 tools mapped with explicit boundaries).
- Freshness is strong: most candidates verified with 2026 timestamps and live PyPI/GitHub checks; deprecation of `kalshi-python` and removal of `0xalberto/polymarket-arbitrage-bot` are correctly reflected.
- Benchmark testability is high — install commands, endpoints, and auth models are present for nearly every candidate.

**Weaknesses**
- **Candidate Depth gaps**: `kalshi_python_sync` and `kalshi_python_async` carry `stars: unknown`, `tests_present: null`, and `ci_status: unknown` because the declared `exchange-infra` repo is not publicly browsable. These critical Kalshi-side executors are flagged `deeper-review` but lack independent repo-health verification.
- `coverage_pct` is `null` across the entire catalog — acknowledged in known_gaps but still a depth weakness.
- `ent0n29/polybot` and `PaulieB14/polymarket-subgraph-analytics` use `language: other` with a `language_detail` workaround rather than corrected primary language metadata.
- A few candidates (e.g., `Rimantovas/polymarket-rtds` with 3 stars, `sgdva/polyoddwatcher` with 4 stars) function more as filler to hit the ≥3 threshold than as serious benchmarkable options.

**Goal-state status**: All five done-definition criteria are met. The remaining work is depth-sharpening on the Kalshi successor SDKs and replacing low-signal filler candidates with stronger alternatives where they exist.

## Iteration 6

**Priority dimension**: Benchmark Testability
**Improvement suggestion**: For the next iteration, replace the universal `test_coverage: unknown` with a structured `test_evidence` object per candidate containing: (1) `test_command` — the exact command to run the project's tests after install (e.g., `npm test`, `pytest tests/`, `cargo test`), (2) `test_count` — number of test files or cases observed (already done for the two Kalshi SDKs at 162; do the same by inspecting the repo/sdist for the other ~20 candidates), (3) `ci_signal` — link to a passing GitHub Actions / workflow run or `none-found` if absent, and (4) `min_runtime` — pinned Node/Python/Rust version. Pair this with version-pinned, runnable install commands for the four thin entries (prediction-market-arbitrage-bot, prediction-market-backtesting, ent0n29/polybot, subgraph-analytics) so the catalog becomes directly executable by an automated benchmark harness without manual triage. Also fold `Polymarket/agents` and `caiovicentino/polymarket-mcp-server` into a module candidate list (or an explicit `secondary_tools` section) so every cross-module entry traces back to a fully-populated candidate record.

### Review
## Catalog Review — 2026-04-07

**Strengths**
- All 10 modules have ≥3 candidates with first_choice/backup recommendations and rationales.
- Cross-module mapping is explicit (7 entries) and clearly states coverage boundaries (e.g., pmxt lacks risk/backtesting, Kalshi SDKs are venue-only).
- Freshness is strong: most candidates updated within the last 60 days, deprecated `kalshi-python` is flagged with migration path to `kalshi_python_sync/async==3.11.0`, and a stale benchmark candidate (0xalberto/polymarket-arbitrage-bot) was explicitly retired.
- `live_verification` block with PyPI artifact-level checks (sdist test counts, setuptools exclude rules, build backend, license) is unusually rigorous and supports the private-repo Kalshi SDK claims.
- Known gaps section is honest about risk_manager, correlation_detector sparsity, and the test_coverage opacity.

**Weaknesses**
- `test_coverage` is `unknown` for **every** candidate. Even where tests are known to exist (pmxt jest, poly-websockets vitest, Kalshi 162 sdist tests), no numeric coverage % or even pass/fail signal is captured — this is the single most consistent gap and directly affects benchmark testability.
- Several candidates have install commands that are too thin to actually run a benchmark unattended: `npm install` (prediction-market-arbitrage-bot), `make install` (prediction-market-backtesting), `./start-all-services.sh` (ent0n29/polybot), `git clone …` (subgraph-analytics) — no version pin, no entry-point, no minimum runtime/Node/Python version stated.
- A few entries lack `language` precision (`other` for polybot and subgraph-analytics) and Python/Node/Rust version requirements are missing across the board (only kalshi_python_sync/async note `requires Python >=3.13`).
- `Polymarket/agents` and `caiovicentino/polymarket-mcp-server` are referenced in `cross_module_tools` but have **no entries in any module's candidates list** — they should either be promoted into a module or moved to a 'reference-only secondary tools' appendix so the cross-module table is grounded.
- Recommendations rationale is solid but does not state *why first_choice beats backup* in measurable terms (latency, coverage breadth, license, maintenance velocity) — it reads as qualitative judgment rather than benchmark-ready criteria.

**Verdict**: Catalog is near goal-state. The dominant blocker for the next iteration is verifiable per-candidate test/CI evidence, not coverage breadth.

## Iteration 7

**Priority dimension**: Candidate Depth
**Improvement suggestion**: In the next iteration, close the depth gap by populating two fields uniformly across every candidate: (1) `forks` (currently only Phase 1 modules have them — pull from GitHub API for the 15+ candidates missing it) and (2) `license` (SPDX identifier from each repo's LICENSE file or package metadata). Additionally, replace `test_coverage: unknown` with a concrete `tests_present: true/false` + `test_harness` pair (mirroring what was done for the Kalshi SDKs) by inspecting each repo's test directory or CI config — this is cheap to verify and converts an unknown into actionable benchmark signal. Finally, add a one-line build-vs-adapt suggestion for the risk_manager gap (e.g., 'adapt poly-maker's position-tracking module + layer Kelly sizing from polymarket-kalshi-weather-bot' vs 'build a thin standalone library') to satisfy goal-state criterion #5.

### Review
# Catalog Review (2026-04-07)

**Strengths**
- All 10 modules have ≥3 candidates with first_choice/backup and rationale documented.
- Live verification block (PyPI sdist/wheel inspection, GitHub stars/forks, docs gitSource) gives strong provenance for the Kalshi private-repo edge case.
- Cross-module mapping is explicit with coverage boundaries (pmxt, nautilus_trader, polybot, Kalshi SDKs, MCP server, etc.).
- Known gaps section honestly flags risk_manager and correlation_detector as ecosystem-level holes rather than papering over them.
- Freshness is strong: most candidates updated within the last 30–60 days; deprecations (kalshi-python, 0xalberto bot) are called out.

**Weaknesses**
- `test_coverage` is `unknown` for nearly every candidate, even where tests are clearly present (jest, vitest, pytest). This is the most consistent depth gap.
- Fork counts are present for Phase 1 modules but missing for embedding_engine, realtime_feed, data_normalizer, risk_manager, backtesting_engine, and analytics_dashboard candidates — repo health signal is uneven across modules.
- Several candidates lack license fields (only Kalshi SDKs surface package_license); license clarity matters for adapt-vs-build decisions.
- `prediction-market-backtesting` is flagged with “mixed licensing” but the actual license terms are not captured.
- Risk_manager gap is documented but no concrete build-vs-adapt suggestion is offered (goal state #5).

## Iteration 8

**Priority dimension**: Candidate Depth
**Improvement suggestion**: For each module's first_choice and backup candidate (20 entries total), run the documented test harness locally and replace `test_coverage: unpublished` with a measured line/branch coverage percentage from `pytest-cov`, `cargo tarpaulin`, `nyc`, or `vitest --coverage`. This converts the largest remaining 'unverified' field in the catalog into hard data and directly raises Candidate Depth toward 10.

### Review
## Catalog Review

**Strengths**
- All 10 modules have ≥3 candidates with explicit verdicts (deeper-review vs reference-only).
- Cross-module mapping is well-articulated with explicit boundary statements for each multi-module tool.
- Freshness signals are strong: most repos updated in 2026-Q1/Q2, with explicit notes when freshness lags (e.g., FinBERT 2022, kalshi-python 2025-03).
- Benchmark testability is excellent — install commands, primary endpoints, and auth models are populated for every candidate, sufficient for automated harness setup.
- Known gaps section honestly documents the risk-manager library void and the Kalshi private-repo opacity with concrete adapt-vs-build guidance.

**Weaknesses**
- `test_coverage` is `unpublished` for **every single candidate** — no numeric coverage % anywhere in the catalog. While `tests_present` and `test_harness` fields partially compensate, the depth dimension is bottlenecked here.
- Two Kalshi official SDKs (`kalshi_python_sync`, `kalshi_python_async`) have `stars`/`forks` as `private/unavailable` and `ci_status: unverifiable-private-repo`. Acceptable given the documented private-repo constraint, but it leaves a verification gap.
- A few candidates lack test harnesses entirely (`finbert`, `realtime_data_client`, `polymarket_rtds`, `btc_arb_bot`, `weather_bot`, `polyoddwatcher`, `subgraph_analytics`) — flagged honestly but limits Phase 1 confidence.
- `correlation_detector` module reuses arbitrage bots and an offline data framework as proxies; the gap is acknowledged but no novel candidate has been surfaced.

**Overall**: Catalog is near goal-state. The most actionable lift is converting `test_coverage: unpublished` into measured numbers for the top-2 first-choice/backup candidates per module, since those are the ones the harness will actually exercise.

## Iteration 9

**Priority dimension**: Candidate Depth
**Improvement suggestion**: Run measured local test/coverage harnesses (or document concrete blockers) for the next tier of high-priority candidates that still show `test_coverage: unknown`: `real-time-data-client` (Vitest/Jest), `nautilus_trader` (pytest with Polymarket adapter scope), `rs-clob-client` (`cargo test`), `poly-maker` (pytest), and at least one Kalshi official SDK (`kalshi_python_sync` smoke test under Python 3.13). For each, capture command + tests-passed + line/branch % (or explicit blocker reason) into `coverage_verification.results`, and resolve the two `language: other` entries to their actual primary language so automated benchmark dispatch can route them correctly.

### Review
## Catalog Review — 2026-04-07

**Strengths**
- All 10 modules now have ≥3 candidates with explicit verdicts and rationale.
- Cross-module mapping table is rich (7 tools) with clear coverage boundaries.
- Phase 1 priorities (`pmxt`, `py-clob-client`, `prediction-market-arbitrage-bot`) carry **measured** local line/branch coverage with reproducible commands and documented blockers — a major freshness lift.
- Recommendations are paired (first/backup) per module with concrete rationale, and known gaps explicitly call out the risk-manager and correlation-detector voids.

**Weaknesses**
- **Candidate Depth**: ~75% of candidates still carry `test_coverage: unknown`. Critical entries like `real-time-data-client`, `nautilus_trader`, `rs-clob-client`, `poly-maker`, and both Kalshi official SDKs lack measured numbers, license info, or maintainer signal beyond stars.
- **Benchmark Testability**: Install commands exist for all entries, but several lack auth/runtime prerequisites needed for automation: Kalshi SDKs require Python ≥3.13 (noted) but no API key bootstrap path; `ent0n29/polybot` lists only `./start-all-services.sh` with no service inventory; `prediction-market-backtesting` references `make install` without dataset prerequisites.
- Stars listed as `"private/unavailable"` for Kalshi official SDKs hint at unverified maintainer signal — needs PyPI download counts or release cadence as a substitute metric.
- `language: other` entries (`ent0n29/polybot`, `PaulieB14/polymarket-subgraph-analytics`) should be resolved to actual primary languages.

**Goal-state check**
1. ≥3 candidates per module ✅
2. All required fields populated ⚠️ (test_coverage gaps + ambiguous languages)
3. Cross-module candidates ✅
4. First/backup with rationale ✅
5. Known gaps documented ✅

## Iteration 10

**Priority dimension**: Benchmark Testability
**Improvement suggestion**: Resolve the four documented coverage blockers in the next iteration by: (1) installing rustc 1.94.1 via rustup to unblock nautilus_trader's editable build and capture pytest+coverage on tests/integration_tests/adapters/polymarket/, (2) installing cargo-llvm-cov to extract line/branch % from the already-passing 20 rs-clob-client tests, (3) writing a minimal smoke harness (mock WebSocket server + connection assertion) for real-time-data-client since the repo ships none, and (4) adding the same minimal harness pattern for poly-maker's risk-control modules. This converts 4 of the 5 'blocked/null' coverage entries into measured numbers and moves Benchmark Testability from 8→10 without adding new candidates.

### Review
## Judge Review — Prediction Market Tool Catalog (2026-04-07)

**Strengths**
- All 10 modules have ≥3 candidates with first_choice + backup + rationale.
- Cross-module mapping is explicit with documented coverage boundaries (7 entries).
- Freshness is strong: most repos updated within ~30 days of 2026-04-07; deprecated kalshi-python is flagged with successor SDKs.
- Live verification artifacts (PyPI sdist inspection, local cargo/pytest runs) replace many `unknown` fields with measured results or explicit blockers.
- Auth models, primary endpoints, and install commands are populated for nearly every candidate — sufficient for automated harness scaffolding.

**Weaknesses**
- `test_coverage` is still `unknown` for the majority of candidates; only 5 modules have measured results, and even those report `null` for line/branch %.
- Several blockers (rustc 1.94.1 for nautilus_trader, missing cargo-llvm-cov for rs-clob-client, missing test scripts for real-time-data-client and poly-maker) are documented but unresolved — they prevent the catalog from crossing into fully benchmarkable state.
- Kalshi sync/async SDKs lack a public repo, so star/CI signals are inherently absent — acknowledged but a structural weakness for benchmark scoring.
- Stars field uses inconsistent typing (`private/unavailable` string vs integers), which will trip automated parsing.

**Verdict:** Catalog is near-complete for planning purposes. The remaining gap is converting blockers into actual coverage measurements rather than adding new candidates.

## Iteration 11

**Priority dimension**: Candidate Depth
**Improvement suggestion**: Run smoke-harness coverage measurement for the four remaining first_choice/backup candidates whose `test_coverage` is still 'unknown' but where the package ships testable surface area: (1) pmxt — execute the published `npm test` (jest) against pmxtjs@2.25.2 with `c8` and record line/branch %, (2) py-clob-client — invoke the repo's pytest suite under `coverage run` against py-clob-client==0.34.6, (3) prediction-market-arbitrage-bot — add a minimal mock-API smoke harness exercising the cross-venue pairing function and measure with c8, and (4) sentence-transformers — run the upstream `pytest tests/` subset against the installed 5.3.0 wheel with `pytest-cov`. Convert each result into a `coverage_verification.results.<name>` block mirroring the existing four entries (command, tests_passed, line/branch %, harness, blocker). This directly closes the Candidate Depth gap on the recommendations that matter most for Phase 1 benchmarking.

### Review
## Catalog Review — 2026-04-08

**Strengths**
- Every module has ≥3 candidates with explicit first/backup choices and rationale.
- Cross-module mapping is exhaustive (7 tools mapped with coverage boundaries).
- Live verification section converts 4 previously-blocked coverage entries into measured line/branch results (real-time-data-client, rs-clob-client, poly-maker, nautilus_trader symbol adapter).
- Freshness is strong: 8 of ~20 candidates updated within 30 days of catalog date; deprecated candidates (kalshi-python, FinBERT) are explicitly flagged as reference-only.
- Auth models and primary endpoints are populated for every candidate, enabling automated harness wiring.

**Weaknesses**
- `test_coverage` remains "unknown" for the majority of candidates (pmxt, py-clob-client, prediction-market-analysis, sentence-transformers, spaCy, FinBERT, all three correlation/arbitrage bots, prediction-market-backtesting, polybot, polyoddwatcher, weather-bot, kalshi-ai-trading-bot, kalshi_python_async). Benchmark Testability is the weakest dimension because most candidates lack measured numbers despite having install commands.
- Several `last_updated` dates for cross-module entries (e.g., Polymarket/agents at 2024-11-05) are noted only in the cross_module_tools boundary, not in a candidate row.
- `stars: null` for the Kalshi private SDKs is correctly justified, but no proxy signal (e.g., download counts from PyPI) is captured.

**Priority gap**: Candidate Depth — too many `test_coverage: unknown` fields where a smoke harness could plausibly produce a number, especially for the first_choice picks that drive recommendations (pmxt, py-clob-client, prediction-market-arbitrage-bot, sentence-transformers).
