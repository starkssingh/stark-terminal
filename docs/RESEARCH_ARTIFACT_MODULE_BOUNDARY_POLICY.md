# Research Artifact Module Boundary Policy

Prompt 75 adds module boundary policies for these module families:

- research_artifact_registry
- research_artifact_registry_api
- research_artifact_registry_display
- research_artifact_registry_boundary

Module policies keep each module boundary-hardening-only or placeholder-only.
They permit planning metadata, API contract skeleton placeholders, display
contract skeleton placeholders, and boundary invariant helpers only.

Modules may not ingest artifacts, persist artifacts, upload files, download
files, preview files, create active UI, create frontend components, create
desktop components, parse papers, parse PDFs, ingest arXiv, call LLM paper
analysis, generate strategies, generate strategy code, run backtests, optimize,
generate recommendations, generate actions, score confidence, generate
DecisionObjects, generate readiness-to-trade, expose broker controls, execute,
grant approvals, or grant overrides.

Future prompt and audit approval are required before unlocking anything.
Development remains on Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.

## Prompt 76 Integration Readiness Note

Prompt 76 confirms module boundary policy integration across
research_artifact_registry, research_artifact_registry_api,
research_artifact_registry_display, and research_artifact_registry_boundary.
The modules remain planning-only, API-contract-skeleton-only,
display-contract-skeleton-only, and boundary-hardening-only. They expose no
cross-module bypass for active ingestion/storage, upload/download, file
preview, active UI, frontend/desktop implementation, paper parsing, strategy
generation, backtesting, recommendations, confidence scoring, DecisionObject
generation, readiness-to-trade, broker controls, approvals/overrides, or
execution.
