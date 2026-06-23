from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.decision_evidence.bundle import default_decision_object_evidence_bundle_contract
from stark_terminal_core.decision_evidence.health import check_decision_evidence_health
from stark_terminal_core.decision_evidence.human_review import (
    build_decision_evidence_human_review_attachment_set,
    default_decision_evidence_human_review_attachments,
    evaluate_decision_evidence_human_review_attachment_set,
)
from stark_terminal_core.decision_evidence.items import default_decision_evidence_item_contracts
from stark_terminal_core.decision_evidence.provenance import (
    build_decision_evidence_provenance_map,
    default_decision_evidence_provenance_requirements,
    evaluate_decision_evidence_provenance_map,
)
from stark_terminal_core.decision_evidence.readiness import build_decision_evidence_bundle_readiness_report
from stark_terminal_core.decision_evidence.safety import (
    default_decision_evidence_safety_policy,
    evaluate_decision_evidence_bundle_safety,
    evaluate_decision_evidence_items_safety,
)
from stark_terminal_core.decision_evidence.validation import (
    build_decision_evidence_validation_checklist,
    evaluate_decision_evidence_validation_checklist,
)

router = APIRouter()


@router.get("/decision-evidence/health")
def decision_evidence_health() -> dict[str, Any]:
    status = check_decision_evidence_health(get_settings())
    return {
        "service": "stark-terminal-decision-evidence",
        **status.model_dump(),
    }


@router.get("/decision-evidence/contracts")
def decision_evidence_contracts() -> dict[str, Any]:
    settings = get_settings()
    items = default_decision_evidence_item_contracts()
    provenance_requirements = default_decision_evidence_provenance_requirements(items)
    return {
        "service": "stark-terminal-decision-evidence",
        "schema_version": settings.decision_evidence_schema_version,
        "computation_scope": "contracts-only",
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "execution_allowed_now": False,
        "default_evidence_item_kinds": [item.kind.value for item in items],
        "required_provenance": [requirement.provenance_id for requirement in provenance_requirements],
        "forbidden_outputs": [
            "recommendation_generation",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation",
            "execution_apis",
            "broker_integration",
            "event_publishing_to_decision_or_execution_systems",
        ],
    }


@router.get("/decision-evidence/readiness-template")
def decision_evidence_readiness_template() -> dict[str, Any]:
    settings = get_settings()
    bundle = default_decision_object_evidence_bundle_contract()
    provenance_map = evaluate_decision_evidence_provenance_map(
        build_decision_evidence_provenance_map(),
    )
    validation_checklist = evaluate_decision_evidence_validation_checklist(
        build_decision_evidence_validation_checklist(),
    )
    human_review_attachments = evaluate_decision_evidence_human_review_attachment_set(
        build_decision_evidence_human_review_attachment_set(),
    )
    policy = default_decision_evidence_safety_policy(settings)
    bundle_safety = evaluate_decision_evidence_bundle_safety(bundle, policy)
    items_safety = evaluate_decision_evidence_items_safety(bundle.evidence_items, policy)
    safety_result = bundle_safety if bundle_safety.decision == "blocked" else items_safety
    readiness = build_decision_evidence_bundle_readiness_report(
        bundle,
        provenance_map,
        validation_checklist,
        human_review_attachments,
        safety_result,
    )
    return {
        "service": "stark-terminal-decision-evidence",
        "contracts_only": True,
        "recommendations_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "execution_allowed_now": False,
        "provenance_map": provenance_map.model_dump(mode="json"),
        "validation_checklist": validation_checklist.model_dump(mode="json"),
        "human_review_attachment_set": human_review_attachments.model_dump(mode="json"),
        "readiness_report": readiness.model_dump(mode="json"),
        "must_not_generate_action_states": True,
        "must_not_generate_confidence_scores": True,
        "must_not_generate_decision_objects": True,
        "must_not_generate_recommendations": True,
    }


@router.get("/decision-evidence/human-review-template")
def decision_evidence_human_review_template() -> dict[str, Any]:
    attachments = default_decision_evidence_human_review_attachments()
    attachment_set = evaluate_decision_evidence_human_review_attachment_set(
        build_decision_evidence_human_review_attachment_set(attachments=attachments),
    )
    return {
        "service": "stark-terminal-decision-evidence",
        "contracts_only": True,
        "attachments": [attachment.model_dump(mode="json") for attachment in attachments],
        "attachment_set": attachment_set.model_dump(mode="json"),
        "approval_granted": False,
        "no_decision_object_generation": True,
        "no_execution": True,
    }

