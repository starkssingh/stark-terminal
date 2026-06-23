# Analytics Dependency Staging

Prompt 26 keeps the analytics dependency stage at `contracts_only`.

## Why Dependencies Are Staged

The target analytics stack is intentionally broad, but heavy numerical, statistical, ML, GPU, options, and backtesting dependencies should enter only when a concrete module needs them and tests justify them.

Prompt 26 adds no heavy analytics dependency. It defines the dependency plan as metadata only.

## Current Stage

Current stage: `contracts_only`.

Allowed now:

- standard library.
- Pydantic.
- FastAPI/TestClient for API tests.
- existing project packages.
- existing data IO dependencies only as already present in the repository.

## Planned Dependencies

Future candidates include:

- NumPy.
- SciPy.
- pandas.
- Polars.
- Numba.
- JAX.
- CuPy.
- statsmodels.
- arch.
- scikit-learn.
- XGBoost.
- LightGBM.
- CatBoost.
- PyTorch.
- TensorFlow.
- QuantLib.
- vectorbt.
- backtrader.

These are planned or evaluation candidates, not Prompt 26 requirements. Installing or using heavy analytics libraries requires a future explicit prompt, tests, docs, and safety review.

## Safety Boundary

Dependency staging must not smuggle in analytics calculations, signals, recommendations, backtesting engines, broker integrations, provider SDKs, scraping dependencies, or execution APIs.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.

