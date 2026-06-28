# Audit Log Journal Target

This document records the future audit log + journal target. It is not an
audit database, not a journal database, not active persistence, not paper
trading, and not execution infrastructure. Execution APIs remain forbidden.

## Future Records

A future audit log and journal must record:

- candidate provenance
- data-quality checks
- feature/regime state
- deterministic engine rationale
- verifier pass/fail details
- human/paper gate status
- rejected candidates
- reasons, evidence references, and outcomes

Rejected candidates must be retained in the future audit model so blocked
decisions can be reviewed, explained, and improved without converting them
into recommendations or trades.

No execution logs exist until execution is explicitly unlocked in future
audited phases. The current system has no execution APIs, no broker controls,
no order placement, no active DecisionObject generation, no trade commit
logic, no paper trading implementation, and no active audit/journal database
for decision outcomes.

