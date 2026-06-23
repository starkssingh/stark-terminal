# Technical Stack

Prompt 41 performs the Decision Desk Milestone Audit and adds no new
dependencies. Decision Desk planning, decision evidence, decision safety, and
decision API skeleton modules remain standard-library plus existing Pydantic
and FastAPI/TestClient usage. No heavy analytics/model libraries, provider SDKs,
scraping libraries, broker/trading dependencies, UI dependencies, or execution
libraries are added.

Prompt 28 keeps the locked target stack and adds no new heavy dependency. It implements Returns and Rolling Window Analytics v0 with standard-library simple/log returns and rolling count/mean/min/max over Prompt 27 numerical contracts. It adds no provider SDKs, no scraping dependencies, no broker/trading dependencies, no heavy analytics dependencies, no full quant/ML libraries, no external calls, no real market ingestion, no volatility/drawdown/correlation calculations, no trading signals, no recommendations, no DecisionObject generation, and no execution APIs.

## Core Language / Runtime

- Python 3.11+
- Future optional C++ performance modules

## Backend / API

- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- SQLAlchemy 2.x
- Alembic
- psycopg 3 via `psycopg[binary]`
- DuckDB
- PyArrow
- Polars
- Redis client library
- clickhouse-connect
- confluent-kafka

## Desktop

- PySide6 / Qt 6

## Data Infrastructure

- PostgreSQL
- TimescaleDB
- DuckDB
- Parquet
- Redis
- Redis Streams
- Kafka or Redpanda-compatible event bus
- ClickHouse
- Custom Stark Feature Registry implemented first
- Feast planned for future evaluation/integration

## Numerical Libraries - Python

- NumPy
- SciPy
- pandas
- Polars
- Numba
- JAX
- CuPy

## Numerical Libraries - Future C++

- Eigen
- Intel MKL
- OpenBLAS
- Boost

## Statistical and Time-Series Models

- ARIMA/SARIMA
- GARCH
- Kalman Filters
- Hidden Markov Models
- State-Space Models
- Johansen cointegration
- PCA
- Factor Models
- Bayesian Models
- Monte Carlo simulation

## Machine Learning

- scikit-learn
- XGBoost
- LightGBM
- CatBoost
- Random Forest
- Elastic Net
- PyTorch
- TensorFlow
- JAX

## Optimization

- CVXPY
- OSQP
- Optional Gurobi
- Optional MOSEK
- Portfolio optimization
- Risk parity
- Kelly criterion
- Position sizing
- Transaction cost minimization

## Options Analytics

- QuantLib
- Custom pricers later
- Black-Scholes
- Heston
- SABR
- Local Volatility
- Monte Carlo
- Binomial Trees
- Finite Difference Methods
- Greeks

## Backtesting

- Internal deterministic backtesting engine
- VectorBT
- Backtrader
- NautilusTrader
- Zipline as reference only if useful
- QuantConnect as external reference only, not a dependency by default

## Risk Analytics

- VaR
- Expected Shortfall
- Stress Testing
- Scenario Analysis
- Greeks
- Correlation Models

## Alternative Data / NLP

- PyTorch
- Transformers
- Sentence Transformers
- News sentiment later
- Event detection later
- Paper understanding later

## Prompt 10 Dependency Boundary

Prompt 10 adds the custom Stark Feature Registry foundation with no new dependency and does not install Feast. The project installs FastAPI, Uvicorn, Pydantic, Pydantic Settings, SQLAlchemy, Alembic, psycopg, DuckDB, PyArrow, Polars, the Redis client library, clickhouse-connect, pytest, httpx, and python-dotenv, with PySide6 as an optional desktop dependency. Kafka/Redpanda, Feast integration, provider SDKs, scraping dependencies, broker/trading dependencies, heavy quant, and ML libraries are documented or planned but intentionally deferred.

## Prompt 11 Audit Boundary

Prompt 11 adds audit tooling and documentation only. It adds no runtime dependency, no Kafka/Redpanda dependency, no Feast dependency, no provider SDK, no scraping dependency, no broker/trading dependency, no quant/ML dependency, no execution APIs, and no real market ingestion.

## Prompt 12 Dependency Boundary

Prompt 12 adds `confluent-kafka` for Kafka/Redpanda client compatibility. It does not add schema-registry libraries, ClickHouse ingestion pipeline dependencies, Feast dependencies, provider SDKs, scraping dependencies, broker/trading dependencies, heavy quant libraries, ML libraries, execution APIs, or real market ingestion. Tests use the in-memory event backbone fallback and do not require a running Kafka/Redpanda server.

## Prompt 13 Dependency Boundary

Prompt 13 adds the Data Quality + Validation Framework with no new dependency. It does not add Great Expectations, Pandera, Deequ, full quant/ML libraries, provider SDKs, scraping dependencies, broker/trading dependencies, execution APIs, real market ingestion, production validation pipelines, feature computation, or analytics signals.

## Prompt 14 Dependency Boundary

Prompt 14 adds Synthetic Market Data Fixtures with no new dependency. It uses the existing standard library, Pydantic, Polars, PyArrow, and local project contracts. It does not add market data SDKs, scraping dependencies, broker/trading dependencies, full quant/ML libraries, execution APIs, real market ingestion, production dataset writes, feature computation, analytics signals, or decisions.

## Prompt 15 Dependency Boundary

Prompt 15 adds Instrument Metadata Persistence Wiring with no new dependency. It uses the existing SQLAlchemy, Pydantic, FastAPI/TestClient, SQLite test fallback, and local project contracts. It does not add market data SDKs, scraping dependencies, broker/trading dependencies, full quant/ML libraries, execution APIs, real market ingestion, OHLCV persistence, provider calls, feature computation, analytics signals, or decisions.

## Prompt 16 Dependency Boundary

Prompt 16 adds Market Data Batch Persistence Contracts with no new dependency. It uses existing SQLAlchemy, Alembic, Pydantic, FastAPI/TestClient, SQLite test fallback, and local project contracts. It does not add market data SDKs, scraping dependencies, broker/trading dependencies, full quant/ML libraries, execution APIs, real market ingestion, full OHLCV persistence, provider calls, TimescaleDB writes, ClickHouse writes, event publishing, feature computation, analytics signals, or decisions.

## Prompt 20 Dependency Boundary

Prompt 20 adds Provider Adapter Guardrails with no new dependency. It uses standard library enums/datetime helpers, Pydantic contracts, FastAPI/TestClient, and existing provider capability enums. It does not add provider SDKs, scraping dependencies, broker/trading dependencies, full quant/ML libraries, external provider calls, real market ingestion, credentials, analytics signals, decisions, or execution APIs.

## Prompt 26 Analytics Dependency Boundary

Prompt 26 adds analytics foundation planning with no new dependency. It uses standard library enums/datetime helpers, Pydantic contracts, FastAPI/TestClient, and existing project settings.

The dependency stage is `contracts_only`. Heavy numerical, statistical, ML, GPU, options, and backtesting libraries such as NumPy, SciPy, Numba, JAX, CuPy, statsmodels, arch, scikit-learn, XGBoost, LightGBM, CatBoost, PyTorch, TensorFlow, QuantLib, vectorbt, and backtrader are documented as planned/evaluation candidates only. Prompt 26 does not require or install them and does not implement analytics calculations, features, signals, recommendations, decisions, backtests, or execution APIs.

## Prompt 27 Numerical Analytics Dependency Boundary

Prompt 27 adds Numerical Analytics Core Contracts with no new dependency. It uses standard library `math`, Pydantic contracts, FastAPI/TestClient, and existing project packages.

The numerical dependency stage is `contracts_and_safe_stdlib`. Heavy analytics dependencies such as NumPy, SciPy, Numba, JAX, CuPy, PyTorch, TensorFlow, statsmodels, arch, TA-Lib, vectorbt, backtrader, QuantLib, XGBoost, LightGBM, CatBoost, and scikit-learn remain blocked by the numerical dependency gate. Prompt 27 does not implement returns, volatility, drawdown, correlation, indicators, features, signals, recommendations, DecisionObject generation, decisions, backtests, or execution APIs.

## Prompt 28 Returns and Rolling Dependency Boundary

Prompt 28 adds Returns and Rolling Window Analytics v0 with no new dependency. It uses only standard-library `math`, Pydantic contracts, FastAPI/TestClient, and existing project packages.

No NumPy, SciPy, Numba, JAX, CuPy, PyTorch, TensorFlow, statsmodels, arch, TA-Lib, vectorbt, backtrader, QuantLib, XGBoost, LightGBM, CatBoost, scikit-learn, provider SDK, scraping dependency, or broker/trading dependency is added. Prompt 28 does not implement volatility, drawdown, correlation, indicators, features, signals, recommendations, DecisionObject generation, decisions, backtests, or execution APIs.

## Prompt 29 Volatility and Drawdown Dependency Boundary

Prompt 29 adds Volatility and Drawdown Analytics v0 with no new dependency. It uses only standard-library `math`, Pydantic contracts, FastAPI/TestClient, and existing project packages.

No NumPy, SciPy, Numba, JAX, CuPy, PyTorch, TensorFlow, statsmodels, arch, TA-Lib, vectorbt, backtrader, QuantLib, XGBoost, LightGBM, CatBoost, scikit-learn, provider SDK, scraping dependency, or broker/trading dependency is added. Prompt 29 does not implement correlation, beta, indicators, features, signals, recommendations, DecisionObject generation, decisions, backtests, regimes, or execution APIs.

## Prompt 30 Analytics Dependency Audit

Prompt 30 adds no dependency. It audits the analytics dependency posture and confirms no heavy analytics dependencies were newly added unexpectedly across Prompts 26-29.

Current analytics remains standard-library/Pydantic/FastAPI/TestClient plus existing project packages only. NumPy, SciPy, Numba, JAX, CuPy, PyTorch, TensorFlow, statsmodels, arch, TA-Lib, vectorbt, backtrader, QuantLib, XGBoost, LightGBM, CatBoost, scikit-learn, provider SDKs, scraping dependencies, and broker/trading dependencies remain gated until future explicit prompts.

## Prompt 31 Correlation and Beta Dependency Boundary

Prompt 31 adds Correlation and Beta Analytics v0 with no new dependency. It uses only standard-library `math`, Pydantic contracts, FastAPI/TestClient, and existing project packages.

No NumPy, SciPy, Numba, JAX, CuPy, PyTorch, TensorFlow, statsmodels, arch, TA-Lib, vectorbt, backtrader, QuantLib, XGBoost, LightGBM, CatBoost, scikit-learn, provider SDK, scraping dependency, or broker/trading dependency is added. Prompt 31 does not implement indicators, features, signals, recommendations, DecisionObject generation, decisions, backtests, regimes, or execution APIs.

## Prompt 32 Time-Series Diagnostics Dependency Boundary

Prompt 32 adds Time-Series Diagnostics Foundation with no new dependency. It uses
only standard-library `datetime` and `math`, Pydantic contracts,
FastAPI/TestClient, and existing project packages.

No NumPy, SciPy, Numba, JAX, CuPy, PyTorch, TensorFlow, statsmodels, arch,
TA-Lib, vectorbt, backtrader, QuantLib, XGBoost, LightGBM, CatBoost,
scikit-learn, provider SDK, scraping dependency, or broker/trading dependency is
added. Prompt 32 does not implement stationarity tests, ADF, KPSS, Hurst,
autocorrelation analytics, regime detection, indicators, features, signals,
recommendations, DecisionObject generation, decisions, backtests, or execution
APIs.

## Prompt 33 Regime Analytics Dependency Boundary

Prompt 33 adds Regime Analytics Planning and Guardrails with no new dependency.
It uses only standard-library datetime helpers, Pydantic contracts,
FastAPI/TestClient, and existing project packages.

No NumPy, SciPy, Numba, JAX, CuPy, PyTorch, TensorFlow, statsmodels, arch,
TA-Lib, vectorbt, backtrader, QuantLib, XGBoost, LightGBM, CatBoost,
scikit-learn, sklearn, hmmlearn, ruptures, provider SDK, scraping dependency,
or broker/trading dependency is added. Prompt 33 does not implement
stationarity tests, HMMs, clustering, ML models, regime classification,
indicators, features, signals, recommendations, DecisionObject generation,
decisions, backtests, or execution APIs.

## Prompt 34 Regime Feature Preparation Dependency Boundary

Prompt 34 adds Regime Feature Preparation Contracts with no new dependency. It
uses only standard-library datetime helpers, Pydantic contracts,
FastAPI/TestClient, and existing project packages.

No NumPy, SciPy, Numba, JAX, CuPy, PyTorch, TensorFlow, statsmodels, arch,
TA-Lib, vectorbt, backtrader, QuantLib, XGBoost, LightGBM, CatBoost,
scikit-learn, sklearn, hmmlearn, ruptures, provider SDK, scraping dependency,
or broker/trading dependency is added. Prompt 34 does not implement feature
computation, feature registry writes, classifier inputs, regime
classification, indicators, signals, recommendations, DecisionObject
generation, decisions, backtests, or execution APIs.

## Prompt 35 Analytics/Regime Dependency Audit

Prompt 35 adds no dependency. It audits Prompts 26-34 and confirms no heavy
analytics/model dependencies, provider SDKs, scraping dependencies, or
broker/trading dependencies were newly added unexpectedly.

The analytics/regime implementation remains standard library, Pydantic,
FastAPI/TestClient, and existing project packages. NumPy, SciPy, pandas,
statsmodels, sklearn, hmmlearn, ruptures, PyTorch, TensorFlow, XGBoost,
LightGBM, CatBoost, QuantLib, TA-Lib, vectorbt, backtrader, provider SDKs,
scraping libraries, and broker/trading libraries remain gated until future
audited prompts explicitly allow them.

Prompt 35 does not implement feature computation, feature registry writes,
classifier inputs, regime classification, stationarity tests, indicators,
signals, recommendations, DecisionObject generation, decisions, backtests, or
execution APIs.
