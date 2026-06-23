# Decision Desk Human Review Guardrails

Prompt 36 requires human review for future Retail Decision Desk work.

Human review guardrails currently:

- block recommendations.
- block DecisionObject generation.
- block execution.
- require an evidence-chain review.
- require risk-language review.
- require execution-boundary review.

Human review is not automatic approval. It does not produce recommendations,
action states, confidence scores, DecisionObjects, broker behavior, or execution
APIs in Prompt 36. No bypass is implemented.

Future prompts must define evidence bundle contracts, safety gates, review
records, and auditability before any Decision Desk skeleton can move closer to a
user-facing decision surface.

## Prompt 38 Human-Review Attachment Note

Prompt 38 adds human-review attachment contracts for DecisionObject evidence
bundles. These attachments are planning artifacts only, not approvals.
`approval_granted` remains false, and attachments continue to block
recommendations, action generation, confidence scoring, active DecisionObject
generation, and execution APIs.

## Prompt 39 Decision Safety Gate Note

Prompt 39 adds Decision Safety human-review gates. These gates are not
approvals, keep `approval_granted=false`, and block recommendations,
action generation, confidence scoring, active DecisionObject generation,
overrides, broker behavior, and execution APIs.

## Prompt 45 Workflow Skeleton Linkage

Prompt 45 adds a Decision Human Review workflow skeleton as contract metadata
only. The workflow skeleton has no active review workflow, no task assignment,
no reviewer auth, no notifications, no approval workflow, no override workflow,
no recommendation generation, no action generation, no confidence scoring, no
DecisionObject generation, no readiness-to-trade, and no execution APIs.

Human-review guardrails still require review boundaries, but the new workflow
placeholders do not approve output and do not bypass blocked-output policy.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.
