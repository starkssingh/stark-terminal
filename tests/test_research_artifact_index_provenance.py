from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index.provenance import (
    ResearchArtifactIndexProvenancePlaceholder,
    default_research_artifact_index_provenance_placeholders,
)


def test_research_artifact_index_provenance_placeholder_validates() -> None:
    placeholder = ResearchArtifactIndexProvenancePlaceholder(
        provenance_id="provenance-placeholder",
        index_id="index-placeholder",
        registry_reference_placeholder="registry-reference-placeholder",
        source_reference_placeholder="source-reference-placeholder",
        audit_notes=["descriptive only"],
    )

    assert placeholder.planning_only is True
    assert placeholder.source_validated is False


def test_research_artifact_index_provenance_rejects_validation_or_trust_claims() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactIndexProvenancePlaceholder(provenance_id="x", index_id="x", source_validated=True)
    with pytest.raises(ValidationError):
        ResearchArtifactIndexProvenancePlaceholder(
            provenance_id="x",
            index_id="x",
            registry_reference_placeholder="registry-reference-placeholder",
            audit_notes=["trusted real market data"],
        )


def test_default_research_artifact_index_provenance_placeholders_do_not_fetch_or_write() -> None:
    fields = set(ResearchArtifactIndexProvenancePlaceholder.model_fields)
    placeholders = default_research_artifact_index_provenance_placeholders()

    assert placeholders
    assert "fetch_url" not in fields
    assert "write_path" not in fields
    assert all(item.source_validated is False for item in placeholders)

