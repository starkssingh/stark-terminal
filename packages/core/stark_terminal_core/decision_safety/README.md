# Decision Safety

Prompt 39 adds the `decision_safety` package as a guardrails-only decision-support layer.

This package defines:

- Decision Safety guardrail contracts.
- human-review gates that are not approvals.
- approval placeholders that are not active workflows.
- override prohibition contracts.
- blocked output policy contracts.
- readiness templates for future Decision Desk API skeleton planning.

Prompt 39 explicitly does not implement recommendations, action generation, confidence scoring, active DecisionObject generation, human approval, overrides, broker behavior, event publishing, or execution APIs.

All helpers are deterministic, side-effect-free, and standard-library/Pydantic only. Future prompts may add API skeleton contracts only after this guardrail layer remains audited and fail-closed.
