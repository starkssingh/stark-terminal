from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]


def test_decision_integration_routes_do_not_include_execution_or_broker_paths() -> None:
    bad: list[str] = []
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if not path.startswith("/decision"):
            continue
        lowered = path.lower()
        if "POST" in methods:
            bad.append(f"{path}:POST")
        for forbidden in [
            "/execute",
            "/execution",
            "/broker",
            "/order",
            "/trade",
            "/recommendation",
            "/readiness-to-trade",
        ]:
            if forbidden in lowered:
                bad.append(f"{path}:{forbidden}")

    assert bad == []


def test_decision_integration_has_no_market_data_to_recommendation_routes() -> None:
    route_text = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in (ROOT / "apps/api/stark_terminal_api/routes").glob("decision*.py")
    )

    for snippet in [
        "@router.post",
        "market_data_to_recommendation",
        "market-data-to-recommendation",
        "readiness_to_trade_endpoint",
        "execute_trade",
        "place_order",
        "broker_client",
    ]:
        assert snippet not in route_text


def test_prompt_48_did_not_add_forbidden_dependencies() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    for dependency in [
        "alpaca",
        "ib_insync",
        "kiteconnect",
        "selenium",
        "playwright",
        "streamlit",
        "dash",
        "celery",
        "authlib",
        "python-jose",
    ]:
        assert dependency not in pyproject

