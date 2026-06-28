from __future__ import annotations

import re
from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]


def test_no_recommendation_execution_docs_state_integration_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no recommendations",
        "no buy/sell/hold/watch/avoid",
        "no action generation",
        "no confidence scoring",
        "no decisionobject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no approvals/overrides",
        "no execution apis",
        "no hidden trade interpretation",
    ]:
        assert phrase in text


def test_no_recommendation_execution_routes_exist() -> None:
    forbidden_path_parts = [
        "recommendation",
        "execute",
        "execution",
        "broker",
        "order",
        "approval",
        "override",
        "readiness-to-trade",
    ]
    for route in app.routes:
        path = getattr(route, "path", "").lower()
        if path.startswith("/research-artifact-registry"):
            for part in forbidden_path_parts:
                assert part not in path, path
            assert "POST" not in getattr(route, "methods", set()), path


def test_no_recommendation_execution_functions_exist() -> None:
    forbidden_defs = [
        "generate_recommendation",
        "generate_action",
        "score_confidence",
        "generate_decision_object",
        "generate_readiness_status",
        "execute_trade",
        "place_order",
        "grant_approval",
        "grant_override",
    ]
    pattern = re.compile(r"^\s*def\s+(" + "|".join(forbidden_defs) + r")\s*\(", re.MULTILINE)
    for root in [
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary",
    ]:
        for path in root.rglob("*.py"):
            assert pattern.search(path.read_text(encoding="utf-8")) is None, str(path.relative_to(ROOT))

