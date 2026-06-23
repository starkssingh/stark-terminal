# Analytics Dependency Audit

Prompt 30 audits the dependency posture after Prompts 26-29.

## Current Dependency State

The analytics implementation currently uses:

- Python standard library math/statistics-style helpers.
- Pydantic contracts.
- FastAPI/TestClient for read-only API tests.
- existing project packages.

No heavy analytics dependencies were newly added unexpectedly in Prompts 26-29. Prompt 31 keeps the same dependency posture for correlation and beta analytics: standard library calculations, Pydantic contracts, FastAPI metadata endpoints, and existing project packages only.

## Blocked Heavy Analytics Dependencies

The dependency gate continues to block NumPy, SciPy, Numba, JAX, CuPy, PyTorch, TensorFlow, statsmodels, arch, TA-Lib, vectorbt, backtrader, QuantLib, XGBoost, LightGBM, CatBoost, and scikit-learn until a future prompt explicitly unlocks a scoped need.

## Provider / Scraping / Broker Dependencies

Prompt 30 confirms:

- no provider SDKs.
- no scraping dependencies.
- no broker/trading dependencies.
- no credentials.
- no external provider calls.
- no real market ingestion.

## Import Posture

Analytics modules must not import `requests`, `httpx`, `aiohttp`, `urllib.request`, or socket clients for external-call behavior. Current analytics modules remain local, deterministic, and side-effect-minimized.

## Future Dependency Gate Requirements

The future dependency gate remains mandatory before any heavy numerical, statistical, ML, GPU, options, or backtesting dependency can be introduced.

Any future heavy dependency requires:

- explicit prompt scope.
- updated dependency stage.
- docs and tests.
- no-signal/no-decision audit.
- API surface review.
- source-reference and validation requirements.
- confirmation that no execution APIs or broker integrations are introduced.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The target desktop product remains Windows-native Stark Terminal.
