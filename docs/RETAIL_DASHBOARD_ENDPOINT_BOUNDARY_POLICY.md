# Retail Dashboard Endpoint Boundary Policy

Prompt 54 adds endpoint boundary policies for the Retail Dashboard endpoint families.

## Endpoint Families

- `retail-dashboard`
- `retail-dashboard-api`
- `retail-dashboard-display`
- `retail-dashboard-boundary`

## Policy

The endpoint boundary policy is read-only and unavailable by default. Allowed methods are limited to `GET`. `POST`, `PUT`, `PATCH`, and `DELETE` remain forbidden for Retail Dashboard boundary surfaces.

Endpoints must not:

- accept market data for dashboard decisions
- generate recommendations
- generate active UI
- generate active DecisionObjects
- expose broker controls
- execute trades
- grant approvals
- grant overrides
- expose secrets or credentials

There is no market-data-to-dashboard-decision endpoint, no approval/override endpoint, no execution endpoint, and no broker linkage.

Development remains on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal.
