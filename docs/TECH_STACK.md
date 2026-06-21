# Technical Stack

Prompt 11 audits the complete target stack while installing no new dependencies.

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
