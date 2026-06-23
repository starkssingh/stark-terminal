from __future__ import annotations

from stark_terminal_analytics.regime_features.contracts import (
    default_regime_feature_candidates,
    default_regime_feature_group_plans,
)
from stark_terminal_analytics.regime_features.evidence_mapping import (
    build_regime_feature_evidence_map,
    default_regime_feature_evidence_mappings,
    evaluate_regime_feature_evidence_map,
)
from stark_terminal_analytics.regime_features.provenance import (
    build_regime_feature_provenance_map,
    default_regime_feature_provenance_requirements,
    evaluate_regime_feature_provenance_map,
)
from stark_terminal_analytics.regime_features.readiness import (
    build_regime_feature_readiness_report,
    regime_features_ready_for_classification,
    regime_features_ready_for_computation,
    regime_features_ready_for_registry_write,
)


def test_regime_feature_candidates_and_groups_are_metadata_only() -> None:
    candidates = default_regime_feature_candidates()
    groups = default_regime_feature_group_plans()

    assert candidates
    assert groups
    for candidate in candidates:
        assert candidate.computation_allowed is False
        assert candidate.registry_write_allowed is False
        assert candidate.classification_allowed is False
        assert candidate.trade_signal is False
        assert candidate.recommendation is False
        assert candidate.decision_object_generated is False
        assert candidate.planned_output_kind == "metadata-contract"

    for group in groups:
        assert group.computation_allowed is False
        assert group.classification_allowed is False


def test_provenance_and_evidence_mappings_cover_candidates() -> None:
    candidates = default_regime_feature_candidates()
    candidate_ids = {candidate.feature_id for candidate in candidates}

    provenance_requirements = default_regime_feature_provenance_requirements(candidates)
    evidence_mappings = default_regime_feature_evidence_mappings(candidates)

    assert {requirement.feature_id for requirement in provenance_requirements} == candidate_ids
    assert {mapping.feature_id for mapping in evidence_mappings} == candidate_ids
    assert all(requirement.synthetic_or_local_only_until_approved for requirement in provenance_requirements)
    assert all(not mapping.computation_allowed for mapping in evidence_mappings)
    assert all(not mapping.classification_allowed for mapping in evidence_mappings)


def test_readiness_remains_not_ready_for_computation_classification_or_production() -> None:
    candidates = default_regime_feature_candidates()
    groups = default_regime_feature_group_plans()
    provenance_map = evaluate_regime_feature_provenance_map(build_regime_feature_provenance_map())
    evidence_map = evaluate_regime_feature_evidence_map(build_regime_feature_evidence_map())

    report = build_regime_feature_readiness_report(candidates, groups, provenance_map, evidence_map)

    assert report.candidate_count == len(candidates)
    assert report.group_count == len(groups)
    assert report.ready_for_feature_computation is False
    assert report.ready_for_registry_write is False
    assert report.ready_for_classification is False
    assert report.ready_for_production is False
    assert regime_features_ready_for_computation(report) is False
    assert regime_features_ready_for_registry_write(report) is False
    assert regime_features_ready_for_classification(report) is False
