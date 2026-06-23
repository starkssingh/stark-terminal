from pathlib import Path

from stark_terminal_analytics.regime_features.dependencies import (
    assert_no_blocked_regime_feature_dependencies_added,
    default_regime_feature_dependency_plan,
    regime_feature_dependency_allowed_now,
)


ROOT = Path(__file__).resolve().parents[1]


def test_default_dependency_plan_contracts_only() -> None:
    plan = default_regime_feature_dependency_plan()

    assert plan.current_stage == "contracts_only"
    assert plan.feature_computation_allowed is False
    assert plan.heavy_dependencies_blocked is True
    assert {"scipy", "sklearn", "hmmlearn", "ruptures"}.issubset(set(plan.blocked_now))


def test_blocked_dependencies_not_allowed_now() -> None:
    for dependency in ["numpy", "scipy", "sklearn", "hmmlearn", "ruptures", "torch"]:
        assert regime_feature_dependency_allowed_now(dependency) is False


def test_pyproject_has_no_blocked_regime_feature_dependencies() -> None:
    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert assert_no_blocked_regime_feature_dependencies_added(pyproject_text) == []


def test_pyproject_check_detects_blocked_dependency_text() -> None:
    pyproject_text = '[project]\ndependencies = ["pydantic", "sklearn>=1.0", "hmmlearn"]\n'

    assert assert_no_blocked_regime_feature_dependencies_added(pyproject_text) == [
        "hmmlearn",
        "sklearn",
    ]

