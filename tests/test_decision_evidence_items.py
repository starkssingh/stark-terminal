from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_evidence.items import (
    DecisionEvidenceItemContract,
    DecisionEvidenceItemKind,
    DecisionEvidenceSafetyLabel,
    DecisionEvidenceStatus,
    default_decision_evidence_item_contracts,
)


def test_valid_decision_evidence_item_contract() -> None:
    item = DecisionEvidenceItemContract(
        item_id="item-1",
        kind=DecisionEvidenceItemKind.DATA_QUALITY,
        name="data quality",
        description="Data-quality evidence item contract.",
    )

    assert item.safety_label == DecisionEvidenceSafetyLabel.CONTRACTS_ONLY
    assert item.value_payload_allowed is False
    assert item.recommendation is False
    assert item.action_generated is False
    assert item.confidence_generated is False
    assert item.decision_object_generated is False
    assert item.execution_ready is False


def test_decision_evidence_item_rejects_unknown_and_unsafe_flags() -> None:
    base = {
        "item_id": "item-1",
        "kind": DecisionEvidenceItemKind.DATA_QUALITY,
        "name": "data quality",
        "description": "Data-quality evidence item contract.",
    }
    with pytest.raises(ValidationError):
        DecisionEvidenceItemContract(**{**base, "kind": DecisionEvidenceItemKind.UNKNOWN})

    for field in [
        "value_payload_allowed",
        "recommendation",
        "action_generated",
        "confidence_generated",
        "decision_object_generated",
        "execution_ready",
    ]:
        with pytest.raises(ValidationError):
            DecisionEvidenceItemContract(**{**base, field: True})


def test_default_decision_evidence_items_cover_expected_kinds() -> None:
    items = default_decision_evidence_item_contracts()
    kinds = {item.kind for item in items}

    assert DecisionEvidenceItemKind.INSTRUMENT_CONTEXT in kinds
    assert DecisionEvidenceItemKind.DATA_QUALITY in kinds
    assert DecisionEvidenceItemKind.RETURNS in kinds
    assert DecisionEvidenceItemKind.VOLATILITY in kinds
    assert DecisionEvidenceItemKind.DRAWDOWN in kinds
    assert DecisionEvidenceItemKind.CORRELATION_BETA in kinds
    assert DecisionEvidenceItemKind.TIME_SERIES_DIAGNOSTICS in kinds
    assert DecisionEvidenceItemKind.REGIME_CONTEXT in kinds
    assert DecisionEvidenceItemKind.REGIME_FEATURE_CONTEXT in kinds
    assert DecisionEvidenceItemKind.RISK_CONTEXT in kinds
    assert DecisionEvidenceItemKind.HUMAN_REVIEW in kinds
    assert all(item.status == DecisionEvidenceStatus.REQUIRED for item in items)
    assert all(item.value_payload_allowed is False for item in items)
