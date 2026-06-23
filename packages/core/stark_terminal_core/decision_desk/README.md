# Retail Decision Desk Planning

The `decision_desk` package is planning and guardrails only in Prompt 36.

It defines Retail Decision Desk plan contracts, action placeholder contracts,
evidence requirements, human-review checklists, display boundaries, readiness
reports, and safety policy helpers.

It implements no recommendations, no action generation, no confidence scoring,
no DecisionObject generation, no execution APIs, no broker behavior, no event
publishing, and no real-data assumptions.

Action placeholders such as `BUY_BIAS`, `SELL_BIAS`, `HOLD`, `WATCH`, `AVOID`,
and `REDUCE` are planned categories only. They are not generated outputs in
Prompt 36 and must not be interpreted as trading recommendations.

Evidence and human review are required before any future Decision Desk work can
move beyond planning. Prompt 37 is expected to add DecisionObject evidence bundle
contracts only, still without generating DecisionObjects.
