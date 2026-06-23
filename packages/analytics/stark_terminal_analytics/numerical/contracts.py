from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
import math

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes


class NumericalDataKind(StrEnum):
    VECTOR = "VECTOR"
    TABLE = "TABLE"
    TIME_SERIES = "TIME_SERIES"
    SCALAR = "SCALAR"
    UNKNOWN = "UNKNOWN"


class NumericalValueType(StrEnum):
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    TIMESTAMP = "TIMESTAMP"
    STRING_LABEL = "STRING_LABEL"
    UNKNOWN = "UNKNOWN"


class NumericalComputationKind(StrEnum):
    VALIDATION = "VALIDATION"
    SUMMARY = "SUMMARY"
    SHAPE_CHECK = "SHAPE_CHECK"
    FINITE_CHECK = "FINITE_CHECK"
    SOURCE_CHECK = "SOURCE_CHECK"
    UNKNOWN = "UNKNOWN"


class NumericalSafetyLabel(StrEnum):
    DESCRIPTIVE_ONLY = "DESCRIPTIVE_ONLY"
    RESEARCH_ONLY = "RESEARCH_ONLY"
    NOT_A_SIGNAL = "NOT_A_SIGNAL"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _status_allows_empty_metrics(status: str) -> bool:
    return status.strip().lower() in {"failed", "failure", "error", "blocked"}


class NumericalSourceReference(BaseModel):
    source_id: str
    source_type: str
    source_data_reference: str
    synthetic: bool = True
    real_market_data: bool = False
    provider_name: str | None = None
    dataset_manifest_id: str | None = None
    notes: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("source_id", "source_type", "source_data_reference", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "numerical source reference text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def real_market_data_must_remain_false(self) -> NumericalSourceReference:
        if self.real_market_data:
            raise ValueError("numerical source references cannot claim real market data in Prompt 27")
        return self


class NumericalVectorContract(BaseModel):
    vector_id: str
    name: str
    values: list[float]
    value_type: NumericalValueType = NumericalValueType.FLOAT
    data_kind: NumericalDataKind = NumericalDataKind.VECTOR
    source: NumericalSourceReference
    finite_required: bool = True
    sorted_by_time: bool | None = None
    descriptive_only: bool = True
    safety_label: NumericalSafetyLabel = NumericalSafetyLabel.DESCRIPTIVE_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("vector_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "numerical vector text fields")

    @field_validator("values")
    @classmethod
    def values_must_be_present(cls, value: list[float]) -> list[float]:
        if not value:
            raise ValueError("numerical vector values cannot be empty")
        return value

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def vector_must_remain_safe(self) -> NumericalVectorContract:
        if self.finite_required and not all(math.isfinite(value) for value in self.values):
            raise ValueError("numerical vector values must be finite")
        if not self.descriptive_only:
            raise ValueError("numerical vector contracts must remain descriptive-only")
        if self.safety_label == NumericalSafetyLabel.UNKNOWN:
            raise ValueError("numerical vector safety label cannot be UNKNOWN")
        if self.data_kind not in {NumericalDataKind.VECTOR, NumericalDataKind.TIME_SERIES}:
            raise ValueError("numerical vector data_kind must be VECTOR or TIME_SERIES")
        return self


class NumericalTableColumn(BaseModel):
    name: str
    value_type: NumericalValueType
    required: bool = True
    nullable: bool = False
    notes: list[str] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def name_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "numerical table column name")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)


class NumericalTableContract(BaseModel):
    table_id: str
    name: str
    columns: list[NumericalTableColumn]
    row_count: int = Field(ge=0)
    source: NumericalSourceReference
    data_kind: NumericalDataKind = NumericalDataKind.TABLE
    descriptive_only: bool = True
    safety_label: NumericalSafetyLabel = NumericalSafetyLabel.DESCRIPTIVE_ONLY
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("table_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "numerical table text fields")

    @field_validator("columns")
    @classmethod
    def columns_must_be_present(cls, value: list[NumericalTableColumn]) -> list[NumericalTableColumn]:
        if not value:
            raise ValueError("numerical table columns cannot be empty")
        return value

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def table_must_remain_safe(self) -> NumericalTableContract:
        if not self.descriptive_only:
            raise ValueError("numerical table contracts must remain descriptive-only")
        if self.safety_label == NumericalSafetyLabel.UNKNOWN:
            raise ValueError("numerical table safety label cannot be UNKNOWN")
        if self.data_kind != NumericalDataKind.TABLE:
            raise ValueError("numerical table data_kind must be TABLE")
        return self


class NumericalComputationRequest(BaseModel):
    request_id: str
    computation_kind: NumericalComputationKind
    input_ids: list[str]
    source: NumericalSourceReference
    require_finite_values: bool = True
    require_source_reference: bool = True
    allow_real_data: bool = False
    allow_trade_signal: bool = False
    allow_recommendation: bool = False
    allow_decision_object: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("request_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "numerical computation request text fields")

    @field_validator("input_ids")
    @classmethod
    def input_ids_must_be_present(cls, value: list[str]) -> list[str]:
        normalized = [_non_empty_text(input_id, "input_ids") for input_id in value]
        if not normalized:
            raise ValueError("input_ids cannot be empty")
        return normalized

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def request_must_remain_safe(self) -> NumericalComputationRequest:
        if self.allow_real_data:
            raise ValueError("numerical computation requests cannot allow real data in Prompt 27")
        if self.allow_trade_signal:
            raise ValueError("numerical computation requests cannot allow trade signals")
        if self.allow_recommendation:
            raise ValueError("numerical computation requests cannot allow recommendations")
        if self.allow_decision_object:
            raise ValueError("numerical computation requests cannot allow DecisionObject generation")
        if not self.require_source_reference:
            raise ValueError("numerical computation requests must require source references")
        return self


class NumericalComputationResult(BaseModel):
    result_id: str
    request_id: str
    computation_kind: NumericalComputationKind
    metrics: dict[str, float | int | str | bool | None]
    source: NumericalSourceReference
    descriptive_only: bool = True
    trade_signal: bool = False
    recommendation: bool = False
    decision_object_generated: bool = False
    safety_label: NumericalSafetyLabel = NumericalSafetyLabel.DESCRIPTIVE_ONLY
    status: str
    error: str | None = None
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("result_id", "request_id", "status", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "numerical computation result text fields")

    @field_validator("error")
    @classmethod
    def error_must_be_sanitized(cls, value: str | None) -> str | None:
        if value is None:
            return None
        sanitized = sanitize_analytics_notes([value])
        return sanitized[0] if sanitized else None

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def result_must_remain_descriptive(self) -> NumericalComputationResult:
        if not self.metrics and not _status_allows_empty_metrics(self.status):
            raise ValueError("successful numerical computation results require metrics")
        if self.trade_signal:
            raise ValueError("numerical computation results cannot be trade signals")
        if self.recommendation:
            raise ValueError("numerical computation results cannot be recommendations")
        if self.decision_object_generated:
            raise ValueError("numerical computation results cannot generate DecisionObjects")
        if not self.descriptive_only:
            raise ValueError("numerical computation results must remain descriptive-only")
        if self.safety_label == NumericalSafetyLabel.UNKNOWN:
            raise ValueError("numerical computation result safety label cannot be UNKNOWN")
        return self


def create_synthetic_source_reference(
    source_id: str = "synthetic-numerical-source",
    source_type: str = "synthetic_local_test",
    source_data_reference: str = "synthetic-local-test-only",
    provider_name: str | None = "local_sample",
    dataset_manifest_id: str | None = None,
) -> NumericalSourceReference:
    return NumericalSourceReference(
        source_id=source_id,
        source_type=source_type,
        source_data_reference=source_data_reference,
        provider_name=provider_name,
        dataset_manifest_id=dataset_manifest_id,
        notes=["Synthetic/local/test source reference for descriptive numerical contracts only."],
    )


def create_vector_contract(
    vector_id: str,
    name: str,
    values: list[float],
    source: NumericalSourceReference | None = None,
) -> NumericalVectorContract:
    return NumericalVectorContract(
        vector_id=vector_id,
        name=name,
        values=values,
        source=source or create_synthetic_source_reference(),
    )


def create_summary_request(
    request_id: str,
    input_ids: list[str],
    source: NumericalSourceReference | None = None,
) -> NumericalComputationRequest:
    return NumericalComputationRequest(
        request_id=request_id,
        computation_kind=NumericalComputationKind.SUMMARY,
        input_ids=input_ids,
        source=source or create_synthetic_source_reference(),
    )


def create_safe_result(
    result_id: str,
    request_id: str,
    computation_kind: NumericalComputationKind,
    metrics: dict[str, float | int | str | bool | None] | None = None,
    source: NumericalSourceReference | None = None,
    status: str = "ok",
    error: str | None = None,
) -> NumericalComputationResult:
    return NumericalComputationResult(
        result_id=result_id,
        request_id=request_id,
        computation_kind=computation_kind,
        metrics=metrics or {},
        source=source or create_synthetic_source_reference(),
        status=status,
        error=error,
    )
