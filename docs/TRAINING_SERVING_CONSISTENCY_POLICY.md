# Training / Serving Consistency Policy

Training/serving consistency means features used in research, training, validation, backtests, and future serving workflows must share definitions, versions, entity keys, timestamps, and lineage.

## Core Concepts

- Feature definitions must be versioned.
- Feature values must carry event timestamps.
- Creation timestamps must be distinct from event timestamps.
- Feature snapshots must be reproducible.
- Source data references must point back to auditable inputs.
- Lineage must record upstream sources, upstream features, and transformations.
- Quality reports must accompany future feature snapshots.

## Event Timestamp vs Created Timestamp

`event_timestamp` is the time the feature value represents. `created_at` or `computed_at` is when Stark Terminal produced or recorded the value. These timestamps must not be conflated.

## Source And Lineage

Feature snapshots should reference source datasets, code/rule versions, and upstream features. Lineage is required by default in Prompt 10 settings.

## Feast Planned

Feast may be considered later for offline/online consistency, feature serving, and registry governance. It is planned only. Prompt 10 does not install Feast, run Feast services, or create Feast feature views.

## Prompt 10 Boundary

Prompt 10 does not compute features, train ML models, serve models, implement feature pipelines, ingest market data, or create execution APIs. The Feature Registry supports future analytics and decision support, not current trading decisions.
