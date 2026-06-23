from pydantic import ValidationError
import pytest

from stark_terminal_analytics.foundation.contracts import (
    AnalyticsInputContract,
    AnalyticsModulePlan,
    AnalyticsOutputContract,
    AnalyticsOutputKind,
    AnalyticsSafetyLevel,
    AnalyticsStage,
    create_default_analytics_input_contract,
    create_default_descriptive_output_contract,
    default_analytics_module_plans,
)


def test_valid_analytics_input_contract() -> None:
    contract = AnalyticsInputContract(
        contract_id="input_v1",
        name="Validated OHLCV input",
        accepted_data_kinds=["validated_ohlcv_bars"],
    )

    assert contract.requires_validated_input is True
    assert contract.requires_source_reference is True
    assert contract.synthetic_allowed is True
    assert contract.real_data_allowed is False
    assert contract.created_at.tzinfo is not None


def test_analytics_input_contract_rejects_unsafe_state() -> None:
    with pytest.raises(ValidationError):
        AnalyticsInputContract(
            contract_id="input_v1",
            name="Real data input",
            accepted_data_kinds=["ohlcv"],
            real_data_allowed=True,
        )
    with pytest.raises(ValidationError):
        AnalyticsInputContract(
            contract_id="input_v1",
            name="Unvalidated input",
            accepted_data_kinds=["ohlcv"],
            requires_validated_input=False,
        )


@pytest.mark.parametrize(
    "field",
    ["trade_signal", "recommendation", "execution_ready"],
)
def test_analytics_output_contract_rejects_trade_actionable_flags(field: str) -> None:
    kwargs = {
        "contract_id": "output_v1",
        "name": "Unsafe output",
        "output_kind": AnalyticsOutputKind.TIME_SERIES_METRIC,
        "safety_level": AnalyticsSafetyLevel.RESEARCH_ONLY,
        field: True,
    }

    with pytest.raises(ValidationError):
        AnalyticsOutputContract(**kwargs)


def test_analytics_module_plan_validates_planning_only_scope() -> None:
    plan = AnalyticsModulePlan(
        module_id="safe_plan",
        name="Safe Plan",
        stage=AnalyticsStage.CONTRACTS_ONLY,
        purpose="Plan descriptive analytics contracts only.",
        planned_inputs=[create_default_analytics_input_contract("safe_input", "Safe input")],
        planned_outputs=[create_default_descriptive_output_contract("safe_output", "Safe output")],
        blocked_capabilities=[
            "trade_signals",
            "recommendations",
            "execution",
            "decision_generation",
        ],
    )

    assert plan.module_id == "safe_plan"
    assert plan.dependencies_required == []


def test_default_analytics_module_plans_are_planning_only() -> None:
    plans = default_analytics_module_plans()
    module_ids = {plan.module_id for plan in plans}

    assert {
        "numerical_core",
        "returns_analytics",
        "rolling_window_analytics",
        "volatility_analytics",
        "drawdown_analytics",
        "correlation_beta_analytics",
        "time_series_diagnostics",
        "regime_analytics_planned",
        "backtesting_planned",
    }.issubset(module_ids)
    for plan in plans:
        assert plan.dependencies_required == []
        assert "trade_signals" in plan.blocked_capabilities
        assert "recommendations" in plan.blocked_capabilities
        assert "execution" in plan.blocked_capabilities
        assert "decision_generation" in plan.blocked_capabilities
        assert all(output.trade_signal is False for output in plan.planned_outputs)
        assert all(output.recommendation is False for output in plan.planned_outputs)
        assert all(output.execution_ready is False for output in plan.planned_outputs)

