# Strategy Research Workspace API Reference Placeholders

Prompt 64 defines reference placeholders for the Strategy Research Workspace
API. References are identifiers and safety metadata only.

## Reference Types

- workspace reference placeholder.
- artifact reference placeholder.
- paper reference placeholder.
- hypothesis reference placeholder.
- dataset reference placeholder.
- experiment reference placeholder.
- safety reference placeholder.

## Boundary

Workspace references are not active workspaces and not active UI.
Artifact references are not validated research artifacts, not parsed paper
artifacts, not strategy-ready artifacts, not backtest-ready artifacts, not
recommendation-ready artifacts, and not execution-ready artifacts.

Paper references include no paper ingestion, no paper parsing, no method
extraction, no strategy extraction, no generated code, no generated backtest,
and no recommendation generation.

Hypothesis references include no generated strategy, no generated signal, no
generated factor, no generated code, no generated backtest, and no generated
recommendation.

Dataset references include no real market data, no live data, no validated
research dataset, no validated backtest dataset, and no execution dataset.

Experiment references include no executable experiment, no executable
backtest, no optimization, no strategy execution, no live-ready state, no
recommendation-ready state, and no execution-ready state.

Safety references include no safety pass, no approval/override, no
readiness-to-trade, no broker controls, and no execution APIs.
