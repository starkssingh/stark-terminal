# DecisionObject Specification

## Purpose

DecisionObject is the central contract of Stark Terminal. Every visible recommendation, state label, or action state must eventually be backed by a DecisionObject or an auditable successor contract.

Prompt 01 defines an enriched schema placeholder. It is not a live decision engine and does not generate trade calls.

## Required Fields

- `instrument`: Instrument symbol or identifier.
- `exchange`: Market or exchange.
- `segment`: Market segment.
- `timeframe`: Analysis timeframe.
- `regime`: Market regime, nullable in Prompt 00.
- `state`: Market state, nullable in Prompt 00.
- `action_state`: Decision action state.
- `confidence`: Score from 0 to 100.
- `confidence_method`: How confidence was produced.
- `risk`: Risk level.
- `evidence`: List of evidence strings.
- `invalidation`: What would invalidate the decision, nullable in Prompt 00.
- `horizon`: Expected decision horizon, nullable in Prompt 00.
- `source_data_reference`: Source data reference, nullable in Prompt 00.
- `decision_source`: Source category for the decision.
- `audit_id`: Optional audit identifier.
- `model_or_rule_version`: Optional version for the rule, model, or review process.
- `generated_at`: UTC timestamp.

## Action State Enum

- `STRONG_BUY_BIAS`
- `BUY_BIAS`
- `WATCH`
- `HOLD`
- `REDUCE_CAUTION`
- `AVOID`
- `SELL_BIAS`
- `STRONG_SELL_BIAS`

## Confidence

Confidence is a numeric score from 0 to 100. It is not a guarantee and must eventually be traceable to evidence, validation state, and model or rule version.

`confidence_method` may be `RULE_SCORE`, `BACKTEST_SIMILARITY`, `MODEL_PROBABILITY`, `ENSEMBLE`, `HUMAN_OVERRIDE`, or `UNKNOWN`.

## Risk

Risk is represented by `LOW`, `MEDIUM`, `HIGH`, or `EXTREME`. Later versions must connect risk labels to explicit calculations or rules.

## Evidence List

Evidence is a list of concise supporting observations. Later versions must distinguish raw facts, computed metrics, model outputs, and human notes where needed.

Directional actionable states require evidence in Prompt 01:

- `BUY_BIAS`
- `STRONG_BUY_BIAS`
- `SELL_BIAS`
- `STRONG_SELL_BIAS`

## Invalidation

Invalidation describes the condition that weakens or cancels the decision state. User-facing decision outputs must include invalidation in later versions.

## Horizon

Horizon describes the expected relevance window for the decision state, such as intraday, swing, positional, or a precise duration.

## Source Data Reference

Source data reference points to the dataset, event, snapshot, or query result used to generate the decision. Later versions must make this auditable and reproducible.

## Decision Source

`decision_source` may be `RULE_BASED`, `BACKTEST_DERIVED`, `MODEL_ASSISTED`, `HUMAN_REVIEWED`, `PAPER_DERIVED`, or `UNKNOWN`.

## Audit and Versioning

`audit_id` and `model_or_rule_version` are included as optional fields in Prompt 01. They prepare the contract for later persistence, event logs, reproducibility, and model/rule governance.

Prompt 01 still does not implement a decision engine, model scoring, trade recommendation system, or execution workflow. Later versions should require invalidation for actionable states before production-grade user-facing output.
