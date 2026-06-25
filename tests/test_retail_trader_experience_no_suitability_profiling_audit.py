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


def _code_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for root in PACKAGE_ROOTS
        for path in root.glob("*.py")
    ).lower()


def test_no_suitability_or_trading_permission_generators_exist() -> None:
    text = _code_text()

    for forbidden in [
        "def build_suitability_profile",
        "def generate_suitability_profile",
        "def create_suitability_profile",
        "def generate_trading_permission_profile",
        "def create_trading_permission_profile",
        "def persona_to_suitability_profile",
        "def journey_to_trading_advice",
        "suitability_profile_generated=true",
        "suitability_profile=true",
        "trading_permission_profile=true",
    ]:
        assert forbidden not in text


def test_retail_trader_experience_responses_do_not_create_suitability_profiles() -> None:
    for path in [
        "/retail-trader-experience/placeholder-experience",
        "/retail-trader-experience-api/response-placeholder",
        "/retail-trader-experience-display/placeholder-experience",
    ]:
        payload = client.get(path).json()
        serialized = json.dumps(payload).lower()
        assert '"suitability_profile_generated": true' not in serialized
        assert '"suitability_profiling_allowed": true' not in serialized
        assert '"suitability_profile": true' not in serialized
        assert '"trading_permission_profile": true' not in serialized


def test_no_suitability_profiling_audit_docs_and_policies_are_explicit() -> None:
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8").lower()
        for path in [
            "docs/RETAIL_TRADER_EXPERIENCE_NO_SUITABILITY_PROFILING_AUDIT.md",
            "docs/RETAIL_TRADER_EXPERIENCE_API_NO_SUITABILITY_PROFILING_POLICY.md",
            "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_SUITABILITY_PROFILING_POLICY.md",
        ]
    )

    for phrase in [
        "no suitability profiling",
        "no trading permission profile",
        "no persona-as-suitability-profile behavior",
        "no journey-as-trading-advice behavior",
        "no suitability-based recommendation behavior",
        "no retail trader categorization for actions",
        "forbidden unless explicitly planned and audited",
    ]:
        assert phrase in text


def test_no_route_path_exposes_suitability_profile_surface() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/retail-trader-experience"):
            assert "suitability" not in path
            assert "profile" not in path
            assert "permission" not in path

