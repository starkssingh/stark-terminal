from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry.provenance import (
    ResearchArtifactProvenancePlaceholder,
    default_research_artifact_provenance_placeholders,
)
from stark_terminal_core.research_artifact_registry.types import ResearchArtifactProvenanceSourceType


def _provenance(**overrides: object) -> ResearchArtifactProvenancePlaceholder:
    data = {
        "provenance_id": "provenance-placeholder-v1",
        "artifact_id": "metadata-placeholder-v1",
        "source_type": ResearchArtifactProvenanceSourceType.PAPER_REFERENCE,
        "source_label": "Paper source placeholder",
        "source_data_reference": "source-data-placeholder",
        "audit_notes": ["Descriptive only."],
    }
    data.update(overrides)
    return ResearchArtifactProvenancePlaceholder(**data)


def test_provenance_placeholder_validates() -> None:
    placeholder = _provenance()

    assert placeholder.source_data_reference == "source-data-placeholder"
    assert placeholder.audit_notes == ["Descriptive only."]


def test_provenance_placeholder_rejects_unknown_source() -> None:
    with pytest.raises(ValidationError):
        _provenance(source_type=ResearchArtifactProvenanceSourceType.UNKNOWN)


def test_provenance_placeholder_rejects_real_data_trust_claim() -> None:
    with pytest.raises(ValidationError):
        _provenance(audit_notes=["validated real market data"])


def test_default_provenance_placeholders_validate() -> None:
    placeholders = default_research_artifact_provenance_placeholders()

    assert placeholders
    assert all("validated real market data" not in " ".join(item.audit_notes).lower() for item in placeholders)

