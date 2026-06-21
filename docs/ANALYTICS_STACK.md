# Analytics Stack

Prompt 14 audits the analytical target stack and current foundations: DuckDB/Parquet research lake foundation, Redis cache foundation, Redis Streams foundation, Kafka/Redpanda Event Backbone foundation, Data Quality + Validation Framework, Synthetic Fixtures foundation, Worker System foundation, Instrument Master/Provider Contracts foundation, ClickHouse Warehouse foundation, and Feature Registry foundation. Actual numerical, statistical, ML, optimization, options, risk, backtesting, feature computation, and NLP engines still happen in later prompts.

## Numerical Computing Layer

The numerical layer will use NumPy, SciPy, pandas, Polars, Numba, JAX, and CuPy where appropriate. Future optional C++ modules may use Eigen, Intel MKL, OpenBLAS, and Boost for performance-sensitive workloads.

## Statistical / Time-Series Layer

The time-series layer will support ARIMA/SARIMA, GARCH, Kalman Filters, Hidden Markov Models, State-Space Models, Johansen cointegration, PCA, Factor Models, Bayesian Models, and Monte Carlo simulation.

## ML Layer

The ML layer will support scikit-learn, XGBoost, LightGBM, CatBoost, Random Forest, Elastic Net, PyTorch, TensorFlow, and JAX. ML models must be validated and treated as evidence sources, not authoritative trade generators.

## Optimization Layer

The optimization layer will support CVXPY, OSQP, optional Gurobi, optional MOSEK, portfolio optimization, risk parity, Kelly criterion, position sizing, and transaction cost minimization.

## Options Analytics Layer

The options layer will support QuantLib, custom pricers later, Black-Scholes, Heston, SABR, Local Volatility, Monte Carlo, Binomial Trees, Finite Difference Methods, and Greeks.

## Backtesting Layer

The backtesting layer will include an internal deterministic backtesting engine and may integrate or reference VectorBT, Backtrader, NautilusTrader, Zipline as reference only if useful, and QuantConnect as an external reference only.

## Risk Analytics Layer

The risk layer will support VaR, Expected Shortfall, Stress Testing, Scenario Analysis, Greeks, Correlation Models, drawdown analysis, exposure checks, and risk explanations for user-facing decisions.

## NLP / Paper Research Layer

The research layer will later support Transformers, Sentence Transformers, news sentiment, event detection, paper understanding, research object extraction, StrategyCandidate generation, experiment tracking, and reproducible research artifacts.

## Prompt 10 Status

Implemented in Prompt 04:

- DuckDB local query helper foundation
- Parquet read/write helper foundation
- Research lake zone contracts
- Dataset manifest and in-memory registry placeholders

Implemented in Prompt 05:

- Redis cache configuration contracts
- Cache key namespace policy
- Redis cache client wrapper
- In-memory local/test cache fallback
- Cache health checks

Implemented in Prompt 06:

- Redis Streams configuration contracts
- Stream naming policy
- EventEnvelope contract
- Stream producer and consumer wrappers
- In-memory local/test stream fallback
- Stream health checks

Implemented in Prompt 07:

- Worker configuration contracts
- Worker role policy
- JobEnvelope and WorkerResult contracts
- Base worker lifecycle abstraction
- Worker registry and in-process harness
- Worker health checks

Implemented in Prompt 08:

- Instrument symbol normalization contracts
- Instrument universe snapshot contracts
- Local synthetic instrument master
- Read-only market data provider interfaces
- Market data request/response contracts
- Provider capability reports

Implemented in Prompt 09:

- ClickHouse analytical warehouse table contracts
- DDL helpers that return SQL strings only
- Disabled-safe warehouse client wrapper
- Memory query recorder for local/test fallback
- Warehouse health checks

Implemented in Prompt 10:

- Feature definition contracts
- Feature set contracts
- Feature value and snapshot contracts
- Feature quality report contracts
- Feature lineage contracts
- In-memory custom Stark Feature Registry
- Feature registry health checks

Still documentation-only:

- Numerical computing implementations
- Statistical/time-series models
- ML models
- Feature computation pipelines
- Optimization routines
- Options analytics
- Backtesting
- Risk analytics
- NLP and Paper Lab

Prompt 10 adds Feature Registry contracts so future analytics, regime, decision, backtest, and model workflows can use governed feature metadata after real feature computation is explicitly implemented. Analytics engines, models, trading decisions, feature computation, and production dashboards remain deferred.

## Prompt 11 Analytics Audit

Prompt 11 confirms analytics engines/models are not implemented yet. The current repository contains contracts, schemas, health checks, and local/test helpers only. no execution APIs, no real market ingestion, and no feature computation are present.

## Prompt 12 Event Backbone Status

Prompt 12 adds Kafka/Redpanda Event Backbone contracts so future analytics, feature, regime, decision, backtest, and warehouse pipelines can use durable event semantics after explicit pipeline prompts. Analytics engines/models, production event pipelines, real market ingestion, feature computation, and trading decisions remain deferred.

## Prompt 13 Data Quality Status

Prompt 13 adds deterministic validation contracts, built-in validators, validation reports, and quality gates so future analytics, feature, regime, decision, backtest, and warehouse workflows can require validated data before use. Validators are not indicators, factors, models, alpha signals, analytics signals, or trading decisions. Analytics engines/models, production validation pipelines, real market ingestion, feature computation, and trading decisions remain deferred.

## Prompt 14 Synthetic Fixture Status

Prompt 14 adds deterministic synthetic OHLCV fixtures for future analytics tests. Fixture data is synthetic, local-only, test/dev only, not real market data, not trading data, and not investment advice.

Synthetic fixture data must not be interpreted as signal data, decision data, model evidence, backtest results, or production market history. Analytics engines/models, production validation pipelines, real market ingestion, feature computation, backtesting, and trading decisions remain deferred.

## Prompt 15 Instrument Persistence Status

Prompt 15 adds Instrument Metadata Persistence Wiring for canonical instrument metadata only. It supports future analytics by giving instruments a validated metadata repository, but it does not implement indicators, feature computation, models, analytics signals, backtesting, options analytics, or decisions.

## Prompt 16 Market Data Batch Metadata Status

Prompt 16 adds Market Data Batch Persistence Contracts for validated synthetic/local batch metadata only. It supports future analytics by making batch row counts, time ranges, source references, fixture ids, and validation report ids auditable before future data movement.

This is not an analytics engine. It does not persist full OHLCV bars, compute indicators, feature values, model inputs, analytics signals, backtest results, options analytics, or decisions.
