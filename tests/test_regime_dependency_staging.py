from pathlib import Path

from stark_terminal_analytics.regime.dependencies import (
    assert_no_blocked_regime_dependencies_added,
    default_regime_dependency_plan,
    regime_dependency_allowed_now,
)


ROOT = Path(__file__).resolve().parents[1]


def test_default_regime_dependency_plan_blocks_heavy_dependencies() -> None:
    plan = default_regime_dependency_plan()

    assert plan.current_stage == "planning_only"
    assert plan.heavy_dependencies_blocked is True
    for dependency in ["statsmodels", "scipy", "sklearn", "hmmlearn", "ruptures", "torch"]:
        assert dependency in plan.blocked_now


def test_regime_dependency_allowed_now_false_for_blocked_libraries() -> None:
    for dependency in ["statsmodels", "scipy", "sklearn", "hmmlearn", "ruptures"]:
        assert regime_dependency_allowed_now(dependency) is False

    assert regime_dependency_allowed_now("standard-library") is True


def test_pyproject_has_no_blocked_regime_dependencies() -> None:
    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert assert_no_blocked_regime_dependencies_added(pyproject_text) == []


def test_pyproject_has_no_provider_scraping_or_broker_dependencies() -> None:
    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()

    forbidden = ["kiteconnect", "upstox", "nsepython", "nsepy", "yfinance", "selenium", "scrapy", "ccxt"]
    assert not any(dependency in pyproject_text for dependency in forbidden)
