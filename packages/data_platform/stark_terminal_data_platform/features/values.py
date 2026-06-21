from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import (
    FeatureComputationMode,
    FeatureEntityType,
    FeatureValueType,
)
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.features.definitions import _normalize_non_empty


SECRET_KEY_PARTS = (
    "password",
    "secret",
    "token",
    "api_key",
    "database_url",
    "redis_url",
    "broker_token",
    "credential",
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _has_secret_like_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = str(key).lower()
            if any(part in normalized for part in SECRET_KEY_PARTS):
                return True
            if _has_secret_like_key(item):
                return True
    elif isinstance(value, list | tuple):
        return any(_has_secret_like_key(item) for item in value)
    return False


def ensure_feature_jsonable(value: Any) -> Any:
    if _has_secret_like_key(value):
        raise ValueError("feature value contains forbidden secret-like keys")
    jsonable = to_jsonable(value)
    try:
        json.dumps(jsonable, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ValueError("feature value must be JSON-serializable") from exc
    return jsonable


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class FeatureEntity(BaseModel):
    entity_type: FeatureEntityType
    keys: dict[str, str]

    @field_validator("keys")
    @classmethod
    def keys_must_be_safe(cls, value: dict[str, str]) -> dict[str, str]:
        if not value:
            raise ValueError("feature entity keys cannot be empty")
        normalized: dict[str, str] = {}
        for key, item in value.items():
            key_text = _normalize_non_empty(str(key), "feature entity key")
            item_text = _normalize_non_empty(str(item), "feature entity value")
            if _has_secret_like_key({key_text: item_text}):
                raise ValueError("feature entity keys cannot contain secret-like names")
            normalized[key_text] = item_text
        return normalized


class FeatureValue(BaseModel):
    feature_name: str
    feature_version: str = "v1"
    entity: FeatureEntity
    value: object
    value_type: FeatureValueType
    event_timestamp: datetime
    created_at: datetime = Field(default_factory=_utc_now)
    source_data_reference: str | None = None

    @field_validator("feature_name", "feature_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _normalize_non_empty(value, "feature value field")

    @field_validator("event_timestamp", "created_at")
    @classmethod
    def timestamp_must_be_utc_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def value_must_match_type(self) -> FeatureValue:
        ensure_feature_jsonable(self.value)
        if self.value_type == FeatureValueType.FLOAT and not (
            isinstance(self.value, int | float) and not isinstance(self.value, bool)
        ):
            raise ValueError("FLOAT feature values must be int or float")
        if self.value_type == FeatureValueType.INTEGER and not (
            isinstance(self.value, int) and not isinstance(self.value, bool)
        ):
            raise ValueError("INTEGER feature values must be int, not bool")
        if self.value_type == FeatureValueType.BOOLEAN and not isinstance(self.value, bool):
            raise ValueError("BOOLEAN feature values must be bool")
        if self.value_type in {FeatureValueType.STRING, FeatureValueType.CATEGORY} and not isinstance(self.value, str):
            raise ValueError("STRING/CATEGORY feature values must be str")
        if self.value_type == FeatureValueType.TIMESTAMP and not isinstance(self.value, datetime | str):
            raise ValueError("TIMESTAMP feature values must be datetime or ISO string")
        return self


class FeatureSnapshot(BaseModel):
    snapshot_id: str
    feature_set_name: str
    feature_set_version: str = "v1"
    values: list[FeatureValue]
    source_data_references: list[str] = Field(default_factory=list)
    computation_mode: FeatureComputationMode = FeatureComputationMode.UNKNOWN
    computed_at: datetime = Field(default_factory=_utc_now)
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("snapshot_id", "feature_set_name", "feature_set_version", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _normalize_non_empty(value, "feature snapshot field")

    @field_validator("values")
    @classmethod
    def values_must_not_be_empty(cls, value: list[FeatureValue]) -> list[FeatureValue]:
        if not value:
            raise ValueError("feature snapshot values cannot be empty")
        return value

    @field_validator("computed_at")
    @classmethod
    def computed_at_must_be_utc_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def values_must_have_compatible_entities(self) -> FeatureSnapshot:
        entity_types = {item.entity.entity_type for item in self.values}
        if len(entity_types) > 1:
            raise ValueError("feature snapshots cannot mix incompatible entity types")
        return self

