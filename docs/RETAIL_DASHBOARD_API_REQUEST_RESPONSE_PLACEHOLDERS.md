# Retail Dashboard API Request Response Placeholders

Prompt 50 defines Retail Dashboard API request and response placeholders for a
future dashboard API surface.

## Request Placeholder

`RetailDashboardAPIRequestPlaceholder` captures a request ID, request kind,
requested section names, requested card names, data reference requirement,
decision reference requirement, safety reference requirement, schema version,
created timestamp, and sanitized notes.

Request placeholders do not enable active UI, recommendation cards, action
generation, confidence scoring, DecisionObject generation, readiness-to-trade,
broker controls, approval, override, or execution.

## Response Placeholder

`RetailDashboardAPIResponsePlaceholder` carries a data reference, decision
reference, safety reference, unavailable response, schema version, created
timestamp, and sanitized notes.

Response placeholders contain no computed recommendation fields, no active
action fields, no active UI fields, no active DecisionObject fields, no
readiness-to-trade fields, no broker control fields, and no execution-ready
fields.

## References

Data reference, decision reference, and safety reference values are placeholders
only. They are not real or live market data, not active DecisionObjects, not
safety passes, not approvals, not overrides, and not execution permissions.

Development remains Mac mini M2 on macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.
