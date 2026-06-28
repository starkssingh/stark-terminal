from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
]
ROUTE_FILES = [
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_api.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py",
]


def test_phase_has_no_recommendation_decision_or_execution_functions() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in SOURCE_ROOTS
        for path in root.glob("*.py")
    )
    for phrase in [
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_to_trade",
        "def create_order_button",
        "def execute_trade",
        "def grant_approval",
        "def grant_override",
    ]:
        assert phrase not in source

    route_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in ROUTE_FILES)
    for forbidden in ["/execute", "/broker", "/order", "/approval", "/override", "@router.post"]:
        assert forbidden not in route_text


def test_phase_no_recommendation_execution_doc_states_boundary() -> None:
    text = (
        ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md"
    ).read_text(encoding="utf-8").lower()
    for phrase in [
        "no recommendations",
        "no buy/sell/hold/watch/avoid outputs",
        "no action generation",
        "no confidence scoring",
        "no active decisionobjects",
        "no readiness-to-trade",
        "no broker controls",
        "no approvals/overrides",
        "no execution apis",
        "no hidden trade interpretation",
    ]:
        assert phrase in text
