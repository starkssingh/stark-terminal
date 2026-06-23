# Regime Dependency Staging

Prompt 33 keeps the Regime Analytics dependency stage at `planning_only`.
This dependency staging is a planning guardrail, not a classifier runtime.

## Current Stage

Allowed now:

- standard library.
- Pydantic.
- FastAPI/TestClient.
- existing project packages.

No new dependency is added in Prompt 33.

## Blocked Dependencies

Heavy model, statistical, ML, and regime-detection dependencies remain blocked:

- NumPy.
- SciPy.
- statsmodels.
- scikit-learn.
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

There is no statsmodels, SciPy, sklearn, hmmlearn, or ruptures dependency in
Prompt 33. There is no classifier implementation.

## Future Dependency Review

Future stationarity or regime model work needs an explicit dependency review,
updated dependency gate, docs, tests, source-reference policy, no-signal audit,
and API surface review. Dependency staging must remain fail-closed until that
future prompt is implemented and verified.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
