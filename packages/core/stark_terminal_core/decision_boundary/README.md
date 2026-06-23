# Decision Boundary

Prompt 47 adds the `decision_boundary` package as boundary-hardening-only
infrastructure for the Decision Desk skeleton stack.

The package defines:

- cross-module forbidden behavior registry contracts.
- endpoint boundary policies.
- module boundary policies.
- invariant helpers for read-only checks.
- health metadata for the boundary-hardening layer.

It does not generate recommendations, action states, confidence scores,
DecisionObjects, approvals, overrides, active UI, active workflow,
readiness-to-trade, broker behavior, or execution APIs.

Future prompts may harden these policies further before dashboard planning.
The package must remain deterministic, side-effect free, and standard-library
only apart from existing Pydantic contracts.
