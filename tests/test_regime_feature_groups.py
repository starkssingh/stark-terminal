from stark_terminal_analytics.regime.contracts import RegimeEvidenceKind
from stark_terminal_analytics.regime_features.contracts import (
    RegimeFeatureGroup,
    default_regime_feature_candidates,
    default_regime_feature_group_plans,
)


def test_default_feature_groups_exist() -> None:
    groups = default_regime_feature_group_plans()

    assert {group.group for group in groups} == {
        RegimeFeatureGroup.RETURNS,
        RegimeFeatureGroup.VOLATILITY,
        RegimeFeatureGroup.DRAWDOWN,
        RegimeFeatureGroup.RELATIONSHIP,
        RegimeFeatureGroup.TIME_SERIES_DIAGNOSTICS,
        RegimeFeatureGroup.VOLUME_LIQUIDITY,
        RegimeFeatureGroup.OPTIONS_CONTEXT,
        RegimeFeatureGroup.MACRO_CONTEXT,
        RegimeFeatureGroup.MARKET_MICROSTRUCTURE,
    }


def test_each_group_has_candidates_and_evidence() -> None:
    for group in default_regime_feature_group_plans():
        assert group.candidates
        assert group.required_evidence_kinds
        assert RegimeEvidenceKind.UNKNOWN not in group.required_evidence_kinds
        assert group.computation_allowed is False
        assert group.classification_allowed is False


def test_candidates_do_not_contain_computed_values_or_signal_outputs() -> None:
    for candidate in default_regime_feature_candidates():
        assert "value" not in type(candidate).model_fields
        assert "computed_value" not in type(candidate).model_fields
        assert candidate.planned_output_kind == "metadata-contract"
        assert "signal" not in candidate.name
        assert "indicator" not in candidate.name
        assert candidate.trade_signal is False
        assert candidate.recommendation is False
