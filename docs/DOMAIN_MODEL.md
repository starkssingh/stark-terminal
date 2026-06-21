# Domain Model

Prompt 13 defines typed contracts for Stark Terminal's core domain, market data requests/responses, feature registry governance, durable events, and data quality validation. These schemas are contracts only. They do not ingest real data, connect to external providers, create production datasets, compute features, run analytics, create analytics signals, place orders, or execute trades.

## Purpose

The domain model gives future infrastructure, analytics, API, desktop, and worker code a durable vocabulary. It keeps identifiers, market data, derivatives, options, audit metadata, and decision objects typed and validated before persistence or ingestion systems are introduced.

## InstrumentId

`InstrumentId` identifies an instrument by normalized uppercase symbol, exchange, and market segment. Its stable string representation is `EXCHANGE:SYMBOL:SEGMENT`, such as `NSE:RELIANCE:NSE_EQUITY`.

## Instrument

`Instrument` describes an instrument with display name, asset class, status, optional lot size, tick size, ISIN, sector, industry, and metadata. Lot size and tick size must be positive when provided.

## MarketDataBar

`MarketDataBar` defines one OHLCV-style bar for an instrument, timeframe, UTC-normalized timestamp, prices, optional volume/open interest, provider identity, quality status, and source data reference. OHLC prices must be positive and internally consistent.

## FuturesContract

`FuturesContract` defines a future by underlying instrument, contract symbol, expiry, lot size, optional tick size, provider, and metadata. It is a contract schema only, not a trading or pricing implementation.

## OptionContract

`OptionContract` defines an option by underlying instrument, contract symbol, expiry, strike, option type, lot size, optional tick size, provider, and metadata. Strike, lot size, and tick size must be positive when present.

## OptionsChainSnapshot

`OptionsChainSnapshot` groups option contracts for one underlying and expiry at one UTC-normalized timestamp. All contracts must share the same underlying and expiry.

## AuditMetadata

`AuditMetadata` records an audit ID, UTC created timestamp, source, optional source data reference, optional model or rule version, and notes. This prepares later persistence and event logs without implementing them in Prompt 01.

## DecisionObject

`DecisionObject` remains the central decision-support contract. Prompt 01 enriches it with `confidence_method`, `decision_source`, `audit_id`, and `model_or_rule_version`. Directional action states require evidence. Later versions should require invalidation for actionable states before user-facing production use.

## Instrument Universe Snapshot

`InstrumentUniverseSnapshot` captures a versioned local universe with snapshot ID, source, instruments, UTC creation timestamp, schema version, and notes. Prompt 08 uses synthetic/local fixtures only and rejects duplicate instrument keys.

## MarketDataRequest

`MarketDataRequest` defines read-only market data requests with request ID, kind, optional instrument, timeframe, start/end range, provider identity, adjustment mode, schema version, and UTC creation timestamp. Historical bar requests require instrument, timeframe, start, and end. Start must be before end.

## MarketDataResponse

`MarketDataResponse` carries provider metadata, bars, instruments, quality status, source data reference, UTC received timestamp, and sanitized errors. Responses must contain bars, instruments, or errors.

## ProviderCapabilityReport

`ProviderCapabilityReport` describes provider identity, status, declared read-only capabilities, network-call policy, schema version, and notes. Prompt 08 implements only local synthetic provider behavior and no external calls.

## Feature Registry Contracts

Prompt 10 adds FeatureDefinition, FeatureSet, FeatureEntity, FeatureValue, FeatureSnapshot, FeatureQualityReport, and FeatureLineageRecord contracts. These govern future feature metadata, source references, freshness/staleness, quality, and lineage. They do not compute features, train models, ingest market data, implement Feast, or generate trade calls.

## Prompt 15 Instrument Persistence Wiring

The `Instrument` domain model now has metadata-only persistence wiring through `InstrumentRepository` and `InstrumentMetadataService`. Identity remains the stable `InstrumentId` tuple of symbol, exchange, and segment. Repository lookups normalize symbol/exchange/segment before querying.

This wiring does not change the domain model into a market-data ingestion model. It persists instrument metadata only, requires validation-before-persistence by default, allows synthetic local/test/dev seeding, and exposes no execution APIs.

## Prompt 16 Market Data Batch Metadata

Prompt 16 adds `MarketDataBatchMetadata` and `MarketDataBatchPersistenceResult`.

`MarketDataBatchMetadata` captures batch-level metadata for validated synthetic/local `MarketDataBatch` objects: `batch_id`, `instrument_id`, `timeframe`, provider identity, `quality_status`, `row_count`, start/end timestamps, `source_data_reference`, synthetic flag, fixture linkage, dataset manifest linkage, validation report linkage, schema version, creation time, and sanitized notes.

`MarketDataBatchPersistenceResult` captures safe persistence outcomes without exposing secrets. The helper `metadata_from_batch` builds metadata from a `MarketDataBatch` after checking that a batch contains one instrument, one timeframe, a source reference, and a stable time range.

This model is batch metadata only. It does not store full OHLCV bars, does not represent real market ingestion, does not create trading signals, and exposes no execution APIs.

## DurableEventEnvelope

Prompt 12 adds DurableEventEnvelope contracts for the Kafka/Redpanda Event Backbone foundation. They reuse EventType, EventSource, and EventPriority from Redis Streams EventEnvelope semantics while adding explicit topic, key, and partition fields. Durable events are coordination/replay contracts only; Kafka/Redpanda is not system of record and does not implement production pipelines, market ingestion, broker integrations, or execution APIs.

## Data Quality Contracts

Prompt 13 adds ValidationIssue, ValidationRule, ValidationResult, ValidationReport, QualityGatePolicy, and QualityGateResult contracts. These provide deterministic local validation and conservative quality gate decisions for existing contracts such as instruments, market data bars, options snapshots, dataset manifests, feature snapshots, feature quality reports, and warehouse table contracts.

Data quality contracts do not ingest market data, make external provider calls, compute analytics signals, compute features, train models, generate decisions, or enable execution APIs.
