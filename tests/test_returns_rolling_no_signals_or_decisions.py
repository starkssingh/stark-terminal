from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_returns_rolling_modules_do_not_expose_action_state_language() -> None:
    text = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for directory in [
            ROOT / "packages/analytics/stark_terminal_analytics/returns",
            ROOT / "packages/analytics/stark_terminal_analytics/rolling",
        ]
        for path in directory.glob("*.py")
    )

    for forbidden in ["buy", "sell", "hold", "watch", "avoid", "order placement", "broker execution"]:
        assert forbidden not in text
    assert "decisionobject(" not in text
    assert "generate_signal" not in text
    assert "recommend_trade" not in text


def test_returns_analytics_route_paths_do_not_imply_recommendations_or_signals() -> None:
    route = (ROOT / "apps/api/stark_terminal_api/routes/returns_analytics.py").read_text(encoding="utf-8")

    assert '@router.get("/returns-analytics/health")' in route
    assert '@router.get("/returns-analytics/contracts")' in route
    assert "/signal" not in route
    assert "/recommendation" not in route
    assert "@router.post" not in route


def test_returns_rolling_docs_explicitly_forbid_signals_recommendations_and_execution() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/RETURNS_ANALYTICS_V0.md",
            "docs/ROLLING_WINDOW_ANALYTICS_V0.md",
            "docs/RETURNS_ROLLING_VALIDATION_POLICY.md",
            "docs/RETURNS_ROLLING_SAFETY_BOUNDARY.md",
        ]
    )

    assert "no signals" in text.lower()
    assert "no recommendations" in text.lower()
    assert "no DecisionObject generation" in text
    assert "no execution apis" in text.lower()
