from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_evidence.bundle import default_decision_object_evidence_bundle_contract
from stark_terminal_core.decision_evidence.human_review import build_decision_evidence_human_review_attachment_set
from stark_terminal_core.decision_evidence.items import DecisionEvidenceStage
from stark_terminal_core.decision_evidence.provenance import build_decision_evidence_provenance_map
from stark_terminal_core.decision_evidence.readiness import (
    DecisionEvidenceBundleReadinessReport,
    build_decision_evidence_bundle_readiness_report,
    decision_evidence_ready_for_bundle_validation,
    decision_evidence_ready_for_decision_object_generation,
    decision_evidence_ready_for_execution,
    decision_evidence_ready_for_recommendations,
)
from stark_terminal_core.decision_evidence.safety import default_decision_evidence_safety_policy, evaluate_decision_evidence_bundle_safety
from stark_terminal_core.decision_evidence.validation import build_decision_evidence_validation_checklist


def test_decision_evidence_readiness_report_blocks_generation_flags() -> None:
    report = DecisionEvidenceBundleReadinessReport(
        report_id="report-1",
        bundle_id="bundle-1",
        planning_stage=DecisionEvidenceStage.CONTRACTS_ONLY,
        evidence_item_count=1,
        provenance_complete=False,
        validation_checklist_complete=False,
        human_review_attachments_complete=False,
        safety_decision="blocked",
        blockers=["missing provenance"],
    )

    assert decision_evidence_ready_for_bundle_validation(report) is False
    assert decision_evidence_ready_for_decision_object_generation(report) is False
    assert decision_evidence_ready_for_recommendations(report) is False
    assert decision_evidence_ready_for_execution(report) is False

    for field in [
        "ready_for_decision_object_generation",
        "ready_for_recommendations",
        "ready_for_action_generation",
        "ready_for_confidence_scoring",
        "ready_for_execution",
    ]:
        with pytest.raises(ValidationError):
            DecisionEvidenceBundleReadinessReport(
                report_id="report-1",
                bundle_id="bundle-1",
                planning_stage=DecisionEvidenceStage.CONTRACTS_ONLY,
                evidence_item_count=1,
                provenance_complete=True,
                validation_checklist_complete=True,
                human_review_attachments_complete=True,
                safety_decision="contracts_allowed",
                **{field: True},
            )


def test_build_decision_evidence_readiness_report_is_conservative() -> None:
    bundle = default_decision_object_evidence_bundle_contract()
    provenance_map = build_decision_evidence_provenance_map()
    checklist = build_decision_evidence_validation_checklist()
    attachments = build_decision_evidence_human_review_attachment_set()
    safety = evaluate_decision_evidence_bundle_safety(bundle, default_decision_evidence_safety_policy())

    report = build_decision_evidence_bundle_readiness_report(bundle, provenance_map, checklist, attachments, safety)

    assert report.evidence_item_count == len(bundle.evidence_items)
    assert report.ready_for_bundle_validation is False
    assert report.ready_for_decision_object_generation is False
    assert report.ready_for_recommendations is False
    assert report.ready_for_action_generation is False
    assert report.ready_for_confidence_scoring is False
    assert report.ready_for_execution is False
    assert report.blockers
