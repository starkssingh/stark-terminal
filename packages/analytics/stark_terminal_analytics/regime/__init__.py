"""Regime Analytics Planning and Guardrails.

Prompt 33 exposes planning contracts, evidence requirements, dependency staging,
readiness templates, and safety helpers only. It does not assign regime labels,
fit models, generate signals, generate recommendations, generate DecisionObjects,
or expose execution APIs.
"""

from stark_terminal_analytics.regime.contracts import (
    RegimeAnalyticsPlan,
    RegimeEvidenceKind,
    RegimeLabelContract,
    RegimeLabelPlaceholder,
    RegimePlanningStage,
    RegimeSafetyLabel,
    default_regime_analytics_plan,
    default_regime_label_contracts,
)
from stark_terminal_analytics.regime.dependencies import (
    RegimeDependencyPlan,
    assert_no_blocked_regime_dependencies_added,
    default_regime_dependency_plan,
    regime_dependency_allowed_now,
)
from stark_terminal_analytics.regime.evidence import (
    RegimeEvidenceChecklist,
    RegimeEvidenceRequirement,
    build_regime_evidence_checklist,
    default_regime_evidence_requirements,
    evaluate_evidence_readiness,
)
from stark_terminal_analytics.regime.health import (
    RegimeAnalyticsHealthStatus,
    check_regime_analytics_health,
)
from stark_terminal_analytics.regime.readiness import (
    RegimeReadinessReport,
    build_regime_readiness_report,
    regime_ready_for_classification,
    regime_ready_for_feature_preparation,
    regime_ready_for_production,
)
from stark_terminal_analytics.regime.roadmap import (
    RegimeRoadmapItem,
    default_regime_roadmap,
)
from stark_terminal_analytics.regime.safety import (
    RegimeSafetyPolicy,
    RegimeSafetyResult,
    default_regime_safety_policy,
    evaluate_regime_plan_safety,
    reject_regime_classification_output,
    reject_regime_signal_or_decision,
)

__all__ = [
    "RegimeAnalyticsHealthStatus",
    "RegimeAnalyticsPlan",
    "RegimeDependencyPlan",
    "RegimeEvidenceChecklist",
    "RegimeEvidenceKind",
    "RegimeEvidenceRequirement",
    "RegimeLabelContract",
    "RegimeLabelPlaceholder",
    "RegimePlanningStage",
    "RegimeReadinessReport",
    "RegimeRoadmapItem",
    "RegimeSafetyLabel",
    "RegimeSafetyPolicy",
    "RegimeSafetyResult",
    "assert_no_blocked_regime_dependencies_added",
    "build_regime_evidence_checklist",
    "build_regime_readiness_report",
    "check_regime_analytics_health",
    "default_regime_analytics_plan",
    "default_regime_dependency_plan",
    "default_regime_evidence_requirements",
    "default_regime_label_contracts",
    "default_regime_roadmap",
    "default_regime_safety_policy",
    "evaluate_evidence_readiness",
    "evaluate_regime_plan_safety",
    "regime_dependency_allowed_now",
    "regime_ready_for_classification",
    "regime_ready_for_feature_preparation",
    "regime_ready_for_production",
    "reject_regime_classification_output",
    "reject_regime_signal_or_decision",
]
