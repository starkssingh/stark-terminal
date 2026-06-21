from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.features.registry import StarkFeatureRegistry


class FeatureRegistryHealthStatus(BaseModel):
    enabled: bool
    backend: str
    feature_store_mode: str
    external_backend_allowed: bool
    registered_features: int
    registered_feature_sets: int
    quality_reports: int
    lineage_records: int
    lineage_required: bool
    quality_report_required: bool
    status: str
    error: str | None = None


def check_feature_registry_health(
    settings: Settings | None = None,
    registry: StarkFeatureRegistry | None = None,
) -> FeatureRegistryHealthStatus:
    resolved_settings = settings or get_settings()
    resolved_registry = registry or StarkFeatureRegistry()
    try:
        if resolved_settings.feature_registry_allow_external_backend:
            status = "caution_external_backend_allowed"
        elif not resolved_settings.feature_registry_enabled:
            status = "disabled"
        else:
            status = "healthy"
        return FeatureRegistryHealthStatus(
            enabled=resolved_settings.feature_registry_enabled,
            backend=resolved_settings.feature_registry_backend,
            feature_store_mode=resolved_settings.feature_store_mode,
            external_backend_allowed=resolved_settings.feature_registry_allow_external_backend,
            registered_features=len(resolved_registry.list_features()),
            registered_feature_sets=len(resolved_registry.list_feature_sets()),
            quality_reports=len(resolved_registry.list_quality_reports()),
            lineage_records=len(resolved_registry.list_lineage()),
            lineage_required=resolved_settings.feature_registry_require_lineage,
            quality_report_required=resolved_settings.feature_registry_require_quality_report,
            status=status,
        )
    except Exception as exc:  # pragma: no cover - defensive health boundary
        return FeatureRegistryHealthStatus(
            enabled=resolved_settings.feature_registry_enabled,
            backend=resolved_settings.feature_registry_backend,
            feature_store_mode=resolved_settings.feature_store_mode,
            external_backend_allowed=resolved_settings.feature_registry_allow_external_backend,
            registered_features=0,
            registered_feature_sets=0,
            quality_reports=0,
            lineage_records=0,
            lineage_required=resolved_settings.feature_registry_require_lineage,
            quality_report_required=resolved_settings.feature_registry_require_quality_report,
            status="unhealthy",
            error=exc.__class__.__name__,
        )

