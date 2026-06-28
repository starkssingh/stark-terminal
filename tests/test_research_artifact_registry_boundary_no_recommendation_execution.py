from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary"
ROUTE_PATH = ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_boundary.py"


def test_boundary_has_no_recommendation_decision_or_execution_functions() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in PACKAGE_ROOT.glob("*.py"))
    for phrase in [
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def create_order_button",
        "def execute_trade",
        "def grant_approval",
        "def grant_override",
    ]:
        assert phrase not in text


def test_boundary_has_no_execution_broker_order_or_approval_routes() -> None:
    route_text = ROUTE_PATH.read_text(encoding="utf-8").lower()
    for phrase in [
        "/execute",
        "/broker",
        "/order",
        "/approval",
        "/override",
        "/recommendation",
        "@router.post",
    ]:
        assert phrase not in route_text
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/research-artifact-registry-boundary"):
            assert "POST" not in methods


def test_boundary_execution_policy_doc_states_all_trading_controls_forbidden() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_EXECUTION_POLICY.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no execution apis",
        "no broker controls",
        "no approvals/overrides",
        "no readiness-to-trade",
        "no decisionobject generation",
        "no recommendation generation",
        "no action generation",
        "no confidence scoring",
        "future prompt and audit required",
    ]:
        assert phrase in text

