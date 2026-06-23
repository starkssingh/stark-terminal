from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_evidence.bundle import (
    DecisionObjectEvidenceBundleContract,
    default_decision_object_evidence_bundle_contract,
)
from stark_terminal_core.decision_evidence.items import default_decision_evidence_item_contracts


def test_valid_decision_object_evidence_bundle_contract() -> None:
    bundle = DecisionObjectEvidenceBundleContract(
        bundle_id="bundle-1",
        name="DecisionObject evidence bundle",
        evidence_items=default_decision_evidence_item_contracts(),
    )

    assert bundle.contracts_only is True
    assert bundle.recommendations_allowed is False
    assert bundle.action_generation_allowed is False
    assert bundle.confidence_scoring_allowed is False
    assert bundle.decision_object_generation_allowed is False
    assert bundle.execution_allowed is False


def test_decision_evidence_bundle_rejects_empty_items_and_unsafe_flags() -> None:
    with pytest.raises(ValidationError):
        DecisionObjectEvidenceBundleContract(bundle_id="bundle-1", name="bundle", evidence_items=[])

    base = {
        "bundle_id": "bundle-1",
        "name": "bundle",
        "evidence_items": default_decision_evidence_item_contracts(),
    }
    for field in [
        "recommendations_allowed",
        "action_generation_allowed",
        "confidence_scoring_allowed",
        "decision_object_generation_allowed",
        "execution_allowed",
    ]:
        with pytest.raises(ValidationError):
            DecisionObjectEvidenceBundleContract(**{**base, field: True})

    with pytest.raises(ValidationError):
        DecisionObjectEvidenceBundleContract(**{**base, "contracts_only": False})


def test_default_decision_object_evidence_bundle_validates() -> None:
    bundle = default_decision_object_evidence_bundle_contract()

    assert bundle.bundle_id == "decisionobject-evidence-bundle-contract-v1"
    assert bundle.contracts_only is True
    assert bundle.provenance_map is not None
    assert bundle.evidence_items
