from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import FeatureComputationMode
from stark_terminal_data_platform.features.lineage import FeatureLineageRecord


def test_valid_lineage_record_creation() -> None:
    record = FeatureLineageRecord(
        lineage_id="lineage-1",
        feature_name="close_return_1d",
        upstream_sources=["normalized://bars"],
        computation_mode=FeatureComputationMode.BATCH,
        transformation_description="Derived from synthetic normalized bars.",
        code_reference="features/close_return.py",
    )

    assert record.created_at.tzinfo is not None
    assert record.upstream_sources == ["normalized://bars"]


def test_lineage_requires_upstream_reference() -> None:
    with pytest.raises(ValidationError):
        FeatureLineageRecord(
            lineage_id="lineage-1",
            feature_name="close_return_1d",
            upstream_sources=[],
            transformation_description="No upstreams.",
        )


def test_lineage_requires_transformation_description() -> None:
    with pytest.raises(ValidationError):
        FeatureLineageRecord(
            lineage_id="lineage-1",
            feature_name="close_return_1d",
            upstream_sources=["normalized://bars"],
            transformation_description="",
        )


@pytest.mark.parametrize("field", ["upstream_sources", "code_reference", "data_snapshot_reference"])
def test_lineage_rejects_secret_like_references(field: str) -> None:
    kwargs = {
        "lineage_id": "lineage-1",
        "feature_name": "close_return_1d",
        "upstream_sources": ["normalized://bars"],
        "transformation_description": "Derived from bars.",
    }
    if field == "upstream_sources":
        kwargs[field] = ["database_url://secret"]
    else:
        kwargs[field] = "token://secret"
    with pytest.raises(ValidationError):
        FeatureLineageRecord(**kwargs)

