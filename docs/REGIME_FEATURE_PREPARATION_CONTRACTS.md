# Regime Feature Preparation Contracts

Prompt 34 implements Regime Feature Preparation contracts for Stark Terminal.
This is a contracts-only and preparation-only layer.

## Purpose

Regime Feature Preparation defines metadata for future regime feature
candidates before any feature values exist. It maps existing descriptive
analytics families to future feature candidates and records what provenance,
evidence, and quality requirements must exist first.

## Current Scope

Prompt 34 adds:

- metadata-only feature candidates.
- feature groups.
- feature provenance requirements.
- evidence mapping contracts.
- readiness report templates.
- safety policy contracts.
- dependency staging.
- read-only `/regime-features` API metadata endpoints.

## Explicit Non-Scope

Prompt 34 implements no feature computation, no feature registry writes, no
classifier inputs, no classification, no regime detection, no market state
decisions, no signals, no recommendations, no DecisionObject generation, and
no execution APIs.

Future feature computation and future regime validation require separate
prompts, source references, validation reports, quality checks, docs, tests, and
audit coverage.

Development verification runs on Mac mini M2 / macOS / Apple Silicon. The
target desktop product remains Windows-native Stark Terminal.
