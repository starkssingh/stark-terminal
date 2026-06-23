from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELATIONSHIP_MODULES = [
    ROOT / "packages/analytics/stark_terminal_analytics/correlation/contracts.py",
    ROOT / "packages/analytics/stark_terminal_analytics/correlation/validation.py",
    ROOT / "packages/analytics/stark_terminal_analytics/correlation/calculations.py",
    ROOT / "packages/analytics/stark_terminal_analytics/beta/contracts.py",
    ROOT / "packages/analytics/stark_terminal_analytics/beta/validation.py",
    ROOT / "packages/analytics/stark_terminal_analytics/beta/calculations.py",
    ROOT / "apps/api/stark_terminal_api/routes/relationship_analytics.py",
]


def test_relationship_analytics_modules_do_not_expose_trade_action_terms() -> None:
    forbidden_terms = ["buy", "sell", "hold", "watch", "avoid"]

    for path in RELATIONSHIP_MODULES:
        text = path.read_text(encoding="utf-8").lower()
        for term in forbidden_terms:
            assert term not in text


def test_relationship_analytics_modules_do_not_generate_decision_objects() -> None:
    for path in RELATIONSHIP_MODULES:
        text = path.read_text(encoding="utf-8")
        assert "DecisionObject(" not in text
        assert "DecisionObjectRecord" not in text


def test_relationship_analytics_route_path_does_not_imply_signals_or_recommendations() -> None:
    route_text = (ROOT / "apps/api/stark_terminal_api/routes/relationship_analytics.py").read_text(
        encoding="utf-8"
    ).lower()

    assert "/relationship-analytics" in route_text
    assert "/signals" not in route_text
    assert "/recommendations" not in route_text
    assert "@router.post" not in route_text


def test_prompt_32_docs_state_no_recommendations_or_execution() -> None:
    docs = "\n".join(
        [
            (ROOT / "docs/CORRELATION_ANALYTICS_V0.md").read_text(encoding="utf-8"),
            (ROOT / "docs/BETA_ANALYTICS_V0.md").read_text(encoding="utf-8"),
            (ROOT / "docs/CORRELATION_BETA_SAFETY_BOUNDARY.md").read_text(encoding="utf-8"),
        ]
    ).lower()

    assert "no signals" in docs
    assert "no recommendations" in docs
    assert "no decisionobject" in docs
    assert "no execution apis" in docs

