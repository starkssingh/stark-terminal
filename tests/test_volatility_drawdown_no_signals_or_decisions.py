from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RISK_MODULES = [
    ROOT / "packages/analytics/stark_terminal_analytics/volatility/contracts.py",
    ROOT / "packages/analytics/stark_terminal_analytics/volatility/validation.py",
    ROOT / "packages/analytics/stark_terminal_analytics/volatility/calculations.py",
    ROOT / "packages/analytics/stark_terminal_analytics/drawdown/contracts.py",
    ROOT / "packages/analytics/stark_terminal_analytics/drawdown/validation.py",
    ROOT / "packages/analytics/stark_terminal_analytics/drawdown/calculations.py",
    ROOT / "apps/api/stark_terminal_api/routes/risk_analytics.py",
]


def test_risk_analytics_modules_do_not_expose_trade_action_terms() -> None:
    forbidden_terms = ["buy", "sell", "hold", "watch", "avoid"]

    for path in RISK_MODULES:
        text = path.read_text(encoding="utf-8").lower()
        for term in forbidden_terms:
            assert term not in text


def test_risk_analytics_route_path_does_not_imply_signals_or_recommendations() -> None:
    route_text = (ROOT / "apps/api/stark_terminal_api/routes/risk_analytics.py").read_text(encoding="utf-8").lower()

    assert "/risk-analytics" in route_text
    assert "/signals" not in route_text
    assert "/recommendations" not in route_text


def test_prompt_29_docs_state_no_recommendations_or_execution() -> None:
    docs = "\n".join(
        [
            (ROOT / "docs/VOLATILITY_ANALYTICS_V0.md").read_text(encoding="utf-8"),
            (ROOT / "docs/DRAWDOWN_ANALYTICS_V0.md").read_text(encoding="utf-8"),
            (ROOT / "docs/VOLATILITY_DRAWDOWN_SAFETY_BOUNDARY.md").read_text(encoding="utf-8"),
        ]
    ).lower()

    assert "no signals" in docs
    assert "no recommendations" in docs
    assert "no decisionobject" in docs
    assert "no execution apis" in docs
