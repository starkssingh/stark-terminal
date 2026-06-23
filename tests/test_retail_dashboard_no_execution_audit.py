from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]


def test_retail_dashboard_routes_do_not_include_execution_broker_or_order_paths() -> None:
    paths = app.openapi()["paths"]
    for path, operations in paths.items():
        if path.startswith(("/retail-dashboard", "/retail-dashboard-api", "/retail-dashboard-display")):
            lowered = path.lower()
            assert "execution" not in lowered
            assert "execute" not in lowered
            assert "broker" not in lowered
            assert "order" not in lowered
            assert "approval" not in lowered
            assert "override" not in lowered
            assert "market-data-to-recommendation" not in lowered
            assert "readiness-to-trade" not in lowered
            assert "post" not in operations


def test_retail_dashboard_code_has_no_execution_or_broker_implementations() -> None:
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for root in [
            ROOT / "packages/core/stark_terminal_core/retail_dashboard",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_api",
            ROOT / "packages/core/stark_terminal_core/retail_dashboard_display",
            ROOT / "apps/api/stark_terminal_api/routes",
        ]
        for path in root.glob("*.py")
        if root.name != "routes" or path.name.startswith("retail_dashboard")
    )
    for phrase in [
        "@router.post",
        "def execute",
        "def place_order",
        "def submit_order",
        "def create_order",
        "def connect_broker",
        "def approve",
        "def override",
        "broker_client",
        "api_key",
        "api_secret",
    ]:
        assert phrase not in text


def test_no_execution_audit_doc_states_forbidden_boundaries() -> None:
    text = (ROOT / "docs/RETAIL_DASHBOARD_NO_EXECUTION_AUDIT.md").read_text(encoding="utf-8")
    for phrase in [
        "no execution APIs",
        "no broker controls",
        "no order buttons",
        "no paper trading controls",
        "no live trading controls",
        "no real-money routing",
        "no dashboard-to-execution path",
        "Execution remains forbidden",
    ]:
        assert phrase in text
