from __future__ import annotations

from pydantic import BaseModel, field_validator

from stark_terminal_data_platform.quality.enums import ValidationScope, ValidationSeverity


SECRET_TEXT_PARTS = (
    "password",
    "secret",
    "token",
    "credential",
    "api_key",
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "kafka_bootstrap_servers",
    "broker_token",
    "broker_secret",
)
FORBIDDEN_EXECUTION_PARTS = (
    "order placement",
    "broker execution",
    "live trading",
    "real-money routing",
)
MAX_PREVIEW_LENGTH = 160


def text_has_sensitive_content(value: str | None) -> bool:
    if value is None:
        return False
    normalized = value.lower()
    if "://" in normalized:
        return True
    return any(part in normalized for part in SECRET_TEXT_PARTS)


def _sanitize_text(value: str, *, allow_execution_safety_text: bool = True) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError("validation text cannot be empty")
    if text_has_sensitive_content(normalized):
        return "[redacted]"
    if not allow_execution_safety_text:
        lowered = normalized.lower()
        if any(part in lowered for part in FORBIDDEN_EXECUTION_PARTS):
            return "[redacted]"
    return normalized


def sanitize_value_preview(value: str | None) -> str | None:
    if value is None:
        return None
    sanitized = _sanitize_text(str(value), allow_execution_safety_text=False)
    if len(sanitized) > MAX_PREVIEW_LENGTH:
        return f"{sanitized[: MAX_PREVIEW_LENGTH - 3]}..."
    return sanitized


class ValidationIssue(BaseModel):
    code: str
    severity: ValidationSeverity
    message: str
    field: str | None = None
    scope: ValidationScope = ValidationScope.UNKNOWN
    value_preview: str | None = None
    remediation: str | None = None

    @field_validator("code", "message", "field", "remediation")
    @classmethod
    def text_fields_must_be_safe(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _sanitize_text(value)

    @field_validator("value_preview")
    @classmethod
    def value_preview_must_be_sanitized(cls, value: str | None) -> str | None:
        return sanitize_value_preview(value)
