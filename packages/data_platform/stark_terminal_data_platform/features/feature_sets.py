from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import FeatureEntityType, FeatureStatus
from stark_terminal_data_platform.features.definitions import (
    FeatureDefinition,
    _normalize_non_empty,
    contains_forbidden_feature_terms,
    feature_key,
    validate_feature_name,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def feature_set_key(name: str, version: str = "v1") -> str:
    return f"{validate_feature_name(name)}:{_normalize_non_empty(version, 'feature set version')}"


class FeatureSet(BaseModel):
    feature_set_id: str
    name: str
    version: str = "v1"
    description: str
    features: list[FeatureDefinition]
    entity_type: FeatureEntityType
    owner: str
    status: FeatureStatus = FeatureStatus.DRAFT
    created_at: datetime = Field(default_factory=_utc_now)
    tags: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @field_validator("feature_set_id", "version", "description", "owner")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = _normalize_non_empty(value, "feature set field")
        if contains_forbidden_feature_terms(normalized):
            raise ValueError("execution, broker, order, and live-trading feature sets are forbidden")
        return normalized

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, value: str) -> str:
        return validate_feature_name(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_utc_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def feature_set_must_be_consistent(self) -> FeatureSet:
        if not self.features:
            raise ValueError("features cannot be empty")
        keys = [feature_key(item.name, item.version) for item in self.features]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate feature keys are not allowed in a feature set")
        incompatible = [feature for feature in self.features if feature.entity_type != self.entity_type]
        if incompatible:
            raise ValueError("all features must share the feature set entity_type")
        return self


def create_feature_set(
    name: str,
    description: str,
    features: list[FeatureDefinition],
    entity_type: FeatureEntityType,
    owner: str,
    version: str = "v1",
    feature_set_id: str | None = None,
    status: FeatureStatus = FeatureStatus.DRAFT,
    tags: list[str] | None = None,
    notes: list[str] | None = None,
) -> FeatureSet:
    return FeatureSet(
        feature_set_id=feature_set_id or feature_set_key(name, version),
        name=name,
        version=version,
        description=description,
        features=features,
        entity_type=entity_type,
        owner=owner,
        status=status,
        tags=tags or [],
        notes=notes or [],
    )

