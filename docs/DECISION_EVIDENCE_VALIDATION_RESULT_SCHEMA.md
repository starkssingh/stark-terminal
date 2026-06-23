# Decision Evidence Validation Result Schema

Prompt 44 defines a validation-only result schema for Decision Evidence
Validation v0.

## Result Fields

The result records:

- `valid`: whether validation found no error or blocker issues.
- `validation_only`: always true.
- `issues`: validation issue contracts.
- `issue_count`: must equal the number of issues.
- `blocker_count`: must equal the number of BLOCKER issues.
- `warning_count`: must equal the number of WARNING issues.
- `status`: validation-only status text.
- safety flags for recommendations, action generation, confidence scoring,
  DecisionObject generation, execution, approval, override, and
  readiness-to-trade.

All dangerous flags remain false. A valid result is not approval, not decision
readiness, not readiness-to-trade, not a recommendation, and not permission to
generate a DecisionObject.

Validation results are not durable truth and are not persisted in Prompt 44.
They do not publish events, create UI output, or expose execution behavior.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.

