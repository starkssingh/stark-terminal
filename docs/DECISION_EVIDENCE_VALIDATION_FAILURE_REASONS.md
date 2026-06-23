# Decision Evidence Validation Failure Reasons

Prompt 44 defines validation issue and failure reason schemas for Decision
Evidence Validation v0.
These failure reasons are validation-only and cannot authorize a decision.

## Failure Reasons

Supported validation issue kinds include:

- missing evidence item.
- invalid evidence item.
- missing source reference.
- invalid source reference.
- missing provenance.
- incomplete provenance.
- missing validation checklist.
- incomplete validation checklist.
- missing human-review attachment.
- incomplete human-review attachment.
- unsafe generated output flag.

## Severity

Issue severity may be INFO, WARNING, ERROR, or BLOCKER. ERROR and BLOCKER
issues must block DecisionObject generation, recommendations, and execution.
Warnings do not authorize a decision; they are still validation-only evidence
about contract state.

Missing or incomplete provenance, missing source reference, missing or
incomplete validation checklist, missing or incomplete human-review attachment,
and unsafe generated output flags are blockers in Prompt 44.

Validation failure is not a recommendation, not approval, not
readiness-to-trade, and not execution readiness.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
