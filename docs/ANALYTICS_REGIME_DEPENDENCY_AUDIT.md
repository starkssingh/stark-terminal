# Analytics/Regime Dependency Audit

Prompt 35 audits the dependency state for analytics and regime work across
Prompts 26-34.

## Current Dependency State

Analytics/regime code uses the Python standard library, Pydantic,
FastAPI/TestClient, and existing project packages. Prompt 35 adds no dependency.

## Heavy Dependencies

No heavy analytics/model dependencies are newly added unexpectedly. The
following remain blocked or future-gated: NumPy, SciPy, pandas, statsmodels,
arch, sklearn, hmmlearn, ruptures, Numba, JAX, CuPy, PyTorch, TensorFlow,
XGBoost, LightGBM, CatBoost, QuantLib, TA-Lib, vectorbt, and backtrader.

## Provider, Scraping, and Broker Dependencies

No provider SDKs, scraping dependencies, broker/trading dependencies, or network
client imports for analytics/regime behavior are introduced. Analytics/regime
modules do not import requests, httpx, aiohttp, urllib network clients, or
socket for external-call behavior.

## Stdlib-Only Calculation Posture

Descriptive analytics already implemented remain stdlib-only. Prompt 35 does
not add calculations. Regime planning and regime feature preparation remain
metadata/contracts only.

## Future Dependency Gate

This section is the future dependency gate for analytics/regime extensions.

Any future stationarity tests, model fitting, feature computation, classifier
inputs, regime classification, backtesting, or Decision Desk implementation must
pass a dependency review and milestone audit before new dependencies can be
added.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target
desktop product remains Windows-native Stark Terminal.
