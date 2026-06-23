import pytest
from pydantic import ValidationError

from stark_terminal_analytics.regime.contracts import RegimeEvidenceKind
from stark_terminal_analytics.regime_features.contracts import (
    RegimeFeatureGroup,
    default_regime_feature_candidates,
)
from stark_terminal_analytics.regime_features.evidence_mapping import (
    RegimeFeatureEvidenceMap,
    RegimeFeatureEvidenceMapping,
    build_regime_feature_evidence_map,
    default_regime_feature_evidence_mappings,
    evaluate_regime_feature_evidence_map,
)


def _mapping() -> RegimeFeatureEvidenceMapping:
    return RegimeFeatureEvidenceMapping(
        mapping_id="mapping-test",
        feature_id="feature-test",
        feature_group=RegimeFeatureGroup.RETURNS,
        evidence_kinds=[RegimeEvidenceKind.RETURNS],
        evidence_description="Contracts-only mapping.",
    )


def test_valid_evidence_mapping() -> None:
    mapping = _mapping()

    assert mapping.required is True
    assert mapping.computation_allowed is False
    assert mapping.classification_allowed is False


@pytest.mark.parametrize(
    "override",
    [
        {"mapping_id": " "},
        {"feature_id": " "},
        {"feature_group": RegimeFeatureGroup.UNKNOWN},
        {"evidence_kinds": []},
        {"evidence_kinds": [RegimeEvidenceKind.UNKNOWN]},
        {"evidence_description": " "},
        {"computation_allowed": True},
        {"classification_allowed": True},
        {"schema_version": " "},
    ],
)
def test_evidence_mapping_rejects_invalid_or_unsafe_fields(override: dict[str, object]) -> None:
    data = _mapping().model_dump()
    data.update(override)
    with pytest.raises(ValidationError):
        RegimeFeatureEvidenceMapping(**data)


def test_default_evidence_mappings_cover_candidates() -> None:
    candidates = default_regime_feature_candidates()
    mappings = default_regime_feature_evidence_mappings(candidates)

    assert {mapping.feature_id for mapping in mappings} == {candidate.feature_id for candidate in candidates}
    assert all(mapping.evidence_kinds for mapping in mappings)
    assert all(mapping.computation_allowed is False for mapping in mappings)
    assert all(mapping.classification_allowed is False for mapping in mappings)


def test_evidence_map_with_blockers_not_complete() -> None:
    evidence_map = build_regime_feature_evidence_map(mappings=[_mapping()])

    assert evidence_map.complete is False
    assert evidence_map.blockers == ["missing evidence mapping for feature: feature-test"]


def test_complete_evidence_map_cannot_have_blockers() -> None:
    with pytest.raises(ValidationError):
        RegimeFeatureEvidenceMap(
            map_id="bad",
            mappings=[_mapping()],
            complete=True,
            blockers=["still missing"],
        )


def test_evidence_map_evaluation_is_deterministic() -> None:
    evidence_map = build_regime_feature_evidence_map(
        mappings=[_mapping()],
        completed_feature_ids={"feature-test"},
    )

    evaluated = evaluate_regime_feature_evidence_map(evidence_map)

    assert evaluated.complete is True
    assert evaluated.blockers == []

