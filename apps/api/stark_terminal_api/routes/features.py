from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.domain.enums import (
    FeatureEntityType,
    FeatureFrequency,
    FeatureQualityStatus,
    FeatureStatus,
    FeatureValueType,
)
from stark_terminal_data_platform.features.health import check_feature_registry_health

router = APIRouter()


@router.get("/features/health")
def feature_registry_health() -> dict[str, Any]:
    status = check_feature_registry_health()
    return {
        "service": "stark-terminal-feature-registry",
        **status.model_dump(),
    }


@router.get("/features/contracts")
def feature_registry_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-feature-registry",
        "schema_version": settings.feature_registry_schema_version,
        "feature_store_mode": settings.feature_store_mode,
        "feature_value_types": [item.value for item in FeatureValueType],
        "feature_entity_types": [item.value for item in FeatureEntityType],
        "feature_frequencies": [item.value for item in FeatureFrequency],
        "feature_statuses": [item.value for item in FeatureStatus],
        "quality_statuses": [item.value for item in FeatureQualityStatus],
    }
