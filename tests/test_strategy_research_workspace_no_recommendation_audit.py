from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_api",
    ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display",
]
ROUTES = list((ROOT / "apps/api/stark_terminal_api/routes").glob("strategy_research_workspace*.py"))


def _combined_code() -> str:
    return "\n".join(
        [path.read_text(encoding="utf-8") for package in PACKAGES for path in package.glob("*.py")]
        + [route.read_text(encoding="utf-8") for route in ROUTES]
    )


def test_strategy_research_workspace_has_no_recommendation_action_confidence_or_decision_functions() -> None:
    combined = _combined_code()

    for forbidden in [
        "def generate_recommendation",
        "def generate_action",
        "def generate_action_state",
        "def score_confidence",
        "def compute_confidence",
        "def generate_decision_object",
        "def display_decision_object",
        "def generate_readiness_status",
        "DecisionObject(",
    ]:
        assert forbidden not in combined


def test_strategy_research_workspace_has_no_recommendation_routes() -> None:
    combined = "\n".join(route.read_text(encoding="utf-8") for route in ROUTES)
    route_paths = "\n".join(re.findall(r'@router\.get\("([^"]+)"', combined))

    for forbidden_path in [
        "recommendation",
        "action-state",
        "confidence",
        "decisionobject",
        "readiness-to-trade",
        "buy",
        "sell",
        "hold",
        "watch",
        "avoid",
    ]:
        assert not re.search(rf"(^|[/_-]){re.escape(forbidden_path)}($|[/_-])", route_paths)


def test_strategy_research_workspace_no_recommendation_docs_forbid_trade_outputs() -> None:
    docs = [
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_NO_RECOMMENDATION_AUDIT.md",
        ROOT / "docs/STRATEGY_RESEARCH_NO_RECOMMENDATION_POLICY.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_RECOMMENDATION_POLICY.md",
        ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs).lower()

    for phrase in [
        "no research-as-recommendation",
        "no buy/sell/hold/watch/avoid active outputs",
        "no action generation",
        "no confidence scoring",
        "no active decisionobject generation/display",
        "no readiness-to-trade",
        "no hidden trade interpretation",
    ]:
        assert phrase in combined
