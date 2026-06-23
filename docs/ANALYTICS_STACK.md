# Analytics Stack

Prompt 33 adds Regime Analytics planning and guardrails while keeping analytics descriptive/data-quality/governance-only. Current data foundations include DuckDB/Parquet research lake foundation, Redis cache, Redis Streams, Kafka/Redpanda Event Backbone, Data Quality + Validation Framework, Synthetic Fixtures, Instrument Metadata Persistence Wiring, Market Data Batch Persistence Contracts, TimescaleDB Synthetic OHLCV Storage Foundation, Synthetic OHLCV Research Lake Export, Provider Adapter Guardrails, Provider Readiness governance, Local Sample Provider Adapter v0, Local File Provider Adapter v0, Worker System, Instrument Master/Provider Contracts, ClickHouse Warehouse, Feature Registry, analytics foundation planning contracts, numerical core contracts, descriptive returns/rolling contracts, descriptive volatility/drawdown contracts, descriptive correlation/beta contracts, time-series diagnostics contracts, regime planning contracts, and analytics milestone audit coverage. Actual indicators, stationarity tests, statistical models beyond scoped stdlib relationship metrics, ML, optimization, options, backtesting, feature computation, actual regime classification, and NLP engines still happen in later prompts.

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

- Numerical computing implementations beyond planning contracts
- Statistical/time-series models
- ML models
- Feature computation pipelines
- Optimization routines
- Options analytics
- Backtesting
- Risk analytics
- NLP and Paper Lab

Implemented in Prompt 26:

- Analytics input contracts requiring validated inputs and source references.
- Analytics output contracts restricted to descriptive/research-only semantics.
- Analytics module plans for numerical core, returns, rolling windows, volatility, drawdown, correlation and beta, diagnostics, regime analytics planning, and backtesting planning.
- Analytics safety policy blocking signals, recommendations, execution-ready outputs, and real-data assumptions.
- Analytics dependency staging with current stage `contracts_only`.
- Analytics roadmap metadata and health checks.

Prompt 26 implements no analytics calculations, indicators, features, signals, recommendations, decisions, backtests, model outputs, or execution APIs.

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

## Prompt 17 Data Foundation Audit Status

Prompt 17 confirms synthetic fixtures and metadata persistence can support future analytics tests, but no analytics engine exists yet. The audit confirms no real market ingestion, no full OHLCV production persistence, no feature computation, no indicators, no analytics signals, no model outputs, no backtest results, and no decisions are produced by Prompts 14-16.

## Prompt 18 Synthetic OHLCV Storage Status

Prompt 18 adds synthetic-only OHLCV storage for future data movement tests. Stored synthetic bars remain local/test/dev data and are not indicators, factors, model features, analytics signals, backtest evidence, trading decisions, or investment advice.

Analytics engines/models, production validation pipelines, real market ingestion, feature computation, backtesting, options analytics, and trading decisions remain deferred.

## Prompt 19 Synthetic OHLCV Export Status

Prompt 19 adds synthetic-only OHLCV export to Parquet research artifacts for future data movement tests. Exported synthetic datasets remain local/test/dev data and are not indicators, factors, model features, analytics signals, backtest evidence, trading decisions, or investment advice.

The export service does not compute analytics, features, signals, decisions, backtests, regimes, options analytics, or model outputs. It is a research lake data movement contract only.

## Prompt 20 Provider Guardrail Status

Prompt 20 adds Provider Adapter Guardrails for future data-source planning. Guardrails, approvals, compliance checklists, and readiness reports are not analytics engines, indicators, features, model inputs, trading signals, backtest evidence, decisions, or investment advice.

Provider guardrails do not call providers, scrape websites, ingest real market data, compute analytics, generate signals, generate decisions, or enable execution APIs.

## Prompt 22 Data Foundation Milestone Audit Status

Prompt 22 audits synthetic OHLCV storage, synthetic OHLCV research lake export, provider guardrails, and Local Sample Provider Adapter v0. The audit confirms these foundations are data movement/governance contracts only.

Synthetic bars, exported Parquet artifacts, provider guardrail reports, and local sample provider responses must not be interpreted as analytics signals, features, model evidence, backtest evidence, trading decisions, recommendations, or investment advice.

Analytics engines, feature computation, indicators, models, regimes, options analytics, backtesting, generated signals, and decision generation remain unimplemented.

## Prompt 24 Local File Provider Status

Prompt 24 adds Local File Provider Adapter v0 for local/test/dev file parsing and provider response validation. Local file provider responses are not indicators, factors, model features, analytics signals, backtest evidence, trading decisions, or investment advice.

The adapter does not compute analytics, features, signals, decisions, backtests, regimes, options analytics, or model outputs. It does not ingest real market data, call providers, scrape, load credentials, or expose execution APIs.

## Prompt 25 Provider Adapter Milestone Audit Status

Prompt 25 audits provider guardrails, provider readiness/candidate selection, Local Sample Provider, and Local File Provider before analytics planning starts. The audit confirms provider responses and governance reports remain data-boundary artifacts only.

Provider health, contracts, candidate scores, local sample responses, and local file responses must not be interpreted as indicators, factors, model features, analytics signals, backtest evidence, trading decisions, recommendations, or investment advice.

## Prompt 26 Analytics Foundation Plan Status

Prompt 26 adds the analytics foundation package and read-only `/analytics-foundation` API surfaces. The foundation is planning-only and descriptive/research-only. It requires future analytics to use validated inputs, source references, tests, docs, and safety audits.

No analytics calculations exist yet. No heavy numerical, statistical, ML, GPU, options, or backtesting dependency is required by Prompt 26. No trading signals, recommendations, decisions, feature computation, model outputs, backtests, or execution APIs are implemented.

## Prompt 27 Numerical Analytics Core Contracts Status

Prompt 27 adds the numerical analytics package and read-only `/numerical-analytics` API surfaces. The package defines source reference, vector, table, computation request, computation result, validation, dependency gate, summary, and health contracts.

Only tiny generic standard-library descriptive summaries are allowed now: count, min, max, and mean. These helpers are not returns, volatility, drawdown, correlation, indicators, features, signals, recommendations, decisions, or backtests.

No heavy numerical dependency is required by Prompt 27. The numerical dependency stage is `contracts_and_safe_stdlib`, and NumPy, SciPy, Numba, JAX, CuPy, PyTorch, TensorFlow, statsmodels, arch, TA-Lib, vectorbt, backtrader, QuantLib, XGBoost, LightGBM, CatBoost, and scikit-learn remain blocked until a future explicit prompt.

## Prompt 28 Returns and Rolling Analytics Status

Prompt 28 adds descriptive Returns Analytics v0 and Rolling Window Analytics v0. It uses standard-library math only and Prompt 27 numerical contracts.

Implemented now:

- simple returns.
- log returns where prices are positive.
- rolling count.
- rolling mean.
- rolling min.
- rolling max.
- validation for finite prices, positive prices, source references, and rolling windows.
- `/returns-analytics/health` and `/returns-analytics/contracts` metadata endpoints.

Prompt 28 does not implement volatility, drawdown, correlation, beta, indicators, feature computation, ML models, regimes, backtests, signals, recommendations, DecisionObject generation, decisions, or execution APIs.

## Prompt 29 Volatility and Drawdown Analytics Status

Prompt 29 adds descriptive Volatility Analytics v0 and Drawdown Analytics v0. It uses standard-library `math` only and Prompt 27 numerical contracts.

Implemented now:

- sample standard deviation of validated return vectors.
- population standard deviation of validated return vectors.
- annualized volatility when explicit positive periods_per_year is supplied.
- drawdown series using current_value / running_peak - 1.
- max drawdown.
- drawdown duration.
- validation for finite returns, finite positive value vectors, annualization parameters, and source references.
- `/risk-analytics/health` and `/risk-analytics/contracts` metadata endpoints.

Prompt 29 does not implement correlation, beta, indicators, feature computation, ML models, regimes, backtests, signals, recommendations, DecisionObject generation, decisions, or execution APIs. Volatility and drawdown results are descriptive-only and not trading interpretation.

## Prompt 30 Analytics Milestone Audit Status

Prompt 30 audits Prompt 26 analytics foundation planning, Prompt 27 numerical contracts, Prompt 28 returns/rolling analytics, and Prompt 29 volatility/drawdown analytics.

Implemented descriptive analytics set after audit:

- analytics foundation planning/contracts/guardrails.
- numerical source/vector/table contracts and validation.
- tiny count/min/max/mean summaries.
- simple returns.
- log returns.
- rolling count, rolling mean, rolling min, and rolling max.
- sample standard deviation.
- population standard deviation.
- explicitly parameterized annualized volatility.
- drawdown series.
- max drawdown.
- drawdown duration.

Prompt 30 adds no new analytics calculation. It confirms no heavy dependencies, no real ingestion, no external calls, no signals, no recommendations, no DecisionObject generation, no decisions, no backtests, no regimes, no indicators, no correlation or beta, no feature computation, and no execution APIs.

## Prompt 31 Correlation and Beta Analytics Status

Prompt 31 adds descriptive Correlation Analytics v0 and Beta Analytics v0. It uses standard-library `math` only and Prompt 27 numerical contracts.

Implemented now:

- Pearson correlation.
- sample covariance.
- sample variance.
- sample-covariance beta.
- validation for equal-length paired vectors, finite values, minimum observations, zero variance, and source references.
- `/relationship-analytics/health` and `/relationship-analytics/contracts` metadata endpoints.

Prompt 31 does not implement indicators, feature computation, ML models, regimes, backtests, signals, recommendations, DecisionObject generation, decisions, or execution APIs. Correlation and beta results are descriptive-only and not trading interpretation.

## Prompt 32 Time-Series Diagnostics Status

Prompt 32 adds Time-Series Diagnostics Foundation. It uses standard-library
`datetime`, `math`, Pydantic contracts, FastAPI/TestClient, and Prompt 27
source-reference contracts.

Implemented now:

- timestamp series contracts.
- timezone-aware timestamp validation.
- monotonicity diagnostics.
- duplicate timestamp diagnostics.
- fixed-interval gap diagnostics.
- irregular interval diagnostics.
- spacing summaries.
- `/time-series-diagnostics/health` and `/time-series-diagnostics/contracts` metadata endpoints.

Prompt 32 does not implement stationarity tests, ADF, KPSS, Hurst,
autocorrelation analytics, regime detection, indicators, feature computation, ML
models, backtests, signals, recommendations, DecisionObject generation,
decisions, or execution APIs. Time-series diagnostics results are
descriptive/data-quality-only and not trading interpretation.

## Prompt 33 Regime Analytics Planning Status

Prompt 33 adds Regime Analytics planning and guardrails. It uses standard
library datetime helpers, Pydantic contracts, FastAPI/TestClient, and existing
project packages.

Implemented now:

- regime label placeholder contracts.
- regime evidence requirement contracts.
- regime safety policy contracts.
- regime readiness report templates.
- regime dependency staging.
- regime roadmap metadata.
- `/regime-analytics/health`, `/regime-analytics/contracts`, `/regime-analytics/readiness-template`, and `/regime-analytics/dependency-gate` metadata endpoints.

Prompt 33 does not implement actual regime classification, regime detection,
stationarity tests, HMMs, clustering, ML models, indicators, feature
computation, backtests, signals, recommendations, DecisionObject generation,
decisions, or execution APIs. Regime outputs are planning-only and not trading
interpretation.

## Prompt 34 Regime Feature Preparation Status

Prompt 34 adds Regime Feature Preparation Contracts. It uses standard-library
datetime helpers, Pydantic contracts, FastAPI/TestClient, and existing project
packages.

Implemented now:

- regime feature candidate contracts.
- regime feature group plans.
- regime feature provenance requirements.
- regime feature evidence mapping.
- regime feature readiness report templates.
- regime feature safety policy contracts.
- regime feature dependency staging.
- `/regime-features/health`, `/regime-features/contracts`, `/regime-features/readiness-template`, and `/regime-features/dependency-gate` metadata endpoints.

Prompt 34 does not implement feature computation, feature registry writes,
classifier inputs, actual regime classification, regime detection, stationarity
tests, HMMs, clustering, ML models, indicators, backtests, signals,
recommendations, DecisionObject generation, decisions, or execution APIs.
Regime feature outputs are contracts-only and not trading interpretation.

## Prompt 35 Analytics/Regime Milestone Audit Summary

Prompt 35 audits the implemented analytics/regime set:

- analytics foundation planning and guardrails.
- numerical contracts, validation, dependency gate, and tiny summaries.
- returns and rolling window analytics v0.
- volatility and drawdown analytics v0.
- correlation and beta analytics v0.
- time-series diagnostics foundation.
- regime analytics planning and guardrails.
- regime feature preparation contracts.

The audit confirms the stack remains descriptive/research/data-quality-only or
planning/contracts-only. It confirms no feature computation, no feature registry
writes, no classifier inputs, no actual regime classification, no stationarity
tests, no signals, no recommendations, no DecisionObject generation, no
backtests, no regimes computed, and no execution APIs.

Prompt 35 marks the analytics/regime foundation ready for Decision Desk
planning and guardrails only.
