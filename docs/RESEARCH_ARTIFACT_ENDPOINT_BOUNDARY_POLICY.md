# Research Artifact Endpoint Boundary Policy

Prompt 75 adds endpoint boundary policies for the Research Artifact Registry
route families:

- research-artifact-registry
- research-artifact-registry-api
- research-artifact-registry-display
- research-artifact-registry-boundary

Policies are boundary-hardening-only, GET-only/read-only, and
unavailable-by-default. They forbid POST, PUT, PATCH, and DELETE methods for
Research Artifact Registry route families in this phase.

Endpoint policies allow no file input, no artifact input for storage, no paper
input, no market-data-to-research-decision input, no active UI, no
ingestion/storage, no upload/download, no file preview, no paper parsing, no
strategy generation, no backtesting, no recommendations, no DecisionObjects,
no broker controls, and no execution.

Future prompt and audit approval are required before unlocking any endpoint
capability. Development remains on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.

## Prompt 76 Integration Readiness Note

Prompt 76 confirms endpoint boundary policy integration across
research-artifact-registry, research-artifact-registry-api,
research-artifact-registry-display, and research-artifact-registry-boundary.
The endpoint families remain GET-only/read-only and unavailable-by-default.
They expose no API-to-display artifact implementation path, no API-to-display
file preview path, no ingestion/storage path, no upload/download path, no
paper parsing path, no strategy generation path, no backtest path, no
recommendation path, no readiness-to-trade path, no broker-control path, and
no execution path.
