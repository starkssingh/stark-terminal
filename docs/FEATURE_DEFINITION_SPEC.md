# Feature Definition Specification

Feature definitions describe governed feature metadata. They do not compute values in Prompt 10.

## FeatureDependency

- `name`: Upstream feature name.
- `version`: Optional upstream version.
- `feature_set`: Optional upstream feature set.

Dependency names must be non-empty and must not imply execution, order placement, broker credentials, or live trading.

## FeatureDefinition

Fields:

- `feature_id`: Stable feature identifier.
- `name`: Feature name.
- `version`: Version string, default `v1`.
- `description`: Human-readable description.
- `value_type`: Feature value type.
- `entity_type`: Entity scope such as instrument, instrument-timeframe, market, or sector.
- `frequency`: Expected update frequency.
- `status`: Draft, active, deprecated, disabled, or unknown.
- `owner`: Owning team/person.
- `entity_keys`: Required entity key names.
- `dependencies`: Upstream feature dependencies.
- `computation_mode`: Future computation mode metadata.
- `freshness_seconds`: Expected freshness target.
- `max_staleness_seconds`: Maximum acceptable staleness.
- `source_data_references`: Upstream data references.
- `tags`, `notes`, `created_at`, `updated_at`.

Feature names, IDs, owner, description, version, and entity keys must be non-empty. Entity keys must be safe identifiers.

## FeatureSet

FeatureSet groups compatible features by entity type. It includes a stable ID, name, version, description, owner, status, tags, notes, and feature definitions. Feature sets reject empty feature lists, duplicate feature keys, and incompatible entity types.

## FeatureEntity

FeatureEntity identifies the entity a value belongs to. Keys must be non-empty strings and must not contain secret-like names such as token, password, API key, credential, database URL, Redis URL, or broker token.

## FeatureValue

FeatureValue records one typed feature value for an entity at an explicit event timestamp. It carries feature name, version, entity, value, value type, event timestamp, creation timestamp, and optional source data reference.

Type checks are intentionally lightweight:

- FLOAT accepts int or float, not bool.
- INTEGER accepts int, not bool.
- BOOLEAN accepts bool.
- STRING and CATEGORY accept str.
- TIMESTAMP accepts datetime or ISO string.
- JSON accepts JSON-serializable values.

## FeatureSnapshot

FeatureSnapshot groups feature values for a feature set with source data references, computation mode, computed timestamp, schema version, and notes. It prepares reproducibility metadata but does not compute features.

## Naming And Versioning

Canonical feature keys use:

```text
feature_name:version
```

Feature set keys use the same format. Versions default to `v1`.

## Forbidden Feature Categories

The following are forbidden in Prompt 10:

- Execution features.
- Order placement features.
- Broker credential features.
- Live trading trigger features.

No feature definition may bypass the Stark Terminal safety exclusions.

