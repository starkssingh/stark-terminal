from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry_display.provenance import (
    ResearchArtifactProvenanceDisplayPlaceholder,
    default_research_artifact_provenance_display_placeholder,
)


def test_provenance_display_placeholder_is_descriptive_only() -> None:
    provenance = default_research_artifact_provenance_display_placeholder()

    assert provenance.descriptive_only is True
    assert provenance.source_validation_claim is False
    assert provenance.external_fetch_enabled is False
    assert provenance.real_data_trust_claim is False
    assert provenance.audit_notes


@pytest.mark.parametrize("field_name", ["source_validation_claim", "external_fetch_enabled", "real_data_trust_claim"])
def test_provenance_display_rejects_trust_or_fetch_claims(field_name: str) -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactProvenanceDisplayPlaceholder(
            provenance_display_id="provenance",
            **{field_name: True},
        )


def test_provenance_display_rejects_active_description() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifactProvenanceDisplayPlaceholder(
            provenance_display_id="provenance",
            descriptive_only=False,
        )
