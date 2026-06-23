# Decision Forbidden Behavior Registry

Prompt 47 adds a Decision forbidden behavior registry as a contract-only,
boundary-hardening artifact.

## Registry Purpose

The registry lists behavior categories that remain forbidden across Decision
Desk modules and endpoints. It does not enable behavior, does not grant
exceptions, and does not act as an approval workflow.

## Forbidden Categories

The registry covers:

- recommendations.
- action generation.
- confidence scoring.
- DecisionObject generation.
- execution APIs.
- approval.
- override.
- active UI.
- active workflow.
- task assignment.
- reviewer auth.
- notifications.
- readiness-to-trade.
- broker behavior.
- real ingestion.
- external calls.
- secrets or credentials.
- provider SDKs.
- scraping.

Each registry entry is forbidden now, requires a future prompt, and requires an
audit before unlock. The registry is therefore a blocking contract, not a
feature switch.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
