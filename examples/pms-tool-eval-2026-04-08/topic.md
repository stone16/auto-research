# Prediction Market Tool Evaluation

## Research Goal

Produce a comprehensive candidate tool catalog for a modular prediction market trading system targeting Polymarket and Kalshi. The system has the following modules, and we need at least 3 candidate tools per module:

### System Modules

1. **Data Connector** — Platform API adapters for fetching market data, orderbooks, positions
2. **Realtime Feed** — WebSocket/streaming clients for real-time price updates
3. **Data Normalizer** — Cross-platform data format unification
4. **Embedding Engine** — Market description vectorization for similarity search
5. **Correlation Detector** — Cross-market relationship discovery (subset, overlap, contradiction)
6. **Arbitrage Calculator** — Cross-market and same-market arbitrage opportunity detection
7. **Order Executor** — Order signing, submission, and lifecycle management
8. **Risk Manager** — Position sizing, exposure limits, drawdown protection
9. **Backtesting Engine** — Historical simulation of trading strategies
10. **Analytics/Dashboard** — Performance monitoring, P&L tracking, visualization

### Output Format

The knowledge base must be structured as a YAML-compatible catalog with the following fields per candidate:

For each module, list candidates with:
- name: Display name
- repo: GitHub URL
- language: python | typescript | rust | other
- install: Installation command
- platforms: [polymarket, kalshi, manifold, ...]
- last_updated: Date of most recent commit
- stars: GitHub star count
- test_coverage: Known test coverage % or "unknown"
- api_docs: URL to documentation
- known_issues: Brief list of known problems
- verdict: deeper-review | reference-only | reject
- notes: Freeform evaluation notes

## Goal State

The catalog is complete when:
1. Every module has at least 3 candidate tools (or explicit documentation that fewer exist)
2. Each candidate has all required fields populated with verified data
3. Cross-module candidates are identified (tools covering multiple modules)
4. A recommended "first choice" and "backup" are identified per module with rationale
5. Known gaps are documented with suggested approaches (build vs. adapt)

## Quality Dimensions

- **Module Coverage**: Every system module has ≥3 candidates or documented evidence that fewer exist in the ecosystem
- **Candidate Depth**: Each candidate has all required fields populated with current, verified data (not assumptions)
- **Benchmark Testability**: Candidates include enough technical detail (install commands, API endpoints, auth requirements) for automated evaluation
- **Cross-Module Mapping**: Tools spanning multiple modules are identified and their coverage boundaries are documented
- **Freshness**: All data reflects 2026 ecosystem state — repo activity, API versions, known breaking changes
