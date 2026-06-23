from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.decision_evidence.bundle import default_decision_object_evidence_bundle_contract
from stark_terminal_core.decision_evidence_validation.contracts import (
    DecisionEvidenceValidationIssueKind,
    DecisionEvidenceValidationIssueSeverity,
    default_decision_evidence_validation_request,
)
from stark_terminal_core.decision_evidence_validation.health import (
    check_decision_evidence_validation_health,
)
from stark_terminal_core.decision_evidence_validation.issues import create_validation_issue
from stark_terminal_core.decision_evidence_validation.results import (
    create_invalid_decision_evidence_validation_result,
)
from stark_terminal_core.decision_evidence_validation.validators import (
    validate_evidence_bundle_contract,
)

router = APIRouter()


@router.get("/decision-evidence-validation/health")
def decision_evidence_validation_health() -> dict[str, Any]:
    status = check_decision_evidence_validation_health(get_settings())
    return {
        "service": "stark-terminal-decision-evidence-validation",
        **status.model_dump(),
    }


@router.get("/decision-evidence-validation/contracts")
def decision_evidence_validation_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-decision-evidence-validation",
        "schema_version": settings.decision_evidence_validation_schema_version,
        "computation_scope": "validation-only",
        "recommendations_allowed_now": False,
        "action_generation_allowed_now": False,
        "confidence_scoring_allowed_now": False,
        "decision_object_generation_allowed_now": False,
        "execution_allowed_now": False,
        "approval_allowed_now": False,
        "override_allowed_now": False,
        "readiness_to_trade_allowed_now": False,
        "validation_only": True,
        "issue_kinds": [
            issue_kind.value
            for issue_kind in DecisionEvidenceValidationIssueKind
            if issue_kind != DecisionEvidenceValidationIssueKind.UNKNOWN
        ],
        "issue_severities": [
            severity.value
            for severity in DecisionEvidenceValidationIssueSeverity
            if severity != DecisionEvidenceValidationIssueSeverity.UNKNOWN
        ],
        "forbidden_outputs": [
            "validation_as_recommendation",
            "validation_as_approval",
            "validation_as_readiness-to-trade",
            "recommendation_generation",
            "action_generation",
            "confidence_scoring",
            "DecisionObject_generation",
            "approval_workflow",
            "override_workflow",
            "execution_apis",
            "broker_behavior",
        ],
    }


@router.get("/decision-evidence-validation/template")
def decision_evidence_validation_template() -> dict[str, Any]:
    request = default_decision_evidence_validation_request()
    template_issue = create_validation_issue(
        issue_id="decision-evidence-validation-template-blocker",
        kind=DecisionEvidenceValidationIssueKind.MISSING_PROVENANCE,
        severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
        message="template result has no supplied bundle context and remains validation-only",
    )
    result = create_invalid_decision_evidence_validation_result(
        request_id=request.request_id,
        bundle_id=request.bundle_id,
        issues=[template_issue],
    )
    return {
        "service": "stark-terminal-decision-evidence-validation",
        "validation_only": True,
        "default_validation_request": request.model_dump(mode="json"),
        "default_validation_result_template": result.model_dump(mode="json"),
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_approval": True,
        "no_override": True,
        "no_readiness_to_trade": True,
        "no_execution": True,
    }


@router.get("/decision-evidence-validation/sample")
def decision_evidence_validation_sample() -> dict[str, Any]:
    request = default_decision_evidence_validation_request()
    bundle = default_decision_object_evidence_bundle_contract()
    result = validate_evidence_bundle_contract(bundle=bundle, request=request)
    return {
        "service": "stark-terminal-decision-evidence-validation",
        "validation_only": True,
        "sample_scope": "built-in-default-contracts-only",
        "request": request.model_dump(mode="json"),
        "bundle_id": bundle.bundle_id,
        "validation_result": result.model_dump(mode="json"),
        "accepts_user_input": False,
        "no_recommendations": True,
        "no_action_generation": True,
        "no_confidence_scoring": True,
        "no_decision_object": True,
        "no_approval": True,
        "no_override": True,
        "no_readiness_to_trade": True,
        "no_execution": True,
    }

