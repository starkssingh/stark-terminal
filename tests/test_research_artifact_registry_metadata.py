from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.research_artifact_registry.metadata import (
    ResearchArtifactMetadataPlaceholder,
    default_research_artifact_metadata_placeholders,
)
from stark_terminal_core.research_artifact_registry.types import (
    ResearchArtifactKind,
    ResearchArtifactLifecycleStatus,
)


def _metadata(**overrides: object) -> ResearchArtifactMetadataPlaceholder:
    data = {
        "artifact_id": "metadata-placeholder-v1",
        "artifact_kind": ResearchArtifactKind.PAPER_REFERENCE,
        "title": "Paper Reference",
        "description": "Reference only.",
        "tags": ["planning-only"],
        "source_reference": "source-placeholder",
        "provenance_reference": "provenance-placeholder",
        "lifecycle_status": ResearchArtifactLifecycleStatus.PLACEHOLDER,
    }
    data.update(overrides)
    return ResearchArtifactMetadataPlaceholder(**data)


def test_metadata_placeholder_validates() -> None:
    placeholder = _metadata()

    assert placeholder.artifact_id == "metadata-placeholder-v1"
    assert placeholder.artifact_kind == ResearchArtifactKind.PAPER_REFERENCE


@pytest.mark.parametrize("field_name", ["artifact_id", "title"])
def test_metadata_placeholder_rejects_empty_required_text(field_name: str) -> None:
    with pytest.raises(ValidationError):
        _metadata(**{field_name: " "})


def test_metadata_placeholder_rejects_unknown_kind() -> None:
    with pytest.raises(ValidationError):
        _metadata(artifact_kind=ResearchArtifactKind.UNKNOWN)


def test_metadata_placeholder_has_no_active_content_fields() -> None:
    fields = set(ResearchArtifactMetadataPlaceholder.model_fields)

    assert "file_contents" not in fields
    assert "parsed_paper_text" not in fields
    assert "strategy_logic" not in fields
    assert "backtest_metrics" not in fields
    assert "recommendation_text" not in fields


def test_default_metadata_placeholders_validate() -> None:
    placeholders = default_research_artifact_metadata_placeholders()

    assert placeholders
    assert all(placeholder.artifact_kind != ResearchArtifactKind.UNKNOWN for placeholder in placeholders)

