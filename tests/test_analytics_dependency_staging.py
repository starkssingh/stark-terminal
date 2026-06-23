import pytest
from pydantic import ValidationError

from stark_terminal_analytics.foundation.dependencies import (
    AnalyticsDependency,
    AnalyticsDependencyPlan,
    AnalyticsDependencyStage,
    default_analytics_dependency_plan,
    dependency_is_allowed_now,
    list_blocked_heavy_dependencies_for_prompt_26,
)


def test_default_dependency_plan_is_contracts_only() -> None:
    plan = default_analytics_dependency_plan()

    assert plan.current_stage == AnalyticsDependencyStage.CONTRACTS_ONLY
    assert plan.dependencies
    assert all(dependency.required_now is False for dependency in plan.dependencies)


def test_heavy_dependencies_are_not_required_now() -> None:
    blocked = list_blocked_heavy_dependencies_for_prompt_26()

    for name in ["NumPy", "SciPy", "Numba", "JAX", "PyTorch", "TensorFlow", "QuantLib", "backtrader"]:
        assert name in blocked
        assert dependency_is_allowed_now(name) is False
    assert dependency_is_allowed_now("Polars") is True


def test_heavy_required_now_dependency_rejected() -> None:
    with pytest.raises(ValidationError):
        AnalyticsDependency(
            name="NumPy",
            category="numerical",
            stage=AnalyticsDependencyStage.NUMERICAL_CORE,
            required_now=True,
            reason="Should not be required in Prompt 26.",
            heavy=True,
        )


def test_dependency_plan_rejects_non_contracts_only_stage() -> None:
    dependency = AnalyticsDependency(
        name="Polars",
        category="tabular",
        stage=AnalyticsDependencyStage.NUMERICAL_CORE,
        reason="Existing project dependency.",
    )

    with pytest.raises(ValidationError):
        AnalyticsDependencyPlan(
            plan_id="plan",
            dependencies=[dependency],
            current_stage=AnalyticsDependencyStage.NUMERICAL_CORE,
        )

