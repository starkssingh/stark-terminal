from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.quality.registry import (
    ValidationRegistry,
    create_default_validation_registry,
)


class DataQualityHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    validator_count: int
    registered_scopes: list[str]
    external_validation_enabled: bool
    require_source_reference: bool
    require_timezone_aware_timestamps: bool
    status: str
    error: str | None = None


def check_data_quality_health(
    settings: Settings | None = None,
    registry: ValidationRegistry | None = None,
) -> DataQualityHealthStatus:
    resolved = settings or get_settings()
    try:
        resolved_registry = registry or create_default_validation_registry(settings=resolved)
        scopes = sorted(resolved_registry.list_scopes())
        status = "healthy"
        error = None
        if not resolved.data_quality_enabled:
            status = "disabled"
        elif resolved.data_quality_external_validation_enabled:
            status = "caution_external_validation_enabled"
        return DataQualityHealthStatus(
            enabled=resolved.data_quality_enabled,
            schema_version=resolved.data_quality_schema_version,
            validator_count=len(scopes),
            registered_scopes=scopes,
            external_validation_enabled=resolved.data_quality_external_validation_enabled,
            require_source_reference=resolved.data_quality_require_source_reference,
            require_timezone_aware_timestamps=resolved.data_quality_require_timezone_aware_timestamps,
            status=status,
            error=error,
        )
    except Exception as exc:
        return DataQualityHealthStatus(
            enabled=resolved.data_quality_enabled,
            schema_version=resolved.data_quality_schema_version,
            validator_count=0,
            registered_scopes=[],
            external_validation_enabled=resolved.data_quality_external_validation_enabled,
            require_source_reference=resolved.data_quality_require_source_reference,
            require_timezone_aware_timestamps=resolved.data_quality_require_timezone_aware_timestamps,
            status="unhealthy",
            error=str(exc) or "data quality health check failed",
        )
