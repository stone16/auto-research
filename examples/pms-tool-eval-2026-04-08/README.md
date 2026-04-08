# PMS Tool Evaluation — auto-research Run Snapshot (2026-04-08)

This directory contains a snapshot of a completed auto-research loop run that catalogued open-source prediction market tools for the `prediction-market-system` (pms) project.

## Run Metadata

- **Branch**: `autoresearch/pms-tool-eval-v1`
- **Producer**: Codex CLI
- **Judge**: Claude
- **Iterations**: 11 (4 keep, 7 discard)
- **Best score**: 1.0000 (iteration 5)
- **Stop reason**: `max_consecutive_discard` (6/6 triggered after iteration 11)
- **Source documents**: `runs/pms-tool-eval/sources/` (local, gitignored) — frozen copies of the three landscape docs in `claudedocs/` (also gitignored in this repo)

## Files

| File | Description |
|------|-------------|
| `tool-catalog.yaml.md` | **Final knowledge base** — 173 lines of YAML-structured tool catalog across 10 prediction market system modules. First-choice + backup + rationale per module. |
| `benchmark.json` | 10-item benchmark used to score catalog iterations (module coverage + cross-module mapping + recommendations) |
| `topic.md` | Research topic definition with 5 quality dimensions (Module Coverage, Candidate Depth, Benchmark Testability, Cross-Module Mapping, Freshness) |
| `iteration-results.tsv` | Full iteration history with scores and kept/discarded status |
| `judge-feedback-trace.md` | Judge dimension scoring and improvement suggestions per iteration |

## Catalog Summary (from tool-catalog.yaml.md)

10 modules populated, each with first_choice + backup recommendations:

| Module | First Choice | Backup |
|--------|-------------|--------|
| data_connector | pmxt | py-clob-client |
| realtime_feed | real-time-data-client | nevuamarkets/poly-websockets |
| data_normalizer | pmxt | prediction-market-backtesting |
| embedding_engine | sentence-transformers | FinBERT |
| correlation_detector | prediction-market-arbitrage-bot | prediction-market-analysis |
| arbitrage_calculator | prediction-market-arbitrage-bot | pmxt |
| order_executor | pmxt | py-clob-client |
| risk_manager | poly-maker | polymarket-kalshi-weather-bot |
| backtesting_engine | nautilus_trader | prediction-market-backtesting |
| analytics_dashboard | ent0n29/polybot | sgdva/polyoddwatcher |

Each candidate includes: name, repo, language, install command, platforms, last_updated, stars, test_coverage, api_docs, auth_model, primary_endpoints, known_issues, verdict, notes.

## Known Gaps (from Codex's final catalog)

1. Kalshi SDK repo is private (`exchange-infra`) — PyPI metadata verifiable, GitHub stars/CI not publicly auditable
2. No standalone OSS risk-management library exists — current options are embedded in strategy bots
3. Dedicated correlation-detector tooling is sparse — best references are cross-platform arbitrage bots + offline data frameworks
4. Test coverage measured locally for 4 priority candidates: real-time-data-client, rs-clob-client, poly-maker, nautilus_trader Polymarket adapter
5. NautilusTrader Rust 1.94.1 build requirement now satisfied; remaining limitation is a repo-level pytest bootstrap defect

## Next Step

Convert `tool-catalog.yaml.md` into pms-v1's `candidates/*.yaml` format and run `pms-harness evaluate --module <name>` against real tools to validate the harness end-to-end.
