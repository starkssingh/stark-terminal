from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_analytics.regime.contracts import default_regime_analytics_plan
from stark_terminal_analytics.regime.roadmap import default_regime_roadmap


class RegimeAnalyticsHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    dependency_stage: str
    real_data_allowed: bool
    classification_allowed: bool
    trade_signals_allowed: bool
    recommendations_allowed: bool
    decision_objects_allowed: bool
    execution_allowed: bool = False
    evidence_required: bool
    human_review_required: bool
    planned_label_count: int
    roadmap_item_count: int
    status: str
    error: str | None = None


def check_regime_analytics_health(settings: Settings | None = None) -> RegimeAnalyticsHealthStatus:
    resolved = settings or get_settings()
    plan = default_regime_analytics_plan()
    roadmap = default_regime_roadmap()
    unsafe_flags = (
        resolved.regime_analytics_allow_real_data
        or resolved.regime_analytics_allow_classification
        or resolved.regime_analytics_allow_trade_signals
        or resolved.regime_analytics_allow_recommendations
        or resolved.regime_analytics_allow_decision_objects
        or resolved.regime_analytics_allow_signal_labels
        or resolved.execution_apis_enabled
    )
    has_required_configuration = (
        bool(resolved.regime_analytics_schema_version.strip())
        and resolved.regime_analytics_dependency_stage == "planning_only"
        and resolved.regime_analytics_require_evidence
        and resolved.regime_analytics_require_human_review
        and bool(plan.planned_labels)
        and bool(roadmap)
    )
    status = "healthy" if resolved.regime_analytics_enabled and not unsafe_flags and has_required_configuration else "blocked"
    error = None if status == "healthy" else "regime analytics planning safety flags are not fail-closed"
    return RegimeAnalyticsHealthStatus(
        enabled=resolved.regime_analytics_enabled,
        schema_version=resolved.regime_analytics_schema_version,
        dependency_stage=resolved.regime_analytics_dependency_stage,
        real_data_allowed=resolved.regime_analytics_allow_real_data,
        classification_allowed=resolved.regime_analytics_allow_classification,
        trade_signals_allowed=resolved.regime_analytics_allow_trade_signals,
        recommendations_allowed=resolved.regime_analytics_allow_recommendations,
        decision_objects_allowed=resolved.regime_analytics_allow_decision_objects,
        execution_allowed=False,
        evidence_required=resolved.regime_analytics_require_evidence,
        human_review_required=resolved.regime_analytics_require_human_review,
        planned_label_count=len(plan.planned_labels),
        roadmap_item_count=len(roadmap),
        status=status,
        error=error,
    )
