from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)
PACKAGE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
    ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
]
ROUTE_FILES = [
    ROOT / "apps/api/stark_terminal_api/routes/retail_trader_experience.py",
    ROOT / "apps/api/stark_terminal_api/routes/retail_trader_experience_api.py",
    ROOT / "apps/api/stark_terminal_api/routes/retail_trader_experience_display.py",
]


def _code_text() -> str:
    package_text = "\n".join(
        path.read_text(encoding="utf-8")
        for root in PACKAGE_ROOTS
        for path in root.glob("*.py")
    )
    route_text = "\n".join(path.read_text(encoding="utf-8") for path in ROUTE_FILES)
    return f"{package_text}\n{route_text}".lower()


def test_no_execution_broker_order_or_approval_routes_are_introduced() -> None:
    forbidden_path_terms = [
        "execution",
        "execute",
        "broker",
        "order",
        "trade",
        "approval",
        "override",
        "market-data-to-recommendation",
        "readiness-to-trade",
    ]

    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/retail-trader-experience"):
            assert "POST" not in getattr(route, "methods", set())
            for term in forbidden_path_terms:
                assert term not in path


def test_no_execution_like_code_or_credentials_exist_in_retail_trader_experience_modules() -> None:
    text = _code_text()

    for forbidden in [
        "@router.post",
        "def execute_trade",
        "def place_order",
        "def submit_order",
        "def route_order",
        "broker_client",
        "def create_order_button",
        "order_button=true",
        "real_money",
        "api_key",
        "password",
        "secret",
        "credential",
    ]:
        assert forbidden not in text


def test_retail_trader_experience_responses_do_not_imply_execution_or_approval() -> None:
    for path in [
        "/retail-trader-experience/placeholder-experience",
        "/retail-trader-experience/readiness-template",
        "/retail-trader-experience-api/response-placeholder",
        "/retail-trader-experience-display/placeholder-experience",
    ]:
        payload = client.get(path).json()
        serialized = json.dumps(payload).lower()
        assert '"execution_ready": true' not in serialized
        assert '"execution_allowed": true' not in serialized
        assert '"broker_controls_allowed": true' not in serialized
        assert '"broker_control_generated": true' not in serialized
        assert '"approval_granted": true' not in serialized
        assert '"override_granted": true' not in serialized


def test_no_execution_audit_docs_and_policies_are_explicit() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8").lower()
        for path in [
            "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_AUDIT.md",
            "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_POLICY.md",
            "docs/RETAIL_TRADER_EXPERIENCE_API_NO_EXECUTION_POLICY.md",
            "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_EXECUTION_POLICY.md",
        ]
    )

    for phrase in [
        "no execution apis",
        "no broker controls",
        "no order buttons",
        "no paper/live trading controls",
        "no real-money routing",
        "no experience-to-execution path",
        "execution remains forbidden",
    ]:
        assert phrase in text
