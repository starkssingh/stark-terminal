from __future__ import annotations

from pathlib import Path

from stark_terminal_core.decision_evidence.bundle import default_decision_object_evidence_bundle_contract
from stark_terminal_core.decision_evidence.human_review import build_decision_evidence_human_review_attachment_set
from stark_terminal_core.decision_evidence.items import default_decision_evidence_item_contracts
from stark_terminal_core.decision_evidence.provenance import build_decision_evidence_provenance_map
from stark_terminal_core.decision_evidence.readiness import decision_evidence_ready_for_decision_object_generation
from stark_terminal_core.decision_evidence.validation import build_decision_evidence_validation_checklist


ROOT = Path(__file__).resolve().parents[1]


def test_decision_evidence_package_remains_contracts_only() -> None:
    items = default_decision_evidence_item_contracts()
    bundle = default_decision_object_evidence_bundle_contract()
    provenance = build_decision_evidence_provenance_map()
    checklist = build_decision_evidence_validation_checklist()
    attachments = build_decision_evidence_human_review_attachment_set()

    assert all(item.value_payload_allowed is False for item in items)
    assert all(item.recommendation is False for item in items)
    assert all(item.action_generated is False for item in items)
    assert all(item.confidence_generated is False for item in items)
    assert all(item.decision_object_generated is False for item in items)
    assert bundle.contracts_only is True
    assert bundle.decision_object_generation_allowed is False
    assert provenance.complete is False
    assert checklist.decision_object_generation_allowed is False
    assert attachments.approval_granted is False
    assert attachments.decision_object_generation_allowed is False


def test_decision_evidence_readiness_is_not_decisionobject_readiness() -> None:
    from stark_terminal_core.decision_evidence.readiness import DecisionEvidenceBundleReadinessReport
    from stark_terminal_core.decision_evidence.items import DecisionEvidenceStage

    report = DecisionEvidenceBundleReadinessReport(
        report_id="decision-evidence-boundary-test",
        bundle_id="bundle-test",
        planning_stage=DecisionEvidenceStage.CONTRACTS_ONLY,
        evidence_item_count=1,
        provenance_complete=False,
        validation_checklist_complete=False,
        human_review_attachments_complete=False,
        safety_decision="blocked",
    )

    assert decision_evidence_ready_for_decision_object_generation(report) is False
    assert report.ready_for_recommendations is False
    assert report.ready_for_action_generation is False
    assert report.ready_for_confidence_scoring is False
    assert report.ready_for_execution is False


def test_decision_evidence_code_has_no_active_generation_functions() -> None:
    package_root = ROOT / "packages/core/stark_terminal_core/decision_evidence"
    route = ROOT / "apps/api/stark_terminal_api/routes/decision_evidence.py"
    text = "\n".join(path.read_text(encoding="utf-8") for path in package_root.glob("*.py"))
    text += route.read_text(encoding="utf-8")

    for phrase in [
        "def generate_decision_object",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "DecisionObject(",
        "@router.post",
    ]:
        assert phrase not in text

