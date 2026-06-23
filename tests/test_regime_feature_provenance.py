import pytest
from pydantic import ValidationError

from stark_terminal_analytics.regime_features.contracts import default_regime_feature_candidates
from stark_terminal_analytics.regime_features.provenance import (
    RegimeFeatureProvenanceMap,
    RegimeFeatureProvenanceRequirement,
    build_regime_feature_provenance_map,
    default_regime_feature_provenance_requirements,
    evaluate_regime_feature_provenance_map,
)


def _requirement() -> RegimeFeatureProvenanceRequirement:
    return RegimeFeatureProvenanceRequirement(
        provenance_id="provenance-test",
        feature_id="feature-test",
        required_source_references=["source-ref"],
        required_analytics_families=["returns_analytics_v0"],
    )


def test_valid_provenance_requirement() -> None:
    requirement = _requirement()

    assert requirement.requires_validation_report is True
    assert requirement.synthetic_or_local_only_until_approved is True


@pytest.mark.parametrize(
    "override",
    [
        {"provenance_id": " "},
        {"feature_id": " "},
        {"required_source_references": []},
        {"required_analytics_families": []},
        {"schema_version": " "},
    ],
)
def test_provenance_requirement_rejects_missing_required_fields(override: dict[str, object]) -> None:
    data = _requirement().model_dump()
    data.update(override)
    with pytest.raises(ValidationError):
        RegimeFeatureProvenanceRequirement(**data)


def test_default_provenance_requirements_cover_candidates() -> None:
    candidates = default_regime_feature_candidates()
    requirements = default_regime_feature_provenance_requirements(candidates)

    assert {requirement.feature_id for requirement in requirements} == {
        candidate.feature_id for candidate in candidates
    }
    assert all(requirement.required_source_references for requirement in requirements)
    assert all(requirement.required_analytics_families for requirement in requirements)


def test_provenance_map_with_blockers_not_complete() -> None:
    provenance_map = build_regime_feature_provenance_map(requirements=[_requirement()])

    assert provenance_map.complete is False
    assert provenance_map.blockers == ["missing provenance for feature: feature-test"]


def test_complete_provenance_map_cannot_have_blockers() -> None:
    with pytest.raises(ValidationError):
        RegimeFeatureProvenanceMap(
            map_id="bad",
            requirements=[_requirement()],
            complete=True,
            blockers=["still missing"],
        )


def test_provenance_evaluation_is_deterministic() -> None:
    provenance_map = build_regime_feature_provenance_map(
        requirements=[_requirement()],
        completed_feature_ids={"feature-test"},
    )

    evaluated = evaluate_regime_feature_provenance_map(provenance_map)

    assert evaluated.complete is True
    assert evaluated.blockers == []

