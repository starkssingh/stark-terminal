import pytest

from stark_terminal_analytics.regime.contracts import (
    RegimeAnalyticsPlan,
    RegimeEvidenceKind,
    RegimeLabelContract,
    RegimeLabelPlaceholder,
    RegimePlanningStage,
    default_regime_analytics_plan,
    default_regime_label_contracts,
)


def test_valid_regime_label_contract_is_planning_only() -> None:
    label = RegimeLabelContract(
        label_id="planned-range-bound",
        label=RegimeLabelPlaceholder.RANGE_BOUND,
        display_name="Range Bound",
        description="Planning label only.",
    )

    assert label.planning_only is True
    assert label.classification_allowed is False
    assert label.trade_signal is False
    assert label.recommendation is False
    assert label.decision_object_generated is False


@pytest.mark.parametrize(
    "override",
    [
        {"planning_only": False},
        {"classification_allowed": True},
        {"trade_signal": True},
        {"recommendation": True},
        {"decision_object_generated": True},
    ],
)
def test_regime_label_rejects_unsafe_flags(override: dict[str, object]) -> None:
    data = {
        "label_id": "planned-stress",
        "label": RegimeLabelPlaceholder.STRESS,
        "display_name": "Stress",
        "description": "Planning label only.",
    }
    data.update(override)

    with pytest.raises(ValueError):
        RegimeLabelContract(**data)


def test_default_labels_exist_and_are_placeholders_only() -> None:
    labels = default_regime_label_contracts()

    assert labels
    assert {label.label for label in labels} >= {
        RegimeLabelPlaceholder.TRENDING_UP,
        RegimeLabelPlaceholder.TRENDING_DOWN,
        RegimeLabelPlaceholder.RANGE_BOUND,
        RegimeLabelPlaceholder.UNCLASSIFIED,
    }
    assert all(label.planning_only for label in labels)
    assert all(not label.classification_allowed for label in labels)


def test_default_regime_plan_validates_required_evidence_and_forbidden_outputs() -> None:
    plan = default_regime_analytics_plan()

    assert plan.stage == RegimePlanningStage.PLANNING_ONLY
    assert plan.planned_labels
    assert RegimeEvidenceKind.RETURNS in plan.required_evidence_kinds
    assert RegimeEvidenceKind.TIME_SERIES_DIAGNOSTICS in plan.required_evidence_kinds
    assert "trading_signals" in plan.forbidden_outputs
    assert "recommendations" in plan.forbidden_outputs
    assert "DecisionObject_generation" in plan.forbidden_outputs
    assert "execution_apis" in plan.forbidden_outputs
    assert plan.classification_allowed is False
    assert plan.real_data_allowed is False
    assert plan.requires_human_review is True


@pytest.mark.parametrize(
    "override",
    [
        {"planned_labels": []},
        {"required_evidence_kinds": []},
        {"required_evidence_kinds": [RegimeEvidenceKind.UNKNOWN]},
        {"forbidden_outputs": ["execution_apis"]},
        {"classification_allowed": True},
        {"real_data_allowed": True},
        {"requires_human_review": False},
    ],
)
def test_regime_plan_rejects_unsafe_or_incomplete_contracts(override: dict[str, object]) -> None:
    plan = default_regime_analytics_plan()
    data = plan.model_dump()
    data.update(override)

    with pytest.raises(ValueError):
        RegimeAnalyticsPlan(**data)
