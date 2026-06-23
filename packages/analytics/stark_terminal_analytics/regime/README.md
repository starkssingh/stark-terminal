# Regime Analytics Planning and Guardrails

This package contains Prompt 33 regime planning contracts and guardrails only.

Implemented now:

- regime label placeholder contracts.
- evidence requirement contracts.
- evidence checklist and readiness report templates.
- safety policy helpers that fail closed.
- dependency staging metadata.
- roadmap metadata.
- health status metadata.

Not implemented now:

- regime classification.
- market state decisions.
- stationarity tests.
- Hidden Markov Models, clustering, or ML models.
- indicators or feature computation.
- backtests.
- signals or recommendations.
- DecisionObject generation.
- execution APIs.

Evidence requirements and human review remain required. Heavy statistical,
machine-learning, and regime-model dependencies remain blocked until future
explicit prompts update the dependency gate with docs, tests, and safety review.
