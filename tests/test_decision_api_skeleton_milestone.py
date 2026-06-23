from __future__ import annotations

from pathlib import Path

from stark_terminal_core.decision_api.contracts import default_decision_desk_api_contract_metadata
from stark_terminal_core.decision_api.requests import default_decision_desk_request_placeholder
from stark_terminal_core.decision_api.responses import default_decision_desk_response_placeholder
from stark_terminal_core.decision_api.unavailable import default_decision_desk_unavailable_response


ROOT = Path(__file__).resolve().parents[1]


def test_decision_api_package_remains_contract_skeleton_only() -> None:
    metadata = default_decision_desk_api_contract_metadata()
    request = default_decision_desk_request_placeholder()
    response = default_decision_desk_response_placeholder()
    unavailable = default_decision_desk_unavailable_response()

    assert metadata.returns_unavailable_by_default is True
    assert metadata.recommendations_allowed is False
    assert metadata.confidence_scoring_allowed is False
    assert metadata.decision_object_generation_allowed is False
    assert metadata.approval_allowed is False
    assert metadata.override_allowed is False
    assert metadata.execution_allowed is False
    assert request.evidence_bundle_reference_required is True
    assert request.safety_reference_required is True
    assert response.planning_only is True
    assert response.recommendation_generated is False
    assert response.decision_object_generated is False
    assert response.execution_ready is False
    assert unavailable.unavailable is True
    assert unavailable.planning_only is True


def test_decision_api_has_no_decision_post_or_generation_endpoint() -> None:
    route_text = (ROOT / "apps/api/stark_terminal_api/routes/decision_desk_api.py").read_text(encoding="utf-8")
    package_root = ROOT / "packages/core/stark_terminal_core/decision_api"
    package_text = "\n".join(path.read_text(encoding="utf-8") for path in package_root.glob("*.py"))

    for forbidden_path in [
        "/recommendation",
        "/confidence",
        "/decision-object",
        "/approval",
        "/override",
        "/execution",
    ]:
        assert forbidden_path not in route_text
    for phrase in [
        "@router.post",
        "def generate_decision_object",
        "def generate_recommendation",
        "def approve_decision",
        "def override_decision",
        "def score_confidence",
        "DecisionObject(",
    ]:
        assert phrase not in package_text + route_text

