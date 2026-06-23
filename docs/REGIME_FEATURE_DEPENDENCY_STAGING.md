# Regime Feature Dependency Staging

Prompt 34 keeps the Regime Feature Preparation dependency stage at
`contracts_only`. This dependency staging is a contract guardrail, not a feature
runtime.

## Current Stage

Allowed now:

- standard library.
- Pydantic.
- FastAPI/TestClient.
- existing project packages.

No new dependency is added in Prompt 34.

## Blocked Dependencies

Heavy feature/model dependencies remain blocked:

- NumPy.
- SciPy.
- statsmodels.
- scikit-learn.
- sklearn.
- hmmlearn.
- ruptures.
- PyTorch.
- TensorFlow.
- XGBoost.
- LightGBM.
- CatBoost.
- TA-Lib.
- vectorbt.
- backtrader.

There is no SciPy, sklearn, hmmlearn, or ruptures dependency in Prompt 34.
There is no feature computation implementation.

## Future Review

Future feature computation requires explicit dependency review, updated
dependency staging, docs, tests, source-reference policy, validation and quality
requirements, no-signal audit, and API surface review.

Prompt 34 keeps no feature computation, no feature registry writes, no
classification, no signals, no recommendations, no DecisionObject generation,
and no execution APIs.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
