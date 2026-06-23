from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ANALYTICS_ROOT = ROOT / "packages/analytics/stark_terminal_analytics"
ROUTES_ROOT = ROOT / "apps/api/stark_terminal_api/routes"


def _analytics_python_texts() -> list[tuple[Path, str]]:
    return [(path, path.read_text(encoding="utf-8")) for path in ANALYTICS_ROOT.rglob("*.py")]


def test_analytics_regime_modules_do_not_expose_trading_action_terms() -> None:
    action_terms = ("buy", "sell", "hold", "watch", "avoid")

    for path, text in _analytics_python_texts():
        lowered = text.lower()
        for term in action_terms:
            assert re.search(rf"\b{term}\b", lowered) is None, f"{term} found in {path}"


def test_analytics_regime_modules_do_not_generate_decision_objects() -> None:
    for path, text in _analytics_python_texts():
        assert "DecisionObject(" not in text, f"DecisionObject generation found in {path}"


def test_analytics_regime_routes_have_no_recommendation_signal_or_post_endpoints() -> None:
    route_names = [
        "analytics_foundation.py",
        "numerical_analytics.py",
        "returns_analytics.py",
        "risk_analytics.py",
        "relationship_analytics.py",
        "time_series_diagnostics.py",
        "regime_analytics.py",
        "regime_features.py",
    ]

    for name in route_names:
        text = (ROUTES_ROOT / name).read_text(encoding="utf-8").lower()
        assert "@router.post" not in text
        assert "/recommend" not in text
        assert "/signal" not in text
        assert "DecisionObject(" not in text


def test_docs_api_explicitly_forbid_signals_and_recommendations() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/ANALYTICS_REGIME_NO_SIGNAL_AUDIT.md",
            "docs/SAFETY_AUDIT.md",
            "docs/API_SURFACE_INVENTORY.md",
        ]
    )

    for phrase in [
        "no buy/sell/hold/watch/avoid outputs",
        "no signal",
        "no recommendation",
        "no DecisionObject generation",
        "no execution APIs",
    ]:
        assert phrase in text
