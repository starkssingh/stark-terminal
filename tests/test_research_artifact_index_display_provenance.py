from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_index_display.provenance import (
    ResearchArtifactIndexProvenanceDisplayPlaceholder,
    default_research_artifact_index_provenance_display_placeholder,
)


def test_research_artifact_index_provenance_display_is_descriptive_only() -> None:
    placeholder = default_research_artifact_index_provenance_display_placeholder()

    assert placeholder.descriptive_only is True
    assert placeholder.source_validation_claim is False
    assert placeholder.external_fetch_enabled is False
    assert placeholder.real_data_trust_claim is False


@pytest.mark.parametrize(
    "field_name",
    [
        "descriptive_only",
        "source_validation_claim",
        "external_fetch_enabled",
        "real_data_trust_claim",
    ],
)
def test_research_artifact_index_provenance_display_rejects_trust_or_generated_claims(
    field_name: str,
) -> None:
    value = False if field_name == "descriptive_only" else True
    with pytest.raises(ValidationError):
        ResearchArtifactIndexProvenanceDisplayPlaceholder(
            provenance_display_id="provenance",
            label="Provenance",
            **{field_name: value},
        )
