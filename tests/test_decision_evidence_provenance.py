from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_evidence.items import default_decision_evidence_item_contracts
from stark_terminal_core.decision_evidence.provenance import (
    DecisionEvidenceProvenanceRequirement,
    DecisionEvidenceSourceReference,
    build_decision_evidence_provenance_map,
    default_decision_evidence_provenance_requirements,
    evaluate_decision_evidence_provenance_map,
)


def test_valid_decision_evidence_source_reference() -> None:
    source = DecisionEvidenceSourceReference(
        source_id="source-1",
        source_type="synthetic_fixture",
        source_data_reference="fixtures/local",
    )

    assert source.synthetic_or_local_only_until_approved is True
    assert source.real_market_data is False


def test_decision_evidence_source_reference_rejects_real_market_data() -> None:
    with pytest.raises(ValidationError):
        DecisionEvidenceSourceReference(
            source_id="source-1",
            source_type="provider",
            source_data_reference="live",
            real_market_data=True,
        )


def test_decision_evidence_provenance_requirement_and_map() -> None:
    requirement = DecisionEvidenceProvenanceRequirement(
        provenance_id="prov-1",
        item_id="item-1",
        required_source_types=[" source_reference ", "validation_report"],
    )
    assert requirement.required_source_types == ["source_reference", "validation_report"]

    with pytest.raises(ValidationError):
        DecisionEvidenceProvenanceRequirement(
            provenance_id="prov-1",
            item_id="item-1",
            required_source_types=[],
        )

    requirements = default_decision_evidence_provenance_requirements(default_decision_evidence_item_contracts())
    assert requirements
    provenance_map = build_decision_evidence_provenance_map(requirements=requirements)
    evaluated = evaluate_decision_evidence_provenance_map(provenance_map)

    assert evaluated.complete is False
    assert evaluated.blockers
    assert len(requirements) == len(default_decision_evidence_item_contracts())
