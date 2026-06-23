from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ANALYTICS_ROOT = ROOT / "packages/analytics/stark_terminal_analytics"
ANALYTICS_ROUTE_FILES = [
    ROOT / "apps/api/stark_terminal_api/routes/analytics_foundation.py",
    ROOT / "apps/api/stark_terminal_api/routes/numerical_analytics.py",
    ROOT / "apps/api/stark_terminal_api/routes/returns_analytics.py",
    ROOT / "apps/api/stark_terminal_api/routes/risk_analytics.py",
    ROOT / "apps/api/stark_terminal_api/routes/relationship_analytics.py",
    ROOT / "apps/api/stark_terminal_api/routes/time_series_diagnostics.py",
    ROOT / "apps/api/stark_terminal_api/routes/regime_analytics.py",
]


def test_analytics_modules_do_not_expose_trade_action_terms() -> None:
    forbidden_terms = ["buy", "sell", "hold", "watch", "avoid"]

    for path in ANALYTICS_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for term in forbidden_terms:
            assert not re.search(rf"\b{re.escape(term)}\b", text), f"{path} exposes action term {term}"


def test_analytics_modules_do_not_generate_decision_objects() -> None:
    for path in ANALYTICS_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "DecisionObject(" not in text
        assert "DecisionObjectRecord" not in text


def test_analytics_routes_do_not_expose_signal_or_recommendation_paths() -> None:
    for path in ANALYTICS_ROUTE_FILES:
        text = path.read_text(encoding="utf-8").lower()
        assert "/signals" not in text
        assert "/signal" not in text
        assert "/recommendations" not in text
        assert "/recommendation" not in text
        assert "@router.post" not in text


def test_analytics_modules_do_not_use_action_state_or_confidence_trading_logic() -> None:
    forbidden_phrases = [
        "action_state",
        "action state",
        "confidence_score",
        "confidence for action",
        "trade_call",
    ]

    for path in ANALYTICS_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for phrase in forbidden_phrases:
            assert phrase not in text, f"{path} contains {phrase}"


def test_prompt_30_docs_explicitly_forbid_signals_and_decisions() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/ANALYTICS_NO_SIGNAL_AUDIT.md",
            "docs/ANALYTICS_MILESTONE_AUDIT.md",
            "docs/API_SURFACE_INVENTORY.md",
        ]
    ).lower()

    assert "no signals" in text
    assert "no recommendations" in text
    assert "no decisionobject generation" in text
    assert "no execution apis" in text
