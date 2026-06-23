# Regime Feature Preparation

Prompt 34 adds Regime Feature Preparation Contracts for Stark Terminal.

This package is contracts/preparation only:

- no feature computation.
- no feature registry writes.
- no regime classification.
- no market state decisions.
- no signals or recommendations.
- no DecisionObject generation.
- no execution APIs.

The package defines metadata-only feature candidates, feature groups,
provenance requirements, evidence mappings, readiness reports, safety policy,
dependency staging, and health metadata. Provenance and evidence mapping are
required before any future feature computation can be designed.

Heavy feature/model libraries remain blocked until a future prompt explicitly
updates dependency staging, docs, tests, audit coverage, and safety policy.
