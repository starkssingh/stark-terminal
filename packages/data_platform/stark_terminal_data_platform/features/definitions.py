from __future__ import annotations

from datetime import datetime, timezone
import re
from typing import Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import (
    FeatureComputationMode,
    FeatureEntityType,
    FeatureFrequency,
    FeatureStatus,
    FeatureValueType,
)


FORBIDDEN_FEATURE_TERMS = (
    "execution",
    "execute",
    "order",
    "broker",
    "credential",
    "live_trading",
    "live-trading",
    "trade_trigger",
    "trade-trigger",
    "routing",
    "real_money",
)
SAFE_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_non_empty(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def contains_forbidden_feature_terms(value: str) -> bool:
    normalized = value.lower()
    return any(term in normalized for term in FORBIDDEN_FEATURE_TERMS)


def validate_feature_name(name: str) -> str:
    normalized = _normalize_non_empty(name, "feature name")
    if contains_forbidden_feature_terms(normalized):
        raise ValueError("execution, broker, order, and live-trading features are forbidden")
    if "://" in normalized or "../" in normalized or "..\\" in normalized:
        raise ValueError("feature name contains unsafe path or URL-like content")
    if any(ord(ch) < 32 for ch in normalized):
        raise ValueError("feature name contains control characters")
    return normalized


def validate_entity_key(key: str) -> str:
    normalized = _normalize_non_empty(key, "entity key")
    if not SAFE_IDENTIFIER_RE.fullmatch(normalized):
        raise ValueError("entity keys must be safe identifiers")
    return normalized


def feature_key(name: str, version: str = "v1") -> str:
    return f"{validate_feature_name(name)}:{_normalize_non_empty(version, 'feature version')}"


def _validate_string_list(values: Iterable[str], field_name: str) -> list[str]:
    normalized = [_normalize_non_empty(value, field_name) for value in values]
    return normalized


class FeatureDependency(BaseModel):
    name: str
    version: str | None = None
    feature_set: str | None = None

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, value: str) -> str:
        return validate_feature_name(value)

    @field_validator("version", "feature_set")
    @classmethod
    def optional_text_must_be_non_empty(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return _normalize_non_empty(value, "feature dependency field")


class FeatureDefinition(BaseModel):
    feature_id: str
    name: str
    version: str = "v1"
    description: str
    value_type: FeatureValueType
    entity_type: FeatureEntityType
    frequency: FeatureFrequency
    status: FeatureStatus = FeatureStatus.DRAFT
    owner: str
    entity_keys: list[str]
    dependencies: list[FeatureDependency] = Field(default_factory=list)
    computation_mode: FeatureComputationMode = FeatureComputationMode.UNKNOWN
    freshness_seconds: int | None = None
    max_staleness_seconds: int | None = None
    source_data_references: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime | None = None
    notes: list[str] = Field(default_factory=list)

    @field_validator("feature_id", "version", "description", "owner")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = _normalize_non_empty(value, "feature definition field")
        if contains_forbidden_feature_terms(normalized):
            raise ValueError("execution, broker, order, and live-trading features are forbidden")
        return normalized

    @field_validator("name")
    @classmethod
    def name_must_be_valid(cls, value: str) -> str:
        return validate_feature_name(value)

    @field_validator("entity_keys")
    @classmethod
    def entity_keys_must_be_safe(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("entity_keys cannot be empty")
        return [validate_entity_key(item) for item in value]

    @field_validator("freshness_seconds", "max_staleness_seconds")
    @classmethod
    def optional_seconds_must_be_positive(cls, value: int | None) -> int | None:
        if value is not None and value <= 0:
            raise ValueError("feature freshness/staleness seconds must be positive")
        return value

    @field_validator("source_data_references", "tags", "notes")
    @classmethod
    def string_lists_must_be_non_empty_values(cls, value: list[str]) -> list[str]:
        return _validate_string_list(value, "feature list value")

    @field_validator("created_at", "updated_at")
    @classmethod
    def datetimes_must_be_utc_aware(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def staleness_must_cover_freshness(self) -> FeatureDefinition:
        if (
            self.freshness_seconds is not None
            and self.max_staleness_seconds is not None
            and self.max_staleness_seconds < self.freshness_seconds
        ):
            raise ValueError("max_staleness_seconds must be >= freshness_seconds")
        return self


def create_feature_definition(
    name: str,
    description: str,
    value_type: FeatureValueType,
    entity_type: FeatureEntityType,
    frequency: FeatureFrequency,
    owner: str,
    entity_keys: list[str],
    settings: Settings | None = None,
    version: str = "v1",
    feature_id: str | None = None,
    status: FeatureStatus = FeatureStatus.DRAFT,
    dependencies: list[FeatureDependency] | None = None,
    computation_mode: FeatureComputationMode = FeatureComputationMode.UNKNOWN,
    freshness_seconds: int | None = None,
    max_staleness_seconds: int | None = None,
    source_data_references: list[str] | None = None,
    tags: list[str] | None = None,
    notes: list[str] | None = None,
) -> FeatureDefinition:
    resolved_settings = settings or get_settings()
    resolved_freshness = freshness_seconds or resolved_settings.feature_default_freshness_seconds
    resolved_staleness = max_staleness_seconds or resolved_settings.feature_max_allowed_staleness_seconds
    return FeatureDefinition(
        feature_id=feature_id or feature_key(name, version),
        name=name,
        version=version,
        description=description,
        value_type=value_type,
        entity_type=entity_type,
        frequency=frequency,
        status=status,
        owner=owner,
        entity_keys=entity_keys,
        dependencies=dependencies or [],
        computation_mode=computation_mode,
        freshness_seconds=resolved_freshness,
        max_staleness_seconds=resolved_staleness,
        source_data_references=source_data_references or [],
        tags=tags or [],
        notes=notes or [],
    )

