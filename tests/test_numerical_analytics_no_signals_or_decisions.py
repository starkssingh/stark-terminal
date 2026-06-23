from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_numerical_modules_do_not_expose_action_state_language() -> None:
    text = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in (ROOT / "packages/analytics/stark_terminal_analytics/numerical").glob("*.py")
    )

    for forbidden in ["buy", "sell", "hold", "watch", "avoid", "order placement", "broker execution"]:
        assert forbidden not in text
    assert "decisionobject(" not in text
    assert "generate_signal" not in text
    assert "recommend_trade" not in text


def test_numerical_route_paths_do_not_imply_recommendations_or_signals() -> None:
    route = _read_route()

    assert '@router.get("/numerical-analytics/health")' in route
    assert '@router.get("/numerical-analytics/contracts")' in route
    assert '@router.get("/numerical-analytics/dependency-gate")' in route
    assert "/signal" not in route
    assert "/recommendation" not in route
    assert "@router.post" not in route


def test_numerical_docs_explicitly_forbid_signals_recommendations_and_execution() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/NUMERICAL_ANALYTICS_CORE_CONTRACTS.md",
            "docs/NUMERICAL_ANALYTICS_VALIDATION_POLICY.md",
            "docs/NUMERICAL_ANALYTICS_DEPENDENCY_GATE.md",
            "docs/NUMERICAL_ANALYTICS_SAFETY_BOUNDARY.md",
        ]
    )

    assert "no signals" in text.lower()
    assert "no recommendations" in text.lower()
    assert "no DecisionObject generation" in text
    assert "no execution apis" in text.lower()


def _read_route() -> str:
    return (ROOT / "apps/api/stark_terminal_api/routes/numerical_analytics.py").read_text(encoding="utf-8")
