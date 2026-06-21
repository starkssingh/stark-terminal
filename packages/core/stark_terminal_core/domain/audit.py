from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator

from stark_terminal_core.domain.identifiers import AuditId


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AuditMetadata(BaseModel):
    audit_id: AuditId
    created_at: datetime = Field(default_factory=utc_now)
    source: str
    source_data_reference: str | None = None
    model_or_rule_version: str | None = None
    notes: list[str] = Field(default_factory=list)

    @field_validator("source", mode="before")
    @classmethod
    def source_must_be_non_empty(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("source must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError("source cannot be empty")
        return normalized

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
