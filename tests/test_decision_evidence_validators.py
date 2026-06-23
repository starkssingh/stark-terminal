from __future__ import annotations

from stark_terminal_core.decision_evidence.bundle import (
    create_decision_object_evidence_bundle_contract,
    default_decision_object_evidence_bundle_contract,
)
from stark_terminal_core.decision_evidence.human_review import (
    build_decision_evidence_human_review_attachment_set,
    default_decision_evidence_human_review_attachments,
)
from stark_terminal_core.decision_evidence.items import (
    DecisionEvidenceItemContract,
    default_decision_evidence_item_contracts,
)
from stark_terminal_core.decision_evidence.provenance import (
    build_decision_evidence_provenance_map,
    default_decision_evidence_provenance_requirements,
)
from stark_terminal_core.decision_evidence.validation import (
    build_decision_evidence_validation_checklist,
    default_decision_evidence_validation_requirements,
)
from stark_terminal_core.decision_evidence_validation.contracts import (
    DecisionEvidenceValidationIssueKind,
)
from stark_terminal_core.decision_evidence_validation.validators import (
    validate_evidence_bundle_contract,
    validate_evidence_item_safety_flags,
    validate_evidence_items,
    validate_human_review_attachment_set,
    validate_provenance_map,
    validate_validation_checklist,
)


def _complete_bundle_context():
    items = default_decision_evidence_item_contracts()
    provenance_requirements = default_decision_evidence_provenance_requirements(items)
    provenance = build_decision_evidence_provenance_map(
        requirements=provenance_requirements,
        satisfied_provenance_ids={requirement.provenance_id for requirement in provenance_requirements},
    )
    checklist_requirements = default_decision_evidence_validation_requirements()
    checklist = build_decision_evidence_validation_checklist(
        requirements=checklist_requirements,
        completed_requirement_ids={requirement.requirement_id for requirement in checklist_requirements},
    )
    attachments = [
        attachment.model_copy(update={"completed": True})
        for attachment in default_decision_evidence_human_review_attachments()
    ]
    human_review = build_decision_evidence_human_review_attachment_set(
        attachments=attachments,
        completed_attachment_ids={attachment.attachment_id for attachment in attachments},
    )
    bundle = create_decision_object_evidence_bundle_contract(
        bundle_id="bundle-complete",
        name="Complete validation-only bundle",
        evidence_items=items,
        provenance_map=provenance,
    )
    return bundle, provenance, checklist, human_review


def test_default_evidence_bundle_fails_until_checklists_and_human_review_are_supplied() -> None:
    result = validate_evidence_bundle_contract(default_decision_object_evidence_bundle_contract())

    assert result.valid is False
    assert result.validation_only is True
    assert result.blocker_count > 0
    assert result.decision_object_generation_allowed is False


def test_complete_contract_context_validates_but_does_not_permit_decisionobject_generation() -> None:
    bundle, provenance, checklist, human_review = _complete_bundle_context()
    result = validate_evidence_bundle_contract(
        bundle=bundle,
        provenance_map=provenance,
        checklist=checklist,
        human_review=human_review,
    )

    assert result.valid is True
    assert result.validation_only is True
    assert result.decision_object_generation_allowed is False
    assert result.readiness_to_trade is False
    assert "not_decision_ready" in result.status


def test_missing_evidence_item_creates_blocker() -> None:
    items = default_decision_evidence_item_contracts()
    issues = validate_evidence_items(items[:-1])

    assert any(issue.kind == DecisionEvidenceValidationIssueKind.MISSING_EVIDENCE_ITEM for issue in issues)
    assert any(issue.blocks_decision_object_generation for issue in issues)


def test_unsafe_evidence_item_flag_creates_blocker() -> None:
    item = default_decision_evidence_item_contracts()[0]
    data = item.model_dump()
    data["recommendation"] = True
    unsafe = DecisionEvidenceItemContract.model_construct(**data)

    issues = validate_evidence_item_safety_flags(unsafe)

    assert any(issue.kind == DecisionEvidenceValidationIssueKind.UNSAFE_GENERATED_OUTPUT_FLAG for issue in issues)


def test_missing_and_incomplete_provenance_create_blockers() -> None:
    missing = validate_provenance_map(None)
    incomplete = validate_provenance_map(default_decision_object_evidence_bundle_contract().provenance_map)

    assert missing[0].kind == DecisionEvidenceValidationIssueKind.MISSING_PROVENANCE
    assert any(issue.kind == DecisionEvidenceValidationIssueKind.INCOMPLETE_PROVENANCE for issue in incomplete)


def test_incomplete_validation_checklist_and_human_review_create_blockers() -> None:
    incomplete_checklist = build_decision_evidence_validation_checklist()
    incomplete_human_review = build_decision_evidence_human_review_attachment_set()

    checklist_issues = validate_validation_checklist(incomplete_checklist)
    human_review_issues = validate_human_review_attachment_set(incomplete_human_review)

    assert any(
        issue.kind == DecisionEvidenceValidationIssueKind.INCOMPLETE_VALIDATION_CHECKLIST
        for issue in checklist_issues
    )
    assert any(
        issue.kind == DecisionEvidenceValidationIssueKind.INCOMPLETE_HUMAN_REVIEW_ATTACHMENT
        for issue in human_review_issues
    )


def test_validators_do_not_mutate_inputs() -> None:
    bundle, provenance, checklist, human_review = _complete_bundle_context()
    before = bundle.model_dump(mode="json")

    validate_evidence_bundle_contract(
        bundle=bundle,
        provenance_map=provenance,
        checklist=checklist,
        human_review=human_review,
    )

    assert bundle.model_dump(mode="json") == before
