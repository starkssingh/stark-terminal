# Retail Trader Experience Cross-Endpoint Consistency Audit

Prompt 62 audits Retail Trader Experience endpoint consistency across Prompts
56-61.

Endpoint families audited:

- `/retail-trader-experience/*`
- `/retail-trader-experience-api/*`
- `/retail-trader-experience-display/*`
- `/retail-trader-experience-boundary/*`

## Expected Safe Field Consistency

All Retail Trader Experience endpoint families must expose safe metadata only.
Dangerous flags must remain false, including active UI, frontend components,
desktop components, recommendations, action generation, confidence scoring,
DecisionObject generation, readiness-to-trade, suitability profiling,
approvals, overrides, broker controls, and execution.

## Unavailable-By-Default Consistency

Planning/API/display endpoints use unavailable-by-default, planning-only,
api-contract-skeleton-only, display-contract-skeleton-only, or
placeholder-only language. Boundary endpoints use boundary-hardening-only
language. None of these states can be interpreted as production trader
experience readiness.

## Skeleton-Only Consistency

Contract and placeholder endpoints return metadata, placeholders, unavailable
responses, readiness templates, or invariant results. They do not return
generated output, active experience output, active widgets, DecisionObjects,
recommendation cards, suitability profiles, readiness-to-trade, broker
controls, or execution controls.

## No Generated Output Consistency

Endpoint families must not generate recommendations, buy/sell/hold/watch/avoid
active outputs, action states, confidence scores, active DecisionObjects,
approvals, overrides, readiness-to-trade, suitability profiles, broker
controls, or execution instructions.

## No Secret Or Live Data Exposure

Endpoints must not expose secrets, credentials, raw database URLs, provider
tokens, broker tokens, raw provider URLs, live market data, real market data
claims, provider SDK behavior, external calls, scraping, or production event
publishing.

## Forbidden Endpoint Classes

There is no market-data input for trader recommendations, no active UI
endpoint, no suitability profiling endpoint, no broker-control endpoint, no
approval or override endpoint, no execution-like endpoint, no
API-to-active-UI path, no API-to-recommendation-card path, no
display-to-execution path, no persona-to-suitability-profile path, no
journey-to-trading-advice path, and no boundary bypass path.

Development remains Mac mini M2 / macOS / Apple Silicon. The target desktop
product remains Windows-native Stark Terminal.
