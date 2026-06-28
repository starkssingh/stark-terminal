# Research Artifact Cross-Module Invariants

Prompt 75 adds cross-module invariant helpers for the Research Artifact
Registry planning/API/display/boundary stack. The invariant result is
boundary-hardening-only and passes only when endpoint policies, module
policies, and the forbidden behavior registry remain complete and fail-closed.

The invariant result cannot allow active ingestion/storage, file
upload/download, file preview, active UI, frontend/desktop implementation,
paper parsing, PDF parsing, arXiv ingestion, LLM paper analysis, strategy
generation, strategy code generation, backtesting, optimization,
recommendations, action generation, confidence scoring, DecisionObject
generation, readiness-to-trade, broker controls, approvals, overrides, or
execution APIs.

Rejection helpers return blocked invariant results for ingestion, storage,
upload/download, active UI, paper parsing, strategy generation, backtesting,
recommendations, broker controls, readiness-to-trade, and execution. They do
not enable behavior.

Development remains on Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.

## Prompt 76 Integration Readiness Note

Prompt 76 confirms cross-endpoint integration readiness across
research-artifact-registry, research-artifact-registry-api,
research-artifact-registry-display, and research-artifact-registry-boundary
families. Cross-module invariants still permit only planning, contract,
display-contract, audit, and boundary metadata. No endpoint or module may
bypass no-ingestion/storage, no-upload/download, no-active-UI, no-paper
parsing, no-strategy generation, no-backtesting, no-recommendation, or
no-execution boundaries.
