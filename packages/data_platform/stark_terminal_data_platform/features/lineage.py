from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import FeatureComputationMode
from stark_terminal_data_platform.features.definitions import _normalize_non_empty, validate_feature_name
from stark_terminal_data_platform.features.values import SECRET_KEY_PARTS


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _reject_secret_reference(value: str) -> str:
    normalized = _normalize_non_empty(value, "lineage reference")
    lowered = normalized.lower()
    if any(part in lowered for part in SECRET_KEY_PARTS):
        raise ValueError("lineage references cannot contain secret-like content")
    return normalized


class FeatureLineageRecord(BaseModel):
    lineage_id: str
    feature_name: str
    feature_version: str = "v1"
    upstream_sources: list[str]
    upstream_features: list[str] = Field(default_factory=list)
    computation_mode: FeatureComputationMode = FeatureComputationMode.UNKNOWN
    transformation_description: str
    code_reference: str | None = None
    data_snapshot_reference: str | None = None
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("lineage_id", "feature_version", "transformation_description")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _reject_secret_reference(value)

    @field_validator("feature_name")
    @classmethod
    def feature_name_must_be_valid(cls, value: str) -> str:
        return validate_feature_name(value)

    @field_validator("upstream_sources", "upstream_features", "notes")
    @classmethod
    def string_lists_must_be_safe(cls, value: list[str]) -> list[str]:
        return [_reject_secret_reference(item) for item in value]

    @field_validator("code_reference", "data_snapshot_reference")
    @classmethod
    def optional_references_must_be_safe(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return _reject_secret_reference(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_utc_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def must_have_upstream_reference(self) -> FeatureLineageRecord:
        if not self.upstream_sources and not self.upstream_features:
            raise ValueError("lineage requires upstream sources or upstream features")
        return self

