# Numerical Analytics Dependency Gate

Prompt 27 keeps the numerical dependency stage at `contracts_and_safe_stdlib`.

## Current Stage

Allowed now:

- Python standard library.
- `math` and `statistics` style deterministic helpers.
- Pydantic contracts.
- FastAPI/TestClient for metadata endpoints and tests.
- existing project packages.
- existing Polars, PyArrow, and DuckDB only as already installed data-platform dependencies, not as new market analytics requirements.

## Heavy Dependencies Blocked

The numerical dependency gate blocks new heavy analytics dependencies in Prompt 27, including NumPy, SciPy, Numba, JAX, CuPy, PyTorch, TensorFlow, statsmodels, arch, TA-Lib, vectorbt, backtrader, QuantLib, XGBoost, LightGBM, CatBoost, and scikit-learn.

If a future prompt needs one of these dependencies, it must update the dependency stage, docs, tests, audit coverage, and safety review explicitly.

## Prompt 27 Boundary

No heavy dependencies are added in Prompt 27. The numerical core uses standard-library math only for count, min, max, and mean.

The dependency gate must not smuggle in returns, volatility, drawdown, correlation, indicators, factors, ML models, backtesting engines, signals, recommendations, DecisionObject generation, provider SDKs, scraping dependencies, broker dependencies, or execution APIs.

Development environment: Mac mini M2 / macOS / Apple Silicon. Target desktop product: Windows-native Stark Terminal.
