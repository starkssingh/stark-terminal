from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
]
client = TestClient(app)


def test_retail_trader_experience_modules_do_not_generate_recommendations_or_decisions() -> None:
    forbidden_function_names = [
        "generate_trader_recommendation",
        "generate_recommendation",
        "score_confidence",
        "generate_decision_object",
    ]
    for root in PACKAGE_ROOTS:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8").lower()
            for name in forbidden_function_names:
                assert f"def {name}" not in text
            assert "DecisionObject(" not in path.read_text(encoding="utf-8")


def test_no_execution_broker_order_or_market_data_recommendation_routes() -> None:
    route_paths = [
        getattr(route, "path", "")
        for route in app.routes
        if getattr(route, "path", "").startswith("/retail-trader-experience")
    ]
    serialized = " ".join(route_paths).lower()
    for forbidden in [
        "execution",
        "broker",
        "order",
        "market-data-to-recommendation",
        "recommendation",
        "readiness-to-trade",
    ]:
        assert forbidden not in serialized

    for path in [
        "/retail-trader-experience/health",
        "/retail-trader-experience-api/health",
        "/retail-trader-experience-display/health",
    ]:
        assert client.post(path).status_code in {404, 405}


def test_recommendation_execution_docs_remain_explicit() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8").lower()
        for path in [
            "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
            "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_AUDIT.md",
            "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_AUDIT.md",
            "docs/API_SURFACE_INVENTORY.md",
        ]
    )
    for phrase in [
        "no recommendation cards",
        "no buy/sell/hold/watch/avoid active outputs",
        "no action generation",
        "no confidence scoring",
        "active decisionobject display",
        "no readiness-to-trade",
        "no broker controls",
        "no execution apis",
    ]:
        assert phrase in text
