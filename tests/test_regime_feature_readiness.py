import pytest
from pydantic import ValidationError

from stark_terminal_analytics.regime_features.contracts import (
    default_regime_feature_candidates,
    default_regime_feature_group_plans,
)
from stark_terminal_analytics.regime_features.evidence_mapping import build_regime_feature_evidence_map
from stark_terminal_analytics.regime_features.provenance import build_regime_feature_provenance_map
from stark_terminal_analytics.regime_features.readiness import (
    RegimeFeatureReadinessReport,
    build_regime_feature_readiness_report,
    regime_features_ready_for_classification,
    regime_features_ready_for_computation,
    regime_features_ready_for_registry_write,
)


def test_regime_feature_readiness_report_validates() -> None:
    report = RegimeFeatureReadinessReport(
        report_id="report-test",
        candidate_count=1,
        group_count=1,
        provenance_complete=False,
        evidence_mapping_complete=False,
        blockers=["missing provenance"],
    )

    assert report.ready_for_feature_computation is False
    assert report.ready_for_registry_write is False
    assert report.ready_for_classification is False
    assert report.ready_for_production is False


@pytest.mark.parametrize(
    "override",
    [
        {"report_id": " "},
        {"candidate_count": -1},
        {"group_count": -1},
        {"ready_for_feature_computation": True},
        {"ready_for_registry_write": True},
        {"ready_for_classification": True},
        {"ready_for_production": True},
        {"schema_version": " "},
    ],
)
def test_readiness_report_rejects_invalid_or_unsafe_fields(override: dict[str, object]) -> None:
    data = RegimeFeatureReadinessReport(
        report_id="report-test",
        candidate_count=1,
        group_count=1,
        provenance_complete=False,
        evidence_mapping_complete=False,
    ).model_dump()
    data.update(override)
    with pytest.raises(ValidationError):
        RegimeFeatureReadinessReport(**data)


def test_readiness_helpers_always_block_prompt_34_progression() -> None:
    report = RegimeFeatureReadinessReport(
        report_id="report-test",
        candidate_count=1,
        group_count=1,
        provenance_complete=True,
        evidence_mapping_complete=True,
    )

    assert regime_features_ready_for_computation(report) is False
    assert regime_features_ready_for_registry_write(report) is False
    assert regime_features_ready_for_classification(report) is False


def test_build_readiness_report_counts_and_blockers() -> None:
    candidates = default_regime_feature_candidates()
    groups = default_regime_feature_group_plans()
    report = build_regime_feature_readiness_report(
        candidates,
        groups,
        build_regime_feature_provenance_map(),
        build_regime_feature_evidence_map(),
    )

    assert report.candidate_count == len(candidates)
    assert report.group_count == len(groups)
    assert report.blockers
    assert report.ready_for_feature_computation is False
    assert report.ready_for_registry_write is False
    assert report.ready_for_classification is False
    assert report.ready_for_production is False

