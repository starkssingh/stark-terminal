from __future__ import annotations

import re
from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api"


def _python_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.glob("*.py"))


def test_retail_trader_experience_api_modules_do_not_define_forbidden_generators() -> None:
    text = _python_text()
    forbidden_function_names = [
        "generate_trader_recommendation",
        "build_active_experience",
        "create_order_button",
        "generate_decision_object",
        "generate_recommendation",
        "score_confidence",
        "generate_readiness_status",
        "build_suitability_profile",
    ]
    for name in forbidden_function_names:
        assert not re.search(rf"def\s+{name}\s*\(", text)


def test_retail_trader_experience_api_modules_do_not_generate_decisions_or_execution() -> None:
    text = _python_text().lower()
    forbidden_snippets = [
        "execution_ready: bool = true",
        "recommendation_generated: bool = true",
        "action_generated: bool = true",
        "confidence_generated: bool = true",
        "decision_object_generated: bool = true",
        "suitability_profile_generated: bool = true",
        "requests.post",
        "httpx.",
        "broker_sdk",
        "order_button",
    ]
    for snippet in forbidden_snippets:
        assert snippet not in text


def test_retail_trader_experience_api_routes_are_read_only_and_not_active_paths() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if not path.startswith("/retail-trader-experience-api"):
            continue
        assert methods <= {"GET", "HEAD"}
        lowered = path.lower()
        for forbidden in [
            "recommendation",
            "execution",
            "broker",
            "order",
            "approval",
            "override",
            "suitability-profile",
            "market-data",
        ]:
            assert forbidden not in lowered


def test_retail_trader_experience_api_docs_explicitly_forbid_active_ui_suitability_and_execution() -> None:
    docs = [
        "docs/RETAIL_TRADER_EXPERIENCE_API_CONTRACT_SKELETON.md",
        "docs/RETAIL_TRADER_EXPERIENCE_API_SAFETY_BOUNDARY.md",
        "docs/RETAIL_TRADER_EXPERIENCE_API_NO_RECOMMENDATION_POLICY.md",
        "docs/RETAIL_TRADER_EXPERIENCE_API_NO_EXECUTION_POLICY.md",
        "docs/RETAIL_TRADER_EXPERIENCE_API_NO_SUITABILITY_PROFILING_POLICY.md",
    ]
    combined = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in docs)

    for phrase in [
        "no active UI",
        "no frontend",
        "no desktop",
        "no recommendation",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject",
        "no readiness-to-trade",
        "no suitability profiling",
        "no broker controls",
        "no execution",
    ]:
        assert phrase in combined
