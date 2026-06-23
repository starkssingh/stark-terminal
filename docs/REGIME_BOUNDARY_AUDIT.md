# Regime Boundary Audit

Prompt 35 audits the boundary around regime-related code after Prompts 33 and
34. The regime area is governance and contracts only. It is not a regime engine,
classifier, feature pipeline, signal engine, recommendation engine, or execution
system.

## What Regime Code Can Do Today

- Define regime label placeholders.
- Define evidence requirement contracts.
- Build planning-only evidence checklists.
- Build readiness templates.
- Expose dependency gate metadata.
- Define feature candidate metadata.
- Define feature group plans.
- Define provenance requirements.
- Define evidence mapping contracts.
- Build readiness reports that remain not ready for classification or
  production.

## What Regime Code Cannot Do Today

- Classify market state.
- Detect regimes.
- Assign regime labels.
- Compute regime features.
- Write to the Feature Registry.
- Generate classifier inputs.
- Run stationarity tests.
- Run ADF, KPSS, Hurst, HMM, clustering, ML, or model-fitting logic.
- Generate signals, recommendations, decisions, or DecisionObjects.
- Execute trades or expose execution APIs.
- Produce buy/sell/hold/watch/avoid outputs.
- Emit action-state or confidence trading fields.

## Boundary Before Future Regime Work

Future regime feature computation, registry integration, classifier input
generation, model training, regime label assignment, validation, or production
use requires a separate prompt, dependency review, source-reference policy,
data-quality gates, human-review guardrails, tests, docs, and milestone audit.

Regime readiness is not a recommendation. A label placeholder is not a market
state decision. Evidence requirements are not hidden decision logic.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.
