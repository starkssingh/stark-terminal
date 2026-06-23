from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_evidence.bundle import (
    DecisionObjectEvidenceBundleContract,
    default_decision_object_evidence_bundle_contract,
)
from stark_terminal_core.decision_evidence.items import (
    DecisionEvidenceItemContract,
    DecisionEvidenceItemKind,
    default_decision_evidence_item_contracts,
)
from stark_terminal_core.decision_evidence.safety import (
    DecisionEvidenceSafetyPolicy,
    default_decision_evidence_safety_policy,
    evaluate_decision_evidence_bundle_safety,
    evaluate_decision_evidence_items_safety,
    reject_decision_object_generation,
    reject_recommendation_action_confidence_generation,
)


def test_default_decision_evidence_safety_policy_forbids_dangerous_outputs() -> None:
    policy = default_decision_evidence_safety_policy()

    assert policy.allow_real_data is False
    assert policy.allow_recommendations is False
    assert policy.allow_action_generation is False
    assert policy.allow_confidence_scoring is False
    assert policy.allow_decision_object_generation is False
    assert policy.allow_execution is False
    assert policy.require_source_reference is True
    assert policy.require_validation_checklist is True
    assert policy.require_human_review_attachment is True


def test_decision_evidence_safety_policy_rejects_unsafe_flags() -> None:
    for field in [
        "allow_real_data",
        "allow_recommendations",
        "allow_action_generation",
        "allow_confidence_scoring",
        "allow_decision_object_generation",
        "allow_execution",
    ]:
        with pytest.raises(ValidationError):
            DecisionEvidenceSafetyPolicy(policy_id="policy-1", name="Policy", **{field: True})


def test_decision_evidence_safety_evaluators_block_missing_or_unsafe_contracts() -> None:
    policy = default_decision_evidence_safety_policy()
    bundle = default_decision_object_evidence_bundle_contract()
    safe_result = evaluate_decision_evidence_bundle_safety(bundle, policy)
    assert safe_result.decision == "contracts_allowed"

    missing_provenance_bundle = DecisionObjectEvidenceBundleContract(
        bundle_id="bundle-1",
        name="Bundle",
        evidence_items=default_decision_evidence_item_contracts(),
    )
    blocked_result = evaluate_decision_evidence_bundle_safety(missing_provenance_bundle, policy)
    assert blocked_result.decision == "blocked"
    assert "provenance map is required" in blocked_result.reasons


def test_decision_evidence_items_safety_and_reject_helpers() -> None:
    policy = default_decision_evidence_safety_policy()
    item = DecisionEvidenceItemContract(
        item_id="item-1",
        kind=DecisionEvidenceItemKind.DATA_QUALITY,
        name="data quality",
        description="Data-quality item.",
    )

    result = evaluate_decision_evidence_items_safety([item], policy)
    assert result.decision == "contracts_allowed"
    assert reject_decision_object_generation().decision == "blocked"
    assert reject_recommendation_action_confidence_generation().decision == "blocked"
