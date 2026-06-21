from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_data_platform.quality.enums import (
    QualityGateDecision,
    ValidationRuleType,
    ValidationScope,
    ValidationSeverity,
    ValidationStatus,
)
from stark_terminal_data_platform.quality.health import check_data_quality_health

router = APIRouter()


@router.get("/data-quality/health")
def data_quality_health() -> dict[str, Any]:
    status = check_data_quality_health()
    return {
        "service": "stark-terminal-data-quality",
        **status.model_dump(),
    }


@router.get("/data-quality/contracts")
def data_quality_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-data-quality",
        "schema_version": settings.data_quality_schema_version,
        "validation_scopes": [item.value for item in ValidationScope],
        "validation_statuses": [item.value for item in ValidationStatus],
        "validation_severities": [item.value for item in ValidationSeverity],
        "quality_gate_decisions": [item.value for item in QualityGateDecision],
        "rule_types": [item.value for item in ValidationRuleType],
    }
