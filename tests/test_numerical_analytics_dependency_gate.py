from pathlib import Path

from stark_terminal_analytics.numerical.dependencies import (
    assert_no_blocked_numerical_dependencies_added,
    default_numerical_dependency_gate,
    numerical_dependency_allowed_now,
)


ROOT = Path(__file__).resolve().parents[1]


def test_default_numerical_dependency_gate_blocks_heavy_dependencies() -> None:
    gate = default_numerical_dependency_gate()

    assert gate.stage == "contracts_and_safe_stdlib"
    assert gate.heavy_dependencies_blocked is True
    for dependency in ["numpy", "scipy", "numba", "jax", "torch", "tensorflow", "quantlib", "backtrader"]:
        assert dependency in gate.blocked_now
        assert numerical_dependency_allowed_now(dependency) is False


def test_numerical_dependency_gate_allows_only_safe_current_dependencies() -> None:
    assert numerical_dependency_allowed_now("standard-library") is True
    assert numerical_dependency_allowed_now("math") is True
    assert numerical_dependency_allowed_now("statistics") is True
    assert numerical_dependency_allowed_now("pydantic") is True
    assert numerical_dependency_allowed_now("numpy") is False


def test_pyproject_has_no_blocked_numerical_dependencies_added() -> None:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert assert_no_blocked_numerical_dependencies_added(text) == []
    assert assert_no_blocked_numerical_dependencies_added('[project]\ndependencies=["numpy"]') == ["numpy"]


def test_no_provider_sdk_scraping_or_broker_dependencies_added() -> None:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()

    for dependency in [
        "kiteconnect",
        "upstox",
        "nsepython",
        "beautifulsoup",
        "selenium",
        "scrapy",
        "alpaca-trade-api",
        "ib_insync",
        "ccxt",
    ]:
        assert dependency not in text
