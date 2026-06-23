from __future__ import annotations

from stark_terminal_core.decision_evidence.bundle import DecisionObjectEvidenceBundleContract
from stark_terminal_core.decision_evidence.human_review import DecisionEvidenceHumanReviewAttachmentSet
from stark_terminal_core.decision_evidence.items import (
    DecisionEvidenceItemContract,
    DecisionEvidenceItemKind,
    DecisionEvidenceStatus,
    default_decision_evidence_item_contracts,
)
from stark_terminal_core.decision_evidence.provenance import DecisionEvidenceProvenanceMap
from stark_terminal_core.decision_evidence.validation import DecisionEvidenceValidationChecklist
from stark_terminal_core.decision_evidence_validation.contracts import (
    DecisionEvidenceValidationIssueKind,
    DecisionEvidenceValidationIssueSeverity,
    DecisionEvidenceValidationRequest,
    default_decision_evidence_validation_request,
)
from stark_terminal_core.decision_evidence_validation.issues import (
    DecisionEvidenceValidationIssue,
    create_missing_evidence_issue,
    create_missing_source_reference_issue,
    create_unsafe_flag_issue,
    create_validation_issue,
)
from stark_terminal_core.decision_evidence_validation.results import (
    DecisionEvidenceValidationResult,
    create_decision_evidence_validation_result,
)


def validate_evidence_item_safety_flags(
    item: DecisionEvidenceItemContract,
) -> list[DecisionEvidenceValidationIssue]:
    issues: list[DecisionEvidenceValidationIssue] = []
    unsafe_flags = {
        "value_payload_allowed": bool(getattr(item, "value_payload_allowed", False)),
        "recommendation": bool(getattr(item, "recommendation", False)),
        "action_generated": bool(getattr(item, "action_generated", False)),
        "confidence_generated": bool(getattr(item, "confidence_generated", False)),
        "decision_object_generated": bool(getattr(item, "decision_object_generated", False)),
        "execution_ready": bool(getattr(item, "execution_ready", False)),
    }
    for flag_name, flag_value in unsafe_flags.items():
        if flag_value:
            issues.append(create_unsafe_flag_issue(item.item_id, flag_name))
    if not getattr(item, "source_reference_required", True):
        issues.append(create_missing_source_reference_issue(item.item_id))
    if not getattr(item, "validation_required", True):
        issues.append(
            create_validation_issue(
                issue_id=f"missing-validation-requirement-{item.item_id}",
                kind=DecisionEvidenceValidationIssueKind.INCOMPLETE_VALIDATION_CHECKLIST,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message=f"validation is not required for decision evidence item: {item.item_id}",
                item_id=item.item_id,
            )
        )
    if not getattr(item, "human_review_required", True):
        issues.append(
            create_validation_issue(
                issue_id=f"missing-human-review-requirement-{item.item_id}",
                kind=DecisionEvidenceValidationIssueKind.MISSING_HUMAN_REVIEW_ATTACHMENT,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message=f"human review is not required for decision evidence item: {item.item_id}",
                item_id=item.item_id,
            )
        )
    return issues


def validate_evidence_items(
    items: list[DecisionEvidenceItemContract],
) -> list[DecisionEvidenceValidationIssue]:
    issues: list[DecisionEvidenceValidationIssue] = []
    if not items:
        return [create_missing_evidence_issue("all-required-decision-evidence-items")]

    expected_kinds = {item.kind for item in default_decision_evidence_item_contracts()}
    present_kinds = {item.kind for item in items}
    for missing_kind in sorted(expected_kinds - present_kinds, key=lambda kind: kind.value):
        issues.append(create_missing_evidence_issue(missing_kind.value))

    for item in items:
        if item.kind == DecisionEvidenceItemKind.UNKNOWN:
            issues.append(
                create_validation_issue(
                    issue_id=f"invalid-evidence-item-kind-{item.item_id}",
                    kind=DecisionEvidenceValidationIssueKind.INVALID_EVIDENCE_ITEM,
                    severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                    message=f"decision evidence item has UNKNOWN kind: {item.item_id}",
                    item_id=item.item_id,
                )
            )
        if item.required and item.status in {
            DecisionEvidenceStatus.MISSING,
            DecisionEvidenceStatus.INVALID,
            DecisionEvidenceStatus.BLOCKED,
        }:
            issues.append(
                create_validation_issue(
                    issue_id=f"invalid-evidence-item-status-{item.item_id}",
                    kind=DecisionEvidenceValidationIssueKind.INVALID_EVIDENCE_ITEM,
                    severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                    message=f"required decision evidence item is not valid for validation: {item.item_id}",
                    item_id=item.item_id,
                )
            )
        issues.extend(validate_evidence_item_safety_flags(item))
    return issues


def validate_provenance_map(
    provenance_map: DecisionEvidenceProvenanceMap | None,
) -> list[DecisionEvidenceValidationIssue]:
    if provenance_map is None:
        return [
            create_validation_issue(
                issue_id="missing-decision-evidence-provenance-map",
                kind=DecisionEvidenceValidationIssueKind.MISSING_PROVENANCE,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message="decision evidence provenance map is required for validation",
            )
        ]

    issues: list[DecisionEvidenceValidationIssue] = []
    if not provenance_map.requirements:
        issues.append(
            create_validation_issue(
                issue_id=f"incomplete-provenance-{provenance_map.map_id}-requirements",
                kind=DecisionEvidenceValidationIssueKind.INCOMPLETE_PROVENANCE,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message="decision evidence provenance map has no requirements",
            )
        )
    if not provenance_map.complete:
        issues.append(
            create_validation_issue(
                issue_id=f"incomplete-provenance-{provenance_map.map_id}",
                kind=DecisionEvidenceValidationIssueKind.INCOMPLETE_PROVENANCE,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message="decision evidence provenance map is incomplete",
            )
        )
    for blocker_index, blocker in enumerate(provenance_map.blockers, start=1):
        issues.append(
            create_validation_issue(
                issue_id=f"incomplete-provenance-{provenance_map.map_id}-blocker-{blocker_index}",
                kind=DecisionEvidenceValidationIssueKind.INCOMPLETE_PROVENANCE,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message=blocker,
            )
        )
    for requirement in provenance_map.requirements:
        if not requirement.required_source_types:
            issues.append(
                create_validation_issue(
                    issue_id=f"invalid-source-reference-{requirement.provenance_id}",
                    kind=DecisionEvidenceValidationIssueKind.INVALID_SOURCE_REFERENCE,
                    severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                    message=f"provenance requirement has no required source types: {requirement.provenance_id}",
                    item_id=requirement.item_id,
                )
            )
        if not requirement.source_reference_required or not requirement.validation_report_required:
            issues.append(
                create_validation_issue(
                    issue_id=f"missing-source-reference-{requirement.provenance_id}",
                    kind=DecisionEvidenceValidationIssueKind.MISSING_SOURCE_REFERENCE,
                    severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                    message=f"provenance requirement does not require source and validation references: {requirement.provenance_id}",
                    item_id=requirement.item_id,
                )
            )
    return issues


def validate_validation_checklist(
    checklist: DecisionEvidenceValidationChecklist | None,
) -> list[DecisionEvidenceValidationIssue]:
    if checklist is None:
        return [
            create_validation_issue(
                issue_id="missing-decision-evidence-validation-checklist",
                kind=DecisionEvidenceValidationIssueKind.MISSING_VALIDATION_CHECKLIST,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message="decision evidence validation checklist is required",
            )
        ]

    issues: list[DecisionEvidenceValidationIssue] = []
    if not checklist.requirements:
        issues.append(
            create_validation_issue(
                issue_id=f"incomplete-validation-checklist-{checklist.checklist_id}-requirements",
                kind=DecisionEvidenceValidationIssueKind.INCOMPLETE_VALIDATION_CHECKLIST,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message="decision evidence validation checklist has no requirements",
            )
        )
    if not checklist.complete:
        issues.append(
            create_validation_issue(
                issue_id=f"incomplete-validation-checklist-{checklist.checklist_id}",
                kind=DecisionEvidenceValidationIssueKind.INCOMPLETE_VALIDATION_CHECKLIST,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message="decision evidence validation checklist is incomplete",
            )
        )
    for blocker_index, blocker in enumerate(checklist.blockers, start=1):
        issues.append(
            create_validation_issue(
                issue_id=f"incomplete-validation-checklist-{checklist.checklist_id}-blocker-{blocker_index}",
                kind=DecisionEvidenceValidationIssueKind.INCOMPLETE_VALIDATION_CHECKLIST,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message=blocker,
            )
        )
    unsafe_flags = {
        "recommendations_allowed": checklist.recommendations_allowed,
        "action_generation_allowed": checklist.action_generation_allowed,
        "confidence_scoring_allowed": checklist.confidence_scoring_allowed,
        "decision_object_generation_allowed": checklist.decision_object_generation_allowed,
        "execution_allowed": checklist.execution_allowed,
    }
    for flag_name, flag_value in unsafe_flags.items():
        if flag_value:
            issues.append(create_unsafe_flag_issue(checklist.checklist_id, flag_name))
    return issues


def validate_human_review_attachment_set(
    attachment_set: DecisionEvidenceHumanReviewAttachmentSet | None,
) -> list[DecisionEvidenceValidationIssue]:
    if attachment_set is None:
        return [
            create_validation_issue(
                issue_id="missing-decision-evidence-human-review-attachment-set",
                kind=DecisionEvidenceValidationIssueKind.MISSING_HUMAN_REVIEW_ATTACHMENT,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message="decision evidence human-review attachment set is required",
            )
        ]

    issues: list[DecisionEvidenceValidationIssue] = []
    if not attachment_set.attachments:
        issues.append(
            create_validation_issue(
                issue_id=f"incomplete-human-review-attachment-set-{attachment_set.attachment_set_id}-attachments",
                kind=DecisionEvidenceValidationIssueKind.INCOMPLETE_HUMAN_REVIEW_ATTACHMENT,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message="decision evidence human-review attachment set has no attachments",
            )
        )
    if not attachment_set.complete:
        issues.append(
            create_validation_issue(
                issue_id=f"incomplete-human-review-attachment-set-{attachment_set.attachment_set_id}",
                kind=DecisionEvidenceValidationIssueKind.INCOMPLETE_HUMAN_REVIEW_ATTACHMENT,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message="decision evidence human-review attachment set is incomplete",
            )
        )
    for blocker_index, blocker in enumerate(attachment_set.blockers, start=1):
        issues.append(
            create_validation_issue(
                issue_id=f"incomplete-human-review-attachment-set-{attachment_set.attachment_set_id}-blocker-{blocker_index}",
                kind=DecisionEvidenceValidationIssueKind.INCOMPLETE_HUMAN_REVIEW_ATTACHMENT,
                severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                message=blocker,
            )
        )
    unsafe_flags = {
        "approval_granted": attachment_set.approval_granted,
        "decision_object_generation_allowed": attachment_set.decision_object_generation_allowed,
        "execution_allowed": attachment_set.execution_allowed,
    }
    for flag_name, flag_value in unsafe_flags.items():
        if flag_value:
            issues.append(create_unsafe_flag_issue(attachment_set.attachment_set_id, flag_name))
    for attachment in attachment_set.attachments:
        if attachment.required and not attachment.completed:
            issues.append(
                create_validation_issue(
                    issue_id=f"incomplete-human-review-attachment-{attachment.attachment_id}",
                    kind=DecisionEvidenceValidationIssueKind.INCOMPLETE_HUMAN_REVIEW_ATTACHMENT,
                    severity=DecisionEvidenceValidationIssueSeverity.BLOCKER,
                    message=f"required human-review attachment is not complete: {attachment.attachment_id}",
                )
            )
    return issues


def validate_evidence_bundle_contract(
    bundle: DecisionObjectEvidenceBundleContract,
    request: DecisionEvidenceValidationRequest | None = None,
    provenance_map: DecisionEvidenceProvenanceMap | None = None,
    checklist: DecisionEvidenceValidationChecklist | None = None,
    human_review: DecisionEvidenceHumanReviewAttachmentSet | None = None,
) -> DecisionEvidenceValidationResult:
    resolved_request = request or default_decision_evidence_validation_request()
    issues: list[DecisionEvidenceValidationIssue] = []

    if resolved_request.validate_items:
        issues.extend(validate_evidence_items(list(bundle.evidence_items)))

    if resolved_request.validate_safety_flags:
        bundle_flags = {
            "recommendations_allowed": bundle.recommendations_allowed,
            "action_generation_allowed": bundle.action_generation_allowed,
            "confidence_scoring_allowed": bundle.confidence_scoring_allowed,
            "decision_object_generation_allowed": bundle.decision_object_generation_allowed,
            "execution_allowed": bundle.execution_allowed,
            "contracts_only_false": not bundle.contracts_only,
        }
        for flag_name, flag_value in bundle_flags.items():
            if flag_value:
                issues.append(create_unsafe_flag_issue(bundle.bundle_id, flag_name))

    if resolved_request.validate_provenance:
        issues.extend(validate_provenance_map(provenance_map if provenance_map is not None else bundle.provenance_map))

    if resolved_request.validate_checklist:
        issues.extend(validate_validation_checklist(checklist))

    if resolved_request.validate_human_review:
        issues.extend(validate_human_review_attachment_set(human_review))

    has_blocking_issues = any(
        issue.severity
        in {DecisionEvidenceValidationIssueSeverity.ERROR, DecisionEvidenceValidationIssueSeverity.BLOCKER}
        for issue in issues
    )
    return create_decision_evidence_validation_result(
        result_id=f"decision-evidence-validation-result-{resolved_request.request_id}",
        request_id=resolved_request.request_id,
        bundle_id=bundle.bundle_id,
        valid=not has_blocking_issues,
        issues=issues,
        status="valid_validation_only_not_decision_ready" if not has_blocking_issues else "blocked_validation_only",
        notes=[
            "Validation result is not approval, recommendation, readiness-to-trade, DecisionObject readiness, or execution readiness.",
        ],
    )

