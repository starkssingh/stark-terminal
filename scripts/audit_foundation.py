from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import tomllib


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "docs/MILESTONE_A_B_AUDIT.md",
    "docs/REPO_INVENTORY.md",
    "docs/API_SURFACE_INVENTORY.md",
    "docs/SAFETY_AUDIT.md",
    "docs/NEXT_PHASE_PLAN.md",
    "docs/KAFKA_REDPANDA_FOUNDATION.md",
    "docs/EVENT_BACKBONE_TOPIC_POLICY.md",
    "docs/DURABLE_EVENT_ENVELOPE_SPEC.md",
    "docs/DATA_QUALITY_FRAMEWORK.md",
    "docs/VALIDATION_RULE_SPEC.md",
    "docs/QUALITY_GATE_POLICY.md",
    "docs/DATA_QUALITY_REPORT_SPEC.md",
    "docs/SYNTHETIC_MARKET_DATA_FIXTURES.md",
    "docs/OHLCV_FIXTURE_CONTRACTS.md",
    "docs/SAMPLE_DATA_POLICY.md",
    "docs/INSTRUMENT_PERSISTENCE_FOUNDATION.md",
    "docs/INSTRUMENT_REPOSITORY_POLICY.md",
    "docs/MARKET_DATA_BATCH_PERSISTENCE.md",
    "docs/BATCH_METADATA_POLICY.md",
    "docs/DATA_FOUNDATION_AUDIT.md",
    "docs/DATA_PERSISTENCE_BOUNDARY.md",
    "docs/SYNTHETIC_DATA_SAFETY_AUDIT.md",
    "docs/DATA_FOUNDATION_NEXT_PHASE.md",
    "docs/SYNTHETIC_OHLCV_STORAGE_FOUNDATION.md",
    "docs/TIMESCALE_SYNTHETIC_STORAGE_POLICY.md",
    "docs/SYNTHETIC_OHLCV_RESEARCH_LAKE_EXPORT.md",
    "docs/OHLCV_EXPORT_MANIFEST_POLICY.md",
    "docs/PROVIDER_ADAPTER_IMPLEMENTATION_PLAN.md",
    "docs/PROVIDER_GUARDRAIL_POLICY.md",
    "docs/PROVIDER_APPROVAL_WORKFLOW.md",
    "docs/PROVIDER_COMPLIANCE_CHECKLIST.md",
    "docs/LOCAL_SAMPLE_PROVIDER_ADAPTER.md",
    "docs/LOCAL_SAMPLE_PROVIDER_POLICY.md",
    "docs/DATA_FOUNDATION_MILESTONE_AUDIT.md",
    "docs/SYNTHETIC_STORAGE_EXPORT_AUDIT.md",
    "docs/PROVIDER_GUARDRAIL_AUDIT.md",
    "docs/LOCAL_SAMPLE_PROVIDER_AUDIT.md",
    "docs/DATA_FOUNDATION_MILESTONE_NEXT_PHASE.md",
    "docs/REAL_PROVIDER_READINESS_CHECKLIST.md",
    "docs/PROVIDER_CANDIDATE_SELECTION_POLICY.md",
    "docs/PROVIDER_RISK_SCORING_POLICY.md",
    "docs/PROVIDER_CAPABILITY_GAP_ANALYSIS.md",
    "docs/LOCAL_FILE_PROVIDER_ADAPTER.md",
    "docs/LOCAL_FILE_PROVIDER_POLICY.md",
    "docs/LOCAL_FILE_PATH_SAFETY.md",
    "docs/PROVIDER_ADAPTER_MILESTONE_AUDIT.md",
    "docs/PROVIDER_BOUNDARY_AUDIT.md",
    "docs/PROVIDER_NO_EXTERNAL_CALLS_AUDIT.md",
    "docs/PROVIDER_NEXT_PHASE_PLAN.md",
    "docs/QUANT_ANALYTICS_FOUNDATION_PLAN.md",
    "docs/TIME_SERIES_ANALYTICS_BOUNDARY.md",
    "docs/ANALYTICS_SAFETY_POLICY.md",
    "docs/ANALYTICS_DEPENDENCY_STAGING.md",
    "docs/ANALYTICS_ROADMAP.md",
    "docs/NUMERICAL_ANALYTICS_CORE_CONTRACTS.md",
    "docs/NUMERICAL_ANALYTICS_VALIDATION_POLICY.md",
    "docs/NUMERICAL_ANALYTICS_DEPENDENCY_GATE.md",
    "docs/NUMERICAL_ANALYTICS_SAFETY_BOUNDARY.md",
    "docs/RETURNS_ANALYTICS_V0.md",
    "docs/ROLLING_WINDOW_ANALYTICS_V0.md",
    "docs/RETURNS_ROLLING_VALIDATION_POLICY.md",
    "docs/RETURNS_ROLLING_SAFETY_BOUNDARY.md",
    "docs/VOLATILITY_ANALYTICS_V0.md",
    "docs/DRAWDOWN_ANALYTICS_V0.md",
    "docs/VOLATILITY_DRAWDOWN_VALIDATION_POLICY.md",
    "docs/VOLATILITY_DRAWDOWN_SAFETY_BOUNDARY.md",
    "docs/ANALYTICS_MILESTONE_AUDIT.md",
    "docs/ANALYTICS_BOUNDARY_AUDIT.md",
    "docs/ANALYTICS_NO_SIGNAL_AUDIT.md",
    "docs/ANALYTICS_DEPENDENCY_AUDIT.md",
    "docs/ANALYTICS_NEXT_PHASE_PLAN.md",
    "docs/CORRELATION_ANALYTICS_V0.md",
    "docs/BETA_ANALYTICS_V0.md",
    "docs/CORRELATION_BETA_VALIDATION_POLICY.md",
    "docs/CORRELATION_BETA_SAFETY_BOUNDARY.md",
    "docs/TIME_SERIES_DIAGNOSTICS_FOUNDATION.md",
    "docs/TIMESTAMP_DIAGNOSTICS_POLICY.md",
    "docs/TIME_SERIES_GAP_DIAGNOSTICS.md",
    "docs/TIME_SERIES_DIAGNOSTICS_SAFETY_BOUNDARY.md",
    "docs/STATIONARITY_REGIME_DIAGNOSTICS_DEFERRED.md",
    "docs/REGIME_ANALYTICS_PLANNING.md",
    "docs/REGIME_LABEL_CONTRACTS.md",
    "docs/REGIME_EVIDENCE_REQUIREMENTS.md",
    "docs/REGIME_ANALYTICS_SAFETY_POLICY.md",
    "docs/REGIME_DEPENDENCY_STAGING.md",
    "docs/REGIME_ANALYTICS_ROADMAP.md",
    "docs/REGIME_FEATURE_PREPARATION_CONTRACTS.md",
    "docs/REGIME_FEATURE_GROUPS.md",
    "docs/REGIME_FEATURE_PROVENANCE_POLICY.md",
    "docs/REGIME_FEATURE_EVIDENCE_MAPPING.md",
    "docs/REGIME_FEATURE_SAFETY_POLICY.md",
    "docs/REGIME_FEATURE_DEPENDENCY_STAGING.md",
    "docs/ANALYTICS_REGIME_MILESTONE_AUDIT.md",
    "docs/REGIME_BOUNDARY_AUDIT.md",
    "docs/REGIME_NO_CLASSIFICATION_AUDIT.md",
    "docs/REGIME_FEATURE_PREPARATION_AUDIT.md",
    "docs/ANALYTICS_REGIME_NO_SIGNAL_AUDIT.md",
    "docs/ANALYTICS_REGIME_DEPENDENCY_AUDIT.md",
    "docs/DECISION_DESK_READINESS_PLAN.md",
    "docs/RETAIL_DECISION_DESK_PLANNING.md",
    "docs/DECISION_DESK_ACTION_PLACEHOLDERS.md",
    "docs/DECISION_DESK_EVIDENCE_REQUIREMENTS.md",
    "docs/DECISION_DESK_HUMAN_REVIEW_GUARDRAILS.md",
    "docs/DECISION_DESK_SAFETY_POLICY.md",
    "docs/DECISION_DESK_DISPLAY_BOUNDARY.md",
    "docs/DECISIONOBJECT_EVIDENCE_BUNDLE_CONTRACTS.md",
    "docs/DECISION_EVIDENCE_ITEM_SCHEMA.md",
    "docs/DECISION_EVIDENCE_PROVENANCE_POLICY.md",
    "docs/DECISION_EVIDENCE_VALIDATION_CHECKLIST.md",
    "docs/DECISION_EVIDENCE_HUMAN_REVIEW_ATTACHMENTS.md",
    "docs/DECISION_EVIDENCE_SAFETY_POLICY.md",
    "docs/DECISION_SAFETY_GUARDRAILS.md",
    "docs/DECISION_HUMAN_REVIEW_GATES.md",
    "docs/DECISION_APPROVAL_PLACEHOLDERS.md",
    "docs/DECISION_OVERRIDE_PROHIBITION.md",
    "docs/DECISION_BLOCKED_OUTPUT_POLICY.md",
    "docs/DECISION_SAFETY_READINESS_POLICY.md",
    "docs/DECISION_DESK_API_CONTRACT_SKELETON.md",
    "docs/DECISION_DESK_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/DECISION_DESK_UNAVAILABLE_RESPONSES.md",
    "docs/DECISION_DESK_API_SAFETY_BOUNDARY.md",
    "docs/DECISION_DESK_API_NO_RECOMMENDATION_POLICY.md",
    "docs/DECISION_DESK_MILESTONE_AUDIT.md",
    "docs/DECISION_DESK_BOUNDARY_AUDIT.md",
    "docs/DECISION_EVIDENCE_BOUNDARY_AUDIT.md",
    "docs/DECISION_SAFETY_BOUNDARY_AUDIT.md",
    "docs/DECISION_API_SKELETON_AUDIT.md",
    "docs/DECISION_NO_RECOMMENDATION_AUDIT.md",
    "docs/DECISION_DESK_NEXT_PHASE_PLAN.md",
    "docs/DECISION_DESK_READINESS_API_SKELETON.md",
    "docs/DECISION_READINESS_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/DECISION_READINESS_REFERENCE_PLACEHOLDERS.md",
    "docs/DECISION_READINESS_UNAVAILABLE_RESPONSES.md",
    "docs/DECISION_READINESS_API_SAFETY_BOUNDARY.md",
    "docs/DECISION_READINESS_NO_RECOMMENDATION_POLICY.md",
    "docs/DECISION_DESK_DISPLAY_CONTRACT_SKELETON.md",
    "docs/DECISION_DISPLAY_CARD_PLACEHOLDERS.md",
    "docs/DECISION_DISPLAY_SECTION_PLACEHOLDERS.md",
    "docs/DECISION_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/DECISION_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/DECISION_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    "docs/DECISION_EVIDENCE_VALIDATION_V0.md",
    "docs/DECISION_EVIDENCE_VALIDATION_RESULT_SCHEMA.md",
    "docs/DECISION_EVIDENCE_VALIDATION_FAILURE_REASONS.md",
    "docs/DECISION_EVIDENCE_VALIDATION_SAFETY_BOUNDARY.md",
    "docs/DECISION_EVIDENCE_VALIDATION_API_SKELETON.md",
    "docs/DECISION_EVIDENCE_VALIDATION_NO_RECOMMENDATION_POLICY.md",
    "docs/DECISION_HUMAN_REVIEW_WORKFLOW_SKELETON.md",
    "docs/DECISION_REVIEW_TASK_PLACEHOLDERS.md",
    "docs/DECISION_REVIEW_ROLE_PLACEHOLDERS.md",
    "docs/DECISION_REVIEW_QUEUE_PLACEHOLDERS.md",
    "docs/DECISION_REVIEW_UNAVAILABLE_RESPONSES.md",
    "docs/DECISION_REVIEW_NO_APPROVAL_POLICY.md",
    "docs/DECISION_DESK_MILESTONE_AUDIT_2.md",
    "docs/DECISION_READINESS_API_BOUNDARY_AUDIT.md",
    "docs/DECISION_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/DECISION_EVIDENCE_VALIDATION_BOUNDARY_AUDIT.md",
    "docs/DECISION_HUMAN_REVIEW_WORKFLOW_BOUNDARY_AUDIT.md",
    "docs/DECISION_NO_APPROVAL_WORKFLOW_AUDIT.md",
    "docs/DECISION_DESK_NEXT_PHASE_PLAN_2.md",
    "docs/DECISION_DESK_SYSTEM_BOUNDARY_HARDENING.md",
    "docs/DECISION_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "docs/DECISION_ENDPOINT_BOUNDARY_POLICY.md",
    "docs/DECISION_MODULE_BOUNDARY_POLICY.md",
    "docs/DECISION_CROSS_MODULE_INVARIANTS.md",
    "docs/DECISION_BOUNDARY_HARDENING_NO_EXECUTION_POLICY.md",
    "docs/DECISION_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    "docs/DECISION_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
    "docs/DECISION_API_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/DECISION_BOUNDARY_INTEGRATION_AUDIT.md",
    "docs/DECISION_INTEGRATION_NO_RECOMMENDATION_AUDIT.md",
    "docs/RETAIL_DASHBOARD_READINESS_PLAN.md",
    "docs/RETAIL_DASHBOARD_PLANNING.md",
    "docs/RETAIL_DASHBOARD_GUARDRAILS.md",
    "docs/RETAIL_DASHBOARD_SECTION_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_CARD_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_FORBIDDEN_INTERACTIONS.md",
    "docs/RETAIL_DASHBOARD_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_DASHBOARD_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_DASHBOARD_API_CONTRACT_SKELETON.md",
    "docs/RETAIL_DASHBOARD_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_API_REFERENCE_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_API_UNAVAILABLE_RESPONSES.md",
    "docs/RETAIL_DASHBOARD_API_SAFETY_BOUNDARY.md",
    "docs/RETAIL_DASHBOARD_API_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_DASHBOARD_API_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_CONTRACT_SKELETON.md",
    "docs/RETAIL_DASHBOARD_LAYOUT_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_WIDGET_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_VISUAL_SECTION_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_DASHBOARD_SAFETY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_API_BOUNDARY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_DASHBOARD_NO_RECOMMENDATION_AUDIT.md",
    "docs/RETAIL_DASHBOARD_NO_EXECUTION_AUDIT.md",
    "docs/RETAIL_DASHBOARD_MILESTONE_READINESS.md",
    "docs/RETAIL_DASHBOARD_MILESTONE_AUDIT.md",
    "docs/RETAIL_DASHBOARD_PLANNING_MILESTONE_AUDIT.md",
    "docs/RETAIL_DASHBOARD_API_MILESTONE_AUDIT.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_MILESTONE_AUDIT.md",
    "docs/RETAIL_DASHBOARD_SAFETY_MILESTONE_AUDIT.md",
    "docs/RETAIL_DASHBOARD_PHASE_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_DASHBOARD_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RETAIL_DASHBOARD_NEXT_PHASE_PLAN.md",
    "docs/RETAIL_DASHBOARD_SYSTEM_BOUNDARY_HARDENING.md",
    "docs/RETAIL_DASHBOARD_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "docs/RETAIL_DASHBOARD_ENDPOINT_BOUNDARY_POLICY.md",
    "docs/RETAIL_DASHBOARD_MODULE_BOUNDARY_POLICY.md",
    "docs/RETAIL_DASHBOARD_CROSS_MODULE_INVARIANTS.md",
    "docs/RETAIL_DASHBOARD_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
    "docs/RETAIL_DASHBOARD_BOUNDARY_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_DASHBOARD_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    "docs/RETAIL_DASHBOARD_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_API_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_BOUNDARY_INTEGRATION_AUDIT.md",
    "docs/RETAIL_DASHBOARD_INTEGRATION_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_DASHBOARD_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_READINESS_PLAN.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PLANNING.md",
    "docs/RETAIL_TRADER_EXPERIENCE_GUARDRAILS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PERSONA_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_JOURNEY_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_SECTION_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_CARD_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_FORBIDDEN_INTERACTIONS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_CONTRACT_SKELETON.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_REFERENCE_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_UNAVAILABLE_RESPONSES.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_SAFETY_BOUNDARY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_NO_SUITABILITY_PROFILING_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_CONTRACT_SKELETON.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_PERSONA_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_JOURNEY_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_SECTION_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_WIDGET_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_SUITABILITY_PROFILING_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_SAFETY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_BOUNDARY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_SUITABILITY_PROFILING_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_READINESS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PLANNING_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_SAFETY_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_SUITABILITY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NEXT_PHASE_PLAN.md",
    "docs/RETAIL_TRADER_EXPERIENCE_SYSTEM_BOUNDARY_HARDENING.md",
    "docs/RETAIL_TRADER_EXPERIENCE_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_ENDPOINT_BOUNDARY_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_MODULE_BOUNDARY_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_CROSS_MODULE_INVARIANTS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_SUITABILITY_PROFILING_POLICY.md",
    "docs/NORTH_STAR.md",
    "docs/PROMPT_LOG.md",
    "docs/TECH_STACK.md",
    "docs/INFRASTRUCTURE_STACK.md",
    "docs/ANALYTICS_STACK.md",
    "docs/SAFETY_RULES.md",
    "docs/DATA_POLICY.md",
    "docs/CONFIGURATION.md",
]

REQUIRED_PACKAGE_DIRS = [
    "apps/api/stark_terminal_api",
    "apps/api/stark_terminal_api/routes",
    "apps/desktop/stark_terminal_desktop",
    "packages/core/stark_terminal_core",
    "packages/core/stark_terminal_core/config",
    "packages/core/stark_terminal_core/domain",
    "packages/core/stark_terminal_core/decision_desk",
    "packages/core/stark_terminal_core/decision_evidence",
    "packages/core/stark_terminal_core/decision_safety",
    "packages/core/stark_terminal_core/decision_api",
    "packages/core/stark_terminal_core/decision_readiness_api",
    "packages/core/stark_terminal_core/decision_display",
    "packages/core/stark_terminal_core/decision_evidence_validation",
    "packages/core/stark_terminal_core/decision_human_review",
    "packages/core/stark_terminal_core/decision_boundary",
    "packages/core/stark_terminal_core/retail_dashboard",
    "packages/core/stark_terminal_core/retail_dashboard_api",
    "packages/core/stark_terminal_core/retail_dashboard_display",
    "packages/core/stark_terminal_core/retail_dashboard_boundary",
    "packages/core/stark_terminal_core/retail_trader_experience",
    "packages/core/stark_terminal_core/retail_trader_experience_api",
    "packages/core/stark_terminal_core/retail_trader_experience_display",
    "packages/core/stark_terminal_core/retail_trader_experience_boundary",
    "packages/core/stark_terminal_core/research_artifact_registry",
    "packages/core/stark_terminal_core/research_artifact_registry_api",
    "packages/core/stark_terminal_core/research_artifact_registry_display",
    "packages/core/stark_terminal_core/research_artifact_registry_boundary",
    "packages/core/stark_terminal_core/research_artifact_index",
    "packages/core/stark_terminal_core/research_artifact_index_api",
    "packages/core/stark_terminal_core/research_artifact_index_display",
    "packages/core/stark_terminal_core/research_artifact_index_boundary",
    "packages/core/stark_terminal_core/serialization",
    "packages/data_platform/stark_terminal_data_platform",
    "packages/data_platform/stark_terminal_data_platform/db",
    "packages/data_platform/stark_terminal_data_platform/timeseries",
    "packages/data_platform/stark_terminal_data_platform/lake",
    "packages/data_platform/stark_terminal_data_platform/cache",
    "packages/data_platform/stark_terminal_data_platform/streams",
    "packages/data_platform/stark_terminal_data_platform/event_backbone",
    "packages/data_platform/stark_terminal_data_platform/quality",
    "packages/data_platform/stark_terminal_data_platform/fixtures",
    "packages/data_platform/stark_terminal_data_platform/repositories",
    "packages/data_platform/stark_terminal_data_platform/services",
    "packages/data_platform/stark_terminal_data_platform/exports",
    "packages/data_platform/stark_terminal_data_platform/workers",
    "packages/data_platform/stark_terminal_data_platform/instruments",
    "packages/data_platform/stark_terminal_data_platform/providers",
    "packages/data_platform/stark_terminal_data_platform/warehouse",
    "packages/data_platform/stark_terminal_data_platform/features",
    "packages/analytics/stark_terminal_analytics",
    "packages/analytics/stark_terminal_analytics/foundation",
    "packages/analytics/stark_terminal_analytics/numerical",
    "packages/analytics/stark_terminal_analytics/returns",
    "packages/analytics/stark_terminal_analytics/rolling",
    "packages/analytics/stark_terminal_analytics/volatility",
    "packages/analytics/stark_terminal_analytics/drawdown",
    "packages/analytics/stark_terminal_analytics/correlation",
    "packages/analytics/stark_terminal_analytics/beta",
    "packages/analytics/stark_terminal_analytics/diagnostics",
    "packages/analytics/stark_terminal_analytics/regime",
    "packages/analytics/stark_terminal_analytics/regime_features",
    "packages/research/stark_terminal_research",
]

REQUIRED_ROUTE_FILES = [
    "apps/api/stark_terminal_api/routes/health.py",
    "apps/api/stark_terminal_api/routes/config.py",
    "apps/api/stark_terminal_api/routes/database.py",
    "apps/api/stark_terminal_api/routes/timeseries.py",
    "apps/api/stark_terminal_api/routes/research_lake.py",
    "apps/api/stark_terminal_api/routes/cache.py",
    "apps/api/stark_terminal_api/routes/streams.py",
    "apps/api/stark_terminal_api/routes/event_backbone.py",
    "apps/api/stark_terminal_api/routes/data_quality.py",
    "apps/api/stark_terminal_api/routes/fixtures.py",
    "apps/api/stark_terminal_api/routes/instrument_metadata.py",
    "apps/api/stark_terminal_api/routes/market_data_batches.py",
    "apps/api/stark_terminal_api/routes/synthetic_ohlcv_storage.py",
    "apps/api/stark_terminal_api/routes/synthetic_ohlcv_exports.py",
    "apps/api/stark_terminal_api/routes/provider_guardrails.py",
    "apps/api/stark_terminal_api/routes/provider_readiness.py",
    "apps/api/stark_terminal_api/routes/local_sample_provider.py",
    "apps/api/stark_terminal_api/routes/local_file_provider.py",
    "apps/api/stark_terminal_api/routes/analytics_foundation.py",
    "apps/api/stark_terminal_api/routes/numerical_analytics.py",
    "apps/api/stark_terminal_api/routes/returns_analytics.py",
    "apps/api/stark_terminal_api/routes/risk_analytics.py",
    "apps/api/stark_terminal_api/routes/relationship_analytics.py",
    "apps/api/stark_terminal_api/routes/time_series_diagnostics.py",
    "apps/api/stark_terminal_api/routes/regime_analytics.py",
    "apps/api/stark_terminal_api/routes/regime_features.py",
    "apps/api/stark_terminal_api/routes/decision_desk.py",
    "apps/api/stark_terminal_api/routes/decision_evidence.py",
    "apps/api/stark_terminal_api/routes/decision_safety.py",
    "apps/api/stark_terminal_api/routes/decision_desk_api.py",
    "apps/api/stark_terminal_api/routes/decision_readiness_api.py",
    "apps/api/stark_terminal_api/routes/decision_display.py",
    "apps/api/stark_terminal_api/routes/decision_evidence_validation.py",
    "apps/api/stark_terminal_api/routes/decision_human_review.py",
    "apps/api/stark_terminal_api/routes/decision_boundary.py",
    "apps/api/stark_terminal_api/routes/retail_dashboard.py",
    "apps/api/stark_terminal_api/routes/retail_dashboard_api.py",
    "apps/api/stark_terminal_api/routes/retail_dashboard_display.py",
    "apps/api/stark_terminal_api/routes/retail_dashboard_boundary.py",
    "apps/api/stark_terminal_api/routes/retail_trader_experience.py",
    "apps/api/stark_terminal_api/routes/retail_trader_experience_api.py",
    "apps/api/stark_terminal_api/routes/retail_trader_experience_display.py",
    "apps/api/stark_terminal_api/routes/retail_trader_experience_boundary.py",
    "apps/api/stark_terminal_api/routes/strategy_research_workspace.py",
    "apps/api/stark_terminal_api/routes/strategy_research_workspace_api.py",
    "apps/api/stark_terminal_api/routes/strategy_research_workspace_display.py",
    "apps/api/stark_terminal_api/routes/research_artifact_registry.py",
    "apps/api/stark_terminal_api/routes/research_artifact_registry_api.py",
    "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py",
    "apps/api/stark_terminal_api/routes/research_artifact_registry_boundary.py",
    "apps/api/stark_terminal_api/routes/research_artifact_index.py",
    "apps/api/stark_terminal_api/routes/research_artifact_index_api.py",
    "apps/api/stark_terminal_api/routes/research_artifact_index_display.py",
    "apps/api/stark_terminal_api/routes/research_artifact_index_boundary.py",
    "apps/api/stark_terminal_api/routes/workers.py",
    "apps/api/stark_terminal_api/routes/instruments.py",
    "apps/api/stark_terminal_api/routes/warehouse.py",
    "apps/api/stark_terminal_api/routes/features.py",
]

FORBIDDEN_ROUTE_TERMS = (
    "execution",
    "execute",
    "order",
    "broker",
    "live_trading",
    "live-trading",
    "real_money",
    "real-money",
)

FORBIDDEN_DATA_FILE_TERMS = (
    "execution",
    "execute",
    "order",
    "broker",
    "scrape",
    "scraper",
    "real_ingestion",
    "live_provider",
    "live_data",
)

REQUIRED_DATA_FOUNDATION_FILES = [
    "packages/data_platform/stark_terminal_data_platform/fixtures/manifests.py",
    "packages/data_platform/stark_terminal_data_platform/fixtures/synthetic_ohlcv.py",
    "packages/data_platform/stark_terminal_data_platform/fixtures/catalog.py",
    "packages/data_platform/stark_terminal_data_platform/fixtures/validation.py",
    "packages/data_platform/stark_terminal_data_platform/fixtures/parquet.py",
    "packages/data_platform/stark_terminal_data_platform/repositories/instruments.py",
    "packages/data_platform/stark_terminal_data_platform/services/instruments.py",
    "packages/core/stark_terminal_core/domain/market_data_batch.py",
    "packages/data_platform/stark_terminal_data_platform/db/models/market_data_batch.py",
    "packages/data_platform/stark_terminal_data_platform/repositories/market_data_batches.py",
    "packages/data_platform/stark_terminal_data_platform/services/market_data_batches.py",
    "packages/data_platform/stark_terminal_data_platform/repositories/ohlcv_bars.py",
    "packages/data_platform/stark_terminal_data_platform/services/synthetic_ohlcv_storage.py",
    "packages/data_platform/stark_terminal_data_platform/exports/synthetic_ohlcv.py",
    "packages/data_platform/stark_terminal_data_platform/exports/README.md",
    "packages/data_platform/stark_terminal_data_platform/providers/guardrails.py",
    "packages/data_platform/stark_terminal_data_platform/providers/approval.py",
    "packages/data_platform/stark_terminal_data_platform/providers/readiness.py",
    "packages/data_platform/stark_terminal_data_platform/providers/local_sample.py",
    "packages/data_platform/stark_terminal_data_platform/providers/candidates.py",
    "packages/data_platform/stark_terminal_data_platform/providers/selection.py",
    "packages/data_platform/stark_terminal_data_platform/providers/local_file.py",
    "docs/PROVIDER_ADAPTER_MILESTONE_AUDIT.md",
    "docs/PROVIDER_BOUNDARY_AUDIT.md",
    "docs/PROVIDER_NO_EXTERNAL_CALLS_AUDIT.md",
    "docs/PROVIDER_NEXT_PHASE_PLAN.md",
    "docs/QUANT_ANALYTICS_FOUNDATION_PLAN.md",
    "docs/TIME_SERIES_ANALYTICS_BOUNDARY.md",
    "docs/ANALYTICS_SAFETY_POLICY.md",
    "docs/ANALYTICS_DEPENDENCY_STAGING.md",
    "docs/ANALYTICS_ROADMAP.md",
    "apps/api/stark_terminal_api/routes/synthetic_ohlcv_storage.py",
    "apps/api/stark_terminal_api/routes/synthetic_ohlcv_exports.py",
    "apps/api/stark_terminal_api/routes/provider_guardrails.py",
    "apps/api/stark_terminal_api/routes/provider_readiness.py",
    "apps/api/stark_terminal_api/routes/analytics_foundation.py",
    "apps/api/stark_terminal_api/routes/numerical_analytics.py",
    "apps/api/stark_terminal_api/routes/returns_analytics.py",
    "apps/api/stark_terminal_api/routes/risk_analytics.py",
    "apps/api/stark_terminal_api/routes/fixtures.py",
    "apps/api/stark_terminal_api/routes/instrument_metadata.py",
    "apps/api/stark_terminal_api/routes/market_data_batches.py",
    "alembic/versions/0003_market_data_batch_metadata.py",
]

REQUIRED_SAFETY_PHRASES = [
    "no execution APIs",
    "no real market ingestion",
    "no broker execution",
    "Kafka/Redpanda Event Backbone",
    "durable event backbone",
    "Data Quality",
    "validation framework",
    "synthetic",
    "OHLCV",
    "local-only",
    "test/dev only",
    "no external calls",
    "no real market data",
    "Instrument Metadata Persistence",
    "InstrumentRepository",
    "InstrumentMetadataService",
    "Market Data Batch Persistence",
    "Data Foundation Audit",
    "Data Persistence Boundary",
    "Synthetic Data Safety Audit",
    "TimescaleDB Synthetic OHLCV Storage Foundation",
    "Synthetic OHLCV Storage",
    "Timescale Synthetic Storage Policy",
    "validation-before-storage",
    "Synthetic OHLCV Research Lake Export",
    "DatasetManifest",
    "Parquet",
    "DuckDB",
    "validation-before-export",
    "no production research lake writes by default",
    "Provider Adapter",
    "Provider Adapter Guardrails",
    "Local Sample Provider",
    "Data Foundation Milestone Audit",
    "Synthetic Storage Export Audit",
    "Provider Guardrail Audit",
    "Local Sample Provider Audit",
    "Data Foundation Milestone Next Phase",
    "no analytics/signals/decisions",
    "Guardrail",
    "approval workflow",
    "compliance checklist",
    "no credentials",
    "no provider SDKs",
    "LOCAL_SAMPLE",
    "no real provider implementation",
    "no trading signals",
    "Real Provider Readiness",
    "Candidate Selection",
    "risk scoring",
    "capability gap",
    "no SDKs",
    "no production approval",
    "Local File Provider",
    "local-file-only",
    "path safety",
    "no arbitrary file read API",
    "Provider Adapter Milestone Audit",
    "Provider Boundary Audit",
    "Provider No External Calls Audit",
    "Provider Next Phase Plan",
    "Quant Analytics",
    "Time-Series Analytics",
    "analytics safety",
    "dependency staging",
    "no signals",
    "no recommendations",
    "no analytics calculations",
    "Numerical Analytics",
    "source reference",
    "finite values",
    "dependency gate",
    "descriptive-only",
    "no returns",
    "no volatility",
    "no drawdown",
    "no correlation",
    "no DecisionObject",
    "Returns Analytics",
    "Rolling Window Analytics",
    "simple returns",
    "log returns",
    "rolling mean",
    "rolling min",
    "rolling max",
    "rolling count",
    "Volatility Analytics",
    "Drawdown Analytics",
    "sample standard deviation",
    "population standard deviation",
    "annualized volatility",
    "drawdown series",
    "max drawdown",
    "drawdown duration",
    "no backtesting",
    "no regimes",
    "Analytics Milestone Audit",
    "Analytics Boundary Audit",
    "Analytics No-Signal Audit",
    "Analytics Dependency Audit",
    "Analytics Next Phase Plan",
    "Prompts 26-29",
    "no heavy dependencies",
    "no DecisionObject generation",
    "no buy/sell/hold/watch/avoid outputs",
    "Correlation Analytics",
    "Beta Analytics",
    "Pearson correlation",
    "sample covariance",
    "sample variance",
    "equal length",
    "minimum observations",
    "zero variance",
    "Time-Series Diagnostics",
    "timestamp diagnostics",
    "monotonic",
    "duplicate timestamp",
    "gap diagnostics",
    "expected interval",
    "missing count",
    "no stationarity tests",
    "no regime detection",
    "no indicators",
    "Regime Analytics",
    "planning-only",
    "label placeholders",
    "evidence requirements",
    "human review",
    "no classification",
    "Regime Feature Preparation",
    "contracts-only",
    "feature groups",
    "provenance",
    "evidence mapping",
    "no feature computation",
    "no feature registry writes",
    "Analytics/Regime Milestone Audit",
    "Regime Boundary Audit",
    "Regime No-Classification Audit",
    "Regime Feature Preparation Audit",
    "Analytics/Regime No-Signal Audit",
    "Analytics/Regime Dependency Audit",
    "Decision Desk Readiness Plan",
    "Retail Decision Desk",
    "action placeholders",
    "evidence requirements",
    "human review",
    "human-review guardrails",
    "display boundary",
    "no action generation",
    "no confidence scoring",
    "Prompt 36",
    "Prompts 26-34",
    "Prompt 38",
    "DecisionObject Evidence Bundle",
    "evidence item",
    "validation checklist",
    "human review attachment",
    "Prompt 39",
    "Decision Safety",
    "human-review gates",
    "approval placeholders",
    "override prohibition",
    "blocked output policy",
    "no approvals",
    "no overrides",
    "Decision Desk API",
    "contract skeleton",
    "request placeholder",
    "response placeholder",
    "unavailable response",
    "Decision Desk Milestone Audit",
    "Decision Desk Boundary Audit",
    "Decision Evidence Boundary Audit",
    "Decision Safety Boundary Audit",
    "Decision API Skeleton Audit",
    "Decision No-Recommendation Audit",
    "Decision Desk Next Phase Plan",
    "Prompts 36-40",
    "unavailable-by-default",
    "no approval",
    "no override",
    "no active DecisionObject generation",
    "no market-data-to-recommendation endpoint",
    "Prompt 42",
    "Decision Desk Readiness API",
    "no readiness-to-trade",
    "Prompt 43",
    "Decision Desk Display",
    "display contract skeleton",
    "no active UI",
    "Prompt 44",
    "Decision Evidence Validation",
    "validation-only",
    "validation result",
    "failure reasons",
    "no validation-as-recommendation",
    "no validation-as-readiness-to-trade",
    "no validation-as-approval",
    "Prompt 45",
    "Decision Human Review",
    "workflow skeleton",
    "task placeholder",
    "role placeholder",
    "queue placeholder",
    "unavailable response",
    "no active workflow",
    "no task assignment",
    "no reviewer auth",
    "no notifications",
    "Prompt 46",
    "Decision Desk Milestone Audit 2",
    "Decision Readiness API Boundary Audit",
    "Decision Display Boundary Audit",
    "Decision Evidence Validation Boundary Audit",
    "Decision Human Review Workflow Boundary Audit",
    "Decision No-Approval Workflow Audit",
    "Prompts 42-45",
    "no active approval workflow",
    "no active override workflow",
    "Prompt 47",
    "Decision Desk System Boundary Hardening",
    "forbidden behavior registry",
    "endpoint boundary policy",
    "module boundary policy",
    "cross-module invariants",
    "no endpoint boundary bypass",
    "no cross-module boundary bypass",
    "no module bypasses forbidden behavior registry",
    "boundary-hardening-only",
    "Prompt 48",
    "Decision API/Display Integration Readiness Audit",
    "Decision Cross-Endpoint Consistency Audit",
    "Decision API Display Boundary Audit",
    "Decision Boundary Integration Audit",
    "Decision Integration No-Recommendation Audit",
    "Retail Dashboard Readiness Plan",
    "Prompt 49",
    "Retail Dashboard Planning and Guardrails",
    "planning and guardrails",
    "no recommendation cards",
    "no broker controls",
    "no dashboard-as-recommendation",
    "no dashboard-as-execution-control",
    "no placeholder-card-as-decision",
    "no real market data dashboard display",
    "retail-dashboard-planning",
    "Prompt 50",
    "Retail Dashboard API",
    "API contract skeleton",
    "unavailable by default",
    "no active UI",
    "no recommendation cards",
    "no action generation",
    "no confidence scoring",
    "no DecisionObject generation",
    "no readiness-to-trade",
    "no broker controls",
    "no execution APIs",
    "Prompt 51",
    "Retail Dashboard Display",
    "display contract skeleton",
    "unavailable by default",
    "no active UI",
    "no frontend component",
    "no desktop UI component",
    "no recommendation cards",
    "no action generation",
    "no confidence scoring",
    "no DecisionObject generation",
    "no readiness-to-trade",
    "no broker controls",
    "no execution APIs",
    "Prompt 52",
    "Retail Dashboard Safety Boundary Audit",
    "Prompts 49-51",
    "Retail Dashboard API Boundary Audit",
    "Retail Dashboard Display Boundary Audit",
    "no frontend implementation",
    "no desktop UI implementation",
    "no active dashboard widgets",
    "no dashboard-as-recommendation",
    "no dashboard-as-execution-control",
    "Retail Dashboard Milestone Audit",
    "Prompt 53",
    "Prompts 49-52",
    "Retail Dashboard Planning Milestone Audit",
    "Retail Dashboard API Milestone Audit",
    "Retail Dashboard Display Milestone Audit",
    "Retail Dashboard Safety Milestone Audit",
    "Retail Dashboard Phase No Active UI Audit",
    "Retail Dashboard Phase No Recommendation Execution Audit",
    "Retail Dashboard Next Phase Plan",
    "Retail Dashboard System Boundary Hardening",
    "Prompt 54",
    "forbidden behavior registry",
    "endpoint boundary policy",
    "module boundary policy",
    "cross-module invariants",
    "no frontend components",
    "no desktop components",
    "no cross-module dashboard boundary bypass",
    "no endpoint dashboard boundary bypass",
    "Retail Dashboard forbidden behavior registry",
    "boundary-hardening-only",
    "Prompts 40-47",
    "Retail Dashboard Planning and Guardrails only",
    "no API-to-display recommendation path",
    "no readiness-to-display-trade",
    "no display-as-decision",
    "decision-api-display-readiness",
    "Prompt 56",
    "Retail Trader Experience Planning and Guardrails",
    "planning and guardrails",
    "persona placeholders",
    "journey placeholders",
    "experience section",
    "experience card",
    "forbidden interactions",
    "no frontend components",
    "no desktop components",
    "no recommendation cards",
    "no action generation",
    "no confidence scoring",
    "no DecisionObject generation",
    "no readiness-to-trade",
    "no broker controls",
    "no suitability profiling",
    "no placeholder-experience-as-decision",
    "retail-trader-experience-planning",
    "Prompt 57",
    "Retail Trader Experience API Contract Skeleton",
    "API contract skeleton",
    "api-contract-skeleton-only",
    "request placeholders",
    "response placeholders",
    "persona reference",
    "journey reference",
    "dashboard reference",
    "decision reference",
    "safety reference",
    "unavailable responses",
    "no retail trader API as recommendation",
    "no retail trader API as execution control",
    "no retail trader API suitability profiling",
    "retail-trader-experience-api-skeleton",
    "Prompt 58",
    "Retail Trader Experience Display Contract Skeleton",
    "display contract skeleton",
    "display-contract-skeleton-only",
    "persona visual placeholder",
    "journey visual placeholder",
    "visual section",
    "widget placeholder",
    "badge placeholder",
    "unavailable display response",
    "display safety boundary",
    "no retail trader display as recommendation",
    "no retail trader display as execution control",
    "no retail trader display suitability profiling",
    "retail-trader-experience-display-skeleton",
    "Prompt 59",
    "Retail Trader Experience Safety Boundary Audit",
    "Prompts 56-58",
    "Retail Trader Experience API Boundary Audit",
    "Retail Trader Experience Display Boundary Audit",
    "Retail Trader Experience No-Active-UI Audit",
    "Retail Trader Experience No-Recommendation Audit",
    "Retail Trader Experience No-Execution Audit",
    "Retail Trader Experience No-Suitability-Profiling Audit",
    "Retail Trader Experience Milestone Readiness",
    "no experience-as-recommendation",
    "no experience-as-execution-control",
    "no persona-as-suitability-profile",
    "no live data display",
    "no placeholder-as-trader-output",
    "no persona-to-suitability-profile path",
    "no trader-experience-to-execution path",
    "retail-trader-experience-safety-boundary",
    "Prompt 60",
    "Retail Trader Experience Milestone Audit",
    "Prompts 56-59",
    "Retail Trader Experience Planning Milestone Audit",
    "Retail Trader Experience API Milestone Audit",
    "Retail Trader Experience Display Milestone Audit",
    "Retail Trader Experience Safety Milestone Audit",
    "Retail Trader Experience Phase No-Active-UI Audit",
    "Retail Trader Experience Phase No-Recommendation Execution Audit",
    "Retail Trader Experience Phase No-Suitability Audit",
    "Retail Trader Experience Next Phase Plan",
    "retail-trader-experience-milestone",
    "Strategy Research Workspace Status",
    "no placeholder-as-trader-output",
    "no persona-to-suitability-profile path",
    "no trader-experience-to-execution endpoint",
    "Prompt 61",
    "Retail Trader Experience System Boundary Hardening",
    "forbidden behavior registry",
    "endpoint boundary policy",
    "module boundary policy",
    "cross-module invariants",
    "boundary-hardening-only",
    "no endpoint Retail Trader Experience boundary bypass",
    "no cross-module Retail Trader Experience boundary bypass",
    "no module bypasses forbidden behavior registry",
    "no journey-to-trading-advice path",
    "Prompt 62",
    "Retail Trader Experience API/Display Integration Readiness Audit",
    "Prompts 56-61",
    "Retail Trader Experience Cross-Endpoint Consistency Audit",
    "Retail Trader Experience API/Display Boundary Audit",
    "Retail Trader Experience Boundary Integration Audit",
    "Retail Trader Experience Integration No-Active-UI Audit",
    "Retail Trader Experience Integration No-Recommendation Execution Audit",
    "Retail Trader Experience Integration No-Suitability Audit",
    "Strategy Research Workspace Readiness Plan",
    "cross-endpoint consistency",
    "cross-module consistency",
    "no API-to-display recommendation path",
    "no display-to-decision path",
    "no display-to-execution path",
    "no boundary bypass path",
    "Strategy Research Workspace Planning and Guardrails",
    "Prompt 63",
    "Strategy Research Workspace Planning",
    "Strategy Research Workspace Guardrails",
    "Strategy Research Workspace Placeholders",
    "Strategy Research Artifact Placeholders",
    "Strategy Research Paper Reference Placeholders",
    "Strategy Research Hypothesis Placeholders",
    "Strategy Research Dataset Reference Placeholders",
    "Strategy Research Experiment Placeholders",
    "Strategy Research Forbidden Interactions",
    "Strategy Research No Strategy Generation Policy",
    "Strategy Research No Backtesting Policy",
    "Strategy Research No Recommendation Policy",
    "Strategy Research No Execution Policy",
    "no paper ingestion",
    "no paper parsing",
    "no strategy generation",
    "no strategy code generation",
    "no backtesting",
    "no optimization",
    "no recommendation generation",
    "no research-to-recommendation path",
    "no research-to-execution path",
    "strategy-research-workspace-planning",
    "Prompt 64",
    "Strategy Research Workspace API",
    "Strategy Research Workspace API Contract Skeleton",
    "api-contract-skeleton-only",
    "unavailable by default",
    "request placeholders",
    "response placeholders",
    "workspace reference placeholder",
    "artifact reference placeholder",
    "paper reference placeholder",
    "hypothesis reference placeholder",
    "dataset reference placeholder",
    "experiment reference placeholder",
    "safety reference placeholder",
    "unavailable responses",
    "no paper ingestion",
    "no paper parsing",
    "no strategy generation",
    "no strategy code generation",
    "no backtesting",
    "no optimization",
    "no recommendation generation",
    "no confidence scoring",
    "no DecisionObject generation",
    "no readiness-to-trade",
    "no broker controls",
    "no execution APIs",
    "strategy-research-workspace-api-skeleton",
    "no classifier inputs",
    "Decision Desk planning",
    "dependency staging",
    "batch metadata",
    "no full OHLCV bars",
    "no full OHLCV production persistence",
    "validation-before-persistence",
    "Feature Registry",
    "Mac mini M2",
    "Windows-native",
]

REQUIRED_ANALYTICS_FOUNDATION_FILES = [
    "packages/analytics/stark_terminal_analytics/foundation/__init__.py",
    "packages/analytics/stark_terminal_analytics/foundation/contracts.py",
    "packages/analytics/stark_terminal_analytics/foundation/safety.py",
    "packages/analytics/stark_terminal_analytics/foundation/dependencies.py",
    "packages/analytics/stark_terminal_analytics/foundation/roadmap.py",
    "packages/analytics/stark_terminal_analytics/foundation/health.py",
    "packages/analytics/stark_terminal_analytics/foundation/README.md",
]

REQUIRED_NUMERICAL_ANALYTICS_FILES = [
    "packages/analytics/stark_terminal_analytics/numerical/__init__.py",
    "packages/analytics/stark_terminal_analytics/numerical/contracts.py",
    "packages/analytics/stark_terminal_analytics/numerical/validation.py",
    "packages/analytics/stark_terminal_analytics/numerical/dependencies.py",
    "packages/analytics/stark_terminal_analytics/numerical/summary.py",
    "packages/analytics/stark_terminal_analytics/numerical/health.py",
    "packages/analytics/stark_terminal_analytics/numerical/README.md",
    "apps/api/stark_terminal_api/routes/numerical_analytics.py",
    "docs/NUMERICAL_ANALYTICS_CORE_CONTRACTS.md",
    "docs/NUMERICAL_ANALYTICS_VALIDATION_POLICY.md",
    "docs/NUMERICAL_ANALYTICS_DEPENDENCY_GATE.md",
    "docs/NUMERICAL_ANALYTICS_SAFETY_BOUNDARY.md",
]

REQUIRED_RETURNS_ROLLING_ANALYTICS_FILES = [
    "packages/analytics/stark_terminal_analytics/returns/__init__.py",
    "packages/analytics/stark_terminal_analytics/returns/contracts.py",
    "packages/analytics/stark_terminal_analytics/returns/validation.py",
    "packages/analytics/stark_terminal_analytics/returns/calculations.py",
    "packages/analytics/stark_terminal_analytics/returns/health.py",
    "packages/analytics/stark_terminal_analytics/returns/README.md",
    "packages/analytics/stark_terminal_analytics/rolling/__init__.py",
    "packages/analytics/stark_terminal_analytics/rolling/contracts.py",
    "packages/analytics/stark_terminal_analytics/rolling/validation.py",
    "packages/analytics/stark_terminal_analytics/rolling/calculations.py",
    "packages/analytics/stark_terminal_analytics/rolling/health.py",
    "packages/analytics/stark_terminal_analytics/rolling/README.md",
    "apps/api/stark_terminal_api/routes/returns_analytics.py",
    "docs/RETURNS_ANALYTICS_V0.md",
    "docs/ROLLING_WINDOW_ANALYTICS_V0.md",
    "docs/RETURNS_ROLLING_VALIDATION_POLICY.md",
    "docs/RETURNS_ROLLING_SAFETY_BOUNDARY.md",
]

REQUIRED_VOLATILITY_DRAWDOWN_ANALYTICS_FILES = [
    "packages/analytics/stark_terminal_analytics/volatility/__init__.py",
    "packages/analytics/stark_terminal_analytics/volatility/contracts.py",
    "packages/analytics/stark_terminal_analytics/volatility/validation.py",
    "packages/analytics/stark_terminal_analytics/volatility/calculations.py",
    "packages/analytics/stark_terminal_analytics/volatility/health.py",
    "packages/analytics/stark_terminal_analytics/volatility/README.md",
    "packages/analytics/stark_terminal_analytics/drawdown/__init__.py",
    "packages/analytics/stark_terminal_analytics/drawdown/contracts.py",
    "packages/analytics/stark_terminal_analytics/drawdown/validation.py",
    "packages/analytics/stark_terminal_analytics/drawdown/calculations.py",
    "packages/analytics/stark_terminal_analytics/drawdown/health.py",
    "packages/analytics/stark_terminal_analytics/drawdown/README.md",
    "apps/api/stark_terminal_api/routes/risk_analytics.py",
    "docs/VOLATILITY_ANALYTICS_V0.md",
    "docs/DRAWDOWN_ANALYTICS_V0.md",
    "docs/VOLATILITY_DRAWDOWN_VALIDATION_POLICY.md",
    "docs/VOLATILITY_DRAWDOWN_SAFETY_BOUNDARY.md",
]

REQUIRED_ANALYTICS_MILESTONE_AUDIT_FILES = [
    "docs/ANALYTICS_MILESTONE_AUDIT.md",
    "docs/ANALYTICS_BOUNDARY_AUDIT.md",
    "docs/ANALYTICS_NO_SIGNAL_AUDIT.md",
    "docs/ANALYTICS_DEPENDENCY_AUDIT.md",
    "docs/ANALYTICS_NEXT_PHASE_PLAN.md",
]

REQUIRED_CORRELATION_BETA_ANALYTICS_FILES = [
    "packages/analytics/stark_terminal_analytics/correlation/__init__.py",
    "packages/analytics/stark_terminal_analytics/correlation/contracts.py",
    "packages/analytics/stark_terminal_analytics/correlation/validation.py",
    "packages/analytics/stark_terminal_analytics/correlation/calculations.py",
    "packages/analytics/stark_terminal_analytics/correlation/health.py",
    "packages/analytics/stark_terminal_analytics/correlation/README.md",
    "packages/analytics/stark_terminal_analytics/beta/__init__.py",
    "packages/analytics/stark_terminal_analytics/beta/contracts.py",
    "packages/analytics/stark_terminal_analytics/beta/validation.py",
    "packages/analytics/stark_terminal_analytics/beta/calculations.py",
    "packages/analytics/stark_terminal_analytics/beta/health.py",
    "packages/analytics/stark_terminal_analytics/beta/README.md",
    "apps/api/stark_terminal_api/routes/relationship_analytics.py",
    "docs/CORRELATION_ANALYTICS_V0.md",
    "docs/BETA_ANALYTICS_V0.md",
    "docs/CORRELATION_BETA_VALIDATION_POLICY.md",
    "docs/CORRELATION_BETA_SAFETY_BOUNDARY.md",
]

REQUIRED_TIME_SERIES_DIAGNOSTICS_FILES = [
    "packages/analytics/stark_terminal_analytics/diagnostics/__init__.py",
    "packages/analytics/stark_terminal_analytics/diagnostics/contracts.py",
    "packages/analytics/stark_terminal_analytics/diagnostics/validation.py",
    "packages/analytics/stark_terminal_analytics/diagnostics/calculations.py",
    "packages/analytics/stark_terminal_analytics/diagnostics/health.py",
    "packages/analytics/stark_terminal_analytics/diagnostics/README.md",
    "apps/api/stark_terminal_api/routes/time_series_diagnostics.py",
    "docs/TIME_SERIES_DIAGNOSTICS_FOUNDATION.md",
    "docs/TIMESTAMP_DIAGNOSTICS_POLICY.md",
    "docs/TIME_SERIES_GAP_DIAGNOSTICS.md",
    "docs/TIME_SERIES_DIAGNOSTICS_SAFETY_BOUNDARY.md",
    "docs/STATIONARITY_REGIME_DIAGNOSTICS_DEFERRED.md",
]

REQUIRED_REGIME_ANALYTICS_FILES = [
    "packages/analytics/stark_terminal_analytics/regime/__init__.py",
    "packages/analytics/stark_terminal_analytics/regime/contracts.py",
    "packages/analytics/stark_terminal_analytics/regime/safety.py",
    "packages/analytics/stark_terminal_analytics/regime/evidence.py",
    "packages/analytics/stark_terminal_analytics/regime/readiness.py",
    "packages/analytics/stark_terminal_analytics/regime/dependencies.py",
    "packages/analytics/stark_terminal_analytics/regime/roadmap.py",
    "packages/analytics/stark_terminal_analytics/regime/health.py",
    "packages/analytics/stark_terminal_analytics/regime/README.md",
    "apps/api/stark_terminal_api/routes/regime_analytics.py",
    "docs/REGIME_ANALYTICS_PLANNING.md",
    "docs/REGIME_LABEL_CONTRACTS.md",
    "docs/REGIME_EVIDENCE_REQUIREMENTS.md",
    "docs/REGIME_ANALYTICS_SAFETY_POLICY.md",
    "docs/REGIME_DEPENDENCY_STAGING.md",
    "docs/REGIME_ANALYTICS_ROADMAP.md",
]

REQUIRED_REGIME_FEATURE_PREPARATION_FILES = [
    "packages/analytics/stark_terminal_analytics/regime_features/__init__.py",
    "packages/analytics/stark_terminal_analytics/regime_features/contracts.py",
    "packages/analytics/stark_terminal_analytics/regime_features/provenance.py",
    "packages/analytics/stark_terminal_analytics/regime_features/evidence_mapping.py",
    "packages/analytics/stark_terminal_analytics/regime_features/readiness.py",
    "packages/analytics/stark_terminal_analytics/regime_features/safety.py",
    "packages/analytics/stark_terminal_analytics/regime_features/dependencies.py",
    "packages/analytics/stark_terminal_analytics/regime_features/health.py",
    "packages/analytics/stark_terminal_analytics/regime_features/README.md",
    "apps/api/stark_terminal_api/routes/regime_features.py",
    "docs/REGIME_FEATURE_PREPARATION_CONTRACTS.md",
    "docs/REGIME_FEATURE_GROUPS.md",
    "docs/REGIME_FEATURE_PROVENANCE_POLICY.md",
    "docs/REGIME_FEATURE_EVIDENCE_MAPPING.md",
    "docs/REGIME_FEATURE_SAFETY_POLICY.md",
    "docs/REGIME_FEATURE_DEPENDENCY_STAGING.md",
]

REQUIRED_ANALYTICS_REGIME_MILESTONE_AUDIT_FILES = [
    "docs/ANALYTICS_REGIME_MILESTONE_AUDIT.md",
    "docs/REGIME_BOUNDARY_AUDIT.md",
    "docs/REGIME_NO_CLASSIFICATION_AUDIT.md",
    "docs/REGIME_FEATURE_PREPARATION_AUDIT.md",
    "docs/ANALYTICS_REGIME_NO_SIGNAL_AUDIT.md",
    "docs/ANALYTICS_REGIME_DEPENDENCY_AUDIT.md",
    "docs/DECISION_DESK_READINESS_PLAN.md",
]

REQUIRED_RETAIL_DECISION_DESK_FILES = [
    "packages/core/stark_terminal_core/decision_desk/__init__.py",
    "packages/core/stark_terminal_core/decision_desk/planning.py",
    "packages/core/stark_terminal_core/decision_desk/action_placeholders.py",
    "packages/core/stark_terminal_core/decision_desk/evidence.py",
    "packages/core/stark_terminal_core/decision_desk/human_review.py",
    "packages/core/stark_terminal_core/decision_desk/safety.py",
    "packages/core/stark_terminal_core/decision_desk/readiness.py",
    "packages/core/stark_terminal_core/decision_desk/display.py",
    "packages/core/stark_terminal_core/decision_desk/health.py",
    "packages/core/stark_terminal_core/decision_desk/README.md",
    "apps/api/stark_terminal_api/routes/decision_desk.py",
    "docs/RETAIL_DECISION_DESK_PLANNING.md",
    "docs/DECISION_DESK_ACTION_PLACEHOLDERS.md",
    "docs/DECISION_DESK_EVIDENCE_REQUIREMENTS.md",
    "docs/DECISION_DESK_HUMAN_REVIEW_GUARDRAILS.md",
    "docs/DECISION_DESK_SAFETY_POLICY.md",
    "docs/DECISION_DESK_DISPLAY_BOUNDARY.md",
]

REQUIRED_DECISION_EVIDENCE_FILES = [
    "packages/core/stark_terminal_core/decision_evidence/__init__.py",
    "packages/core/stark_terminal_core/decision_evidence/bundle.py",
    "packages/core/stark_terminal_core/decision_evidence/items.py",
    "packages/core/stark_terminal_core/decision_evidence/provenance.py",
    "packages/core/stark_terminal_core/decision_evidence/validation.py",
    "packages/core/stark_terminal_core/decision_evidence/human_review.py",
    "packages/core/stark_terminal_core/decision_evidence/safety.py",
    "packages/core/stark_terminal_core/decision_evidence/readiness.py",
    "packages/core/stark_terminal_core/decision_evidence/health.py",
    "packages/core/stark_terminal_core/decision_evidence/README.md",
    "apps/api/stark_terminal_api/routes/decision_evidence.py",
    "docs/DECISIONOBJECT_EVIDENCE_BUNDLE_CONTRACTS.md",
    "docs/DECISION_EVIDENCE_ITEM_SCHEMA.md",
    "docs/DECISION_EVIDENCE_PROVENANCE_POLICY.md",
    "docs/DECISION_EVIDENCE_VALIDATION_CHECKLIST.md",
    "docs/DECISION_EVIDENCE_HUMAN_REVIEW_ATTACHMENTS.md",
    "docs/DECISION_EVIDENCE_SAFETY_POLICY.md",
]

REQUIRED_DECISION_SAFETY_FILES = [
    "packages/core/stark_terminal_core/decision_safety/__init__.py",
    "packages/core/stark_terminal_core/decision_safety/guardrails.py",
    "packages/core/stark_terminal_core/decision_safety/human_review.py",
    "packages/core/stark_terminal_core/decision_safety/approval.py",
    "packages/core/stark_terminal_core/decision_safety/overrides.py",
    "packages/core/stark_terminal_core/decision_safety/blocked_outputs.py",
    "packages/core/stark_terminal_core/decision_safety/readiness.py",
    "packages/core/stark_terminal_core/decision_safety/health.py",
    "packages/core/stark_terminal_core/decision_safety/README.md",
    "apps/api/stark_terminal_api/routes/decision_safety.py",
    "docs/DECISION_SAFETY_GUARDRAILS.md",
    "docs/DECISION_HUMAN_REVIEW_GATES.md",
    "docs/DECISION_APPROVAL_PLACEHOLDERS.md",
    "docs/DECISION_OVERRIDE_PROHIBITION.md",
    "docs/DECISION_BLOCKED_OUTPUT_POLICY.md",
    "docs/DECISION_SAFETY_READINESS_POLICY.md",
]

REQUIRED_DECISION_API_FILES = [
    "packages/core/stark_terminal_core/decision_api/__init__.py",
    "packages/core/stark_terminal_core/decision_api/requests.py",
    "packages/core/stark_terminal_core/decision_api/responses.py",
    "packages/core/stark_terminal_core/decision_api/references.py",
    "packages/core/stark_terminal_core/decision_api/unavailable.py",
    "packages/core/stark_terminal_core/decision_api/contracts.py",
    "packages/core/stark_terminal_core/decision_api/health.py",
    "packages/core/stark_terminal_core/decision_api/README.md",
    "apps/api/stark_terminal_api/routes/decision_desk_api.py",
    "docs/DECISION_DESK_API_CONTRACT_SKELETON.md",
    "docs/DECISION_DESK_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/DECISION_DESK_UNAVAILABLE_RESPONSES.md",
    "docs/DECISION_DESK_API_SAFETY_BOUNDARY.md",
    "docs/DECISION_DESK_API_NO_RECOMMENDATION_POLICY.md",
]

REQUIRED_DECISION_DESK_MILESTONE_AUDIT_FILES = [
    "docs/DECISION_DESK_MILESTONE_AUDIT.md",
    "docs/DECISION_DESK_BOUNDARY_AUDIT.md",
    "docs/DECISION_EVIDENCE_BOUNDARY_AUDIT.md",
    "docs/DECISION_SAFETY_BOUNDARY_AUDIT.md",
    "docs/DECISION_API_SKELETON_AUDIT.md",
    "docs/DECISION_NO_RECOMMENDATION_AUDIT.md",
    "docs/DECISION_DESK_NEXT_PHASE_PLAN.md",
]

REQUIRED_DECISION_READINESS_API_FILES = [
    "packages/core/stark_terminal_core/decision_readiness_api/__init__.py",
    "packages/core/stark_terminal_core/decision_readiness_api/requests.py",
    "packages/core/stark_terminal_core/decision_readiness_api/responses.py",
    "packages/core/stark_terminal_core/decision_readiness_api/references.py",
    "packages/core/stark_terminal_core/decision_readiness_api/unavailable.py",
    "packages/core/stark_terminal_core/decision_readiness_api/contracts.py",
    "packages/core/stark_terminal_core/decision_readiness_api/health.py",
    "packages/core/stark_terminal_core/decision_readiness_api/README.md",
    "apps/api/stark_terminal_api/routes/decision_readiness_api.py",
    "docs/DECISION_DESK_READINESS_API_SKELETON.md",
    "docs/DECISION_READINESS_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/DECISION_READINESS_REFERENCE_PLACEHOLDERS.md",
    "docs/DECISION_READINESS_UNAVAILABLE_RESPONSES.md",
    "docs/DECISION_READINESS_API_SAFETY_BOUNDARY.md",
    "docs/DECISION_READINESS_NO_RECOMMENDATION_POLICY.md",
]

REQUIRED_DECISION_DISPLAY_FILES = [
    "packages/core/stark_terminal_core/decision_display/__init__.py",
    "packages/core/stark_terminal_core/decision_display/contracts.py",
    "packages/core/stark_terminal_core/decision_display/cards.py",
    "packages/core/stark_terminal_core/decision_display/sections.py",
    "packages/core/stark_terminal_core/decision_display/badges.py",
    "packages/core/stark_terminal_core/decision_display/references.py",
    "packages/core/stark_terminal_core/decision_display/unavailable.py",
    "packages/core/stark_terminal_core/decision_display/health.py",
    "packages/core/stark_terminal_core/decision_display/README.md",
    "apps/api/stark_terminal_api/routes/decision_display.py",
    "docs/DECISION_DESK_DISPLAY_CONTRACT_SKELETON.md",
    "docs/DECISION_DISPLAY_CARD_PLACEHOLDERS.md",
    "docs/DECISION_DISPLAY_SECTION_PLACEHOLDERS.md",
    "docs/DECISION_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/DECISION_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/DECISION_DISPLAY_NO_RECOMMENDATION_POLICY.md",
]

REQUIRED_DECISION_EVIDENCE_VALIDATION_FILES = [
    "packages/core/stark_terminal_core/decision_evidence_validation/__init__.py",
    "packages/core/stark_terminal_core/decision_evidence_validation/contracts.py",
    "packages/core/stark_terminal_core/decision_evidence_validation/issues.py",
    "packages/core/stark_terminal_core/decision_evidence_validation/validators.py",
    "packages/core/stark_terminal_core/decision_evidence_validation/results.py",
    "packages/core/stark_terminal_core/decision_evidence_validation/safety.py",
    "packages/core/stark_terminal_core/decision_evidence_validation/health.py",
    "packages/core/stark_terminal_core/decision_evidence_validation/README.md",
    "apps/api/stark_terminal_api/routes/decision_evidence_validation.py",
    "docs/DECISION_EVIDENCE_VALIDATION_V0.md",
    "docs/DECISION_EVIDENCE_VALIDATION_RESULT_SCHEMA.md",
    "docs/DECISION_EVIDENCE_VALIDATION_FAILURE_REASONS.md",
    "docs/DECISION_EVIDENCE_VALIDATION_SAFETY_BOUNDARY.md",
    "docs/DECISION_EVIDENCE_VALIDATION_API_SKELETON.md",
    "docs/DECISION_EVIDENCE_VALIDATION_NO_RECOMMENDATION_POLICY.md",
]

REQUIRED_DECISION_HUMAN_REVIEW_FILES = [
    "packages/core/stark_terminal_core/decision_human_review/__init__.py",
    "packages/core/stark_terminal_core/decision_human_review/workflow.py",
    "packages/core/stark_terminal_core/decision_human_review/tasks.py",
    "packages/core/stark_terminal_core/decision_human_review/roles.py",
    "packages/core/stark_terminal_core/decision_human_review/queues.py",
    "packages/core/stark_terminal_core/decision_human_review/status.py",
    "packages/core/stark_terminal_core/decision_human_review/unavailable.py",
    "packages/core/stark_terminal_core/decision_human_review/safety.py",
    "packages/core/stark_terminal_core/decision_human_review/health.py",
    "packages/core/stark_terminal_core/decision_human_review/README.md",
    "apps/api/stark_terminal_api/routes/decision_human_review.py",
    "docs/DECISION_HUMAN_REVIEW_WORKFLOW_SKELETON.md",
    "docs/DECISION_REVIEW_TASK_PLACEHOLDERS.md",
    "docs/DECISION_REVIEW_ROLE_PLACEHOLDERS.md",
    "docs/DECISION_REVIEW_QUEUE_PLACEHOLDERS.md",
    "docs/DECISION_REVIEW_UNAVAILABLE_RESPONSES.md",
    "docs/DECISION_REVIEW_NO_APPROVAL_POLICY.md",
]

REQUIRED_DECISION_DESK_MILESTONE_AUDIT_2_FILES = [
    "docs/DECISION_DESK_MILESTONE_AUDIT_2.md",
    "docs/DECISION_READINESS_API_BOUNDARY_AUDIT.md",
    "docs/DECISION_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/DECISION_EVIDENCE_VALIDATION_BOUNDARY_AUDIT.md",
    "docs/DECISION_HUMAN_REVIEW_WORKFLOW_BOUNDARY_AUDIT.md",
    "docs/DECISION_NO_APPROVAL_WORKFLOW_AUDIT.md",
    "docs/DECISION_DESK_NEXT_PHASE_PLAN_2.md",
    "tests/test_decision_desk_milestone_audit_2_docs.py",
    "tests/test_decision_readiness_api_boundary_milestone.py",
    "tests/test_decision_display_boundary_milestone.py",
    "tests/test_decision_evidence_validation_boundary_milestone.py",
    "tests/test_decision_human_review_workflow_boundary_milestone.py",
    "tests/test_decision_no_approval_workflow_milestone.py",
    "tests/test_decision_desk_phase2_api_milestone_safety.py",
    "tests/test_decision_desk_phase2_milestone_readiness.py",
]

REQUIRED_DECISION_BOUNDARY_FILES = [
    "packages/core/stark_terminal_core/decision_boundary/__init__.py",
    "packages/core/stark_terminal_core/decision_boundary/forbidden.py",
    "packages/core/stark_terminal_core/decision_boundary/endpoints.py",
    "packages/core/stark_terminal_core/decision_boundary/modules.py",
    "packages/core/stark_terminal_core/decision_boundary/invariants.py",
    "packages/core/stark_terminal_core/decision_boundary/health.py",
    "packages/core/stark_terminal_core/decision_boundary/README.md",
    "apps/api/stark_terminal_api/routes/decision_boundary.py",
    "docs/DECISION_DESK_SYSTEM_BOUNDARY_HARDENING.md",
    "docs/DECISION_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "docs/DECISION_ENDPOINT_BOUNDARY_POLICY.md",
    "docs/DECISION_MODULE_BOUNDARY_POLICY.md",
    "docs/DECISION_CROSS_MODULE_INVARIANTS.md",
    "docs/DECISION_BOUNDARY_HARDENING_NO_EXECUTION_POLICY.md",
    "tests/test_decision_boundary_settings.py",
    "tests/test_decision_boundary_forbidden_registry.py",
    "tests/test_decision_boundary_endpoint_policy.py",
    "tests/test_decision_boundary_module_policy.py",
    "tests/test_decision_boundary_invariants.py",
    "tests/test_api_decision_boundary.py",
    "tests/test_decision_boundary_docs_status.py",
    "tests/test_decision_boundary_cross_module_no_recommendations.py",
    "tests/test_decision_boundary_cross_endpoint_no_execution.py",
    "tests/test_decision_boundary_no_active_ui_or_workflow.py",
]

REQUIRED_DECISION_API_DISPLAY_INTEGRATION_AUDIT_FILES = [
    "docs/DECISION_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    "docs/DECISION_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
    "docs/DECISION_API_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/DECISION_BOUNDARY_INTEGRATION_AUDIT.md",
    "docs/DECISION_INTEGRATION_NO_RECOMMENDATION_AUDIT.md",
    "docs/RETAIL_DASHBOARD_READINESS_PLAN.md",
    "tests/test_decision_api_display_integration_audit_docs.py",
    "tests/test_decision_cross_endpoint_consistency.py",
    "tests/test_decision_api_display_boundary_integration.py",
    "tests/test_decision_boundary_integration.py",
    "tests/test_decision_integration_no_recommendation.py",
    "tests/test_decision_integration_no_active_ui_or_workflow.py",
    "tests/test_decision_integration_no_execution.py",
    "tests/test_retail_dashboard_readiness_plan.py",
]

REQUIRED_RETAIL_DASHBOARD_FILES = [
    "packages/core/stark_terminal_core/retail_dashboard/__init__.py",
    "packages/core/stark_terminal_core/retail_dashboard/planning.py",
    "packages/core/stark_terminal_core/retail_dashboard/sections.py",
    "packages/core/stark_terminal_core/retail_dashboard/cards.py",
    "packages/core/stark_terminal_core/retail_dashboard/references.py",
    "packages/core/stark_terminal_core/retail_dashboard/interactions.py",
    "packages/core/stark_terminal_core/retail_dashboard/safety.py",
    "packages/core/stark_terminal_core/retail_dashboard/readiness.py",
    "packages/core/stark_terminal_core/retail_dashboard/health.py",
    "packages/core/stark_terminal_core/retail_dashboard/README.md",
    "apps/api/stark_terminal_api/routes/retail_dashboard.py",
    "docs/RETAIL_DASHBOARD_PLANNING.md",
    "docs/RETAIL_DASHBOARD_GUARDRAILS.md",
    "docs/RETAIL_DASHBOARD_SECTION_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_CARD_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_FORBIDDEN_INTERACTIONS.md",
    "docs/RETAIL_DASHBOARD_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_DASHBOARD_NO_EXECUTION_POLICY.md",
    "tests/test_retail_dashboard_settings.py",
    "tests/test_retail_dashboard_planning_contracts.py",
    "tests/test_retail_dashboard_sections.py",
    "tests/test_retail_dashboard_cards.py",
    "tests/test_retail_dashboard_references.py",
    "tests/test_retail_dashboard_forbidden_interactions.py",
    "tests/test_retail_dashboard_safety.py",
    "tests/test_retail_dashboard_readiness.py",
    "tests/test_api_retail_dashboard.py",
    "tests/test_retail_dashboard_docs_status.py",
    "tests/test_retail_dashboard_no_active_ui_or_execution.py",
]

REQUIRED_RETAIL_DASHBOARD_API_FILES = [
    "packages/core/stark_terminal_core/retail_dashboard_api/__init__.py",
    "packages/core/stark_terminal_core/retail_dashboard_api/requests.py",
    "packages/core/stark_terminal_core/retail_dashboard_api/responses.py",
    "packages/core/stark_terminal_core/retail_dashboard_api/references.py",
    "packages/core/stark_terminal_core/retail_dashboard_api/unavailable.py",
    "packages/core/stark_terminal_core/retail_dashboard_api/contracts.py",
    "packages/core/stark_terminal_core/retail_dashboard_api/health.py",
    "packages/core/stark_terminal_core/retail_dashboard_api/README.md",
    "apps/api/stark_terminal_api/routes/retail_dashboard_api.py",
    "docs/RETAIL_DASHBOARD_API_CONTRACT_SKELETON.md",
    "docs/RETAIL_DASHBOARD_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_API_REFERENCE_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_API_UNAVAILABLE_RESPONSES.md",
    "docs/RETAIL_DASHBOARD_API_SAFETY_BOUNDARY.md",
    "docs/RETAIL_DASHBOARD_API_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_DASHBOARD_API_NO_EXECUTION_POLICY.md",
    "tests/test_retail_dashboard_api_settings.py",
    "tests/test_retail_dashboard_api_request_placeholders.py",
    "tests/test_retail_dashboard_api_response_placeholders.py",
    "tests/test_retail_dashboard_api_references.py",
    "tests/test_retail_dashboard_api_unavailable_responses.py",
    "tests/test_retail_dashboard_api_contracts.py",
    "tests/test_api_retail_dashboard_api.py",
    "tests/test_retail_dashboard_api_docs_status.py",
    "tests/test_retail_dashboard_api_no_active_ui_or_execution.py",
]

REQUIRED_RETAIL_DASHBOARD_DISPLAY_FILES = [
    "packages/core/stark_terminal_core/retail_dashboard_display/__init__.py",
    "packages/core/stark_terminal_core/retail_dashboard_display/contracts.py",
    "packages/core/stark_terminal_core/retail_dashboard_display/layouts.py",
    "packages/core/stark_terminal_core/retail_dashboard_display/widgets.py",
    "packages/core/stark_terminal_core/retail_dashboard_display/sections.py",
    "packages/core/stark_terminal_core/retail_dashboard_display/badges.py",
    "packages/core/stark_terminal_core/retail_dashboard_display/unavailable.py",
    "packages/core/stark_terminal_core/retail_dashboard_display/safety.py",
    "packages/core/stark_terminal_core/retail_dashboard_display/health.py",
    "packages/core/stark_terminal_core/retail_dashboard_display/README.md",
    "apps/api/stark_terminal_api/routes/retail_dashboard_display.py",
    "docs/RETAIL_DASHBOARD_DISPLAY_CONTRACT_SKELETON.md",
    "docs/RETAIL_DASHBOARD_LAYOUT_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_WIDGET_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_VISUAL_SECTION_PLACEHOLDERS.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_NO_EXECUTION_POLICY.md",
    "tests/test_retail_dashboard_display_settings.py",
    "tests/test_retail_dashboard_display_contracts.py",
    "tests/test_retail_dashboard_display_layouts.py",
    "tests/test_retail_dashboard_display_widgets.py",
    "tests/test_retail_dashboard_display_sections.py",
    "tests/test_retail_dashboard_display_badges.py",
    "tests/test_retail_dashboard_display_unavailable_responses.py",
    "tests/test_retail_dashboard_display_safety.py",
    "tests/test_api_retail_dashboard_display.py",
    "tests/test_retail_dashboard_display_docs_status.py",
    "tests/test_retail_dashboard_display_no_active_ui_or_execution.py",
]

REQUIRED_RETAIL_DASHBOARD_SAFETY_AUDIT_FILES = [
    "docs/RETAIL_DASHBOARD_SAFETY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_API_BOUNDARY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_DASHBOARD_NO_RECOMMENDATION_AUDIT.md",
    "docs/RETAIL_DASHBOARD_NO_EXECUTION_AUDIT.md",
    "docs/RETAIL_DASHBOARD_MILESTONE_READINESS.md",
    "tests/test_retail_dashboard_safety_boundary_audit_docs.py",
    "tests/test_retail_dashboard_api_boundary_audit.py",
    "tests/test_retail_dashboard_display_boundary_audit.py",
    "tests/test_retail_dashboard_no_active_ui_audit.py",
    "tests/test_retail_dashboard_no_recommendation_audit.py",
    "tests/test_retail_dashboard_no_execution_audit.py",
    "tests/test_retail_dashboard_api_surface_safety.py",
    "tests/test_retail_dashboard_milestone_readiness.py",
]

REQUIRED_RETAIL_DASHBOARD_MILESTONE_AUDIT_FILES = [
    "docs/RETAIL_DASHBOARD_MILESTONE_AUDIT.md",
    "docs/RETAIL_DASHBOARD_PLANNING_MILESTONE_AUDIT.md",
    "docs/RETAIL_DASHBOARD_API_MILESTONE_AUDIT.md",
    "docs/RETAIL_DASHBOARD_DISPLAY_MILESTONE_AUDIT.md",
    "docs/RETAIL_DASHBOARD_SAFETY_MILESTONE_AUDIT.md",
    "docs/RETAIL_DASHBOARD_PHASE_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_DASHBOARD_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RETAIL_DASHBOARD_NEXT_PHASE_PLAN.md",
    "tests/test_retail_dashboard_milestone_audit_docs.py",
    "tests/test_retail_dashboard_planning_milestone.py",
    "tests/test_retail_dashboard_api_milestone.py",
    "tests/test_retail_dashboard_display_milestone.py",
    "tests/test_retail_dashboard_safety_milestone.py",
    "tests/test_retail_dashboard_phase_no_active_ui.py",
    "tests/test_retail_dashboard_phase_no_recommendation_execution.py",
    "tests/test_retail_dashboard_next_phase_readiness.py",
]

REQUIRED_RETAIL_DASHBOARD_BOUNDARY_FILES = [
    "packages/core/stark_terminal_core/retail_dashboard_boundary/__init__.py",
    "packages/core/stark_terminal_core/retail_dashboard_boundary/forbidden.py",
    "packages/core/stark_terminal_core/retail_dashboard_boundary/endpoints.py",
    "packages/core/stark_terminal_core/retail_dashboard_boundary/modules.py",
    "packages/core/stark_terminal_core/retail_dashboard_boundary/invariants.py",
    "packages/core/stark_terminal_core/retail_dashboard_boundary/health.py",
    "packages/core/stark_terminal_core/retail_dashboard_boundary/README.md",
    "apps/api/stark_terminal_api/routes/retail_dashboard_boundary.py",
    "docs/RETAIL_DASHBOARD_SYSTEM_BOUNDARY_HARDENING.md",
    "docs/RETAIL_DASHBOARD_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "docs/RETAIL_DASHBOARD_ENDPOINT_BOUNDARY_POLICY.md",
    "docs/RETAIL_DASHBOARD_MODULE_BOUNDARY_POLICY.md",
    "docs/RETAIL_DASHBOARD_CROSS_MODULE_INVARIANTS.md",
    "docs/RETAIL_DASHBOARD_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
    "docs/RETAIL_DASHBOARD_BOUNDARY_NO_EXECUTION_POLICY.md",
    "tests/test_retail_dashboard_boundary_settings.py",
    "tests/test_retail_dashboard_boundary_forbidden_registry.py",
    "tests/test_retail_dashboard_boundary_endpoint_policy.py",
    "tests/test_retail_dashboard_boundary_module_policy.py",
    "tests/test_retail_dashboard_boundary_invariants.py",
    "tests/test_api_retail_dashboard_boundary.py",
    "tests/test_retail_dashboard_boundary_docs_status.py",
    "tests/test_retail_dashboard_boundary_cross_module_no_recommendations.py",
    "tests/test_retail_dashboard_boundary_cross_endpoint_no_execution.py",
    "tests/test_retail_dashboard_boundary_no_active_ui_or_broker_controls.py",
]

REQUIRED_RETAIL_DASHBOARD_API_DISPLAY_INTEGRATION_FILES = [
    "docs/RETAIL_DASHBOARD_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    "docs/RETAIL_DASHBOARD_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_API_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_DASHBOARD_BOUNDARY_INTEGRATION_AUDIT.md",
    "docs/RETAIL_DASHBOARD_INTEGRATION_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_DASHBOARD_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_READINESS_PLAN.md",
    "tests/test_retail_dashboard_api_display_integration_audit_docs.py",
    "tests/test_retail_dashboard_cross_endpoint_consistency.py",
    "tests/test_retail_dashboard_api_display_boundary_integration.py",
    "tests/test_retail_dashboard_boundary_integration.py",
    "tests/test_retail_dashboard_integration_no_active_ui.py",
    "tests/test_retail_dashboard_integration_no_recommendation_execution.py",
    "tests/test_retail_dashboard_integration_api_surface_safety.py",
    "tests/test_retail_trader_experience_readiness_plan.py",
]

REQUIRED_RETAIL_TRADER_EXPERIENCE_FILES = [
    "packages/core/stark_terminal_core/retail_trader_experience/__init__.py",
    "packages/core/stark_terminal_core/retail_trader_experience/planning.py",
    "packages/core/stark_terminal_core/retail_trader_experience/personas.py",
    "packages/core/stark_terminal_core/retail_trader_experience/journeys.py",
    "packages/core/stark_terminal_core/retail_trader_experience/sections.py",
    "packages/core/stark_terminal_core/retail_trader_experience/cards.py",
    "packages/core/stark_terminal_core/retail_trader_experience/references.py",
    "packages/core/stark_terminal_core/retail_trader_experience/interactions.py",
    "packages/core/stark_terminal_core/retail_trader_experience/safety.py",
    "packages/core/stark_terminal_core/retail_trader_experience/readiness.py",
    "packages/core/stark_terminal_core/retail_trader_experience/health.py",
    "packages/core/stark_terminal_core/retail_trader_experience/README.md",
    "apps/api/stark_terminal_api/routes/retail_trader_experience.py",
    "docs/RETAIL_TRADER_EXPERIENCE_PLANNING.md",
    "docs/RETAIL_TRADER_EXPERIENCE_GUARDRAILS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PERSONA_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_JOURNEY_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_SECTION_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_CARD_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_FORBIDDEN_INTERACTIONS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_POLICY.md",
    "tests/test_retail_trader_experience_settings.py",
    "tests/test_retail_trader_experience_planning_contracts.py",
    "tests/test_retail_trader_experience_personas.py",
    "tests/test_retail_trader_experience_journeys.py",
    "tests/test_retail_trader_experience_sections.py",
    "tests/test_retail_trader_experience_cards.py",
    "tests/test_retail_trader_experience_references.py",
    "tests/test_retail_trader_experience_forbidden_interactions.py",
    "tests/test_retail_trader_experience_safety.py",
    "tests/test_retail_trader_experience_readiness.py",
    "tests/test_api_retail_trader_experience.py",
    "tests/test_retail_trader_experience_docs_status.py",
    "tests/test_retail_trader_experience_no_active_ui_or_execution.py",
]

REQUIRED_RETAIL_TRADER_EXPERIENCE_API_FILES = [
    "packages/core/stark_terminal_core/retail_trader_experience_api/__init__.py",
    "packages/core/stark_terminal_core/retail_trader_experience_api/requests.py",
    "packages/core/stark_terminal_core/retail_trader_experience_api/responses.py",
    "packages/core/stark_terminal_core/retail_trader_experience_api/references.py",
    "packages/core/stark_terminal_core/retail_trader_experience_api/unavailable.py",
    "packages/core/stark_terminal_core/retail_trader_experience_api/contracts.py",
    "packages/core/stark_terminal_core/retail_trader_experience_api/health.py",
    "packages/core/stark_terminal_core/retail_trader_experience_api/README.md",
    "apps/api/stark_terminal_api/routes/retail_trader_experience_api.py",
    "docs/RETAIL_TRADER_EXPERIENCE_API_CONTRACT_SKELETON.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_REFERENCE_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_UNAVAILABLE_RESPONSES.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_SAFETY_BOUNDARY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_NO_SUITABILITY_PROFILING_POLICY.md",
    "tests/test_retail_trader_experience_api_settings.py",
    "tests/test_retail_trader_experience_api_request_placeholders.py",
    "tests/test_retail_trader_experience_api_response_placeholders.py",
    "tests/test_retail_trader_experience_api_references.py",
    "tests/test_retail_trader_experience_api_unavailable_responses.py",
    "tests/test_retail_trader_experience_api_contracts.py",
    "tests/test_api_retail_trader_experience_api.py",
    "tests/test_retail_trader_experience_api_docs_status.py",
    "tests/test_retail_trader_experience_api_no_active_ui_or_execution.py",
]

REQUIRED_RETAIL_TRADER_EXPERIENCE_DISPLAY_FILES = [
    "packages/core/stark_terminal_core/retail_trader_experience_display/__init__.py",
    "packages/core/stark_terminal_core/retail_trader_experience_display/contracts.py",
    "packages/core/stark_terminal_core/retail_trader_experience_display/personas.py",
    "packages/core/stark_terminal_core/retail_trader_experience_display/journeys.py",
    "packages/core/stark_terminal_core/retail_trader_experience_display/sections.py",
    "packages/core/stark_terminal_core/retail_trader_experience_display/widgets.py",
    "packages/core/stark_terminal_core/retail_trader_experience_display/badges.py",
    "packages/core/stark_terminal_core/retail_trader_experience_display/unavailable.py",
    "packages/core/stark_terminal_core/retail_trader_experience_display/safety.py",
    "packages/core/stark_terminal_core/retail_trader_experience_display/health.py",
    "packages/core/stark_terminal_core/retail_trader_experience_display/README.md",
    "apps/api/stark_terminal_api/routes/retail_trader_experience_display.py",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_CONTRACT_SKELETON.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_PERSONA_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_JOURNEY_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_SECTION_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_WIDGET_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_NO_SUITABILITY_PROFILING_POLICY.md",
    "tests/test_retail_trader_experience_display_settings.py",
    "tests/test_retail_trader_experience_display_contracts.py",
    "tests/test_retail_trader_experience_display_personas.py",
    "tests/test_retail_trader_experience_display_journeys.py",
    "tests/test_retail_trader_experience_display_sections.py",
    "tests/test_retail_trader_experience_display_widgets.py",
    "tests/test_retail_trader_experience_display_badges.py",
    "tests/test_retail_trader_experience_display_unavailable_responses.py",
    "tests/test_retail_trader_experience_display_safety.py",
    "tests/test_api_retail_trader_experience_display.py",
    "tests/test_retail_trader_experience_display_docs_status.py",
    "tests/test_retail_trader_experience_display_no_active_ui_or_execution.py",
]

REQUIRED_RETAIL_TRADER_EXPERIENCE_SAFETY_AUDIT_FILES = [
    "docs/RETAIL_TRADER_EXPERIENCE_SAFETY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_BOUNDARY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_SUITABILITY_PROFILING_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_READINESS.md",
    "tests/test_retail_trader_experience_safety_boundary_audit_docs.py",
    "tests/test_retail_trader_experience_api_boundary_audit.py",
    "tests/test_retail_trader_experience_display_boundary_audit.py",
    "tests/test_retail_trader_experience_no_active_ui_audit.py",
    "tests/test_retail_trader_experience_no_recommendation_audit.py",
    "tests/test_retail_trader_experience_no_execution_audit.py",
    "tests/test_retail_trader_experience_no_suitability_profiling_audit.py",
    "tests/test_retail_trader_experience_api_surface_safety.py",
    "tests/test_retail_trader_experience_milestone_readiness.py",
]

REQUIRED_RETAIL_TRADER_EXPERIENCE_MILESTONE_AUDIT_FILES = [
    "docs/RETAIL_TRADER_EXPERIENCE_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PLANNING_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_DISPLAY_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_SAFETY_MILESTONE_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PHASE_NO_SUITABILITY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NEXT_PHASE_PLAN.md",
    "tests/test_retail_trader_experience_milestone_audit_docs.py",
    "tests/test_retail_trader_experience_planning_milestone.py",
    "tests/test_retail_trader_experience_api_milestone.py",
    "tests/test_retail_trader_experience_display_milestone.py",
    "tests/test_retail_trader_experience_safety_milestone.py",
    "tests/test_retail_trader_experience_phase_no_active_ui.py",
    "tests/test_retail_trader_experience_phase_no_recommendation_execution.py",
    "tests/test_retail_trader_experience_phase_no_suitability.py",
    "tests/test_retail_trader_experience_next_phase_readiness.py",
]

REQUIRED_RETAIL_TRADER_EXPERIENCE_BOUNDARY_FILES = [
    "docs/RETAIL_TRADER_EXPERIENCE_SYSTEM_BOUNDARY_HARDENING.md",
    "docs/RETAIL_TRADER_EXPERIENCE_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_ENDPOINT_BOUNDARY_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_MODULE_BOUNDARY_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_CROSS_MODULE_INVARIANTS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_EXECUTION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_NO_SUITABILITY_PROFILING_POLICY.md",
    "packages/core/stark_terminal_core/retail_trader_experience_boundary/__init__.py",
    "packages/core/stark_terminal_core/retail_trader_experience_boundary/forbidden.py",
    "packages/core/stark_terminal_core/retail_trader_experience_boundary/endpoints.py",
    "packages/core/stark_terminal_core/retail_trader_experience_boundary/modules.py",
    "packages/core/stark_terminal_core/retail_trader_experience_boundary/invariants.py",
    "packages/core/stark_terminal_core/retail_trader_experience_boundary/health.py",
    "packages/core/stark_terminal_core/retail_trader_experience_boundary/README.md",
    "apps/api/stark_terminal_api/routes/retail_trader_experience_boundary.py",
    "tests/test_retail_trader_experience_boundary_settings.py",
    "tests/test_retail_trader_experience_boundary_forbidden_registry.py",
    "tests/test_retail_trader_experience_boundary_endpoint_policy.py",
    "tests/test_retail_trader_experience_boundary_module_policy.py",
    "tests/test_retail_trader_experience_boundary_invariants.py",
    "tests/test_api_retail_trader_experience_boundary.py",
    "tests/test_retail_trader_experience_boundary_docs_status.py",
    "tests/test_retail_trader_experience_boundary_cross_module_no_recommendations.py",
    "tests/test_retail_trader_experience_boundary_cross_endpoint_no_execution.py",
    "tests/test_retail_trader_experience_boundary_no_active_ui_or_broker_controls.py",
    "tests/test_retail_trader_experience_boundary_no_suitability_profiling.py",
]

REQUIRED_RETAIL_TRADER_EXPERIENCE_API_DISPLAY_INTEGRATION_FILES = [
    "docs/RETAIL_TRADER_EXPERIENCE_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_API_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_INTEGRATION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_INTEGRATION_NO_ACTIVE_UI_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RETAIL_TRADER_EXPERIENCE_INTEGRATION_NO_SUITABILITY_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_READINESS_PLAN.md",
    "tests/test_retail_trader_experience_api_display_integration_audit_docs.py",
    "tests/test_retail_trader_experience_cross_endpoint_consistency.py",
    "tests/test_retail_trader_experience_api_display_boundary_integration.py",
    "tests/test_retail_trader_experience_boundary_integration.py",
    "tests/test_retail_trader_experience_integration_no_active_ui.py",
    "tests/test_retail_trader_experience_integration_no_recommendation_execution.py",
    "tests/test_retail_trader_experience_integration_no_suitability.py",
    "tests/test_retail_trader_experience_integration_api_surface_safety.py",
    "tests/test_strategy_research_workspace_readiness_plan.py",
]

REQUIRED_STRATEGY_RESEARCH_WORKSPACE_FILES = [
    "docs/STRATEGY_RESEARCH_WORKSPACE_PLANNING.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_GUARDRAILS.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_ARTIFACT_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_PAPER_REFERENCE_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_HYPOTHESIS_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_DATASET_REFERENCE_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_EXPERIMENT_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_FORBIDDEN_INTERACTIONS.md",
    "docs/STRATEGY_RESEARCH_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/STRATEGY_RESEARCH_NO_BACKTESTING_POLICY.md",
    "docs/STRATEGY_RESEARCH_NO_RECOMMENDATION_POLICY.md",
    "docs/STRATEGY_RESEARCH_NO_EXECUTION_POLICY.md",
    "packages/core/stark_terminal_core/strategy_research_workspace/__init__.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/planning.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/workspaces.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/artifacts.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/papers.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/strategies.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/datasets.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/experiments.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/interactions.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/safety.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/readiness.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/health.py",
    "packages/core/stark_terminal_core/strategy_research_workspace/README.md",
    "apps/api/stark_terminal_api/routes/strategy_research_workspace.py",
    "tests/test_strategy_research_workspace_settings.py",
    "tests/test_strategy_research_workspace_planning_contracts.py",
    "tests/test_strategy_research_workspace_placeholders.py",
    "tests/test_strategy_research_artifacts.py",
    "tests/test_strategy_research_paper_references.py",
    "tests/test_strategy_research_hypotheses.py",
    "tests/test_strategy_research_dataset_references.py",
    "tests/test_strategy_research_experiments.py",
    "tests/test_strategy_research_forbidden_interactions.py",
    "tests/test_strategy_research_safety.py",
    "tests/test_strategy_research_readiness.py",
    "tests/test_api_strategy_research_workspace.py",
    "tests/test_strategy_research_workspace_docs_status.py",
    "tests/test_strategy_research_workspace_no_active_ui_or_execution.py",
]

REQUIRED_STRATEGY_RESEARCH_WORKSPACE_API_FILES = [
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_CONTRACT_SKELETON.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_REFERENCE_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_UNAVAILABLE_RESPONSES.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_SAFETY_BOUNDARY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_PAPER_PARSING_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_BACKTESTING_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_RECOMMENDATION_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_NO_EXECUTION_POLICY.md",
    "packages/core/stark_terminal_core/strategy_research_workspace_api/__init__.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_api/requests.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_api/responses.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_api/references.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_api/unavailable.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_api/contracts.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_api/health.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_api/README.md",
    "apps/api/stark_terminal_api/routes/strategy_research_workspace_api.py",
    "tests/test_strategy_research_workspace_api_settings.py",
    "tests/test_strategy_research_workspace_api_request_placeholders.py",
    "tests/test_strategy_research_workspace_api_response_placeholders.py",
    "tests/test_strategy_research_workspace_api_references.py",
    "tests/test_strategy_research_workspace_api_unavailable_responses.py",
    "tests/test_strategy_research_workspace_api_contracts.py",
    "tests/test_api_strategy_research_workspace_api.py",
    "tests/test_strategy_research_workspace_api_docs_status.py",
    "tests/test_strategy_research_workspace_api_no_active_ui_or_execution.py",
]

REQUIRED_STRATEGY_RESEARCH_WORKSPACE_DISPLAY_FILES = [
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_CONTRACT_SKELETON.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_WORKSPACE_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_ARTIFACT_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_PAPER_REFERENCE_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_HYPOTHESIS_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_DATASET_REFERENCE_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_EXPERIMENT_PLACEHOLDERS.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_NO_PAPER_PARSING_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_NO_BACKTESTING_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_NO_EXECUTION_POLICY.md",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/__init__.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/contracts.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/workspaces.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/artifacts.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/papers.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/hypotheses.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/datasets.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/experiments.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/badges.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/unavailable.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/safety.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/health.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_display/README.md",
    "apps/api/stark_terminal_api/routes/strategy_research_workspace_display.py",
    "tests/test_strategy_research_workspace_display_settings.py",
    "tests/test_strategy_research_workspace_display_contracts.py",
    "tests/test_strategy_research_workspace_display_workspaces.py",
    "tests/test_strategy_research_workspace_display_artifacts.py",
    "tests/test_strategy_research_workspace_display_papers.py",
    "tests/test_strategy_research_workspace_display_hypotheses.py",
    "tests/test_strategy_research_workspace_display_datasets.py",
    "tests/test_strategy_research_workspace_display_experiments.py",
    "tests/test_strategy_research_workspace_display_badges.py",
    "tests/test_strategy_research_workspace_display_unavailable_responses.py",
    "tests/test_strategy_research_workspace_display_safety.py",
    "tests/test_api_strategy_research_workspace_display.py",
    "tests/test_strategy_research_workspace_display_docs_status.py",
    "tests/test_strategy_research_workspace_display_no_active_ui_or_execution.py",
]

REQUIRED_STRATEGY_RESEARCH_WORKSPACE_SAFETY_AUDIT_FILES = [
    "docs/STRATEGY_RESEARCH_WORKSPACE_SAFETY_BOUNDARY_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_BOUNDARY_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_MILESTONE_READINESS.md",
    "tests/test_strategy_research_workspace_safety_boundary_audit_docs.py",
    "tests/test_strategy_research_workspace_api_boundary_audit.py",
    "tests/test_strategy_research_workspace_display_boundary_audit.py",
    "tests/test_strategy_research_workspace_api_surface_safety.py",
    "tests/test_strategy_research_workspace_milestone_readiness.py",
]

REQUIRED_STRATEGY_RESEARCH_WORKSPACE_MILESTONE_AUDIT_FILES = [
    "docs/STRATEGY_RESEARCH_WORKSPACE_MILESTONE_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PLANNING_MILESTONE_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_MILESTONE_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_MILESTONE_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_SAFETY_MILESTONE_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_ACTIVE_UI_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_PAPER_PARSING_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_STRATEGY_GENERATION_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_BACKTESTING_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_NEXT_PHASE_PLAN.md",
    "tests/test_strategy_research_workspace_milestone_audit_docs.py",
    "tests/test_strategy_research_workspace_planning_milestone.py",
    "tests/test_strategy_research_workspace_api_milestone.py",
    "tests/test_strategy_research_workspace_display_milestone.py",
    "tests/test_strategy_research_workspace_safety_milestone.py",
    "tests/test_strategy_research_workspace_phase_no_active_ui.py",
    "tests/test_strategy_research_workspace_phase_no_paper_parsing.py",
    "tests/test_strategy_research_workspace_phase_no_strategy_generation.py",
    "tests/test_strategy_research_workspace_phase_no_backtesting.py",
    "tests/test_strategy_research_workspace_phase_no_recommendation_execution.py",
    "tests/test_strategy_research_workspace_next_phase_readiness.py",
]

REQUIRED_STRATEGY_RESEARCH_WORKSPACE_BOUNDARY_FILES = [
    "docs/STRATEGY_RESEARCH_WORKSPACE_SYSTEM_BOUNDARY_HARDENING.md",
    "docs/STRATEGY_RESEARCH_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "docs/STRATEGY_RESEARCH_ENDPOINT_BOUNDARY_POLICY.md",
    "docs/STRATEGY_RESEARCH_MODULE_BOUNDARY_POLICY.md",
    "docs/STRATEGY_RESEARCH_CROSS_MODULE_INVARIANTS.md",
    "docs/STRATEGY_RESEARCH_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
    "docs/STRATEGY_RESEARCH_BOUNDARY_NO_PAPER_PARSING_POLICY.md",
    "docs/STRATEGY_RESEARCH_BOUNDARY_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/STRATEGY_RESEARCH_BOUNDARY_NO_BACKTESTING_POLICY.md",
    "docs/STRATEGY_RESEARCH_BOUNDARY_NO_EXECUTION_POLICY.md",
    "packages/core/stark_terminal_core/strategy_research_workspace_boundary/__init__.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_boundary/forbidden.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_boundary/endpoints.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_boundary/modules.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_boundary/invariants.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_boundary/health.py",
    "packages/core/stark_terminal_core/strategy_research_workspace_boundary/README.md",
    "apps/api/stark_terminal_api/routes/strategy_research_workspace_boundary.py",
    "tests/test_strategy_research_workspace_boundary_settings.py",
    "tests/test_strategy_research_workspace_boundary_forbidden_registry.py",
    "tests/test_strategy_research_workspace_boundary_endpoint_policy.py",
    "tests/test_strategy_research_workspace_boundary_module_policy.py",
    "tests/test_strategy_research_workspace_boundary_invariants.py",
    "tests/test_api_strategy_research_workspace_boundary.py",
    "tests/test_strategy_research_workspace_boundary_docs_status.py",
    "tests/test_strategy_research_workspace_boundary_no_active_ui.py",
    "tests/test_strategy_research_workspace_boundary_no_paper_parsing.py",
    "tests/test_strategy_research_workspace_boundary_no_strategy_generation.py",
    "tests/test_strategy_research_workspace_boundary_no_backtesting.py",
    "tests/test_strategy_research_workspace_boundary_no_recommendation_execution.py",
]

REQUIRED_STRATEGY_RESEARCH_WORKSPACE_API_DISPLAY_INTEGRATION_FILES = [
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_BOUNDARY_INTEGRATION_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_ACTIVE_UI_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_PAPER_PARSING_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_STRATEGY_BACKTEST_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_READINESS_PLAN.md",
    "tests/test_strategy_research_workspace_api_display_integration_audit_docs.py",
    "tests/test_strategy_research_workspace_cross_endpoint_consistency.py",
    "tests/test_strategy_research_workspace_api_display_boundary_integration.py",
    "tests/test_strategy_research_workspace_boundary_integration.py",
    "tests/test_strategy_research_workspace_integration_no_active_ui.py",
    "tests/test_strategy_research_workspace_integration_no_paper_parsing.py",
    "tests/test_strategy_research_workspace_integration_no_strategy_backtest.py",
    "tests/test_strategy_research_workspace_integration_no_recommendation_execution.py",
    "tests/test_research_artifact_registry_readiness_plan.py",
]

REQUIRED_RESEARCH_ARTIFACT_REGISTRY_FILES = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_PLANNING.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_GUARDRAILS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_METADATA_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_PROVENANCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_LIFECYCLE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_FORBIDDEN_INTERACTIONS.md",
    "docs/RESEARCH_ARTIFACT_NO_INGESTION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_NO_RECOMMENDATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_NO_EXECUTION_POLICY.md",
    "packages/core/stark_terminal_core/research_artifact_registry/__init__.py",
    "packages/core/stark_terminal_core/research_artifact_registry/README.md",
    "packages/core/stark_terminal_core/research_artifact_registry/types.py",
    "packages/core/stark_terminal_core/research_artifact_registry/metadata.py",
    "packages/core/stark_terminal_core/research_artifact_registry/references.py",
    "packages/core/stark_terminal_core/research_artifact_registry/provenance.py",
    "packages/core/stark_terminal_core/research_artifact_registry/lifecycle.py",
    "packages/core/stark_terminal_core/research_artifact_registry/placeholders.py",
    "packages/core/stark_terminal_core/research_artifact_registry/interactions.py",
    "packages/core/stark_terminal_core/research_artifact_registry/safety.py",
    "packages/core/stark_terminal_core/research_artifact_registry/readiness.py",
    "packages/core/stark_terminal_core/research_artifact_registry/health.py",
    "apps/api/stark_terminal_api/routes/research_artifact_registry.py",
    "tests/test_research_artifact_registry_settings.py",
    "tests/test_research_artifact_registry_types.py",
    "tests/test_research_artifact_registry_metadata.py",
    "tests/test_research_artifact_registry_references.py",
    "tests/test_research_artifact_registry_provenance.py",
    "tests/test_research_artifact_registry_lifecycle.py",
    "tests/test_research_artifact_registry_placeholders.py",
    "tests/test_research_artifact_registry_forbidden_interactions.py",
    "tests/test_research_artifact_registry_safety.py",
    "tests/test_research_artifact_registry_readiness.py",
    "tests/test_api_research_artifact_registry.py",
    "tests/test_research_artifact_registry_docs_status.py",
    "tests/test_research_artifact_registry_no_ingestion_or_parsing.py",
    "tests/test_research_artifact_registry_no_strategy_backtest_recommendation_execution.py",
]

REQUIRED_RESEARCH_ARTIFACT_REGISTRY_API_FILES = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_CONTRACT_SKELETON.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_UNAVAILABLE_RESPONSES.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_SAFETY_BOUNDARY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_INGESTION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_RECOMMENDATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_NO_EXECUTION_POLICY.md",
    "packages/core/stark_terminal_core/research_artifact_registry_api/__init__.py",
    "packages/core/stark_terminal_core/research_artifact_registry_api/README.md",
    "packages/core/stark_terminal_core/research_artifact_registry_api/contracts.py",
    "packages/core/stark_terminal_core/research_artifact_registry_api/requests.py",
    "packages/core/stark_terminal_core/research_artifact_registry_api/responses.py",
    "packages/core/stark_terminal_core/research_artifact_registry_api/references.py",
    "packages/core/stark_terminal_core/research_artifact_registry_api/unavailable.py",
    "packages/core/stark_terminal_core/research_artifact_registry_api/safety.py",
    "packages/core/stark_terminal_core/research_artifact_registry_api/health.py",
    "apps/api/stark_terminal_api/routes/research_artifact_registry_api.py",
    "tests/test_research_artifact_registry_api_settings.py",
    "tests/test_research_artifact_registry_api_contracts.py",
    "tests/test_research_artifact_registry_api_request_placeholders.py",
    "tests/test_research_artifact_registry_api_response_placeholders.py",
    "tests/test_research_artifact_registry_api_references.py",
    "tests/test_research_artifact_registry_api_unavailable_responses.py",
    "tests/test_research_artifact_registry_api_safety.py",
    "tests/test_api_research_artifact_registry_api.py",
    "tests/test_research_artifact_registry_api_docs_status.py",
    "tests/test_research_artifact_registry_api_no_ingestion_or_parsing.py",
    "tests/test_research_artifact_registry_api_no_strategy_backtest_recommendation_execution.py",
]

REQUIRED_RESEARCH_ARTIFACT_REGISTRY_DISPLAY_FILES = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_CONTRACT_SKELETON.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_METADATA_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_CARD_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_PROVENANCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_LIFECYCLE_BADGES.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_ACTIVE_UI_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_INGESTION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_RECOMMENDATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_NO_EXECUTION_POLICY.md",
    "packages/core/stark_terminal_core/research_artifact_registry_display/__init__.py",
    "packages/core/stark_terminal_core/research_artifact_registry_display/init.py",
    "packages/core/stark_terminal_core/research_artifact_registry_display/README.md",
    "packages/core/stark_terminal_core/research_artifact_registry_display/contracts.py",
    "packages/core/stark_terminal_core/research_artifact_registry_display/cards.py",
    "packages/core/stark_terminal_core/research_artifact_registry_display/references.py",
    "packages/core/stark_terminal_core/research_artifact_registry_display/provenance.py",
    "packages/core/stark_terminal_core/research_artifact_registry_display/lifecycle.py",
    "packages/core/stark_terminal_core/research_artifact_registry_display/badges.py",
    "packages/core/stark_terminal_core/research_artifact_registry_display/unavailable.py",
    "packages/core/stark_terminal_core/research_artifact_registry_display/safety.py",
    "packages/core/stark_terminal_core/research_artifact_registry_display/health.py",
    "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py",
    "tests/test_research_artifact_registry_display_settings.py",
    "tests/test_research_artifact_registry_display_contracts.py",
    "tests/test_research_artifact_registry_display_cards.py",
    "tests/test_research_artifact_registry_display_references.py",
    "tests/test_research_artifact_registry_display_provenance.py",
    "tests/test_research_artifact_registry_display_lifecycle.py",
    "tests/test_research_artifact_registry_display_badges.py",
    "tests/test_research_artifact_registry_display_unavailable_responses.py",
    "tests/test_research_artifact_registry_display_safety.py",
    "tests/test_api_research_artifact_registry_display.py",
    "tests/test_research_artifact_registry_display_docs_status.py",
    "tests/test_research_artifact_registry_display_no_active_ui.py",
    "tests/test_research_artifact_registry_display_no_ingestion_or_parsing.py",
    "tests/test_research_artifact_registry_display_no_strategy_backtest_recommendation_execution.py",
]

REQUIRED_RESEARCH_ARTIFACT_REGISTRY_SAFETY_AUDIT_FILES = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_SAFETY_BOUNDARY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_BOUNDARY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_MILESTONE_READINESS.md",
    "tests/test_research_artifact_registry_safety_boundary_audit_docs.py",
    "tests/test_research_artifact_registry_api_boundary_audit.py",
    "tests/test_research_artifact_registry_display_boundary_audit.py",
    "tests/test_research_artifact_registry_api_surface_safety.py",
    "tests/test_research_artifact_registry_milestone_readiness.py",
]

REQUIRED_RESEARCH_ARTIFACT_REGISTRY_MILESTONE_AUDIT_FILES = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PLANNING_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_SAFETY_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_ACTIVE_INGESTION_STORAGE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_UPLOAD_DOWNLOAD_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_ACTIVE_UI_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_PAPER_PARSING_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_STRATEGY_GENERATION_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_BACKTESTING_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_NEXT_PHASE_PLAN.md",
    "tests/test_research_artifact_registry_milestone_audit_docs.py",
    "tests/test_research_artifact_registry_planning_milestone.py",
    "tests/test_research_artifact_registry_api_milestone.py",
    "tests/test_research_artifact_registry_display_milestone.py",
    "tests/test_research_artifact_registry_safety_milestone.py",
    "tests/test_research_artifact_registry_phase_no_active_ingestion_storage.py",
    "tests/test_research_artifact_registry_phase_no_upload_download.py",
    "tests/test_research_artifact_registry_phase_no_active_ui.py",
    "tests/test_research_artifact_registry_phase_no_paper_parsing.py",
    "tests/test_research_artifact_registry_phase_no_strategy_generation.py",
    "tests/test_research_artifact_registry_phase_no_backtesting.py",
    "tests/test_research_artifact_registry_phase_no_recommendation_execution.py",
    "tests/test_research_artifact_registry_next_phase_readiness.py",
]

REQUIRED_RESEARCH_ARTIFACT_REGISTRY_BOUNDARY_FILES = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_SYSTEM_BOUNDARY_HARDENING.md",
    "docs/RESEARCH_ARTIFACT_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "docs/RESEARCH_ARTIFACT_ENDPOINT_BOUNDARY_POLICY.md",
    "docs/RESEARCH_ARTIFACT_MODULE_BOUNDARY_POLICY.md",
    "docs/RESEARCH_ARTIFACT_CROSS_MODULE_INVARIANTS.md",
    "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_INGESTION_STORAGE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_UPLOAD_DOWNLOAD_POLICY.md",
    "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
    "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_BOUNDARY_NO_EXECUTION_POLICY.md",
    "packages/core/stark_terminal_core/research_artifact_registry_boundary/__init__.py",
    "packages/core/stark_terminal_core/research_artifact_registry_boundary/init.py",
    "packages/core/stark_terminal_core/research_artifact_registry_boundary/README.md",
    "packages/core/stark_terminal_core/research_artifact_registry_boundary/forbidden.py",
    "packages/core/stark_terminal_core/research_artifact_registry_boundary/endpoints.py",
    "packages/core/stark_terminal_core/research_artifact_registry_boundary/modules.py",
    "packages/core/stark_terminal_core/research_artifact_registry_boundary/invariants.py",
    "packages/core/stark_terminal_core/research_artifact_registry_boundary/health.py",
    "apps/api/stark_terminal_api/routes/research_artifact_registry_boundary.py",
    "tests/test_research_artifact_registry_boundary_settings.py",
    "tests/test_research_artifact_registry_boundary_forbidden_registry.py",
    "tests/test_research_artifact_registry_boundary_endpoint_policy.py",
    "tests/test_research_artifact_registry_boundary_module_policy.py",
    "tests/test_research_artifact_registry_boundary_invariants.py",
    "tests/test_api_research_artifact_registry_boundary.py",
    "tests/test_research_artifact_registry_boundary_docs_status.py",
    "tests/test_research_artifact_registry_boundary_no_ingestion_storage.py",
    "tests/test_research_artifact_registry_boundary_no_upload_download.py",
    "tests/test_research_artifact_registry_boundary_no_active_ui.py",
    "tests/test_research_artifact_registry_boundary_no_paper_parsing.py",
    "tests/test_research_artifact_registry_boundary_no_strategy_generation.py",
    "tests/test_research_artifact_registry_boundary_no_backtesting.py",
    "tests/test_research_artifact_registry_boundary_no_recommendation_execution.py",
]

REQUIRED_RESEARCH_ARTIFACT_REGISTRY_API_DISPLAY_INTEGRATION_FILES = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_BOUNDARY_INTEGRATION_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_ACTIVE_INGESTION_STORAGE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_UPLOAD_DOWNLOAD_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_ACTIVE_UI_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_PAPER_PARSING_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_STRATEGY_BACKTEST_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_INDEX_READINESS_PLAN.md",
    "tests/test_research_artifact_registry_api_display_integration_audit_docs.py",
    "tests/test_research_artifact_registry_cross_endpoint_consistency.py",
    "tests/test_research_artifact_registry_api_display_boundary_integration.py",
    "tests/test_research_artifact_registry_boundary_integration.py",
    "tests/test_research_artifact_registry_integration_no_active_ingestion_storage.py",
    "tests/test_research_artifact_registry_integration_no_upload_download.py",
    "tests/test_research_artifact_registry_integration_no_active_ui.py",
    "tests/test_research_artifact_registry_integration_no_paper_parsing.py",
    "tests/test_research_artifact_registry_integration_no_strategy_backtest.py",
    "tests/test_research_artifact_registry_integration_no_recommendation_execution.py",
    "tests/test_research_artifact_index_readiness_plan.py",
]

REQUIRED_RESEARCH_ARTIFACT_INDEX_FILES = [
    "docs/RESEARCH_ARTIFACT_INDEX_PLANNING.md",
    "docs/RESEARCH_ARTIFACT_INDEX_GUARDRAILS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_METADATA_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_KEY_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_TAG_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_PROVENANCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_LIFECYCLE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_FORBIDDEN_INTERACTIONS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_INDEXING_ENGINE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_SEARCH_RANKING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_EMBEDDINGS_VECTOR_STORE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_INGESTION_STORAGE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NO_RECOMMENDATION_EXECUTION_POLICY.md",
    "packages/core/stark_terminal_core/research_artifact_index/__init__.py",
    "packages/core/stark_terminal_core/research_artifact_index/init.py",
    "packages/core/stark_terminal_core/research_artifact_index/README.md",
    "packages/core/stark_terminal_core/research_artifact_index/types.py",
    "packages/core/stark_terminal_core/research_artifact_index/metadata.py",
    "packages/core/stark_terminal_core/research_artifact_index/keys.py",
    "packages/core/stark_terminal_core/research_artifact_index/references.py",
    "packages/core/stark_terminal_core/research_artifact_index/tags.py",
    "packages/core/stark_terminal_core/research_artifact_index/provenance.py",
    "packages/core/stark_terminal_core/research_artifact_index/lifecycle.py",
    "packages/core/stark_terminal_core/research_artifact_index/interactions.py",
    "packages/core/stark_terminal_core/research_artifact_index/safety.py",
    "packages/core/stark_terminal_core/research_artifact_index/readiness.py",
    "packages/core/stark_terminal_core/research_artifact_index/health.py",
    "apps/api/stark_terminal_api/routes/research_artifact_index.py",
    "tests/test_research_artifact_index_settings.py",
    "tests/test_research_artifact_index_types.py",
    "tests/test_research_artifact_index_metadata.py",
    "tests/test_research_artifact_index_keys.py",
    "tests/test_research_artifact_index_references.py",
    "tests/test_research_artifact_index_tags.py",
    "tests/test_research_artifact_index_provenance.py",
    "tests/test_research_artifact_index_lifecycle.py",
    "tests/test_research_artifact_index_forbidden_interactions.py",
    "tests/test_research_artifact_index_safety.py",
    "tests/test_research_artifact_index_readiness.py",
    "tests/test_api_research_artifact_index.py",
    "tests/test_research_artifact_index_docs_status.py",
    "tests/test_research_artifact_index_no_indexing_search_embeddings.py",
    "tests/test_research_artifact_index_no_ingestion_parsing_strategy_execution.py",
    "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
    "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
    "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
    "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
    "docs/AUDIT_LOG_JOURNAL_TARGET.md",
    "tests/test_active_decision_architecture_target_docs.py",
    "tests/test_decision_candidate_pipeline_target_docs.py",
    "tests/test_verifier_layer_target_architecture_docs.py",
    "tests/test_no_trade_commit_language_in_active_decision_target.py",
]

REQUIRED_RESEARCH_ARTIFACT_INDEX_API_FILES = [
    "docs/RESEARCH_ARTIFACT_INDEX_API_CONTRACT_SKELETON.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_REQUEST_RESPONSE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_UNAVAILABLE_RESPONSES.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_SAFETY_BOUNDARY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_INDEXING_ENGINE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_SEARCH_RANKING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_EMBEDDINGS_VECTOR_STORE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_INGESTION_STORAGE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_API_NO_RECOMMENDATION_EXECUTION_POLICY.md",
    "packages/core/stark_terminal_core/research_artifact_index_api/__init__.py",
    "packages/core/stark_terminal_core/research_artifact_index_api/init.py",
    "packages/core/stark_terminal_core/research_artifact_index_api/README.md",
    "packages/core/stark_terminal_core/research_artifact_index_api/contracts.py",
    "packages/core/stark_terminal_core/research_artifact_index_api/requests.py",
    "packages/core/stark_terminal_core/research_artifact_index_api/responses.py",
    "packages/core/stark_terminal_core/research_artifact_index_api/references.py",
    "packages/core/stark_terminal_core/research_artifact_index_api/unavailable.py",
    "packages/core/stark_terminal_core/research_artifact_index_api/safety.py",
    "packages/core/stark_terminal_core/research_artifact_index_api/health.py",
    "apps/api/stark_terminal_api/routes/research_artifact_index_api.py",
    "tests/test_research_artifact_index_api_settings.py",
    "tests/test_research_artifact_index_api_contracts.py",
    "tests/test_research_artifact_index_api_request_placeholders.py",
    "tests/test_research_artifact_index_api_response_placeholders.py",
    "tests/test_research_artifact_index_api_references.py",
    "tests/test_research_artifact_index_api_unavailable_responses.py",
    "tests/test_research_artifact_index_api_safety.py",
    "tests/test_api_research_artifact_index_api.py",
    "tests/test_research_artifact_index_api_docs_status.py",
    "tests/test_research_artifact_index_api_no_indexing_search_embeddings.py",
    "tests/test_research_artifact_index_api_no_ingestion_parsing_strategy_execution.py",
    "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
    "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
    "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
    "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
    "docs/AUDIT_LOG_JOURNAL_TARGET.md",
    "tests/test_active_decision_architecture_target_docs.py",
    "tests/test_decision_candidate_pipeline_target_docs.py",
    "tests/test_verifier_layer_target_architecture_docs.py",
    "tests/test_no_trade_commit_language_in_active_decision_target.py",
]

REQUIRED_RESEARCH_ARTIFACT_INDEX_DISPLAY_FILES = [
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_CONTRACT_SKELETON.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_METADATA_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_CARD_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_REFERENCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_TAG_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_PROVENANCE_PLACEHOLDERS.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_LIFECYCLE_BADGES.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_UNAVAILABLE_RESPONSES.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_SAFETY_BOUNDARY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_ACTIVE_UI_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_INDEXING_ENGINE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_SEARCH_RANKING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_EMBEDDINGS_VECTOR_STORE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_INGESTION_STORAGE_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_PAPER_PARSING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_STRATEGY_GENERATION_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_BACKTESTING_POLICY.md",
    "docs/RESEARCH_ARTIFACT_INDEX_DISPLAY_NO_RECOMMENDATION_EXECUTION_POLICY.md",
    "packages/core/stark_terminal_core/research_artifact_index_display/__init__.py",
    "packages/core/stark_terminal_core/research_artifact_index_display/init.py",
    "packages/core/stark_terminal_core/research_artifact_index_display/README.md",
    "packages/core/stark_terminal_core/research_artifact_index_display/contracts.py",
    "packages/core/stark_terminal_core/research_artifact_index_display/cards.py",
    "packages/core/stark_terminal_core/research_artifact_index_display/references.py",
    "packages/core/stark_terminal_core/research_artifact_index_display/tags.py",
    "packages/core/stark_terminal_core/research_artifact_index_display/provenance.py",
    "packages/core/stark_terminal_core/research_artifact_index_display/lifecycle.py",
    "packages/core/stark_terminal_core/research_artifact_index_display/badges.py",
    "packages/core/stark_terminal_core/research_artifact_index_display/unavailable.py",
    "packages/core/stark_terminal_core/research_artifact_index_display/safety.py",
    "packages/core/stark_terminal_core/research_artifact_index_display/health.py",
    "apps/api/stark_terminal_api/routes/research_artifact_index_display.py",
    "tests/test_research_artifact_index_display_settings.py",
    "tests/test_research_artifact_index_display_contracts.py",
    "tests/test_research_artifact_index_display_cards.py",
    "tests/test_research_artifact_index_display_references.py",
    "tests/test_research_artifact_index_display_tags.py",
    "tests/test_research_artifact_index_display_provenance.py",
    "tests/test_research_artifact_index_display_lifecycle.py",
    "tests/test_research_artifact_index_display_badges.py",
    "tests/test_research_artifact_index_display_unavailable_responses.py",
    "tests/test_research_artifact_index_display_safety.py",
    "tests/test_api_research_artifact_index_display.py",
    "tests/test_research_artifact_index_display_docs_status.py",
    "tests/test_research_artifact_index_display_no_active_ui.py",
    "tests/test_research_artifact_index_display_no_indexing_search_embeddings.py",
    "tests/test_research_artifact_index_display_no_ingestion_parsing_strategy_execution.py",
    "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
    "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
    "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
    "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
    "docs/AUDIT_LOG_JOURNAL_TARGET.md",
    "tests/test_active_decision_architecture_target_docs.py",
    "tests/test_decision_candidate_pipeline_target_docs.py",
    "tests/test_verifier_layer_target_architecture_docs.py",
    "tests/test_no_trade_commit_language_in_active_decision_target.py",
]

REQUIRED_RESEARCH_ARTIFACT_INDEX_SAFETY_AUDIT_FILES = [
    "docs/RESEARCH_ARTIFACT_INDEX_SAFETY_BOUNDARY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_INDEX_MILESTONE_READINESS.md",
    "tests/test_research_artifact_index_safety_boundary_audit_docs.py",
    "tests/test_research_artifact_index_api_surface_safety.py",
    "tests/test_research_artifact_index_milestone_readiness.py",
    "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
    "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
    "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
    "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
    "docs/AUDIT_LOG_JOURNAL_TARGET.md",
    "tests/test_active_decision_architecture_target_docs.py",
    "tests/test_decision_candidate_pipeline_target_docs.py",
    "tests/test_verifier_layer_target_architecture_docs.py",
    "tests/test_no_trade_commit_language_in_active_decision_target.py",
]

REQUIRED_DOCUMENTATION_CONSOLIDATION_FILES = [
    "docs/testing/TEST_POLICY.md",
    "docs/testing/TEST_BASELINE.md",
    "docs/testing/CONSOLIDATION_MAP.md",
    "docs/phases/PHASE_DOCUMENTATION_POLICY.md",
    "docs/phases/research_artifact_index.md",
    "docs/phases/research_artifact_registry.md",
    "docs/phases/strategy_research_workspace.md",
    "docs/phases/active_decision_architecture.md",
    "docs/audits/safety_boundaries.md",
    "docs/audits/no_execution.md",
    "docs/audits/research_artifact_boundaries.md",
    "docs/reports/DOCS_CONSOLIDATED_REPORT.md",
    "docs/reports/TESTS_CONSOLIDATED_REPORT.md",
    "docs/reports/DELETED_FILES_REPORT.md",
    "docs/reports/SAFETY_COVERAGE_REPORT.md",
    "docs/reports/ACTIVE_TEST_BASELINE_REPORT.md",
    "tests/phases/test_research_artifact_index_phase.py",
    "tests/phases/test_research_artifact_registry_phase.py",
    "tests/phases/test_strategy_research_workspace_phase.py",
    "tests/phases/test_active_decision_architecture_phase.py",
    "tests/boundaries/test_no_execution_boundary.py",
    "tests/boundaries/test_research_artifact_boundaries.py",
    "tests/boundaries/test_documentation_consolidation_policy.py",
    "docs/archive/prompt_audits/README.md",
    "tests/archive/prompt_audits/README.md",
]

REQUIRED_RESEARCH_ARTIFACT_INDEX_MILESTONE_AUDIT_FILES = [
    "docs/RESEARCH_ARTIFACT_INDEX_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_INDEX_NEXT_PHASE_PLAN.md",
    "tests/phases/test_research_artifact_index_milestone_phase.py",
    "tests/boundaries/test_research_artifact_index_milestone_boundaries.py",
    "tests/boundaries/test_research_artifact_index_next_phase_readiness.py",
]

REQUIRED_RESEARCH_ARTIFACT_INDEX_BOUNDARY_FILES = [
    "docs/RESEARCH_ARTIFACT_INDEX_SYSTEM_BOUNDARY_HARDENING.md",
    "packages/core/stark_terminal_core/research_artifact_index_boundary/__init__.py",
    "packages/core/stark_terminal_core/research_artifact_index_boundary/init.py",
    "packages/core/stark_terminal_core/research_artifact_index_boundary/README.md",
    "packages/core/stark_terminal_core/research_artifact_index_boundary/forbidden.py",
    "packages/core/stark_terminal_core/research_artifact_index_boundary/endpoints.py",
    "packages/core/stark_terminal_core/research_artifact_index_boundary/modules.py",
    "packages/core/stark_terminal_core/research_artifact_index_boundary/invariants.py",
    "packages/core/stark_terminal_core/research_artifact_index_boundary/health.py",
    "apps/api/stark_terminal_api/routes/research_artifact_index_boundary.py",
    "tests/phases/test_research_artifact_index_system_boundary_phase.py",
    "tests/boundaries/test_research_artifact_index_system_boundaries.py",
    "tests/boundaries/test_api_research_artifact_index_boundary.py",
]

REQUIRED_RESEARCH_ARTIFACT_INDEX_API_DISPLAY_INTEGRATION_FILES = [
    "docs/RESEARCH_ARTIFACT_INDEX_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    "docs/RESEARCH_METADATA_GRAPH_READINESS_PLAN.md",
    "tests/phases/test_research_artifact_index_api_display_integration_phase.py",
    "tests/boundaries/test_research_artifact_index_api_display_integration_boundaries.py",
    "tests/boundaries/test_api_research_artifact_index_integration_consistency.py",
]

REQUIRED_RESEARCH_METADATA_GRAPH_PLANNING_FILES = [
    "docs/RESEARCH_METADATA_GRAPH_PLANNING_AND_GUARDRAILS.md",
    "docs/phases/research_metadata_graph.md",
    "packages/core/stark_terminal_core/research_metadata_graph/__init__.py",
    "packages/core/stark_terminal_core/research_metadata_graph/init.py",
    "packages/core/stark_terminal_core/research_metadata_graph/README.md",
    "packages/core/stark_terminal_core/research_metadata_graph/planning.py",
    "packages/core/stark_terminal_core/research_metadata_graph/nodes.py",
    "packages/core/stark_terminal_core/research_metadata_graph/edges.py",
    "packages/core/stark_terminal_core/research_metadata_graph/provenance.py",
    "packages/core/stark_terminal_core/research_metadata_graph/lifecycle.py",
    "packages/core/stark_terminal_core/research_metadata_graph/references.py",
    "packages/core/stark_terminal_core/research_metadata_graph/guardrails.py",
    "packages/core/stark_terminal_core/research_metadata_graph/readiness.py",
    "packages/core/stark_terminal_core/research_metadata_graph/health.py",
    "apps/api/stark_terminal_api/routes/research_metadata_graph.py",
    "tests/phases/test_research_metadata_graph_phase.py",
    "tests/boundaries/test_research_metadata_graph_boundaries.py",
    "tests/boundaries/test_api_research_metadata_graph.py",
]

REQUIRED_RESEARCH_METADATA_GRAPH_API_FILES = [
    "docs/RESEARCH_METADATA_GRAPH_API_CONTRACT_SKELETON.md",
    "packages/core/stark_terminal_core/research_metadata_graph_api/__init__.py",
    "packages/core/stark_terminal_core/research_metadata_graph_api/init.py",
    "packages/core/stark_terminal_core/research_metadata_graph_api/README.md",
    "packages/core/stark_terminal_core/research_metadata_graph_api/contracts.py",
    "packages/core/stark_terminal_core/research_metadata_graph_api/requests.py",
    "packages/core/stark_terminal_core/research_metadata_graph_api/responses.py",
    "packages/core/stark_terminal_core/research_metadata_graph_api/references.py",
    "packages/core/stark_terminal_core/research_metadata_graph_api/unavailable.py",
    "packages/core/stark_terminal_core/research_metadata_graph_api/safety.py",
    "packages/core/stark_terminal_core/research_metadata_graph_api/health.py",
    "apps/api/stark_terminal_api/routes/research_metadata_graph_api.py",
    "tests/phases/test_research_metadata_graph_api_phase.py",
    "tests/boundaries/test_research_metadata_graph_api_boundaries.py",
    "tests/boundaries/test_api_research_metadata_graph_contract.py",
]

REQUIRED_RESEARCH_METADATA_GRAPH_DISPLAY_FILES = [
    "docs/RESEARCH_METADATA_GRAPH_DISPLAY_CONTRACT_SKELETON.md",
    "packages/core/stark_terminal_core/research_metadata_graph_display/__init__.py",
    "packages/core/stark_terminal_core/research_metadata_graph_display/init.py",
    "packages/core/stark_terminal_core/research_metadata_graph_display/README.md",
    "packages/core/stark_terminal_core/research_metadata_graph_display/contracts.py",
    "packages/core/stark_terminal_core/research_metadata_graph_display/nodes.py",
    "packages/core/stark_terminal_core/research_metadata_graph_display/edges.py",
    "packages/core/stark_terminal_core/research_metadata_graph_display/provenance.py",
    "packages/core/stark_terminal_core/research_metadata_graph_display/lifecycle.py",
    "packages/core/stark_terminal_core/research_metadata_graph_display/references.py",
    "packages/core/stark_terminal_core/research_metadata_graph_display/unavailable.py",
    "packages/core/stark_terminal_core/research_metadata_graph_display/safety.py",
    "packages/core/stark_terminal_core/research_metadata_graph_display/health.py",
    "apps/api/stark_terminal_api/routes/research_metadata_graph_display.py",
    "tests/phases/test_research_metadata_graph_display_phase.py",
    "tests/boundaries/test_research_metadata_graph_display_boundaries.py",
    "tests/boundaries/test_api_research_metadata_graph_display.py",
]

REQUIRED_RESEARCH_METADATA_GRAPH_SAFETY_AUDIT_FILES = [
    "docs/RESEARCH_METADATA_GRAPH_SAFETY_BOUNDARY_AUDIT.md",
    "tests/phases/test_research_metadata_graph_safety_audit_phase.py",
    "tests/boundaries/test_research_metadata_graph_safety_boundaries.py",
    "tests/boundaries/test_api_research_metadata_graph_safety_surface.py",
]

REQUIRED_RESEARCH_METADATA_GRAPH_PHASE_CLOSURE_FILES = [
    "docs/phases/research_metadata_graph.md",
    "tests/phases/test_research_metadata_graph_phase_closure.py",
]

REQUIRED_RESEARCH_KNOWLEDGE_MAP_PLANNING_FILES = [
    "docs/phases/research_knowledge_map.md",
    "packages/core/stark_terminal_core/research_knowledge_map/__init__.py",
    "packages/core/stark_terminal_core/research_knowledge_map/init.py",
    "packages/core/stark_terminal_core/research_knowledge_map/README.md",
    "packages/core/stark_terminal_core/research_knowledge_map/planning.py",
    "packages/core/stark_terminal_core/research_knowledge_map/items.py",
    "packages/core/stark_terminal_core/research_knowledge_map/relationships.py",
    "packages/core/stark_terminal_core/research_knowledge_map/evidence.py",
    "packages/core/stark_terminal_core/research_knowledge_map/provenance.py",
    "packages/core/stark_terminal_core/research_knowledge_map/lifecycle.py",
    "packages/core/stark_terminal_core/research_knowledge_map/guardrails.py",
    "packages/core/stark_terminal_core/research_knowledge_map/readiness.py",
    "packages/core/stark_terminal_core/research_knowledge_map/health.py",
    "apps/api/stark_terminal_api/routes/research_knowledge_map.py",
    "tests/phases/test_research_knowledge_map_phase.py",
    "tests/boundaries/test_research_knowledge_map_boundaries.py",
    "tests/boundaries/test_api_research_knowledge_map.py",
]

REQUIRED_RESEARCH_KNOWLEDGE_MAP_API_FILES = [
    "docs/phases/research_knowledge_map.md",
    "packages/core/stark_terminal_core/research_knowledge_map_api/__init__.py",
    "packages/core/stark_terminal_core/research_knowledge_map_api/init.py",
    "packages/core/stark_terminal_core/research_knowledge_map_api/README.md",
    "packages/core/stark_terminal_core/research_knowledge_map_api/contracts.py",
    "packages/core/stark_terminal_core/research_knowledge_map_api/requests.py",
    "packages/core/stark_terminal_core/research_knowledge_map_api/responses.py",
    "packages/core/stark_terminal_core/research_knowledge_map_api/references.py",
    "packages/core/stark_terminal_core/research_knowledge_map_api/unavailable.py",
    "packages/core/stark_terminal_core/research_knowledge_map_api/safety.py",
    "packages/core/stark_terminal_core/research_knowledge_map_api/health.py",
    "apps/api/stark_terminal_api/routes/research_knowledge_map_api.py",
    "tests/phases/test_research_knowledge_map_api_phase.py",
    "tests/boundaries/test_research_knowledge_map_api_boundaries.py",
    "tests/boundaries/test_api_research_knowledge_map_contract.py",
]

REQUIRED_RESEARCH_KNOWLEDGE_MAP_DISPLAY_FILES = [
    "docs/phases/research_knowledge_map.md",
    "packages/core/stark_terminal_core/research_knowledge_map_display/__init__.py",
    "packages/core/stark_terminal_core/research_knowledge_map_display/init.py",
    "packages/core/stark_terminal_core/research_knowledge_map_display/README.md",
    "packages/core/stark_terminal_core/research_knowledge_map_display/contracts.py",
    "packages/core/stark_terminal_core/research_knowledge_map_display/items.py",
    "packages/core/stark_terminal_core/research_knowledge_map_display/relationships.py",
    "packages/core/stark_terminal_core/research_knowledge_map_display/evidence.py",
    "packages/core/stark_terminal_core/research_knowledge_map_display/provenance.py",
    "packages/core/stark_terminal_core/research_knowledge_map_display/lifecycle.py",
    "packages/core/stark_terminal_core/research_knowledge_map_display/unavailable.py",
    "packages/core/stark_terminal_core/research_knowledge_map_display/safety.py",
    "packages/core/stark_terminal_core/research_knowledge_map_display/health.py",
    "apps/api/stark_terminal_api/routes/research_knowledge_map_display.py",
    "tests/phases/test_research_knowledge_map_display_phase.py",
    "tests/boundaries/test_research_knowledge_map_display_boundaries.py",
    "tests/boundaries/test_api_research_knowledge_map_display.py",
]

REQUIRED_RESEARCH_KNOWLEDGE_MAP_SAFETY_FILES = [
    "docs/phases/research_knowledge_map.md",
    "tests/phases/test_research_knowledge_map_safety_phase.py",
    "tests/boundaries/test_research_knowledge_map_safety_boundaries.py",
    "tests/boundaries/test_api_research_knowledge_map_safety_surface.py",
]

REQUIRED_RESEARCH_KNOWLEDGE_MAP_PHASE_CLOSURE_FILES = [
    "docs/phases/research_knowledge_map.md",
    "tests/phases/test_research_knowledge_map_phase_closure.py",
]

REQUIRED_PRODUCT_SURFACE_REORIENTATION_FILES = [
    "docs/phases/product_surface_reorientation.md",
    "tests/phases/test_product_surface_reorientation_phase.py",
    "tests/boundaries/test_product_surface_reorientation_boundaries.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_FILES = [
    "docs/phases/retail_decision_console.md",
    "packages/core/stark_terminal_core/retail_decision_console/__init__.py",
    "packages/core/stark_terminal_core/retail_decision_console/init.py",
    "packages/core/stark_terminal_core/retail_decision_console/README.md",
    "packages/core/stark_terminal_core/retail_decision_console/productization.py",
    "packages/core/stark_terminal_core/retail_decision_console/ui_boundary.py",
    "packages/core/stark_terminal_core/retail_decision_console/navigation.py",
    "packages/core/stark_terminal_core/retail_decision_console/sections.py",
    "packages/core/stark_terminal_core/retail_decision_console/cards.py",
    "packages/core/stark_terminal_core/retail_decision_console/unavailable.py",
    "packages/core/stark_terminal_core/retail_decision_console/readiness.py",
    "packages/core/stark_terminal_core/retail_decision_console/health.py",
    "apps/api/stark_terminal_api/routes/retail_decision_console.py",
    "tests/phases/test_retail_decision_console_phase.py",
    "tests/boundaries/test_retail_decision_console_boundaries.py",
    "tests/boundaries/test_api_retail_decision_console.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_UI_SHELL_FILES = [
    "docs/phases/retail_decision_console.md",
    "packages/core/stark_terminal_core/retail_decision_console/ui_descriptors.py",
    "packages/core/stark_terminal_core/retail_decision_console/ui_shell.py",
    "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    "tests/phases/test_retail_decision_console_ui_shell_phase.py",
    "tests/boundaries/test_retail_decision_console_ui_shell_boundaries.py",
    "tests/boundaries/test_desktop_retail_decision_console_shell.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_DEMO_STATE_FILES = [
    "docs/phases/retail_decision_console.md",
    "packages/core/stark_terminal_core/retail_decision_console/static_state.py",
    "packages/core/stark_terminal_core/retail_decision_console/demo_state.py",
    "packages/core/stark_terminal_core/retail_decision_console/state_safety.py",
    "apps/api/stark_terminal_api/routes/retail_decision_console.py",
    "tests/phases/test_retail_decision_console_demo_state_phase.py",
    "tests/boundaries/test_retail_decision_console_demo_state_boundaries.py",
    "tests/boundaries/test_api_retail_decision_console_demo_state.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_STATIC_STATE_WIRING_FILES = [
    "docs/phases/retail_decision_console.md",
    "packages/core/stark_terminal_core/retail_decision_console/state_view_model.py",
    "packages/core/stark_terminal_core/retail_decision_console/ui_descriptors.py",
    "packages/core/stark_terminal_core/retail_decision_console/ui_shell.py",
    "packages/core/stark_terminal_core/retail_decision_console/static_state.py",
    "packages/core/stark_terminal_core/retail_decision_console/demo_state.py",
    "packages/core/stark_terminal_core/retail_decision_console/state_safety.py",
    "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    "apps/api/stark_terminal_api/routes/retail_decision_console.py",
    "tests/phases/test_retail_decision_console_static_state_wiring_phase.py",
    "tests/boundaries/test_retail_decision_console_static_state_wiring_boundaries.py",
    "tests/boundaries/test_desktop_retail_decision_console_static_state_wiring.py",
    "tests/boundaries/test_api_retail_decision_console_static_state_wiring.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_LOCAL_PREVIEW_FILES = [
    "docs/runbooks/retail_decision_console_local_preview.md",
    "docs/runbooks/retail_decision_console_manual_smoke_test.md",
    "docs/phases/retail_decision_console.md",
    "scripts/preview_retail_decision_console.py",
    "tests/phases/test_retail_decision_console_local_preview_phase.py",
    "tests/boundaries/test_retail_decision_console_local_preview_boundaries.py",
    "tests/boundaries/test_preview_retail_decision_console_script.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_VISUAL_LAYOUT_FILES = [
    "docs/phases/retail_decision_console.md",
    "docs/runbooks/retail_decision_console_local_preview.md",
    "docs/runbooks/retail_decision_console_manual_smoke_test.md",
    "packages/core/stark_terminal_core/retail_decision_console/layout.py",
    "packages/core/stark_terminal_core/retail_decision_console/state_view_model.py",
    "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    "scripts/preview_retail_decision_console.py",
    "tests/phases/test_retail_decision_console_visual_layout_phase.py",
    "tests/boundaries/test_retail_decision_console_visual_layout_boundaries.py",
    "tests/boundaries/test_desktop_retail_decision_console_visual_layout.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_STATIC_INTERACTION_FILES = [
    "docs/phases/retail_decision_console.md",
    "docs/runbooks/retail_decision_console_local_preview.md",
    "docs/runbooks/retail_decision_console_manual_smoke_test.md",
    "packages/core/stark_terminal_core/retail_decision_console/interactions.py",
    "packages/core/stark_terminal_core/retail_decision_console/state_view_model.py",
    "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    "scripts/preview_retail_decision_console.py",
    "tests/phases/test_retail_decision_console_static_interactions_phase.py",
    "tests/boundaries/test_retail_decision_console_static_interactions_boundaries.py",
    "tests/boundaries/test_desktop_retail_decision_console_static_interactions.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_PREVIEW_SNAPSHOT_FILES = [
    "docs/phases/retail_decision_console.md",
    "docs/runbooks/retail_decision_console_local_preview.md",
    "docs/runbooks/retail_decision_console_manual_smoke_test.md",
    "packages/core/stark_terminal_core/retail_decision_console/snapshot_export.py",
    "scripts/preview_retail_decision_console.py",
    "tests/phases/test_retail_decision_console_preview_snapshot_phase.py",
    "tests/boundaries/test_retail_decision_console_preview_snapshot_boundaries.py",
    "tests/boundaries/test_preview_retail_decision_console_snapshot_script.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_LOCAL_QA_BUNDLE_FILES = [
    "docs/phases/retail_decision_console.md",
    "docs/runbooks/retail_decision_console_local_preview.md",
    "docs/runbooks/retail_decision_console_manual_smoke_test.md",
    "docs/runbooks/retail_decision_console_local_qa_bundle.md",
    "packages/core/stark_terminal_core/retail_decision_console/qa_bundle.py",
    "scripts/build_retail_decision_console_qa_bundle.py",
    "tests/phases/test_retail_decision_console_local_qa_bundle_phase.py",
    "tests/boundaries/test_retail_decision_console_local_qa_bundle_boundaries.py",
    "tests/boundaries/test_build_retail_decision_console_qa_bundle_script.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_MANUAL_ACCEPTANCE_FILES = [
    "docs/phases/retail_decision_console.md",
    "docs/runbooks/retail_decision_console_local_preview.md",
    "docs/runbooks/retail_decision_console_manual_smoke_test.md",
    "docs/runbooks/retail_decision_console_local_qa_bundle.md",
    "docs/runbooks/retail_decision_console_manual_acceptance_checklist.md",
    "tests/phases/test_retail_decision_console_manual_acceptance_phase.py",
    "tests/boundaries/test_retail_decision_console_manual_acceptance_boundaries.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_INTERNAL_PREVIEW_FILES = [
    "docs/phases/retail_decision_console.md",
    "docs/runbooks/retail_decision_console_internal_preview_package.md",
    "docs/templates/retail_decision_console_internal_review_notes.md",
    "packages/core/stark_terminal_core/retail_decision_console/internal_preview_package.py",
    "scripts/build_retail_decision_console_internal_preview.py",
    "tests/phases/test_retail_decision_console_internal_preview_package_phase.py",
    "tests/boundaries/test_retail_decision_console_internal_preview_package_boundaries.py",
    "tests/boundaries/test_build_retail_decision_console_internal_preview_script.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_INTERNAL_PREVIEW_SMOKE_FILES = [
    "docs/phases/retail_decision_console.md",
    "docs/runbooks/retail_decision_console_internal_preview_package.md",
    "packages/core/stark_terminal_core/retail_decision_console/internal_preview_smoke.py",
    "scripts/smoke_verify_retail_decision_console_internal_preview.py",
    "tests/phases/test_retail_decision_console_internal_preview_smoke_phase.py",
    "tests/boundaries/test_retail_decision_console_internal_preview_smoke_boundaries.py",
    "tests/boundaries/test_smoke_verify_retail_decision_console_internal_preview_script.py",
]

REQUIRED_RETAIL_DECISION_CONSOLE_INTERNAL_PREVIEW_MILESTONE_FILES = [
    "docs/phases/retail_decision_console.md",
    "docs/runbooks/retail_decision_console_local_preview.md",
    "docs/runbooks/retail_decision_console_manual_smoke_test.md",
    "docs/runbooks/retail_decision_console_local_qa_bundle.md",
    "docs/runbooks/retail_decision_console_manual_acceptance_checklist.md",
    "docs/runbooks/retail_decision_console_internal_preview_package.md",
    "docs/templates/retail_decision_console_internal_review_notes.md",
    "scripts/preview_retail_decision_console.py",
    "scripts/build_retail_decision_console_qa_bundle.py",
    "scripts/build_retail_decision_console_internal_preview.py",
    "scripts/smoke_verify_retail_decision_console_internal_preview.py",
    "tests/phases/test_retail_decision_console_internal_preview_milestone_closure.py",
    "tests/boundaries/test_retail_decision_console_internal_preview_milestone_boundaries.py",
]

FORBIDDEN_ANALYTICS_FOUNDATION_PHRASES = (
    "import numpy",
    "from numpy",
    "import scipy",
    "from scipy",
    "import pandas",
    "from pandas",
    "import numba",
    "from numba",
    "import jax",
    "from jax",
    "import torch",
    "from torch",
    "import tensorflow",
    "from tensorflow",
    "import statsmodels",
    "from statsmodels",
    "def compute_",
    "def calculate_",
    "def generate_signal",
    "def recommend",
)

FORBIDDEN_NUMERICAL_ANALYTICS_IMPLEMENTATION_PHRASES = (
    "import numpy",
    "from numpy",
    "import scipy",
    "from scipy",
    "import pandas",
    "from pandas",
    "import numba",
    "from numba",
    "import jax",
    "from jax",
    "import torch",
    "from torch",
    "import tensorflow",
    "from tensorflow",
    "import statsmodels",
    "from statsmodels",
    "def returns",
    "def return_",
    "def volatility",
    "def drawdown",
    "def correlation",
    "def beta",
    "def indicator",
    "def generate_signal",
    "def recommend",
    "DecisionObject(",
)

FORBIDDEN_RETURNS_ROLLING_SCOPE_PHRASES = (
    "import numpy",
    "from numpy",
    "import scipy",
    "from scipy",
    "import pandas",
    "from pandas",
    "import numba",
    "from numba",
    "import jax",
    "from jax",
    "import torch",
    "from torch",
    "import tensorflow",
    "from tensorflow",
    "import statsmodels",
    "from statsmodels",
    "def volatility",
    "def drawdown",
    "def correlation",
    "def beta",
    "def indicator",
    "def backtest",
    "def generate_signal",
    "def recommend",
    "DecisionObject(",
)

FORBIDDEN_VOLATILITY_DRAWDOWN_SCOPE_PHRASES = (
    "import numpy",
    "from numpy",
    "import scipy",
    "from scipy",
    "import pandas",
    "from pandas",
    "import numba",
    "from numba",
    "import jax",
    "from jax",
    "import torch",
    "from torch",
    "import tensorflow",
    "from tensorflow",
    "import statsmodels",
    "from statsmodels",
    "def correlation",
    "def beta",
    "def indicator",
    "def backtest",
    "def regime",
    "def generate_signal",
    "def recommend",
    "DecisionObject(",
)

FORBIDDEN_RELATIONSHIP_ANALYTICS_SCOPE_PHRASES = (
    "import numpy",
    "from numpy",
    "import scipy",
    "from scipy",
    "import pandas",
    "from pandas",
    "import numba",
    "from numba",
    "import jax",
    "from jax",
    "import torch",
    "from torch",
    "import tensorflow",
    "from tensorflow",
    "import statsmodels",
    "from statsmodels",
    "def indicator",
    "def backtest",
    "def regime",
    "def generate_signal",
    "def recommend",
    "DecisionObject(",
)

FORBIDDEN_TIME_SERIES_DIAGNOSTICS_SCOPE_PHRASES = (
    "import numpy",
    "from numpy",
    "import scipy",
    "from scipy",
    "import pandas",
    "from pandas",
    "import numba",
    "from numba",
    "import jax",
    "from jax",
    "import torch",
    "from torch",
    "import tensorflow",
    "from tensorflow",
    "import statsmodels",
    "from statsmodels",
    "adfuller",
    "kpss",
    "hurst",
    "def autocorrelation",
    "def regime",
    "def indicator",
    "def backtest",
    "def generate_signal",
    "def recommend",
    "DecisionObject(",
)

FORBIDDEN_REGIME_ANALYTICS_SCOPE_PHRASES = (
    "import numpy",
    "from numpy",
    "import scipy",
    "from scipy",
    "import pandas",
    "from pandas",
    "import numba",
    "from numba",
    "import jax",
    "from jax",
    "import torch",
    "from torch",
    "import tensorflow",
    "from tensorflow",
    "import statsmodels",
    "from statsmodels",
    "from sklearn",
    "import sklearn",
    "from hmmlearn",
    "import hmmlearn",
    "from ruptures",
    "import ruptures",
    "adfuller",
    "kpss",
    "hurst",
    "def classify_regime",
    "def detect_regime",
    "def fit_",
    "def predict_",
    "def indicator",
    "def backtest",
    "def generate_signal",
    "def recommend",
    "DecisionObject(",
)

FORBIDDEN_REGIME_FEATURE_SCOPE_PHRASES = (
    "import numpy",
    "from numpy",
    "import scipy",
    "from scipy",
    "import pandas",
    "from pandas",
    "import numba",
    "from numba",
    "import jax",
    "from jax",
    "import torch",
    "from torch",
    "import tensorflow",
    "from tensorflow",
    "import statsmodels",
    "from statsmodels",
    "from sklearn",
    "import sklearn",
    "from hmmlearn",
    "import hmmlearn",
    "from ruptures",
    "import ruptures",
    "adfuller",
    "kpss",
    "hurst",
    "def compute_feature",
    "def calculate_feature",
    "def classify_regime",
    "def detect_regime",
    "def fit_",
    "def predict_",
    "FeatureValue(",
    "FeatureSnapshot(",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_DECISION_DESK_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "def generate_recommendation",
    "def generate_action",
    "def score_confidence",
    "def compute_confidence",
    "def create_decision_object",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_DECISION_EVIDENCE_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "def generate_decision_object",
    "def generate_recommendation",
    "def generate_action",
    "def score_confidence",
    "def compute_confidence",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_DECISION_SAFETY_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "def approve_decision",
    "def generate_decision_object",
    "def generate_recommendation",
    "def generate_action",
    "def score_confidence",
    "def compute_confidence",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_DECISION_API_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "def approve_decision",
    "def override_decision",
    "def generate_decision_object",
    "def generate_recommendation",
    "def generate_action",
    "def score_confidence",
    "def compute_confidence",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_DECISION_READINESS_API_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "def approve_decision",
    "def override_decision",
    "def generate_decision_object",
    "def generate_recommendation",
    "def generate_action",
    "def generate_readiness_status",
    "def score_confidence",
    "def compute_confidence",
    "def render_active_widget",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_DECISION_DISPLAY_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "def approve_decision",
    "def override_decision",
    "def generate_decision_object",
    "def generate_recommendation",
    "def generate_action",
    "def generate_readiness_status",
    "def build_active_decision_card",
    "def score_confidence",
    "def compute_confidence",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_DECISION_EVIDENCE_VALIDATION_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "def approve_decision",
    "def override_decision",
    "def generate_decision_object",
    "def generate_recommendation",
    "def generate_action",
    "def generate_readiness_status",
    "def score_confidence",
    "def compute_confidence",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_DECISION_HUMAN_REVIEW_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "def approve_decision",
    "def override_decision",
    "def assign_review_task",
    "def authenticate_reviewer",
    "def send_review_notification",
    "def generate_decision_object",
    "def generate_recommendation",
    "def generate_action",
    "def generate_readiness_status",
    "def score_confidence",
    "def compute_confidence",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_DECISION_BOUNDARY_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "def approve_decision",
    "def override_decision",
    "def assign_review_task",
    "def authenticate_reviewer",
    "def send_review_notification",
    "def generate_decision_object",
    "def generate_recommendation",
    "def generate_action",
    "def generate_readiness_status",
    "def build_active_decision_card",
    "def score_confidence",
    "def compute_confidence",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_DECISION_INTEGRATION_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "def approve_decision",
    "def override_decision",
    "def assign_review_task",
    "def authenticate_reviewer",
    "def send_review_notification",
    "def generate_decision_object",
    "def generate_recommendation",
    "def generate_action",
    "def generate_readiness_status",
    "def build_active_decision_card",
    "def score_confidence",
    "def compute_confidence",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_RETAIL_DASHBOARD_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "import PySide6",
    "from PySide6",
    "import tkinter",
    "from tkinter",
    "def generate_dashboard_recommendation",
    "def build_active_dashboard",
    "def create_order_button",
    "def approve_decision",
    "def override_decision",
    "def generate_decision_object",
    "def generate_recommendation",
    "def generate_action",
    "def generate_readiness_status",
    "def score_confidence",
    "def compute_confidence",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_RETAIL_TRADER_EXPERIENCE_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "import PySide6",
    "from PySide6",
    "import tkinter",
    "from tkinter",
    "def generate_trader_recommendation",
    "def build_active_experience",
    "def render_active_experience",
    "def create_order_button",
    "def approve_decision",
    "def override_decision",
    "def generate_decision_object",
    "def generate_recommendation",
    "def generate_action",
    "def generate_readiness_status",
    "def build_suitability_profile",
    "def score_confidence",
    "def compute_confidence",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_STRATEGY_RESEARCH_WORKSPACE_SCOPE_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
    "import PySide6",
    "from PySide6",
    "import tkinter",
    "from tkinter",
    "import fitz",
    "import pypdf",
    "import pdfplumber",
    "import arxiv",
    "import openai",
    "import langchain",
    "import pandas",
    "from pandas",
    "def ingest_paper",
    "def parse_paper",
    "def generate_strategy",
    "def generate_strategy_code",
    "def run_backtest",
    "def optimize_strategy",
    "def generate_recommendation",
    "def score_confidence",
    "def compute_confidence",
    "def generate_decision_object",
    "def generate_readiness_status",
    "def create_order_button",
    "def render_active_workspace",
    "def execute_trade",
    "DecisionObject(",
    "@router.post",
)

FORBIDDEN_HEAVY_ANALYTICS_DEPENDENCIES = {
    "numpy",
    "scipy",
    "pandas",
    "numba",
    "jax",
    "cupy",
    "torch",
    "tensorflow",
    "xgboost",
    "lightgbm",
    "catboost",
    "quantlib",
    "statsmodels",
    "arch",
    "scikit-learn",
    "sklearn",
    "hmmlearn",
    "ruptures",
    "vectorbt",
    "backtrader",
}

PROVIDER_EXTERNAL_IMPORT_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
)

ANALYTICS_EXTERNAL_IMPORT_PHRASES = PROVIDER_EXTERNAL_IMPORT_PHRASES

FORBIDDEN_ANALYTICS_ACTION_TERMS = (
    "buy",
    "sell",
    "hold",
    "watch",
    "avoid",
)

FORBIDDEN_PROVIDER_DEPENDENCIES = (
    "kiteconnect",
    "upstox",
    "nsepython",
    "nsepy",
    "yfinance",
    "beautifulsoup",
    "bs4",
    "selenium",
    "scrapy",
    "alpaca-trade-api",
    "ib_insync",
    "ccxt",
)

FORBIDDEN_DECISION_PHASE2_DEPENDENCIES = (
    "streamlit",
    "gradio",
    "dash",
    "plotly-dash",
    "fastapi-users",
    "authlib",
    "passlib",
    "python-jose",
    "pyjwt",
    "sendgrid",
    "twilio",
    "celery",
    "dramatiq",
    "rq",
    "temporalio",
    "prefect",
    "apache-airflow",
    "airflow",
)


@dataclass(frozen=True)
class AuditResult:
    name: str
    passed: bool
    detail: str


def _exists(path: str) -> bool:
    return (ROOT / path).exists()


def _docs_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").rglob("*.md"))


def _check_required_docs() -> AuditResult:
    missing = [path for path in REQUIRED_DOCS if not _exists(path)]
    return AuditResult("required docs", not missing, ", ".join(missing) if missing else "all required docs present")


def _check_required_dirs() -> AuditResult:
    missing = [path for path in REQUIRED_PACKAGE_DIRS if not (ROOT / path).is_dir()]
    return AuditResult("required package dirs", not missing, ", ".join(missing) if missing else "all required dirs present")


def _check_required_routes() -> AuditResult:
    missing = [path for path in REQUIRED_ROUTE_FILES if not _exists(path)]
    return AuditResult("required API routes", not missing, ", ".join(missing) if missing else "all required route files present")


def _check_forbidden_route_names() -> AuditResult:
    bad: list[str] = []
    for route in (ROOT / "apps/api/stark_terminal_api/routes").glob("*.py"):
        lowered = route.name.lower()
        if any(term in lowered for term in FORBIDDEN_ROUTE_TERMS):
            bad.append(route.name)
    return AuditResult("forbidden route names", not bad, ", ".join(bad) if bad else "no forbidden route file names")


def _check_required_data_foundation_files() -> AuditResult:
    missing = [path for path in REQUIRED_DATA_FOUNDATION_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 14-25 data foundation/provider readiness artifacts present"
    return AuditResult("data foundation files", not missing, detail)


def _check_required_analytics_foundation_files() -> AuditResult:
    missing = [path for path in REQUIRED_ANALYTICS_FOUNDATION_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 26 analytics foundation artifacts present"
    return AuditResult("analytics foundation files", not missing, detail)


def _check_required_numerical_analytics_files() -> AuditResult:
    missing = [path for path in REQUIRED_NUMERICAL_ANALYTICS_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 27 numerical analytics artifacts present"
    return AuditResult("numerical analytics files", not missing, detail)


def _check_required_returns_rolling_analytics_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETURNS_ROLLING_ANALYTICS_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 28 returns and rolling analytics artifacts present"
    return AuditResult("returns rolling analytics files", not missing, detail)


def _check_required_volatility_drawdown_analytics_files() -> AuditResult:
    missing = [path for path in REQUIRED_VOLATILITY_DRAWDOWN_ANALYTICS_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 29 volatility/drawdown analytics artifacts present"
    return AuditResult("volatility drawdown analytics files", not missing, detail)


def _check_required_analytics_milestone_audit_files() -> AuditResult:
    missing = [path for path in REQUIRED_ANALYTICS_MILESTONE_AUDIT_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 30 analytics milestone audit artifacts present"
    return AuditResult("analytics milestone audit files", not missing, detail)


def _check_required_correlation_beta_analytics_files() -> AuditResult:
    missing = [path for path in REQUIRED_CORRELATION_BETA_ANALYTICS_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 31 correlation/beta analytics artifacts present"
    return AuditResult("correlation beta analytics files", not missing, detail)


def _check_required_time_series_diagnostics_files() -> AuditResult:
    missing = [path for path in REQUIRED_TIME_SERIES_DIAGNOSTICS_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 32 time-series diagnostics artifacts present"
    return AuditResult("time-series diagnostics files", not missing, detail)


def _check_required_regime_analytics_files() -> AuditResult:
    missing = [path for path in REQUIRED_REGIME_ANALYTICS_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 33 regime analytics planning artifacts present"
    return AuditResult("regime analytics files", not missing, detail)


def _check_required_regime_feature_preparation_files() -> AuditResult:
    missing = [path for path in REQUIRED_REGIME_FEATURE_PREPARATION_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 34 regime feature preparation artifacts present"
    return AuditResult("regime feature preparation files", not missing, detail)


def _check_required_analytics_regime_milestone_audit_files() -> AuditResult:
    missing = [path for path in REQUIRED_ANALYTICS_REGIME_MILESTONE_AUDIT_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 35 analytics/regime milestone audit artifacts present"
    return AuditResult("analytics regime milestone audit files", not missing, detail)


def _check_required_retail_decision_desk_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_DECISION_DESK_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 36 Retail Decision Desk planning artifacts present"
    return AuditResult("retail decision desk files", not missing, detail)


def _check_required_decision_evidence_files() -> AuditResult:
    missing = [path for path in REQUIRED_DECISION_EVIDENCE_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 38 DecisionObject evidence bundle artifacts present"
    return AuditResult("decision evidence files", not missing, detail)


def _check_required_decision_safety_files() -> AuditResult:
    missing = [path for path in REQUIRED_DECISION_SAFETY_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 39 Decision Safety and Human-Review Guardrail artifacts present"
    return AuditResult("decision safety files", not missing, detail)


def _check_required_decision_api_files() -> AuditResult:
    missing = [path for path in REQUIRED_DECISION_API_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 40 Decision Desk API Contract Skeleton artifacts present"
    return AuditResult("decision API files", not missing, detail)


def _check_required_decision_desk_milestone_audit_files() -> AuditResult:
    missing = [path for path in REQUIRED_DECISION_DESK_MILESTONE_AUDIT_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 41 Decision Desk milestone audit artifacts present"
    return AuditResult("decision desk milestone audit files", not missing, detail)


def _check_required_decision_readiness_api_files() -> AuditResult:
    missing = [path for path in REQUIRED_DECISION_READINESS_API_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 42 Decision Desk Readiness API Skeleton artifacts present"
    return AuditResult("decision readiness API files", not missing, detail)


def _check_required_decision_display_files() -> AuditResult:
    missing = [path for path in REQUIRED_DECISION_DISPLAY_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 43 Decision Desk Display Contract Skeleton artifacts present"
    return AuditResult("decision display files", not missing, detail)


def _check_required_decision_evidence_validation_files() -> AuditResult:
    missing = [path for path in REQUIRED_DECISION_EVIDENCE_VALIDATION_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 44 Decision Desk Evidence Bundle Validation v0 artifacts present"
    return AuditResult("decision evidence validation files", not missing, detail)


def _check_required_decision_human_review_files() -> AuditResult:
    missing = [path for path in REQUIRED_DECISION_HUMAN_REVIEW_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 45 Decision Desk Human Review Workflow Skeleton artifacts present"
    return AuditResult("decision human review files", not missing, detail)


def _check_required_decision_desk_milestone_audit_2_files() -> AuditResult:
    missing = [path for path in REQUIRED_DECISION_DESK_MILESTONE_AUDIT_2_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 46 Decision Desk Milestone Audit 2 artifacts present"
    return AuditResult("decision desk milestone audit 2 files", not missing, detail)


def _check_required_decision_boundary_files() -> AuditResult:
    missing = [path for path in REQUIRED_DECISION_BOUNDARY_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 47 Decision Desk System Boundary Hardening artifacts present"
    return AuditResult("decision boundary files", not missing, detail)


def _check_required_decision_api_display_integration_audit_files() -> AuditResult:
    missing = [path for path in REQUIRED_DECISION_API_DISPLAY_INTEGRATION_AUDIT_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 48 Decision Desk API/Display Integration Readiness Audit artifacts present"
    )
    return AuditResult("decision API/display integration audit files", not missing, detail)


def _check_required_retail_dashboard_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_DASHBOARD_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 49 Retail Dashboard Planning and Guardrails artifacts present"
    return AuditResult("retail dashboard planning files", not missing, detail)


def _check_required_retail_dashboard_api_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_DASHBOARD_API_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 50 Retail Dashboard API Contract Skeleton artifacts present"
    return AuditResult("retail dashboard API files", not missing, detail)


def _check_required_retail_dashboard_display_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_DASHBOARD_DISPLAY_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 51 Retail Dashboard Display Contract Skeleton artifacts present"
    )
    return AuditResult("retail dashboard display files", not missing, detail)


def _check_required_retail_dashboard_safety_audit_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_DASHBOARD_SAFETY_AUDIT_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 52 Retail Dashboard Safety Boundary Audit artifacts present"
    )
    return AuditResult("retail dashboard safety boundary audit files", not missing, detail)


def _check_required_retail_dashboard_milestone_audit_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_DASHBOARD_MILESTONE_AUDIT_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 53 Retail Dashboard Milestone Audit artifacts present"
    )
    return AuditResult("retail dashboard milestone audit files", not missing, detail)


def _check_required_retail_dashboard_boundary_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_DASHBOARD_BOUNDARY_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 54 Retail Dashboard System Boundary Hardening artifacts present"
    )
    return AuditResult("retail dashboard boundary hardening files", not missing, detail)


def _check_required_retail_dashboard_api_display_integration_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_DASHBOARD_API_DISPLAY_INTEGRATION_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 55 Retail Dashboard API/Display Integration Readiness Audit artifacts present"
    )
    return AuditResult("retail dashboard api display integration files", not missing, detail)


def _check_required_retail_trader_experience_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_TRADER_EXPERIENCE_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 56 Retail Trader Experience Planning and Guardrails artifacts present"
    )
    return AuditResult("retail trader experience planning files", not missing, detail)


def _check_required_retail_trader_experience_api_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_TRADER_EXPERIENCE_API_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 57 Retail Trader Experience API Contract Skeleton artifacts present"
    )
    return AuditResult("retail trader experience api skeleton files", not missing, detail)


def _check_required_retail_trader_experience_display_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_TRADER_EXPERIENCE_DISPLAY_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 58 Retail Trader Experience Display Contract Skeleton artifacts present"
    )
    return AuditResult("retail trader experience display skeleton files", not missing, detail)


def _check_required_retail_trader_experience_safety_audit_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_TRADER_EXPERIENCE_SAFETY_AUDIT_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 59 Retail Trader Experience Safety Boundary Audit artifacts present"
    )
    return AuditResult("retail trader experience safety audit files", not missing, detail)


def _check_required_retail_trader_experience_milestone_audit_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_TRADER_EXPERIENCE_MILESTONE_AUDIT_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 60 Retail Trader Experience Milestone Audit artifacts present"
    )
    return AuditResult("retail trader experience milestone audit files", not missing, detail)


def _check_required_retail_trader_experience_boundary_files() -> AuditResult:
    missing = [path for path in REQUIRED_RETAIL_TRADER_EXPERIENCE_BOUNDARY_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 61 Retail Trader Experience System Boundary Hardening artifacts present"
    )
    return AuditResult("retail trader experience boundary hardening files", not missing, detail)


def _check_required_retail_trader_experience_api_display_integration_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_TRADER_EXPERIENCE_API_DISPLAY_INTEGRATION_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 62 Retail Trader Experience API/Display Integration Readiness Audit artifacts present"
    )
    return AuditResult("retail trader experience api display integration files", not missing, detail)


def _check_required_strategy_research_workspace_files() -> AuditResult:
    missing = [path for path in REQUIRED_STRATEGY_RESEARCH_WORKSPACE_FILES if not _exists(path)]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 63 Strategy Research Workspace Planning and Guardrails artifacts present"
    )
    return AuditResult("strategy research workspace files", not missing, detail)


def _check_required_strategy_research_workspace_api_files() -> AuditResult:
    missing = [
        path for path in REQUIRED_STRATEGY_RESEARCH_WORKSPACE_API_FILES if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 64 Strategy Research Workspace API Contract Skeleton artifacts present"
    )
    return AuditResult("strategy research workspace api files", not missing, detail)


def _check_required_strategy_research_workspace_display_files() -> AuditResult:
    missing = [
        path for path in REQUIRED_STRATEGY_RESEARCH_WORKSPACE_DISPLAY_FILES if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 65 Strategy Research Workspace Display Contract Skeleton artifacts present"
    )
    return AuditResult("strategy research workspace display files", not missing, detail)


def _check_required_strategy_research_workspace_safety_audit_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_STRATEGY_RESEARCH_WORKSPACE_SAFETY_AUDIT_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 66 Strategy Research Workspace Safety Boundary Audit artifacts present"
    )
    return AuditResult("strategy research workspace safety audit files", not missing, detail)


def _check_required_strategy_research_workspace_milestone_audit_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_STRATEGY_RESEARCH_WORKSPACE_MILESTONE_AUDIT_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 67 Strategy Research Workspace Milestone Audit artifacts present"
    )
    return AuditResult("strategy research workspace milestone audit files", not missing, detail)


def _check_required_strategy_research_workspace_boundary_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_STRATEGY_RESEARCH_WORKSPACE_BOUNDARY_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 68 Strategy Research Workspace System Boundary Hardening artifacts present"
    )
    return AuditResult("strategy research workspace boundary hardening files", not missing, detail)


def _check_required_strategy_research_workspace_api_display_integration_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_STRATEGY_RESEARCH_WORKSPACE_API_DISPLAY_INTEGRATION_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 69 Strategy Research Workspace API/Display Integration Readiness Audit artifacts present"
    )
    return AuditResult("strategy research workspace api display integration files", not missing, detail)


def _check_required_research_artifact_registry_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 70 Research Artifact Registry Planning and Guardrails artifacts present"
    )
    return AuditResult("research artifact registry files", not missing, detail)


def _check_required_research_artifact_registry_api_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_API_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 71 Research Artifact Registry API Contract Skeleton artifacts present"
    )
    return AuditResult("research artifact registry api files", not missing, detail)


def _check_required_research_artifact_registry_display_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_DISPLAY_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 72 Research Artifact Registry Display Contract Skeleton artifacts present"
    )
    return AuditResult("research artifact registry display files", not missing, detail)


def _check_required_research_artifact_registry_safety_audit_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_SAFETY_AUDIT_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 73 Research Artifact Registry Safety Boundary Audit artifacts present"
    )
    return AuditResult("research artifact registry safety audit files", not missing, detail)


def _check_required_research_artifact_registry_milestone_audit_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_MILESTONE_AUDIT_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 74 Research Artifact Registry Milestone Audit artifacts present"
    )
    return AuditResult("research artifact registry milestone audit files", not missing, detail)


def _check_required_research_artifact_registry_boundary_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_BOUNDARY_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 75 Research Artifact Registry System Boundary Hardening artifacts present"
    )
    return AuditResult("research artifact registry boundary files", not missing, detail)


def _check_required_research_artifact_registry_api_display_integration_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_API_DISPLAY_INTEGRATION_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 76 Research Artifact Registry API/Display Integration Readiness Audit artifacts present"
    )
    return AuditResult("research artifact registry api display integration files", not missing, detail)


def _check_required_research_artifact_index_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_INDEX_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 77 Research Artifact Index Planning and Guardrails artifacts present"
    )
    return AuditResult("research artifact index files", not missing, detail)


def _check_required_research_artifact_index_api_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_INDEX_API_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 78 Research Artifact Index API Contract Skeleton artifacts present"
    )
    return AuditResult("research artifact index api files", not missing, detail)


def _check_required_research_artifact_index_display_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_INDEX_DISPLAY_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 79 Research Artifact Index Display Contract Skeleton artifacts present"
    )
    return AuditResult("research artifact index display files", not missing, detail)


def _check_required_research_artifact_index_safety_audit_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_INDEX_SAFETY_AUDIT_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 80 Research Artifact Index Safety Boundary Audit artifacts present"
    )
    return AuditResult("research artifact index safety audit files", not missing, detail)


def _check_required_documentation_consolidation_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_DOCUMENTATION_CONSOLIDATION_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "documentation/test consolidation interlude artifacts present"
    )
    return AuditResult("documentation consolidation files", not missing, detail)


def _check_required_research_artifact_index_milestone_audit_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_INDEX_MILESTONE_AUDIT_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 81 Research Artifact Index Milestone Audit artifacts present"
    )
    return AuditResult("research artifact index milestone audit files", not missing, detail)


def _check_required_research_artifact_index_boundary_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_INDEX_BOUNDARY_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 82 Research Artifact Index System Boundary Hardening artifacts present"
    )
    return AuditResult("research artifact index boundary files", not missing, detail)


def _check_required_research_artifact_index_api_display_integration_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_ARTIFACT_INDEX_API_DISPLAY_INTEGRATION_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 83 Research Artifact Index API/Display Integration Readiness Audit artifacts present"
    )
    return AuditResult("research artifact index api display integration files", not missing, detail)


def _check_required_research_metadata_graph_planning_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_METADATA_GRAPH_PLANNING_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 84 Research Metadata Graph Planning and Guardrails artifacts present"
    )
    return AuditResult("research metadata graph planning files", not missing, detail)


def _check_required_research_metadata_graph_api_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_METADATA_GRAPH_API_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 85 Research Metadata Graph API Contract Skeleton artifacts present"
    )
    return AuditResult("research metadata graph api files", not missing, detail)


def _check_required_research_metadata_graph_display_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_METADATA_GRAPH_DISPLAY_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 86 Research Metadata Graph Display Contract Skeleton artifacts present"
    )
    return AuditResult("research metadata graph display files", not missing, detail)


def _check_required_research_metadata_graph_safety_audit_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_METADATA_GRAPH_SAFETY_AUDIT_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 87 Research Metadata Graph Safety Boundary Audit artifacts present"
    )
    return AuditResult("research metadata graph safety audit files", not missing, detail)


def _check_required_research_metadata_graph_phase_closure_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_METADATA_GRAPH_PHASE_CLOSURE_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 88-B Research Metadata Graph phase closure artifacts present"
    )
    return AuditResult("research metadata graph phase closure files", not missing, detail)


def _check_required_research_knowledge_map_planning_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_KNOWLEDGE_MAP_PLANNING_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 89 Research Knowledge Map Planning and Guardrails artifacts present"
    )
    return AuditResult("research knowledge map planning files", not missing, detail)


def _check_required_research_knowledge_map_api_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_KNOWLEDGE_MAP_API_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 90 Research Knowledge Map API Contract Skeleton artifacts present"
    )
    return AuditResult("research knowledge map api files", not missing, detail)


def _check_required_research_knowledge_map_display_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_KNOWLEDGE_MAP_DISPLAY_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 91 Research Knowledge Map Display Contract Skeleton artifacts present"
    )
    return AuditResult("research knowledge map display files", not missing, detail)


def _check_required_research_knowledge_map_safety_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_KNOWLEDGE_MAP_SAFETY_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 92 Research Knowledge Map Safety Boundary Audit artifacts present"
    )
    return AuditResult("research knowledge map safety audit files", not missing, detail)


def _check_required_research_knowledge_map_phase_closure_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RESEARCH_KNOWLEDGE_MAP_PHASE_CLOSURE_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 93 Research Knowledge Map Phase Closure artifacts present"
    )
    return AuditResult("research knowledge map phase closure files", not missing, detail)


def _check_required_product_surface_reorientation_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_PRODUCT_SURFACE_REORIENTATION_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 94 Product Surface Reorientation artifacts present"
    )
    return AuditResult("product surface reorientation files", not missing, detail)


def _check_required_retail_decision_console_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 95 Retail Decision Console Productization Plan artifacts present"
    )
    return AuditResult("retail decision console files", not missing, detail)


def _check_required_retail_decision_console_ui_shell_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_UI_SHELL_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 96 Retail Decision Console UI Shell Skeleton artifacts present"
    )
    return AuditResult("retail decision console ui shell files", not missing, detail)


def _check_required_retail_decision_console_demo_state_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_DEMO_STATE_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 97 Retail Decision Console Demo Static State artifacts present"
    )
    return AuditResult("retail decision console demo state files", not missing, detail)


def _check_required_retail_decision_console_static_state_wiring_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_STATIC_STATE_WIRING_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 98 Retail Decision Console Static State Wiring artifacts present"
    )
    return AuditResult("retail decision console static state wiring files", not missing, detail)


def _check_required_retail_decision_console_local_preview_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_LOCAL_PREVIEW_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 99 Retail Decision Console Local Preview artifacts present"
    )
    return AuditResult("retail decision console local preview files", not missing, detail)


def _check_required_retail_decision_console_visual_layout_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_VISUAL_LAYOUT_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 100 Retail Decision Console Visual Layout artifacts present"
    )
    return AuditResult("retail decision console visual layout files", not missing, detail)


def _check_required_retail_decision_console_static_interaction_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_STATIC_INTERACTION_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 101 Retail Decision Console Static Interaction artifacts present"
    )
    return AuditResult("retail decision console static interaction files", not missing, detail)


def _check_required_retail_decision_console_preview_snapshot_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_PREVIEW_SNAPSHOT_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 102 Retail Decision Console Preview Snapshot artifacts present"
    )
    return AuditResult("retail decision console preview snapshot files", not missing, detail)


def _check_required_retail_decision_console_local_qa_bundle_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_LOCAL_QA_BUNDLE_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 103 Retail Decision Console Local QA Bundle artifacts present"
    )
    return AuditResult("retail decision console local QA bundle files", not missing, detail)


def _check_required_retail_decision_console_manual_acceptance_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_MANUAL_ACCEPTANCE_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 104 Retail Decision Console Manual Acceptance Checklist artifacts present"
    )
    return AuditResult("retail decision console manual acceptance files", not missing, detail)


def _check_required_retail_decision_console_internal_preview_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_INTERNAL_PREVIEW_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 105 Retail Decision Console Shareable Internal Preview Package artifacts present"
    )
    return AuditResult("retail decision console internal preview package files", not missing, detail)


def _check_required_retail_decision_console_internal_preview_smoke_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_INTERNAL_PREVIEW_SMOKE_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 106 Retail Decision Console Internal Preview Smoke Verification artifacts present"
    )
    return AuditResult("retail decision console internal preview smoke files", not missing, detail)


def _check_required_retail_decision_console_internal_preview_milestone_files() -> AuditResult:
    missing = [
        path
        for path in REQUIRED_RETAIL_DECISION_CONSOLE_INTERNAL_PREVIEW_MILESTONE_FILES
        if not _exists(path)
    ]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 107 Retail Decision Console Internal Preview Milestone Closure artifacts present"
    )
    return AuditResult("retail decision console internal preview milestone files", not missing, detail)


def _check_forbidden_data_file_names() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "apps/api/stark_terminal_api/routes",
        ROOT / "packages/core/stark_terminal_core/domain",
        ROOT / "packages/data_platform/stark_terminal_data_platform",
    ]
    for root in roots:
        for path in root.rglob("*.py"):
            lowered = path.name.lower()
            if any(term in lowered for term in FORBIDDEN_DATA_FILE_TERMS):
                bad.append(str(path.relative_to(ROOT)))
    detail = ", ".join(bad) if bad else "no forbidden data foundation file names"
    return AuditResult("forbidden data file names", not bad, detail)


def _check_required_safety_phrases() -> AuditResult:
    docs_text = _docs_text()
    missing = [phrase for phrase in REQUIRED_SAFETY_PHRASES if phrase not in docs_text]
    return AuditResult("safety phrases", not missing, ", ".join(missing) if missing else "required safety phrases present")


def _check_provider_modules_no_external_imports() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/data_platform/stark_terminal_data_platform/providers",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    provider_route_names = {
        "provider_guardrails.py",
        "provider_readiness.py",
        "local_sample_provider.py",
        "local_file_provider.py",
    }
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in provider_route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in PROVIDER_EXTERNAL_IMPORT_PHRASES:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "provider modules import no external-call clients"
    return AuditResult("provider external imports", not bad, detail)


def _check_provider_dependency_boundaries() -> AuditResult:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    bad = [dependency for dependency in FORBIDDEN_PROVIDER_DEPENDENCIES if dependency in text]
    detail = ", ".join(bad) if bad else "no provider SDK, scraping, or broker/trading dependencies"
    return AuditResult("provider dependencies", not bad, detail)


def _check_decision_phase2_dependency_boundaries() -> AuditResult:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    bad = [dependency for dependency in FORBIDDEN_DECISION_PHASE2_DEPENDENCIES if dependency in text]
    detail = ", ".join(bad) if bad else "no UI, auth, notification, workflow/orchestration, provider SDK, scraping, or broker/trading dependencies added for decision phase 2"
    return AuditResult("decision phase 2 dependencies", not bad, detail)


def _project_dependencies() -> set[str]:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = data.get("project", {}).get("dependencies", [])
    names: set[str] = set()
    for dependency in dependencies:
        name = dependency.split("[", 1)[0].split(">", 1)[0].split("=", 1)[0].split("<", 1)[0].strip().lower()
        names.add(name)
    return names


def _check_analytics_foundation_no_calculations() -> AuditResult:
    bad: list[str] = []
    foundation_root = ROOT / "packages/analytics/stark_terminal_analytics/foundation"
    for path in foundation_root.glob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_ANALYTICS_FOUNDATION_PHRASES:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "analytics foundation contains no calculations or heavy imports"
    return AuditResult("analytics foundation no calculations", not bad, detail)


def _check_numerical_analytics_no_market_calculations() -> AuditResult:
    bad: list[str] = []
    numerical_root = ROOT / "packages/analytics/stark_terminal_analytics/numerical"
    for path in numerical_root.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in FORBIDDEN_NUMERICAL_ANALYTICS_IMPLEMENTATION_PHRASES:
            haystack = text if phrase == "DecisionObject(" else lowered
            needle = phrase if phrase == "DecisionObject(" else phrase.lower()
            if needle in haystack:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "numerical analytics contains no market analytics, signals, DecisionObject generation, or heavy imports"
    return AuditResult("numerical analytics no market calculations", not bad, detail)


def _check_returns_rolling_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/analytics/stark_terminal_analytics/returns",
        ROOT / "packages/analytics/stark_terminal_analytics/rolling",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_RETURNS_ROLLING_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "returns/rolling contains no forbidden analytics, signals, DecisionObject generation, or heavy imports"
    return AuditResult("returns rolling analytics scope", not bad, detail)


def _check_volatility_drawdown_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/analytics/stark_terminal_analytics/volatility",
        ROOT / "packages/analytics/stark_terminal_analytics/drawdown",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_VOLATILITY_DRAWDOWN_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "volatility/drawdown contains no forbidden analytics, signals, DecisionObject generation, or heavy imports"
    return AuditResult("volatility drawdown analytics scope", not bad, detail)


def _check_relationship_analytics_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/analytics/stark_terminal_analytics/correlation",
        ROOT / "packages/analytics/stark_terminal_analytics/beta",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_RELATIONSHIP_ANALYTICS_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "correlation/beta contains no indicators, backtests, regimes, signals, DecisionObject generation, or heavy imports"
    return AuditResult("correlation beta analytics scope", not bad, detail)


def _check_time_series_diagnostics_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    root = ROOT / "packages/analytics/stark_terminal_analytics/diagnostics"
    for path in root.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in FORBIDDEN_TIME_SERIES_DIAGNOSTICS_SCOPE_PHRASES:
            haystack = text if phrase == "DecisionObject(" else lowered
            needle = phrase if phrase == "DecisionObject(" else phrase.lower()
            if needle in haystack:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "time-series diagnostics contains no stationarity tests, regimes, indicators, backtests, signals, DecisionObject generation, or heavy imports"
    return AuditResult("time-series diagnostics scope", not bad, detail)


def _check_regime_analytics_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    root = ROOT / "packages/analytics/stark_terminal_analytics/regime"
    for path in root.glob("*.py"):
        if path.name == "dependencies.py":
            continue
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        for phrase in FORBIDDEN_REGIME_ANALYTICS_SCOPE_PHRASES:
            haystack = text if phrase == "DecisionObject(" else lowered
            needle = phrase if phrase == "DecisionObject(" else phrase.lower()
            if needle in haystack:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "regime planning contains no classification, stationarity tests, regimes, indicators, backtests, signals, DecisionObject generation, or heavy imports"
    return AuditResult("regime analytics scope", not bad, detail)


def _check_regime_feature_preparation_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/analytics/stark_terminal_analytics/regime_features",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "regime_features.py":
                continue
            if path.name == "dependencies.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_REGIME_FEATURE_SCOPE_PHRASES:
                haystack = text if phrase in {"DecisionObject(", "FeatureValue(", "FeatureSnapshot("} else lowered
                needle = phrase if phrase in {"DecisionObject(", "FeatureValue(", "FeatureSnapshot("} else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "regime feature preparation contains no feature computation, registry writes, classification, signals, DecisionObject generation, or heavy imports"
    return AuditResult("regime feature preparation scope", not bad, detail)


def _check_retail_decision_desk_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_desk",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "decision_desk.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_DECISION_DESK_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Retail Decision Desk planning contains no recommendation, action generation, confidence scoring, DecisionObject generation, external-call imports, POST routes, or execution implementation"
    return AuditResult("retail decision desk scope", not bad, detail)


def _check_decision_evidence_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_evidence",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "decision_evidence.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_DECISION_EVIDENCE_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "DecisionObject evidence bundle contracts contain no recommendation, action generation, confidence scoring, active DecisionObject generation, external-call imports, POST routes, or execution implementation"
    return AuditResult("decision evidence scope", not bad, detail)


def _check_decision_safety_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_safety",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "decision_safety.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_DECISION_SAFETY_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Decision Safety guardrails contain no approval workflow, recommendation generation, action generation, confidence scoring, active DecisionObject generation, external-call imports, POST routes, or execution implementation"
    return AuditResult("decision safety scope", not bad, detail)


def _check_decision_api_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_api",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "decision_desk_api.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_DECISION_API_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Decision Desk API skeleton contains no recommendation generation, action generation, confidence scoring, active DecisionObject generation, approval workflow, override workflow, external-call imports, POST routes, market-data-to-recommendation endpoint, broker behavior, or execution implementation"
    return AuditResult("decision API scope", not bad, detail)


def _check_decision_readiness_api_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_readiness_api",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "decision_readiness_api.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_DECISION_READINESS_API_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Decision Desk Readiness API skeleton contains no readiness-to-trade generation, recommendation generation, action generation, confidence scoring, active DecisionObject generation, approval workflow, override workflow, external-call imports, POST routes, market-data-to-readiness endpoint, broker behavior, or execution implementation"
    return AuditResult("decision readiness API scope", not bad, detail)


def _check_decision_display_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_display",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "decision_display.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_DECISION_DISPLAY_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Decision Desk Display skeleton contains no active UI builder, readiness-to-trade generation, recommendation generation, action generation, confidence scoring, active DecisionObject generation, approval workflow, override workflow, external-call imports, POST routes, market-data-to-display-decision endpoint, broker behavior, or execution implementation"
    return AuditResult("decision display scope", not bad, detail)


def _check_decision_evidence_validation_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_evidence_validation",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "decision_evidence_validation.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_DECISION_EVIDENCE_VALIDATION_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Decision Evidence Validation v0 contains no validation-to-recommendation endpoint, readiness-to-trade generation, recommendation generation, action generation, confidence scoring, active DecisionObject generation, approval workflow, override workflow, external-call imports, POST routes, broker behavior, or execution implementation"
    return AuditResult("decision evidence validation scope", not bad, detail)


def _check_decision_human_review_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_human_review",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "decision_human_review.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_DECISION_HUMAN_REVIEW_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Decision Human Review workflow skeleton contains no active workflow, task assignment, reviewer auth, notifications, approval workflow, override workflow, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, external-call imports, POST routes, broker behavior, or execution implementation"
    return AuditResult("decision human review scope", not bad, detail)


def _check_decision_boundary_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_boundary",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "decision_boundary.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_DECISION_BOUNDARY_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Decision Boundary hardening contains no endpoint boundary bypass, no module bypasses forbidden behavior registry, no active UI, no active workflow, task assignment, reviewer auth, notifications, recommendation generation, action generation, confidence scoring, active DecisionObject generation, approval workflow, override workflow, readiness-to-trade generation, external-call imports, POST routes, broker behavior, or execution implementation"
    return AuditResult("decision boundary scope", not bad, detail)


def _check_decision_api_display_integration_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/decision_api",
        ROOT / "packages/core/stark_terminal_core/decision_readiness_api",
        ROOT / "packages/core/stark_terminal_core/decision_display",
        ROOT / "packages/core/stark_terminal_core/decision_boundary",
        ROOT / "packages/core/stark_terminal_core/decision_evidence_validation",
        ROOT / "packages/core/stark_terminal_core/decision_human_review",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_files = {
        "decision_desk_api.py",
        "decision_readiness_api.py",
        "decision_display.py",
        "decision_boundary.py",
        "decision_evidence_validation.py",
        "decision_human_review.py",
    }
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_files:
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_DECISION_INTEGRATION_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Decision API/display integration contains no API-to-display recommendation path, no readiness-to-display-trade path, no active UI, no active workflow, no recommendation generation, no action generation, no confidence scoring, no active DecisionObject generation, no approval workflow, no override workflow, no readiness-to-trade generation, no external-call imports, POST routes, broker behavior, or execution implementation"
    return AuditResult("decision API/display integration scope", not bad, detail)


def _check_retail_dashboard_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/retail_dashboard",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "retail_dashboard.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_RETAIL_DASHBOARD_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Retail Dashboard planning contains no active UI, frontend dashboard implementation, broker controls, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, real market data dashboard display, external-call imports, POST routes, or execution implementation"
    return AuditResult("retail dashboard scope", not bad, detail)


def _check_retail_dashboard_api_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/retail_dashboard_api",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "retail_dashboard_api.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_RETAIL_DASHBOARD_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Retail Dashboard API skeleton contains no active UI, frontend dashboard implementation, broker controls, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, real market data dashboard display, external-call imports, POST routes, or execution implementation"
    return AuditResult("retail dashboard API scope", not bad, detail)


def _check_retail_dashboard_display_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/retail_dashboard_display",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "retail_dashboard_display.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_RETAIL_DASHBOARD_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Retail Dashboard Display skeleton contains no active UI, frontend dashboard implementation, desktop UI implementation, broker controls, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, real market data dashboard display, external-call imports, POST routes, or execution implementation"
    return AuditResult("retail dashboard display scope", not bad, detail)


def _check_retail_dashboard_boundary_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/retail_dashboard_boundary",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "retail_dashboard_boundary.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_RETAIL_DASHBOARD_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Retail Dashboard Boundary contains no active UI, frontend dashboard implementation, desktop UI implementation, broker controls, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, real market data dashboard display, external-call imports, POST routes, or execution implementation"
    return AuditResult("retail dashboard boundary scope", not bad, detail)


def _check_retail_dashboard_integration_no_boundary_bypass() -> AuditResult:
    docs = [
        ROOT / "docs/RETAIL_DASHBOARD_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
        ROOT / "docs/RETAIL_DASHBOARD_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
        ROOT / "docs/RETAIL_DASHBOARD_API_DISPLAY_BOUNDARY_AUDIT.md",
        ROOT / "docs/RETAIL_DASHBOARD_BOUNDARY_INTEGRATION_AUDIT.md",
        ROOT / "docs/RETAIL_DASHBOARD_INTEGRATION_NO_ACTIVE_UI_AUDIT.md",
        ROOT / "docs/RETAIL_DASHBOARD_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists()).lower()
    required = [
        "no api-to-display recommendation path",
        "no display-to-decision path",
        "no display-to-execution path",
        "no boundary bypass path",
        "no active ui",
        "no frontend implementation",
        "no desktop implementation",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no decisionobject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no execution apis",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Retail Dashboard integration docs forbid API-to-display recommendation, display-to-decision, display-to-execution, and boundary bypass paths"
    )
    return AuditResult("retail dashboard integration bypass", not missing, detail)


def _check_retail_trader_experience_integration_no_boundary_bypass() -> AuditResult:
    docs = [
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_API_DISPLAY_BOUNDARY_AUDIT.md",
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_BOUNDARY_INTEGRATION_AUDIT.md",
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_INTEGRATION_NO_ACTIVE_UI_AUDIT.md",
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
        ROOT / "docs/RETAIL_TRADER_EXPERIENCE_INTEGRATION_NO_SUITABILITY_AUDIT.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists()).lower()
    required = [
        "no api-to-display recommendation path",
        "no display-to-decision path",
        "no display-to-execution path",
        "no persona-to-suitability-profile path",
        "no journey-to-trading-advice path",
        "no boundary bypass path",
        "no active ui",
        "no frontend implementation",
        "no desktop implementation",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no decisionobject generation",
        "no readiness-to-trade",
        "no suitability profiling",
        "no broker controls",
        "no execution apis",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Retail Trader Experience integration docs forbid API-to-display recommendation, display-to-decision, display-to-execution, suitability, and boundary bypass paths"
    )
    return AuditResult("retail trader experience integration bypass", not missing, detail)


def _check_retail_trader_experience_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/retail_trader_experience",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "retail_trader_experience.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_RETAIL_TRADER_EXPERIENCE_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Trader Experience planning contains no active UI, frontend implementation, desktop implementation, broker controls, suitability profiling, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, real market data display, external-call imports, POST routes, or execution implementation"
    )
    return AuditResult("retail trader experience scope", not bad, detail)


def _check_retail_trader_experience_api_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/retail_trader_experience_api",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "retail_trader_experience_api.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_RETAIL_TRADER_EXPERIENCE_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Trader Experience API skeleton contains no active UI, frontend implementation, desktop implementation, broker controls, suitability profiling, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, real market data display, external-call imports, POST routes, or execution implementation"
    )
    return AuditResult("retail trader experience api scope", not bad, detail)


def _check_retail_trader_experience_display_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/retail_trader_experience_display",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "retail_trader_experience_display.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_RETAIL_TRADER_EXPERIENCE_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Trader Experience Display skeleton contains no active UI, frontend implementation, desktop implementation, broker controls, suitability profiling, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, real market data display, external-call imports, POST routes, or execution implementation"
    )
    return AuditResult("retail trader experience display scope", not bad, detail)


def _check_retail_trader_experience_boundary_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/retail_trader_experience_boundary",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "retail_trader_experience_boundary.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_RETAIL_TRADER_EXPERIENCE_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Trader Experience Boundary hardening contains no active UI, frontend implementation, desktop implementation, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, suitability profiling generation, broker controls, real market data display, external-call imports, POST routes, or execution implementation"
    )
    return AuditResult("retail trader experience boundary scope", not bad, detail)


def _check_strategy_research_workspace_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/strategy_research_workspace",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "strategy_research_workspace.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_STRATEGY_RESEARCH_WORKSPACE_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Strategy Research Workspace planning contains no active UI, frontend implementation, desktop implementation, paper ingestion, paper parsing, strategy generation, strategy code generation, backtesting, optimization, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, broker controls, real market data display, external-call imports, POST routes, or execution implementation"
    )
    return AuditResult("strategy research workspace scope", not bad, detail)


def _check_strategy_research_workspace_api_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_api",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "strategy_research_workspace_api.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_STRATEGY_RESEARCH_WORKSPACE_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Strategy Research Workspace API skeleton contains no active UI, frontend implementation, desktop implementation, paper ingestion, paper parsing, strategy generation, strategy code generation, backtesting, optimization, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, broker controls, real market data display, external-call imports, POST routes, or execution implementation"
    )
    return AuditResult("strategy research workspace api scope", not bad, detail)


def _check_strategy_research_workspace_display_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "strategy_research_workspace_display.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_STRATEGY_RESEARCH_WORKSPACE_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Strategy Research Workspace Display skeleton contains no active UI, frontend implementation, desktop implementation, paper ingestion, paper parsing, strategy generation, strategy code generation, backtesting, optimization, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, broker controls, real market data display, external-call imports, POST routes, or execution implementation"
    )
    return AuditResult("strategy research workspace display scope", not bad, detail)


def _check_strategy_research_workspace_boundary_no_forbidden_scope() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_boundary",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name != "strategy_research_workspace_boundary.py":
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in FORBIDDEN_STRATEGY_RESEARCH_WORKSPACE_SCOPE_PHRASES:
                haystack = text if phrase == "DecisionObject(" else lowered
                needle = phrase if phrase == "DecisionObject(" else phrase.lower()
                if needle in haystack:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Strategy Research Workspace boundary hardening contains no active UI, frontend implementation, desktop implementation, paper ingestion, paper parsing, strategy generation, strategy code generation, backtesting, optimization, recommendation generation, action generation, confidence scoring, active DecisionObject generation, readiness-to-trade generation, broker controls, real market data display, external-call imports, POST routes, or execution implementation"
    )
    return AuditResult("strategy research workspace boundary scope", not bad, detail)


def _check_strategy_research_workspace_safety_audit_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_STRATEGY_RESEARCH_WORKSPACE_SAFETY_AUDIT_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Prompts 63-65",
        "no active UI",
        "no frontend implementation",
        "no desktop implementation",
        "no paper ingestion",
        "no paper parsing",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendation",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
        "Prompt 67",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Strategy Research Workspace safety audit docs state no-active-UI/no-paper-ingestion/no-paper-parsing/no-strategy-generation/no-backtesting/no-recommendations/no-confidence/no-DecisionObject/no-broker-controls/no-readiness-to-trade/no-execution language"
    )
    return AuditResult("strategy research workspace safety audit docs language", not missing, detail)


def _check_strategy_research_workspace_milestone_audit_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_STRATEGY_RESEARCH_WORKSPACE_MILESTONE_AUDIT_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Prompts 63-66",
        "Strategy Research Workspace Milestone Audit",
        "Strategy Research Workspace Planning and Guardrails",
        "Strategy Research Workspace API Contract Skeleton",
        "Strategy Research Workspace Display Contract Skeleton",
        "Strategy Research Workspace Safety Boundary Audit",
        "no active UI",
        "no frontend implementation",
        "no desktop implementation",
        "no paper ingestion",
        "no paper parsing",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendation",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "Prompt 68",
        "Mac mini M2",
        "Windows-native",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Strategy Research Workspace milestone audit docs state phase no-active-UI/no-paper-parsing/no-strategy/no-backtest/no-recommendation/no-execution boundaries"
    )
    return AuditResult("strategy research workspace milestone audit docs language", not missing, detail)


def _check_strategy_research_workspace_boundary_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_STRATEGY_RESEARCH_WORKSPACE_BOUNDARY_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "boundary-hardening-only",
        "forbidden behavior registry",
        "endpoint boundary policy",
        "module boundary policy",
        "cross-module invariants",
        "no active UI",
        "no frontend",
        "no desktop",
        "no paper ingestion",
        "no paper parsing",
        "no arXiv ingestion",
        "no LLM paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no signal/factor/alpha generation",
        "no backtesting",
        "no optimization",
        "no recommendation generation",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "future prompt",
        "audit before unlock",
        "Mac mini M2",
        "Windows-native",
        "Prompt 69",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Strategy Research Workspace boundary docs state boundary hardening, registry, endpoint/module policies, invariants, and no-active-UI/no-paper-parsing/no-strategy/no-backtest/no-recommendation/no-execution language"
    )
    return AuditResult("strategy research workspace boundary docs language", not missing, detail)


def _check_strategy_research_workspace_api_display_integration_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_STRATEGY_RESEARCH_WORKSPACE_API_DISPLAY_INTEGRATION_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Prompts 63-68",
        "Strategy Research Workspace API/Display Integration Readiness Audit",
        "cross-endpoint consistency",
        "API/display boundary",
        "boundary integration",
        "Research Artifact Registry Planning and Guardrails only",
        "Research Artifact Registry implementation is not yet allowed",
        "no active UI",
        "no frontend implementation",
        "no desktop implementation",
        "no paper ingestion",
        "no paper parsing",
        "no arXiv ingestion",
        "no LLM paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no signal/factor/alpha generation",
        "no backtesting",
        "no optimization",
        "no recommendation",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject",
        "no readiness-to-trade",
        "no broker controls",
        "no approvals",
        "no overrides",
        "no execution APIs",
        "no API-to-display strategy path",
        "no API-to-display backtest result path",
        "no parsed-paper-to-display path",
        "no research-as-recommendation",
        "no research-as-execution-control",
        "Mac mini M2",
        "Windows-native",
        "Prompt 70",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Strategy Research Workspace API/display integration docs state no-active-UI/no-paper-parsing/no-strategy/no-backtest/no-recommendation/no-execution language and Research Artifact Registry planning-only readiness"
    )
    return AuditResult(
        "strategy research workspace api display integration docs language",
        not missing,
        detail,
    )


def _check_research_artifact_registry_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Research Artifact Registry",
        "planning",
        "guardrails",
        "no active artifact ingestion",
        "no active artifact storage",
        "no persistent artifact storage",
        "no file upload",
        "no file download",
        "no paper parsing",
        "no PDF parsing",
        "no arXiv ingestion",
        "no LLM paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendations",
        "no confidence scoring",
        "no DecisionObject",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Registry docs state planning/guardrails and no-ingestion/no-parsing/no-strategy/no-backtest/no-recommendation/no-execution language"
    )
    return AuditResult("research artifact registry docs language", not missing, detail)


def _check_research_artifact_registry_source_boundaries() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {"research_artifact_registry.py"}
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "@router.post",
        "@router.put",
        "@router.delete",
        "def ingest_artifact",
        "def store_artifact",
        "def upload_file",
        "def download_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "Research Artifact Registry source exposes no active ingestion/parsing/strategy/backtest/recommendation/execution behavior"
    return AuditResult("research artifact registry source boundaries", not bad, detail)


def _check_research_artifact_registry_api_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_API_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Research Artifact Registry API",
        "API contract skeleton",
        "read-only",
        "unavailable",
        "unavailable-by-default",
        "no active artifact ingestion",
        "no active artifact storage",
        "no persistent artifact storage",
        "no file upload",
        "no file download",
        "no paper parsing",
        "no PDF parsing",
        "no arXiv ingestion",
        "no LLM paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendations",
        "no confidence scoring",
        "no DecisionObject",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Registry API docs state read-only/unavailable no-ingestion/no-parsing/no-strategy/no-backtest/no-recommendation/no-execution language"
    )
    return AuditResult("research artifact registry api docs language", not missing, detail)


def _check_research_artifact_registry_api_source_boundaries() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {"research_artifact_registry_api.py"}
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "@router.post",
        "@router.put",
        "@router.delete",
        "def ingest_artifact",
        "def store_artifact",
        "def upload_file",
        "def download_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Research Artifact Registry API source exposes no active ingestion/storage/upload/download/parsing/strategy/backtest/recommendation/execution behavior"
    )
    return AuditResult("research artifact registry api source boundaries", not bad, detail)


def _check_research_artifact_registry_display_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_DISPLAY_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Research Artifact Registry Display",
        "display contract skeleton",
        "backend-only",
        "read-only",
        "unavailable",
        "unavailable-by-default",
        "no active UI",
        "frontend",
        "desktop",
        "no active artifact ingestion",
        "no persistent storage",
        "no file preview",
        "no file upload",
        "no file download",
        "no paper parsing",
        "no PDF",
        "no arXiv",
        "no LLM",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendations",
        "no confidence scoring",
        "no DecisionObject",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Registry Display docs state backend-only/read-only/unavailable no-active-UI/no-ingestion/no-parsing/no-strategy/no-backtest/no-recommendation/no-execution language"
    )
    return AuditResult("research artifact registry display docs language", not missing, detail)


def _check_research_artifact_registry_display_source_boundaries() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {"research_artifact_registry_display.py"}
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "@router.post",
        "@router.put",
        "@router.delete",
        "def render_artifact_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
        "def preview_file",
        "def ingest_artifact",
        "def store_artifact",
        "def upload_file",
        "def download_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def create_order_button",
        "def execute_trade",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Research Artifact Registry Display source exposes no active UI/storage/upload/download/parsing/strategy/backtest/recommendation/execution behavior"
    )
    return AuditResult("research artifact registry display source boundaries", not bad, detail)


def _check_research_artifact_registry_safety_audit_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_SAFETY_AUDIT_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Prompts 70-72",
        "Research Artifact Registry Planning and Guardrails",
        "Research Artifact Registry API Contract Skeleton",
        "Research Artifact Registry Display Contract Skeleton",
        "no active artifact ingestion",
        "no active artifact storage",
        "no persistent artifact storage",
        "no upload/download",
        "no active UI",
        "no frontend implementation",
        "no desktop implementation",
        "no paper parsing",
        "no PDF parsing",
        "no arXiv ingestion",
        "no LLM paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject",
        "no readiness-to-trade",
        "no broker controls",
        "no approvals/overrides",
        "no execution APIs",
        "Prompt 74",
        "Mac mini M2",
        "Windows-native",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Registry safety audit docs state no-ingestion/no-storage/no-upload-download/no-active-UI/no-paper-parsing/no-strategy/no-backtest/no-recommendation/no-execution language"
    )
    return AuditResult("research artifact registry safety audit docs language", not missing, detail)


def _check_research_artifact_registry_milestone_audit_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_MILESTONE_AUDIT_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Prompts 70-73",
        "Research Artifact Registry Planning and Guardrails",
        "Research Artifact Registry API Contract Skeleton",
        "Research Artifact Registry Display Contract Skeleton",
        "Research Artifact Registry Safety Boundary Audit",
        "no active artifact ingestion",
        "no persistent artifact storage",
        "no upload/download",
        "no active UI",
        "no frontend implementation",
        "no desktop implementation",
        "no paper parsing",
        "no PDF parsing",
        "no arXiv ingestion",
        "no LLM paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject",
        "no readiness-to-trade",
        "no broker controls",
        "no approvals/overrides",
        "no execution APIs",
        "Prompt 75",
        "Research Artifact Registry System Boundary Hardening",
        "Mac mini M2",
        "Windows-native",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Registry milestone audit docs state phase no-ingestion/no-storage/no-upload-download/no-active-UI/no-paper-parsing/no-strategy/no-backtest/no-recommendation/no-execution language"
    )
    return AuditResult("research artifact registry milestone audit docs language", not missing, detail)


def _check_research_artifact_registry_boundary_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_BOUNDARY_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "boundary-hardening-only",
        "forbidden behavior registry",
        "endpoint boundary policy",
        "module boundary policy",
        "cross-module invariants",
        "Research Artifact Registry Boundary",
        "no active ingestion/storage",
        "no active artifact ingestion",
        "no persistent artifact storage",
        "no file upload/download",
        "no file preview",
        "no active UI",
        "no frontend/desktop implementation",
        "no paper parsing",
        "no PDF/arXiv ingestion",
        "no LLM paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendation generation",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "future prompt and audit required",
        "Prompt 76",
        "Mac mini M2",
        "Windows-native",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Registry boundary docs state boundary-hardening-only no-ingestion/no-storage/no-upload-download/no-active-UI/no-paper-parsing/no-strategy/no-backtest/no-recommendation/no-execution language"
    )
    return AuditResult("research artifact registry boundary docs language", not missing, detail)


def _check_research_artifact_registry_api_display_integration_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_RESEARCH_ARTIFACT_REGISTRY_API_DISPLAY_INTEGRATION_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Prompt 76",
        "Prompts 70-75",
        "Research Artifact Registry API/Display Integration Readiness Audit",
        "Research Artifact Index Planning and Guardrails",
        "cross-endpoint consistency",
        "API/display boundary",
        "boundary integration",
        "no active ingestion/storage",
        "no active artifact ingestion",
        "no persistent storage",
        "no upload/download",
        "no file preview",
        "no active UI",
        "no frontend implementation",
        "no desktop implementation",
        "no paper parsing",
        "no PDF parsing",
        "no arXiv ingestion",
        "no LLM paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendation",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject",
        "no readiness-to-trade",
        "no broker controls",
        "no approvals/overrides",
        "no execution APIs",
        "no API-to-display artifact implementation path",
        "no API-to-display file preview path",
        "no indexing engine",
        "no search engine",
        "no ranking engine",
        "embedding/vector store",
        "Prompt 77",
        "Mac mini M2",
        "Windows-native",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Registry API/display integration docs state no-ingestion/no-storage/no-upload-download/no-active-UI/no-paper-parsing/no-strategy/no-backtest/no-recommendation/no-execution language"
    )
    return AuditResult("research artifact registry api display integration docs language", not missing, detail)


def _check_research_artifact_index_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_RESEARCH_ARTIFACT_INDEX_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Prompt 77",
        "Research Artifact Index",
        "planning and guardrails",
        "planning-only",
        "No indexing engine",
        "No search engine",
        "No ranking engine",
        "No retrieval engine",
        "No embedding",
        "No vector store",
        "No active artifact ingestion",
        "No active artifact storage",
        "No file upload/download/preview",
        "No paper parsing",
        "No PDF",
        "No arXiv",
        "No LLM paper analysis",
        "No strategy generation",
        "No strategy code generation",
        "No backtesting",
        "No optimization",
        "No recommendations",
        "No confidence scoring",
        "No DecisionObject",
        "No readiness-to-trade",
        "No broker controls",
        "No execution",
        "Prompt 78",
        "Mac mini M2",
        "Windows-native",
        "decision candidate is not a trade",
        "execution APIs remain forbidden",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Index docs state planning/no-indexing/no-search/no-ranking/no-embedding/no-ingestion/no-storage/no-execution language"
    )
    return AuditResult("research artifact index docs language", not missing, detail)


def _check_research_artifact_index_api_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_RESEARCH_ARTIFACT_INDEX_API_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Prompt 78",
        "Research Artifact Index API",
        "API contract skeleton",
        "read-only",
        "unavailable-by-default",
        "No indexing engine",
        "No search engine",
        "No ranking engine",
        "No retrieval engine",
        "No embeddings",
        "No vector store",
        "No active artifact ingestion",
        "No active artifact ingestion/storage",
        "No file upload/download/preview",
        "No paper parsing",
        "No PDF",
        "No arXiv",
        "No LLM paper analysis",
        "No strategy generation",
        "No strategy code generation",
        "No backtesting",
        "No optimization",
        "No recommendations",
        "No confidence scoring",
        "No DecisionObject",
        "No readiness-to-trade",
        "No broker controls",
        "No execution",
        "Prompt 79",
        "Mac mini M2",
        "Windows-native",
        "decision candidate is not a trade",
        "execution APIs remain forbidden",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Index API docs state contract-skeleton/read-only/unavailable/no-indexing/no-search/no-ranking/no-embedding/no-ingestion/no-storage/no-execution language"
    )
    return AuditResult("research artifact index api docs language", not missing, detail)


def _check_research_artifact_index_display_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_RESEARCH_ARTIFACT_INDEX_DISPLAY_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Prompt 79",
        "Research Artifact Index Display",
        "display contract skeleton",
        "backend-only",
        "read-only",
        "unavailable-by-default",
        "No active UI",
        "No frontend implementation",
        "No desktop implementation",
        "No file preview",
        "No indexing engine",
        "No search engine",
        "No ranking engine",
        "No retrieval engine",
        "No embeddings",
        "No vector store",
        "No active artifact ingestion",
        "No active artifact ingestion/storage",
        "No file upload/download/preview",
        "No paper parsing",
        "No PDF",
        "No arXiv",
        "No LLM paper analysis",
        "No strategy generation",
        "No strategy code generation",
        "No backtesting",
        "No optimization",
        "No recommendations",
        "No confidence scoring",
        "No DecisionObject",
        "No readiness-to-trade",
        "No broker controls",
        "No execution",
        "Prompt 80",
        "Mac mini M2",
        "Windows-native",
        "decision candidate is not a trade",
        "execution APIs remain forbidden",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Index Display docs state backend-only/read-only/unavailable/no-active-UI/no-indexing/no-search/no-ranking/no-embedding/no-ingestion/no-storage/no-execution language"
    )
    return AuditResult("research artifact index display docs language", not missing, detail)


def _check_research_artifact_registry_boundary_source_boundaries() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {"research_artifact_registry_boundary.py"}
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "@router.post",
        "@router.put",
        "@router.delete",
        "def ingest_artifact",
        "def import_artifact",
        "def fetch_artifact_source",
        "def store_artifact",
        "def persist_artifact",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def read_local_file",
        "def fetch_remote_file",
        "def render_artifact_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def generate_signal",
        "def generate_factor",
        "def generate_alpha",
        "def run_backtest",
        "def optimize_strategy",
        "def parameter_search",
        "def walk_forward",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Research Artifact Registry boundary source exposes no active ingestion/storage/upload/download/UI/parsing/strategy/backtest/recommendation/execution behavior"
    )
    return AuditResult("research artifact registry boundary source boundaries", not bad, detail)


def _check_research_artifact_index_source_boundaries() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_artifact_index",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {"research_artifact_index.py"}
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "@router.post",
        "@router.put",
        "@router.delete",
        "def build_index",
        "def run_indexing",
        "def search_artifacts",
        "def rank_artifacts",
        "def retrieve_artifacts",
        "def embed_artifacts",
        "def create_vector_store",
        "def semantic_search",
        "def keyword_search",
        "def ingest_artifact",
        "def import_artifact",
        "def fetch_artifact_source",
        "def store_artifact",
        "def persist_artifact",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def read_local_file",
        "def fetch_remote_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def parameter_search",
        "def walk_forward",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Research Artifact Index source exposes no indexing/search/ranking/retrieval/embedding/vector/ingestion/storage/parsing/strategy/backtest/recommendation/execution behavior"
    )
    return AuditResult("research artifact index source boundaries", not bad, detail)


def _check_research_artifact_index_api_source_boundaries() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_artifact_index_api",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {"research_artifact_index_api.py"}
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "@router.post",
        "@router.put",
        "@router.delete",
        "def build_index",
        "def run_indexing",
        "def search_artifacts",
        "def rank_artifacts",
        "def retrieve_artifacts",
        "def embed_artifacts",
        "def create_vector_store",
        "def semantic_search",
        "def keyword_search",
        "def ingest_artifact",
        "def import_artifact",
        "def fetch_artifact_source",
        "def store_artifact",
        "def persist_artifact",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def read_local_file",
        "def fetch_remote_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def parameter_search",
        "def walk_forward",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Research Artifact Index API source exposes no indexing/search/ranking/retrieval/embedding/vector/ingestion/storage/parsing/strategy/backtest/recommendation/execution behavior"
    )
    return AuditResult("research artifact index api source boundaries", not bad, detail)


def _check_research_artifact_index_display_source_boundaries() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_artifact_index_display",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {"research_artifact_index_display.py"}
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "@router.post",
        "@router.put",
        "@router.delete",
        "def render_index_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
        "def build_index",
        "def run_indexing",
        "def search_artifacts",
        "def rank_artifacts",
        "def retrieve_artifacts",
        "def embed_artifacts",
        "def create_vector_store",
        "def semantic_search",
        "def keyword_search",
        "def ingest_artifact",
        "def import_artifact",
        "def fetch_artifact_source",
        "def store_artifact",
        "def persist_artifact",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def read_local_file",
        "def fetch_remote_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def parameter_search",
        "def walk_forward",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Research Artifact Index Display source exposes no active UI/frontend/desktop/indexing/search/ranking/retrieval/embedding/vector/ingestion/storage/parsing/strategy/backtest/recommendation/execution behavior"
    )
    return AuditResult("research artifact index display source boundaries", not bad, detail)


def _check_research_artifact_index_safety_audit_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_RESEARCH_ARTIFACT_INDEX_SAFETY_AUDIT_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    required = [
        "Prompt 80",
        "Research Artifact Index Safety Boundary Audit",
        "Prompts 77-79 audited",
        "Research Artifact Index Planning and Guardrails",
        "Research Artifact Index API Contract Skeleton",
        "Research Artifact Index Display Contract Skeleton",
        "No active UI",
        "No frontend implementation",
        "No desktop implementation",
        "No indexing engine",
        "No search engine",
        "No ranking engine",
        "No retrieval",
        "No embeddings",
        "No vector store",
        "No active artifact index ingestion",
        "No persistent artifact index storage",
        "No file upload endpoints",
        "No file download endpoints",
        "No file preview endpoints",
        "No paper parsing",
        "No PDF",
        "No arXiv",
        "No LLM paper analysis",
        "No strategy generation",
        "No strategy code generation",
        "No backtesting",
        "No optimization",
        "No recommendations",
        "No confidence scoring",
        "No active DecisionObjects",
        "No readiness-to-trade",
        "No broker controls",
        "No execution APIs",
        "Prompt 81",
        "decision candidate is not a trade",
        "execution APIs remain forbidden",
        "no active UI",
        "no indexing",
        "no search",
        "no ranking",
        "no retrieval",
        "no embedding",
        "no vector-store",
        "no ingestion",
        "no storage",
        "no upload/download",
        "no preview",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendation",
        "no execution",
    ]
    missing = [phrase for phrase in required if phrase not in combined]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Index safety audit docs state no-active-UI/no-indexing/no-search/no-ranking/no-retrieval/no-embedding/no-vector-store/no-ingestion/no-storage/no-upload-download/no-preview/no-paper-parsing/no-strategy/no-backtest/no-recommendation/no-execution language"
    )
    return AuditResult("research artifact index safety audit docs language", not missing, detail)


def _check_documentation_consolidation_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in REQUIRED_DOCUMENTATION_CONSOLIDATION_FILES
        if path.startswith("docs/")
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    combined_lower = combined.lower()
    required = [
        "documentation/test consolidation interlude",
        "tests remain required",
        "grouped by phase and boundary",
        "phase-first",
        "prompt logs remain",
        "documentation should support development",
        "granular prompt audit docs are superseded",
        "archive pass 1",
        "archive pass 2",
        "older phase micro-audit docs and tests",
        "aggressive deletion pass",
        "docs_consolidated_report",
        "tests_consolidated_report",
        "deleted_files_report",
        "safety_coverage_report",
        "active_test_baseline_report",
        "archived tests are historical references",
        "research artifact index",
        "research artifact registry",
        "strategy research workspace",
        "active decision architecture",
        "decision candidate is not a trade",
        "execution apis remain forbidden",
        "no execution apis",
        "no broker controls",
        "no active ui",
        "no indexing engine",
        "no search engine",
        "no ranking engine",
        "no retrieval engine",
        "no embeddings",
        "no vector store",
        "no active ingestion",
        "no file upload",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "prompt 81",
    ]
    missing = [phrase for phrase in required if phrase not in combined_lower]
    detail = (
        ", ".join(missing)
        if missing
        else "documentation/test consolidation docs state phase-level policy and preserved safety boundaries"
    )
    return AuditResult("documentation consolidation docs language", not missing, detail)


def _check_archived_prompt_audit_tests_not_collectable() -> AuditResult:
    archive_dir = ROOT / "tests/archive/prompt_audits"
    collectable = sorted(path.relative_to(ROOT).as_posix() for path in archive_dir.rglob("*.py"))
    archived = sorted(path.relative_to(ROOT).as_posix() for path in archive_dir.rglob("*.py.archived"))
    reports_present = all(
        (ROOT / path).exists()
        for path in [
            "docs/reports/TESTS_CONSOLIDATED_REPORT.md",
            "docs/reports/DELETED_FILES_REPORT.md",
            "docs/reports/ACTIVE_TEST_BASELINE_REPORT.md",
        ]
    )
    passed = archive_dir.exists() and not collectable and reports_present
    detail = (
        ", ".join(collectable)
        if collectable
        else "archive has no pytest-collectable tests; deleted archive details are preserved in grouped reports"
    )
    if not archive_dir.exists():
        detail = "tests/archive/prompt_audits missing"
    elif not reports_present:
        detail = "grouped deletion reports missing"
    return AuditResult("archived prompt audit tests not collectable", passed, detail)


def _check_research_artifact_index_milestone_audit_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in [
            "docs/RESEARCH_ARTIFACT_INDEX_MILESTONE_AUDIT.md",
            "docs/RESEARCH_ARTIFACT_INDEX_NEXT_PHASE_PLAN.md",
            "docs/phases/research_artifact_index.md",
            "docs/audits/research_artifact_boundaries.md",
            "docs/audits/safety_boundaries.md",
            "docs/testing/CONSOLIDATION_MAP.md",
        ]
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    combined_lower = combined.lower()
    required = [
        "prompt 81",
        "research artifact index milestone audit",
        "prompts 77-80",
        "consolidation interlude",
        "research artifact index planning and guardrails",
        "research artifact index api contract skeleton",
        "research artifact index display contract skeleton",
        "research artifact index safety boundary audit",
        "grouped",
        "phase-level",
        "no active ui",
        "no frontend",
        "no desktop",
        "no indexing",
        "no search",
        "no ranking",
        "no retrieval",
        "no embeddings",
        "no vector store",
        "no active ingestion",
        "no persistent storage",
        "no file upload",
        "download",
        "preview",
        "no paper parsing",
        "pdf parsing",
        "arxiv ingestion",
        "llm paper analysis",
        "no strategy generation",
        "strategy code generation",
        "no backtesting",
        "optimization",
        "no recommendations",
        "action generation",
        "confidence scoring",
        "active decisionobjects",
        "readiness-to-trade",
        "no broker controls",
        "execution apis",
        "prompt 82",
        "research artifact index system boundary hardening",
    ]
    missing = [phrase for phrase in required if phrase not in combined_lower]
    detail = (
        ", ".join(missing)
        if missing
        else "Research Artifact Index milestone audit docs state Prompt 81 grouped milestone and all forbidden boundaries"
    )
    return AuditResult("research artifact index milestone audit docs language", not missing, detail)


def _check_research_artifact_index_safety_audit_source_boundaries() -> AuditResult:
    bad: list[str] = []
    package_roots = [
        ROOT / "packages/core/stark_terminal_core/research_artifact_index",
        ROOT / "packages/core/stark_terminal_core/research_artifact_index_api",
        ROOT / "packages/core/stark_terminal_core/research_artifact_index_display",
    ]
    route_files = [
        ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index.py",
        ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_api.py",
        ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_display.py",
    ]
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "@router.post",
        "@router.put",
        "@router.delete",
        "def render_index_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
        "def build_index",
        "def run_indexing",
        "def search_artifacts",
        "def semantic_search",
        "def keyword_search",
        "def rank_artifacts",
        "def score_artifacts",
        "def retrieve_artifacts",
        "def lookup_artifact",
        "def lookup_index",
        "def lookup_registry",
        "def fetch_index_reference",
        "def embed_artifacts",
        "def create_embeddings",
        "def create_vector_store",
        "def vector_search",
        "def ingest_artifact",
        "def store_artifact",
        "def persist_artifact",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def read_local_file",
        "def fetch_remote_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def generate_signal",
        "def generate_factor",
        "def generate_alpha",
        "def run_backtest",
        "def optimize_strategy",
        "def parameter_search",
        "def walk_forward",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
    ]
    for root in package_roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    for path in route_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden_phrases:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Research Artifact Index safety audit source exposes no active UI/frontend/desktop/indexing/search/ranking/retrieval/embedding/vector/ingestion/storage/parsing/strategy/backtest/recommendation/execution behavior"
    )
    return AuditResult("research artifact index safety audit source boundaries", not bad, detail)


def _check_research_artifact_index_boundary_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in [
            "docs/RESEARCH_ARTIFACT_INDEX_SYSTEM_BOUNDARY_HARDENING.md",
            "docs/phases/research_artifact_index.md",
            "docs/audits/research_artifact_boundaries.md",
            "docs/audits/safety_boundaries.md",
            "docs/testing/CONSOLIDATION_MAP.md",
            "docs/NEXT_PHASE_PLAN.md",
            "docs/PROMPT_LOG.md",
        ]
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    combined_lower = combined.lower()
    required = [
        "prompt 82",
        "research artifact index system boundary hardening",
        "forbidden behavior registry",
        "endpoint polic",
        "module polic",
        "invariant",
        "read-only",
        "no active ui",
        "no frontend",
        "no desktop",
        "no indexing",
        "no search",
        "no ranking",
        "no retrieval",
        "no embeddings",
        "no vector store",
        "no active ingestion",
        "no persistent storage",
        "no file upload/download/preview",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "no execution",
        "grouped docs/tests",
        "no micro-audit sprawl",
        "prompt 83",
    ]
    missing = [phrase for phrase in required if phrase not in combined_lower]
    return AuditResult(
        "research artifact index boundary docs language",
        not missing,
        ", ".join(missing)
        if missing
        else "Research Artifact Index boundary hardening docs preserve grouped policy and forbidden boundaries",
    )


def _check_research_artifact_index_boundary_source_boundaries() -> AuditResult:
    bad: list[str] = []
    package_roots = [
        ROOT / "packages/core/stark_terminal_core/research_artifact_index",
        ROOT / "packages/core/stark_terminal_core/research_artifact_index_api",
        ROOT / "packages/core/stark_terminal_core/research_artifact_index_display",
        ROOT / "packages/core/stark_terminal_core/research_artifact_index_boundary",
    ]
    route_files = [
        ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index.py",
        ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_api.py",
        ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_display.py",
        ROOT / "apps/api/stark_terminal_api/routes/research_artifact_index_boundary.py",
    ]
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "@router.post",
        "@router.put",
        "@router.delete",
        "def render_index_ui",
        "def create_frontend_component",
        "def create_desktop_widget",
        "def build_index",
        "def run_indexing",
        "def search_artifacts",
        "def semantic_search",
        "def keyword_search",
        "def rank_artifacts",
        "def score_artifacts",
        "def retrieve_artifacts",
        "def lookup_artifact",
        "def lookup_index",
        "def lookup_registry",
        "def fetch_index_reference",
        "def embed_artifacts",
        "def create_embeddings",
        "def create_vector_store",
        "def vector_search",
        "def ingest_artifact",
        "def store_artifact",
        "def persist_artifact",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def read_local_file",
        "def fetch_remote_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def generate_signal",
        "def generate_factor",
        "def generate_alpha",
        "def run_backtest",
        "def optimize_strategy",
        "def parameter_search",
        "def walk_forward",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
    ]
    for root in package_roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    for path in route_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden_phrases:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Research Artifact Index boundary source exposes no active UI/index/search/retrieval/embedding/ingestion/storage/parsing/strategy/backtest/recommendation/execution behavior"
    )
    return AuditResult("research artifact index boundary source boundaries", not bad, detail)


def _check_prompt_82_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_ARTIFACT_INDEX_SYSTEM_BOUNDARY_*.md")
        if path.name != "RESEARCH_ARTIFACT_INDEX_SYSTEM_BOUNDARY_HARDENING.md"
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_artifact_index_system_boundary*.py")
        if path.name
        not in {
            "test_research_artifact_index_system_boundary_phase.py",
            "test_research_artifact_index_system_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 82 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 82 no micro audit sprawl", not bad, detail)


def _check_research_artifact_index_api_display_integration_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in [
            "docs/RESEARCH_ARTIFACT_INDEX_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
            "docs/RESEARCH_METADATA_GRAPH_READINESS_PLAN.md",
            "docs/phases/research_artifact_index.md",
            "docs/audits/research_artifact_boundaries.md",
            "docs/audits/safety_boundaries.md",
            "docs/testing/CONSOLIDATION_MAP.md",
            "docs/NEXT_PHASE_PLAN.md",
            "docs/PROMPT_LOG.md",
        ]
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    combined_lower = combined.lower()
    required = [
        "prompt 83",
        "research artifact index api/display integration readiness audit",
        "prompts 77-82",
        "cross-endpoint consistency",
        "cross-module invariant",
        "read-only",
        "no active ui",
        "no frontend",
        "no desktop",
        "no indexing",
        "no search",
        "no ranking",
        "no retrieval",
        "no embeddings",
        "no vector store",
        "no ingestion",
        "no storage",
        "upload/download/preview",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "no execution",
        "research metadata graph planning and guardrails",
        "planning and guardrails only",
        "no active graph database",
        "grouped docs/tests",
        "no micro-audit sprawl",
        "prompt 84",
    ]
    missing = [phrase for phrase in required if phrase not in combined_lower]
    return AuditResult(
        "research artifact index api display integration docs language",
        not missing,
        ", ".join(missing)
        if missing
        else "Research Artifact Index API/display integration docs preserve grouped policy and forbidden boundaries",
    )


def _check_prompt_83_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_ARTIFACT_INDEX_API_DISPLAY_INTEGRATION_*.md")
        if path.name != "RESEARCH_ARTIFACT_INDEX_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md"
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_artifact_index_api_display_integration*.py")
        if path.name
        not in {
            "test_research_artifact_index_api_display_integration_phase.py",
            "test_research_artifact_index_api_display_integration_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 83 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 83 no micro audit sprawl", not bad, detail)


def _check_research_metadata_graph_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in [
            "docs/RESEARCH_METADATA_GRAPH_PLANNING_AND_GUARDRAILS.md",
            "docs/RESEARCH_METADATA_GRAPH_API_CONTRACT_SKELETON.md",
            "docs/RESEARCH_METADATA_GRAPH_DISPLAY_CONTRACT_SKELETON.md",
            "docs/RESEARCH_METADATA_GRAPH_SAFETY_BOUNDARY_AUDIT.md",
            "docs/phases/research_metadata_graph.md",
            "docs/RESEARCH_METADATA_GRAPH_READINESS_PLAN.md",
            "docs/phases/research_artifact_index.md",
            "docs/audits/research_artifact_boundaries.md",
            "docs/audits/safety_boundaries.md",
            "docs/testing/CONSOLIDATION_MAP.md",
            "docs/NEXT_PHASE_PLAN.md",
            "docs/PROMPT_LOG.md",
        ]
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    combined_lower = combined.lower()
    required = [
        "prompt 84",
        "research metadata graph planning and guardrails",
        "planning and guardrails only",
        "prompt 85",
        "research metadata graph api contract skeleton",
        "api contract skeleton",
        "api-contract-skeleton-only",
        "prompt 86",
        "research metadata graph display contract skeleton",
        "display contract skeleton",
        "display-contract-skeleton-only",
        "research metadata graph safety boundary audit",
        "safety boundary audit",
        "prompts 84-86",
        "planning safety verdict",
        "api safety verdict",
        "display safety verdict",
        "no graph tables",
        "no graph migrations",
        "request placeholder",
        "response placeholder",
        "reference placeholder",
        "unavailable response",
        "node display placeholder",
        "edge display placeholder",
        "provenance display placeholder",
        "lifecycle display placeholder",
        "reference display placeholder",
        "unavailable display response",
        "graph node placeholder",
        "graph edge placeholder",
        "provenance",
        "lifecycle",
        "dependency",
        "read-only",
        "no active ui",
        "no frontend",
        "no desktop",
        "no active graph database",
        "no persistent graph writes",
        "no graph traversal",
        "no graph query",
        "no graph search",
        "no graph ranking",
        "no graph retrieval",
        "no embeddings",
        "no vector store",
        "no active ingestion",
        "no persistent storage",
        "upload/download/preview",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "no execution",
        "grouped docs/tests",
        "no micro-audit sprawl",
        "prompt 87",
        "prompt 88",
        "prompt 88-b",
        "research metadata graph phase closure",
        "phase closure verdict",
        "phase closed",
        "research knowledge map planning and guardrails",
        "prompt 89",
    ]
    missing = [phrase for phrase in required if phrase not in combined_lower]
    return AuditResult(
        "research metadata graph docs language",
        not missing,
        ", ".join(missing)
        if missing
        else "Research Metadata Graph planning docs preserve grouped policy and forbidden boundaries",
    )


def _check_research_metadata_graph_source_boundaries() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_metadata_graph",
        ROOT / "packages/core/stark_terminal_core/research_metadata_graph_api",
        ROOT / "packages/core/stark_terminal_core/research_metadata_graph_display",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {
        "research_metadata_graph.py",
        "research_metadata_graph_api.py",
        "research_metadata_graph_display.py",
    }
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "import networkx",
        "from networkx",
        "@router.post",
        "@router.put",
        "@router.patch",
        "@router.delete",
        "def create_graph_database",
        "def persist_graph",
        "def write_graph",
        "def traverse_graph",
        "def query_graph",
        "def search_graph",
        "def rank_graph",
        "def retrieve_graph",
        "def graph_search",
        "def graph_retrieval",
        "def create_embeddings",
        "def create_vector_store",
        "def ingest_graph",
        "def store_graph",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
        "def place_order",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Research Metadata Graph source exposes no graph database/traversal/search/retrieval/embedding/ingestion/storage/parsing/strategy/backtest/recommendation/execution behavior"
    )
    return AuditResult("research metadata graph source boundaries", not bad, detail)


def _check_research_knowledge_map_docs_language() -> AuditResult:
    docs = [
        ROOT / path
        for path in [
            "docs/phases/research_knowledge_map.md",
            "docs/audits/research_artifact_boundaries.md",
            "docs/audits/safety_boundaries.md",
            "docs/audits/no_execution.md",
            "docs/testing/CONSOLIDATION_MAP.md",
            "docs/NEXT_PHASE_PLAN.md",
            "docs/PROMPT_LOG.md",
            "docs/NORTH_STAR.md",
            "docs/API_SURFACE_INVENTORY.md",
            "docs/SAFETY_AUDIT.md",
            "docs/DATA_POLICY.md",
            "docs/INFRASTRUCTURE_STACK.md",
        ]
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in docs if path.exists())
    combined_lower = combined.lower()
    required = [
        "prompt 89",
        "research knowledge map planning and guardrails",
        "planning and guardrails only",
        "planning-only",
        "prompt 90",
        "research knowledge map api contract skeleton",
        "api contract skeleton",
        "api-contract-skeleton-only",
        "request placeholder",
        "response placeholder",
        "reference placeholder",
        "unavailable response",
        "api safety helpers",
        "prompt 91",
        "research knowledge map display contract skeleton",
        "display contract skeleton",
        "display-contract-skeleton-only",
        "item display placeholder",
        "relationship display placeholder",
        "evidence display placeholder",
        "provenance display placeholder",
        "lifecycle display placeholder",
        "unavailable display response",
        "display safety helpers",
        "prompt 92",
        "research knowledge map safety boundary audit",
        "planning safety verdict",
        "api safety verdict",
        "display safety verdict",
        "no active ui/frontend/desktop verdict",
        "no database/tables/migrations verdict",
        "no persistent writes verdict",
        "no traversal/query/search/ranking/retrieval verdict",
        "no embeddings/vector-store verdict",
        "no ingestion/storage/upload/download/preview verdict",
        "no paper parsing verdict",
        "no strategy-generation verdict",
        "no backtesting verdict",
        "no recommendation/no-execution verdict",
        "readiness for phase closure",
        "prompt 93",
        "research knowledge map phase closure",
        "phase closure",
        "phase closed",
        "prompt 94",
        "product surface reorientation and development plan",
        "no active implementation",
        "knowledge item",
        "relationship placeholder",
        "evidence placeholder",
        "provenance placeholder",
        "lifecycle placeholder",
        "readiness",
        "read-only",
        "get-only",
        "phase-based docs/tests policy",
        "no micro-audit sprawl",
        "no active knowledge map",
        "no active ui",
        "no frontend",
        "no desktop",
        "no database",
        "no tables",
        "no migrations",
        "no persistent writes",
        "no traversal",
        "no search",
        "no ranking",
        "no retrieval",
        "no embeddings",
        "no vector store",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "no execution",
    ]
    missing = [phrase for phrase in required if phrase not in combined_lower]
    return AuditResult(
        "research knowledge map docs language",
        not missing,
        ", ".join(missing)
        if missing
        else "Research Knowledge Map planning docs preserve phase policy and forbidden boundaries",
    )


def _check_research_knowledge_map_source_boundaries() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/core/stark_terminal_core/research_knowledge_map",
        ROOT / "packages/core/stark_terminal_core/research_knowledge_map_api",
        ROOT / "packages/core/stark_terminal_core/research_knowledge_map_display",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    route_names = {
        "research_knowledge_map.py",
        "research_knowledge_map_api.py",
        "research_knowledge_map_display.py",
    }
    forbidden_phrases = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import urllib",
        "from urllib",
        "import networkx",
        "from networkx",
        "@router.post",
        "@router.put",
        "@router.patch",
        "@router.delete",
        "def create_database",
        "def create_table",
        "def persist_knowledge",
        "def write_knowledge",
        "def traverse_knowledge",
        "def query_knowledge",
        "def search_knowledge",
        "def rank_knowledge",
        "def retrieve_knowledge",
        "def create_embeddings",
        "def create_vector_store",
        "def ingest_knowledge",
        "def store_knowledge",
        "def upload_file",
        "def download_file",
        "def preview_file",
        "def parse_paper",
        "def parse_pdf",
        "def ingest_arxiv",
        "def analyze_paper_with_llm",
        "def extract_method",
        "def extract_strategy",
        "def generate_strategy",
        "def generate_strategy_code",
        "def run_backtest",
        "def optimize_strategy",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def generate_readiness_status",
        "def execute_trade",
        "def place_order",
    ]
    for root in roots:
        if not root.exists():
            continue
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Research Knowledge Map source exposes no database/traversal/search/retrieval/embedding/parsing/strategy/backtest/recommendation/execution behavior"
    )
    return AuditResult("research knowledge map source boundaries", not bad, detail)


def _check_prompt_84_no_micro_audit_sprawl() -> AuditResult:
    allowed_docs = {
        "RESEARCH_METADATA_GRAPH_PLANNING_AND_GUARDRAILS.md",
        "RESEARCH_METADATA_GRAPH_API_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_DISPLAY_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_READINESS_PLAN.md",
        "RESEARCH_METADATA_GRAPH_SAFETY_BOUNDARY_AUDIT.md",
    }
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_METADATA_GRAPH_*.md")
        if path.name not in allowed_docs
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_metadata_graph*.py")
        if path.name
        not in {
            "test_research_metadata_graph_phase.py",
            "test_research_metadata_graph_boundaries.py",
            "test_api_research_metadata_graph.py",
            "test_research_metadata_graph_api_phase.py",
            "test_research_metadata_graph_api_boundaries.py",
            "test_api_research_metadata_graph_contract.py",
            "test_research_metadata_graph_display_phase.py",
            "test_research_metadata_graph_display_boundaries.py",
            "test_api_research_metadata_graph_display.py",
            "test_research_metadata_graph_safety_audit_phase.py",
            "test_research_metadata_graph_safety_boundaries.py",
            "test_api_research_metadata_graph_safety_surface.py",
            "test_research_metadata_graph_phase_closure.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 84 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 84 no micro audit sprawl", not bad, detail)


def _check_prompt_85_no_micro_audit_sprawl() -> AuditResult:
    allowed_docs = {
        "RESEARCH_METADATA_GRAPH_PLANNING_AND_GUARDRAILS.md",
        "RESEARCH_METADATA_GRAPH_API_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_DISPLAY_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_READINESS_PLAN.md",
        "RESEARCH_METADATA_GRAPH_SAFETY_BOUNDARY_AUDIT.md",
    }
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_METADATA_GRAPH_*.md")
        if path.name not in allowed_docs
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_metadata_graph*.py")
        if path.name
        not in {
            "test_research_metadata_graph_phase.py",
            "test_research_metadata_graph_boundaries.py",
            "test_api_research_metadata_graph.py",
            "test_research_metadata_graph_api_phase.py",
            "test_research_metadata_graph_api_boundaries.py",
            "test_api_research_metadata_graph_contract.py",
            "test_research_metadata_graph_display_phase.py",
            "test_research_metadata_graph_display_boundaries.py",
            "test_api_research_metadata_graph_display.py",
            "test_research_metadata_graph_safety_audit_phase.py",
            "test_research_metadata_graph_safety_boundaries.py",
            "test_api_research_metadata_graph_safety_surface.py",
            "test_research_metadata_graph_phase_closure.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 85 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 85 no micro audit sprawl", not bad, detail)


def _check_prompt_86_no_micro_audit_sprawl() -> AuditResult:
    allowed_docs = {
        "RESEARCH_METADATA_GRAPH_PLANNING_AND_GUARDRAILS.md",
        "RESEARCH_METADATA_GRAPH_API_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_DISPLAY_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_READINESS_PLAN.md",
        "RESEARCH_METADATA_GRAPH_SAFETY_BOUNDARY_AUDIT.md",
    }
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_METADATA_GRAPH_*.md")
        if path.name not in allowed_docs
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_metadata_graph*.py")
        if path.name
        not in {
            "test_research_metadata_graph_phase.py",
            "test_research_metadata_graph_boundaries.py",
            "test_api_research_metadata_graph.py",
            "test_research_metadata_graph_api_phase.py",
            "test_research_metadata_graph_api_boundaries.py",
            "test_api_research_metadata_graph_contract.py",
            "test_research_metadata_graph_display_phase.py",
            "test_research_metadata_graph_display_boundaries.py",
            "test_api_research_metadata_graph_display.py",
            "test_research_metadata_graph_safety_audit_phase.py",
            "test_research_metadata_graph_safety_boundaries.py",
            "test_api_research_metadata_graph_safety_surface.py",
            "test_research_metadata_graph_phase_closure.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 86 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 86 no micro audit sprawl", not bad, detail)


def _check_prompt_87_no_micro_audit_sprawl() -> AuditResult:
    allowed_docs = {
        "RESEARCH_METADATA_GRAPH_PLANNING_AND_GUARDRAILS.md",
        "RESEARCH_METADATA_GRAPH_API_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_DISPLAY_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_READINESS_PLAN.md",
        "RESEARCH_METADATA_GRAPH_SAFETY_BOUNDARY_AUDIT.md",
    }
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_METADATA_GRAPH_*.md")
        if path.name not in allowed_docs
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_metadata_graph*.py")
        if path.name
        not in {
            "test_research_metadata_graph_phase.py",
            "test_research_metadata_graph_boundaries.py",
            "test_api_research_metadata_graph.py",
            "test_research_metadata_graph_api_phase.py",
            "test_research_metadata_graph_api_boundaries.py",
            "test_api_research_metadata_graph_contract.py",
            "test_research_metadata_graph_display_phase.py",
            "test_research_metadata_graph_display_boundaries.py",
            "test_api_research_metadata_graph_display.py",
            "test_research_metadata_graph_safety_audit_phase.py",
            "test_research_metadata_graph_safety_boundaries.py",
            "test_api_research_metadata_graph_safety_surface.py",
            "test_research_metadata_graph_phase_closure.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 87 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 87 no micro audit sprawl", not bad, detail)


def _check_prompt_88_no_micro_audit_sprawl() -> AuditResult:
    allowed_docs = {
        "RESEARCH_METADATA_GRAPH_PLANNING_AND_GUARDRAILS.md",
        "RESEARCH_METADATA_GRAPH_API_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_DISPLAY_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_READINESS_PLAN.md",
        "RESEARCH_METADATA_GRAPH_SAFETY_BOUNDARY_AUDIT.md",
    }
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_METADATA_GRAPH_*.md")
        if path.name not in allowed_docs
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_metadata_graph*.py")
        if path.name
        not in {
            "test_research_metadata_graph_phase.py",
            "test_research_metadata_graph_boundaries.py",
            "test_api_research_metadata_graph.py",
            "test_research_metadata_graph_api_phase.py",
            "test_research_metadata_graph_api_boundaries.py",
            "test_api_research_metadata_graph_contract.py",
            "test_research_metadata_graph_display_phase.py",
            "test_research_metadata_graph_display_boundaries.py",
            "test_api_research_metadata_graph_display.py",
            "test_research_metadata_graph_safety_audit_phase.py",
            "test_research_metadata_graph_safety_boundaries.py",
            "test_api_research_metadata_graph_safety_surface.py",
            "test_research_metadata_graph_phase_closure.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 88 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 88 no micro audit sprawl", not bad, detail)


def _check_prompt_89_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_KNOWLEDGE_MAP*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_knowledge_map*.py")
        if path.name
        not in {
            "test_research_knowledge_map_phase.py",
            "test_research_knowledge_map_boundaries.py",
            "test_api_research_knowledge_map.py",
            "test_research_knowledge_map_api_phase.py",
            "test_research_knowledge_map_api_boundaries.py",
            "test_api_research_knowledge_map_contract.py",
            "test_research_knowledge_map_display_phase.py",
            "test_research_knowledge_map_display_boundaries.py",
            "test_api_research_knowledge_map_display.py",
            "test_research_knowledge_map_safety_phase.py",
            "test_research_knowledge_map_safety_boundaries.py",
            "test_api_research_knowledge_map_safety_surface.py",
            "test_research_knowledge_map_phase_closure.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 89 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 89 no micro audit sprawl", not bad, detail)


def _check_prompt_90_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_KNOWLEDGE_MAP*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_knowledge_map*.py")
        if path.name
        not in {
            "test_research_knowledge_map_phase.py",
            "test_research_knowledge_map_boundaries.py",
            "test_api_research_knowledge_map.py",
            "test_research_knowledge_map_api_phase.py",
            "test_research_knowledge_map_api_boundaries.py",
            "test_api_research_knowledge_map_contract.py",
            "test_research_knowledge_map_display_phase.py",
            "test_research_knowledge_map_display_boundaries.py",
            "test_api_research_knowledge_map_display.py",
            "test_research_knowledge_map_safety_phase.py",
            "test_research_knowledge_map_safety_boundaries.py",
            "test_api_research_knowledge_map_safety_surface.py",
            "test_research_knowledge_map_phase_closure.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 90 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 90 no micro audit sprawl", not bad, detail)


def _check_prompt_91_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_KNOWLEDGE_MAP*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_knowledge_map*.py")
        if path.name
        not in {
            "test_research_knowledge_map_phase.py",
            "test_research_knowledge_map_boundaries.py",
            "test_api_research_knowledge_map.py",
            "test_research_knowledge_map_api_phase.py",
            "test_research_knowledge_map_api_boundaries.py",
            "test_api_research_knowledge_map_contract.py",
            "test_research_knowledge_map_display_phase.py",
            "test_research_knowledge_map_display_boundaries.py",
            "test_api_research_knowledge_map_display.py",
            "test_research_knowledge_map_safety_phase.py",
            "test_research_knowledge_map_safety_boundaries.py",
            "test_api_research_knowledge_map_safety_surface.py",
            "test_research_knowledge_map_phase_closure.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 91 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 91 no micro audit sprawl", not bad, detail)


def _check_prompt_92_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_KNOWLEDGE_MAP*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_knowledge_map*.py")
        if path.name
        not in {
            "test_research_knowledge_map_phase.py",
            "test_research_knowledge_map_boundaries.py",
            "test_api_research_knowledge_map.py",
            "test_research_knowledge_map_api_phase.py",
            "test_research_knowledge_map_api_boundaries.py",
            "test_api_research_knowledge_map_contract.py",
            "test_research_knowledge_map_display_phase.py",
            "test_research_knowledge_map_display_boundaries.py",
            "test_api_research_knowledge_map_display.py",
            "test_research_knowledge_map_safety_phase.py",
            "test_research_knowledge_map_safety_boundaries.py",
            "test_api_research_knowledge_map_safety_surface.py",
            "test_research_knowledge_map_phase_closure.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 92 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 92 no micro audit sprawl", not bad, detail)


def _check_prompt_93_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_KNOWLEDGE_MAP*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*research_knowledge_map*.py")
        if path.name
        not in {
            "test_research_knowledge_map_phase.py",
            "test_research_knowledge_map_boundaries.py",
            "test_api_research_knowledge_map.py",
            "test_research_knowledge_map_api_phase.py",
            "test_research_knowledge_map_api_boundaries.py",
            "test_api_research_knowledge_map_contract.py",
            "test_research_knowledge_map_display_phase.py",
            "test_research_knowledge_map_display_boundaries.py",
            "test_api_research_knowledge_map_display.py",
            "test_research_knowledge_map_safety_phase.py",
            "test_research_knowledge_map_safety_boundaries.py",
            "test_api_research_knowledge_map_safety_surface.py",
            "test_research_knowledge_map_phase_closure.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 93 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 93 no micro audit sprawl", not bad, detail)


def _check_product_surface_reorientation_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/phases/product_surface_reorientation.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Product Surface Reorientation",
        "Retail Decision Console / Decision Desk productization",
        "Prompt 95 - Retail Decision Console Productization Plan and UI Shell Boundary",
        "adds no product runtime capability",
        "Execution APIs remain forbidden",
        "no broker controls",
        "no live trading",
        "no active recommendations",
        "no confidence scoring",
        "no active DecisionObject generation",
        "no fake live market data",
        "phase-based docs/tests",
        "Future work should prioritize product surfaces over audit-only research abstractions",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 94 product surface reorientation language present"
    )
    return AuditResult("product surface reorientation docs language", not missing, detail)


def _check_product_surface_reorientation_no_runtime_capability() -> AuditResult:
    forbidden_paths = [
        "apps/api/stark_terminal_api/routes/product_surface_reorientation.py",
        "packages/core/stark_terminal_core/product_surface_reorientation",
    ]
    bad = [path for path in forbidden_paths if (ROOT / path).exists()]
    detail = (
        ", ".join(bad)
        if bad
        else "Prompt 94 adds no product surface runtime route or package"
    )
    return AuditResult("product surface reorientation no runtime capability", not bad, detail)


def _check_prompt_94_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("PRODUCT_SURFACE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*product_surface_reorientation*.py")
        if path.name
        not in {
            "test_product_surface_reorientation_phase.py",
            "test_product_surface_reorientation_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 94 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 94 no micro audit sprawl", not bad, detail)


def _check_retail_decision_console_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console",
        "Productization Plan and UI Shell Boundary",
        "Prompt 96 - Retail Decision Console UI Shell Skeleton",
        "productization plan and UI shell boundary only",
        "no live decisions",
        "no active recommendations",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject generation",
        "no live market data claims",
        "no broker controls",
        "no order buttons",
        "no execution APIs",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 95 retail decision console productization language present"
    )
    return AuditResult("retail decision console docs language", not missing, detail)


def _check_retail_decision_console_source_boundaries() -> AuditResult:
    roots = [
        ROOT / "packages/core/stark_terminal_core/retail_decision_console",
        ROOT / "apps/api/stark_terminal_api/routes/retail_decision_console.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    ]
    forbidden = [
        "import requests",
        "from requests",
        "requests.",
        "import httpx",
        "from httpx",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "@router.post",
        "@router.put",
        "@router.patch",
        "@router.delete",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def place_order",
        "def execute_trade",
        "def broker",
        "order_button_handler",
        "live_market_data_display",
    ]
    bad: list[str] = []
    for root in roots:
        paths = [root] if root.is_file() else sorted(root.glob("*.py"))
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console source has no external calls, write routes, recommendation, broker, order, or execution behavior"
    )
    return AuditResult("retail decision console source boundaries", not bad, detail)


def _check_retail_decision_console_ui_shell_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console UI Shell Skeleton",
        "desktop shell scope",
        "UI shell skeleton only",
        "Prompt 97 - Retail Decision Console Demo Data Contract and Static State Model",
        "no live data",
        "no generated recommendations",
        "no confidence scoring",
        "no active DecisionObjects",
        "no active DecisionObject generation",
        "no live market data claims",
        "no broker controls",
        "no order buttons",
        "no execution APIs",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 96 retail decision console UI shell language present"
    )
    return AuditResult("retail decision console ui shell docs language", not missing, detail)


def _check_retail_decision_console_ui_shell_source_boundaries() -> AuditResult:
    files = [
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_descriptors.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_shell.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    ]
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
    ]
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console UI shell has no external calls, timers, threads, broker, order, or execution behavior"
    )
    return AuditResult("retail decision console ui shell source boundaries", not bad, detail)


def _check_retail_decision_console_demo_state_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/API_SURFACE_INVENTORY.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console Demo Data Contract and Static State Model",
        "demo_static_state",
        "/retail-decision-console/demo-state",
        "demo/static state",
        "demo-only",
        "unavailable",
        "no live data",
        "no generated recommendations",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject generation",
        "no broker controls",
        "no order buttons",
        "no execution APIs",
        "Prompt 98 - Retail Decision Console Static State Wiring into Desktop Shell",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 97 retail decision console demo static state language present"
    )
    return AuditResult("retail decision console demo state docs language", not missing, detail)


def _check_retail_decision_console_demo_state_source_boundaries() -> AuditResult:
    files = [
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/static_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/demo_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_safety.py",
    ]
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
    ]
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console demo state has no external calls, timers, threads, broker, order, recommendation, confidence, DecisionObject, or execution behavior"
    )
    return AuditResult("retail decision console demo state source boundaries", not bad, detail)


def _check_retail_decision_console_static_state_wiring_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/API_SURFACE_INVENTORY.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console Static State Wiring into Desktop Shell",
        "static_state_wired_shell",
        "/retail-decision-console/static-state-view-model",
        "state-to-view mapping",
        "demo/static state wired",
        "desktop shell wiring scope",
        "no live data",
        "no generated recommendations",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject generation",
        "no broker controls",
        "no order buttons",
        "no execution APIs",
        "Prompt 99 - Retail Decision Console Local Preview Runbook and Manual Smoke Test",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 98 retail decision console static state wiring language present"
    )
    return AuditResult("retail decision console static state wiring docs language", not missing, detail)


def _check_retail_decision_console_static_state_wiring_source_boundaries() -> AuditResult:
    files = [
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_view_model.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_descriptors.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_shell.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/static_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/demo_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_safety.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    ]
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "client.get",
        "api.get",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
    ]
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console static state wiring has no external calls, timers, threads, broker, order, recommendation, confidence, DecisionObject, or execution behavior"
    )
    return AuditResult("retail decision console static state wiring source boundaries", not bad, detail)


def _check_retail_decision_console_local_preview_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/runbooks/retail_decision_console_local_preview.md",
        ROOT / "docs/runbooks/retail_decision_console_manual_smoke_test.md",
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console Local Preview Runbook and Manual Smoke Test",
        "local_preview_runbook",
        "docs/runbooks/retail_decision_console_local_preview.md",
        "docs/runbooks/retail_decision_console_manual_smoke_test.md",
        "scripts/preview_retail_decision_console.py",
        "Demo/static preview only",
        "no live data",
        "no generated recommendations",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject generation",
        "no active DecisionObjects",
        "no broker controls",
        "no order buttons",
        "no execution APIs",
        "Prompt 100 - Retail Decision Console Visual Polish and Section Layout Pass",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 99 retail decision console local preview language present"
    )
    return AuditResult("retail decision console local preview docs language", not missing, detail)


def _check_retail_decision_console_local_preview_source_boundaries() -> AuditResult:
    files = [
        ROOT / "scripts/preview_retail_decision_console.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_view_model.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_descriptors.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_shell.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/static_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/demo_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_safety.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    ]
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "client.get",
        "api.get",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
    ]
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console local preview has no external calls, timers, threads, broker, order, recommendation, confidence, DecisionObject, or execution behavior"
    )
    return AuditResult("retail decision console local preview source boundaries", not bad, detail)


def _check_retail_decision_console_visual_layout_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/runbooks/retail_decision_console_local_preview.md",
        ROOT / "docs/runbooks/retail_decision_console_manual_smoke_test.md",
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/API_SURFACE_INVENTORY.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console Visual Polish and Section Layout Pass",
        "visual_layout_pass",
        "layout zones",
        "section/card ordering",
        "Demo/static preview only",
        "no live data",
        "no generated recommendations",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject generation",
        "no active DecisionObjects",
        "no broker controls",
        "no order buttons",
        "no execution APIs",
        "Prompt 101 - Retail Decision Console Static Interaction Placeholders",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 100 retail decision console visual layout language present"
    )
    return AuditResult("retail decision console visual layout docs language", not missing, detail)


def _check_retail_decision_console_visual_layout_source_boundaries() -> AuditResult:
    files = [
        ROOT / "scripts/preview_retail_decision_console.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/layout.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_view_model.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_descriptors.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_shell.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/static_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/demo_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_safety.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    ]
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "client.get",
        "api.get",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
    ]
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console visual layout has no external calls, timers, threads, broker, order, recommendation, confidence, DecisionObject, or execution behavior"
    )
    return AuditResult("retail decision console visual layout source boundaries", not bad, detail)


def _check_retail_decision_console_static_interaction_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/runbooks/retail_decision_console_local_preview.md",
        ROOT / "docs/runbooks/retail_decision_console_manual_smoke_test.md",
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/API_SURFACE_INVENTORY.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console Static Interaction Placeholders",
        "static_interaction_placeholders",
        "allowed static interactions",
        "forbidden interaction types",
        "Static interactions:",
        "demo-only unavailable local-only",
        "local-only placeholder interactions",
        "no live data",
        "no generated recommendations",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject generation",
        "no active DecisionObjects",
        "no broker controls",
        "no order buttons",
        "no execution APIs",
        "Prompt 102 - Retail Decision Console Preview Snapshot Export",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 101 retail decision console static interaction language present"
    )
    return AuditResult("retail decision console static interaction docs language", not missing, detail)


def _check_retail_decision_console_static_interaction_source_boundaries() -> AuditResult:
    files = [
        ROOT / "scripts/preview_retail_decision_console.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/interactions.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/layout.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_view_model.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_descriptors.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_shell.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/static_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/demo_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_safety.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    ]
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "client.get",
        "api.get",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def fetch_",
        "def start_timer",
        "def start_thread",
    ]
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console static interactions have no external calls, timers, threads, broker, order, recommendation, confidence, DecisionObject, or execution behavior"
    )
    return AuditResult("retail decision console static interaction source boundaries", not bad, detail)


def _check_retail_decision_console_preview_snapshot_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/runbooks/retail_decision_console_local_preview.md",
        ROOT / "docs/runbooks/retail_decision_console_manual_smoke_test.md",
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/API_SURFACE_INVENTORY.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console Preview Snapshot Export",
        "preview_snapshot_export",
        "--print-snapshot",
        "--export-snapshot",
        "JSON, Markdown, and text",
        "no secrets",
        "no credentials",
        "no live data",
        "no generated recommendations",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObject generation",
        "no active DecisionObjects",
        "no broker controls",
        "no order buttons",
        "no execution APIs",
        "Prompt 103 - Retail Decision Console Local QA Bundle",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 102 retail decision console preview snapshot language present"
    )
    return AuditResult("retail decision console preview snapshot docs language", not missing, detail)


def _check_retail_decision_console_preview_snapshot_source_boundaries() -> AuditResult:
    files = [
        ROOT / "scripts/preview_retail_decision_console.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/snapshot_export.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/interactions.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/layout.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_view_model.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_descriptors.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_shell.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/static_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/demo_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_safety.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    ]
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "client.get",
        "api.get",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def fetch_",
        "def start_timer",
        "def start_thread",
    ]
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    script_text = (ROOT / "scripts/preview_retail_decision_console.py").read_text(encoding="utf-8")
    for phrase in ["provider", "broker", "credential"]:
        if phrase in script_text:
            bad.append(f"scripts/preview_retail_decision_console.py:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console preview snapshot has no external calls, timers, threads, active decision generation, broker, order, or execution behavior"
    )
    return AuditResult("retail decision console preview snapshot source boundaries", not bad, detail)


def _check_retail_decision_console_local_qa_bundle_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/runbooks/retail_decision_console_local_preview.md",
        ROOT / "docs/runbooks/retail_decision_console_manual_smoke_test.md",
        ROOT / "docs/runbooks/retail_decision_console_local_qa_bundle.md",
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/API_SURFACE_INVENTORY.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console Local QA Bundle",
        "local_qa_bundle",
        "build_retail_decision_console_qa_bundle.py",
        "manifest.json",
        "preview_snapshot.json",
        "preview_snapshot.md",
        "no_gui_preview.txt",
        "safety_summary.txt",
        "no secrets",
        "no credentials",
        "no live data",
        "no recommendations",
        "no confidence scoring",
        "no active DecisionObject generation",
        "no active DecisionObjects",
        "no broker controls",
        "no order buttons",
        "no execution APIs",
        "Prompt 104 - Retail Decision Console Manual Acceptance Checklist",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 103 retail decision console local QA bundle language present"
    )
    return AuditResult("retail decision console local QA bundle docs language", not missing, detail)


def _check_retail_decision_console_local_qa_bundle_source_boundaries() -> AuditResult:
    files = [
        ROOT / "scripts/build_retail_decision_console_qa_bundle.py",
        ROOT / "scripts/preview_retail_decision_console.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/qa_bundle.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/snapshot_export.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/interactions.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/layout.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_view_model.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_descriptors.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_shell.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/static_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/demo_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_safety.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    ]
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "client.get",
        "api.get",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def fetch_",
        "def start_timer",
        "def start_thread",
    ]
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    for script in [
        ROOT / "scripts/build_retail_decision_console_qa_bundle.py",
        ROOT / "scripts/preview_retail_decision_console.py",
    ]:
        script_text = script.read_text(encoding="utf-8")
        for phrase in ["provider", "broker", "credential"]:
            if phrase in script_text:
                bad.append(f"{script.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console local QA bundle has no external calls, timers, threads, active decision generation, broker, order, or execution behavior"
    )
    return AuditResult("retail decision console local QA bundle source boundaries", not bad, detail)


def _check_retail_decision_console_manual_acceptance_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/runbooks/retail_decision_console_manual_acceptance_checklist.md",
        ROOT / "docs/runbooks/retail_decision_console_local_preview.md",
        ROOT / "docs/runbooks/retail_decision_console_manual_smoke_test.md",
        ROOT / "docs/runbooks/retail_decision_console_local_qa_bundle.md",
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console Manual Acceptance Checklist",
        "manual_acceptance_checklist",
        "not production acceptance",
        "not trading-readiness acceptance",
        "not recommendation-readiness acceptance",
        "not execution-readiness acceptance",
        "Acceptance scope: local demo preview only",
        ".venv/bin/python scripts/preview_retail_decision_console.py --no-gui",
        ".venv/bin/python scripts/preview_retail_decision_console.py --print-snapshot",
        ".venv/bin/python scripts/preview_retail_decision_console.py --export-snapshot tmp/preview_snapshots/retail_decision_console_snapshot.json --snapshot-format json",
        ".venv/bin/python scripts/build_retail_decision_console_qa_bundle.py --output-dir tmp/retail_decision_console_qa_bundle --clean --print-manifest",
        "Visual Acceptance Checks",
        "Safety Acceptance Checks",
        "Snapshot Acceptance Checks",
        "QA Bundle Acceptance Checks",
        "Failure Criteria",
        "Acceptance Verdict Template",
        "no live data",
        "no recommendations",
        "no confidence scoring",
        "no active DecisionObjects",
        "no broker controls",
        "no order buttons",
        "no execution",
        "Prompt 105 - Retail Decision Console Shareable Internal Preview Package",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 104 retail decision console manual acceptance language present"
    )
    return AuditResult("retail decision console manual acceptance docs language", not missing, detail)


def _check_retail_decision_console_manual_acceptance_source_boundaries() -> AuditResult:
    optional_files = [
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/acceptance.py",
        ROOT / "scripts/check_retail_decision_console_acceptance.py",
    ]
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "client.get",
        "api.get",
        "provider",
        "broker",
        "credential",
        "place_order",
        "execute_trade",
        "connect_broker",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def fetch_",
        "def start_timer",
        "def start_thread",
    ]
    bad: list[str] = []
    for path in optional_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console manual acceptance adds no external calls, timers, threads, providers, brokers, credentials, active decision generation, order controls, or execution behavior"
    )
    return AuditResult("retail decision console manual acceptance source boundaries", not bad, detail)


def _check_retail_decision_console_internal_preview_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/runbooks/retail_decision_console_internal_preview_package.md",
        ROOT / "docs/templates/retail_decision_console_internal_review_notes.md",
        ROOT / "docs/runbooks/retail_decision_console_manual_acceptance_checklist.md",
        ROOT / "docs/runbooks/retail_decision_console_local_preview.md",
        ROOT / "docs/runbooks/retail_decision_console_manual_smoke_test.md",
        ROOT / "docs/runbooks/retail_decision_console_local_qa_bundle.md",
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console Shareable Internal Preview Package",
        "internal_preview_package",
        "build_retail_decision_console_internal_preview.py",
        "retail_decision_console_internal_preview_package.md",
        "retail_decision_console_internal_review_notes.md",
        "internal_preview_manifest.json",
        "README_INTERNAL_PREVIEW.md",
        "preview_snapshot.json",
        "preview_snapshot.md",
        "no_gui_preview.txt",
        "safety_summary.txt",
        "manual_acceptance_checklist.md",
        "manual_smoke_test.md",
        "local_preview_runbook.md",
        "local_qa_bundle_runbook.md",
        "internal_review_notes.md",
        "not production ready",
        "not trading ready",
        "not recommendation ready",
        "not execution ready",
        "no secrets",
        "no credentials",
        "no live data",
        "no recommendations",
        "no confidence scoring",
        "no active DecisionObjects",
        "no broker controls",
        "no order buttons",
        "no execution",
        "Prompt 106 - Retail Decision Console Internal Preview Package Smoke Verification",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 105 retail decision console internal preview package language present"
    )
    return AuditResult("retail decision console internal preview package docs language", not missing, detail)


def _check_retail_decision_console_internal_preview_source_boundaries() -> AuditResult:
    files = [
        ROOT / "scripts/build_retail_decision_console_internal_preview.py",
        ROOT / "scripts/build_retail_decision_console_qa_bundle.py",
        ROOT / "scripts/preview_retail_decision_console.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/internal_preview_package.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/qa_bundle.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/snapshot_export.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/interactions.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/layout.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_view_model.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_descriptors.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/ui_shell.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/static_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/demo_state.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/state_safety.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_decision_console.py",
    ]
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "client.get",
        "api.get",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def fetch_",
        "def start_timer",
        "def start_thread",
    ]
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    for script in [
        ROOT / "scripts/build_retail_decision_console_internal_preview.py",
        ROOT / "scripts/build_retail_decision_console_qa_bundle.py",
        ROOT / "scripts/preview_retail_decision_console.py",
    ]:
        script_text = script.read_text(encoding="utf-8")
        for phrase in ["provider", "broker", "credential"]:
            if phrase in script_text:
                bad.append(f"{script.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console internal preview package has no external calls, timers, threads, active decision generation, broker, order, or execution behavior"
    )
    return AuditResult("retail decision console internal preview package source boundaries", not bad, detail)


def _check_retail_decision_console_internal_preview_smoke_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/runbooks/retail_decision_console_internal_preview_package.md",
        ROOT / "docs/runbooks/retail_decision_console_manual_acceptance_checklist.md",
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/PROMPT_LOG.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
        ROOT / "docs/testing/TEST_BASELINE.md",
        ROOT / "docs/testing/CONSOLIDATION_MAP.md",
        ROOT / "PROJECT_MAP.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console Internal Preview Package Smoke Verification",
        "internal_preview_smoke_verification",
        "internal_preview_smoke.py",
        "smoke_verify_retail_decision_console_internal_preview.py",
        "internal_preview_manifest.json",
        "README_INTERNAL_PREVIEW.md",
        "preview_snapshot.json",
        "preview_snapshot.md",
        "no_gui_preview.txt",
        "safety_summary.txt",
        "manual_acceptance_checklist.md",
        "manual_smoke_test.md",
        "local_preview_runbook.md",
        "local_qa_bundle_runbook.md",
        "internal_review_notes.md",
        "Passed: true",
        "not production ready",
        "not trading ready",
        "not recommendation ready",
        "not execution ready",
        "no secrets",
        "no credentials",
        "no live data",
        "no recommendations",
        "no confidence scoring",
        "no active DecisionObjects",
        "no broker controls",
        "no order buttons",
        "no execution",
        "Prompt 107 - Retail Decision Console Internal Preview Milestone Closure",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 106 retail decision console internal preview smoke language present"
    )
    return AuditResult("retail decision console internal preview smoke docs language", not missing, detail)


def _check_retail_decision_console_internal_preview_smoke_source_boundaries() -> AuditResult:
    files = [
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/internal_preview_smoke.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/internal_preview_package.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/qa_bundle.py",
        ROOT / "packages/core/stark_terminal_core/retail_decision_console/snapshot_export.py",
    ]
    forbidden = [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "client.get",
        "api.get",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
        "def generate_recommendation",
        "def generate_action",
        "def score_confidence",
        "def generate_decision_object",
        "def fetch_",
        "def start_timer",
        "def start_thread",
    ]
    bad: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    script = ROOT / "scripts/smoke_verify_retail_decision_console_internal_preview.py"
    script_text = script.read_text(encoding="utf-8")
    for phrase in [
        "requests.",
        "httpx.",
        "urllib",
        "QTimer",
        "QThread",
        "threading",
        "asyncio",
        "subprocess",
        "client.get",
        "api.get",
        "provider",
        "broker",
        "credential",
        "place_order",
        "execute_trade",
        "connect_broker",
        "order_button_handler",
    ]:
        if phrase in script_text:
            bad.append(f"{script.relative_to(ROOT)}:{phrase}")
    detail = (
        ", ".join(bad)
        if bad
        else "Retail Decision Console internal preview smoke verification has no network, API, timers, threads, active decision generation, broker, order, or execution behavior"
    )
    return AuditResult("retail decision console internal preview smoke source boundaries", not bad, detail)


def _check_retail_decision_console_internal_preview_milestone_docs_language() -> AuditResult:
    files = [
        ROOT / "docs/phases/retail_decision_console.md",
        ROOT / "docs/NORTH_STAR.md",
        ROOT / "docs/NEXT_PHASE_PLAN.md",
        ROOT / "docs/PROMPT_LOG.md",
        ROOT / "docs/SAFETY_AUDIT.md",
        ROOT / "docs/DATA_POLICY.md",
        ROOT / "docs/INFRASTRUCTURE_STACK.md",
        ROOT / "docs/testing/TEST_BASELINE.md",
        ROOT / "docs/testing/CONSOLIDATION_MAP.md",
        ROOT / "PROJECT_MAP.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)
    required = [
        "Retail Decision Console Internal Preview Milestone Closure",
        "internal_preview_milestone_closed",
        "internal preview milestone is closed",
        "safe for internal local preview only",
        "not production ready",
        "not trading ready",
        "not recommendation ready",
        "not execution ready",
        "desktop shell module",
        "demo/static state modules",
        "layout module",
        "interaction module",
        "snapshot export module",
        "QA bundle module",
        "internal preview package module",
        "internal preview smoke module",
        "preview script",
        "QA bundle script",
        "internal preview package script",
        "smoke verification script",
        "local preview runbook",
        "manual smoke test runbook",
        "local QA bundle runbook",
        "manual acceptance checklist",
        "internal preview package runbook",
        "internal review notes template",
        "no live data",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "no active DecisionObjects",
        "no broker controls",
        "no order buttons",
        "no execution APIs",
        "git commit -m \"Close retail decision console internal preview milestone\"",
        "Prompt 108 - Retail Decision Console Post-Preview UX Backlog and Next Product Phase Selection",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    detail = (
        ", ".join(missing)
        if missing
        else "Prompt 107 retail decision console internal preview milestone closure language present"
    )
    return AuditResult("retail decision console internal preview milestone docs language", not missing, detail)


def _check_prompt_107_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
            "test_retail_decision_console_manual_acceptance_phase.py",
            "test_retail_decision_console_manual_acceptance_boundaries.py",
            "test_retail_decision_console_internal_preview_package_phase.py",
            "test_retail_decision_console_internal_preview_package_boundaries.py",
            "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 107 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 107 no micro audit sprawl", not bad, detail)


def _check_prompt_106_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
            "test_retail_decision_console_manual_acceptance_phase.py",
            "test_retail_decision_console_manual_acceptance_boundaries.py",
            "test_retail_decision_console_internal_preview_package_phase.py",
            "test_retail_decision_console_internal_preview_package_boundaries.py",
            "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 106 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 106 no micro audit sprawl", not bad, detail)


def _check_prompt_105_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
            "test_retail_decision_console_manual_acceptance_phase.py",
            "test_retail_decision_console_manual_acceptance_boundaries.py",
            "test_retail_decision_console_internal_preview_package_phase.py",
            "test_retail_decision_console_internal_preview_package_boundaries.py",
            "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 105 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 105 no micro audit sprawl", not bad, detail)


def _check_prompt_104_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
        "test_retail_decision_console_manual_acceptance_phase.py",
            "test_retail_decision_console_manual_acceptance_boundaries.py",
        "test_retail_decision_console_internal_preview_package_phase.py",
        "test_retail_decision_console_internal_preview_package_boundaries.py",
        "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 104 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 104 no micro audit sprawl", not bad, detail)


def _check_prompt_103_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
            "test_retail_decision_console_manual_acceptance_phase.py",
            "test_retail_decision_console_manual_acceptance_boundaries.py",
        "test_retail_decision_console_internal_preview_package_phase.py",
        "test_retail_decision_console_internal_preview_package_boundaries.py",
        "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 103 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 103 no micro audit sprawl", not bad, detail)


def _check_prompt_102_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
        "test_retail_decision_console_manual_acceptance_phase.py",
        "test_retail_decision_console_manual_acceptance_boundaries.py",
        "test_retail_decision_console_internal_preview_package_phase.py",
        "test_retail_decision_console_internal_preview_package_boundaries.py",
        "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 102 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 102 no micro audit sprawl", not bad, detail)


def _check_prompt_101_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
        "test_retail_decision_console_manual_acceptance_phase.py",
        "test_retail_decision_console_manual_acceptance_boundaries.py",
        "test_retail_decision_console_internal_preview_package_phase.py",
        "test_retail_decision_console_internal_preview_package_boundaries.py",
        "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 101 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 101 no micro audit sprawl", not bad, detail)


def _check_prompt_100_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
        "test_retail_decision_console_manual_acceptance_phase.py",
        "test_retail_decision_console_manual_acceptance_boundaries.py",
        "test_retail_decision_console_internal_preview_package_phase.py",
        "test_retail_decision_console_internal_preview_package_boundaries.py",
        "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 100 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 100 no micro audit sprawl", not bad, detail)


def _check_prompt_95_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
        "test_retail_decision_console_manual_acceptance_phase.py",
        "test_retail_decision_console_manual_acceptance_boundaries.py",
        "test_retail_decision_console_internal_preview_package_phase.py",
        "test_retail_decision_console_internal_preview_package_boundaries.py",
        "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 95 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 95 no micro audit sprawl", not bad, detail)


def _check_prompt_96_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
        "test_retail_decision_console_manual_acceptance_phase.py",
        "test_retail_decision_console_manual_acceptance_boundaries.py",
        "test_retail_decision_console_internal_preview_package_phase.py",
        "test_retail_decision_console_internal_preview_package_boundaries.py",
        "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 96 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 96 no micro audit sprawl", not bad, detail)


def _check_prompt_97_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
        "test_retail_decision_console_manual_acceptance_phase.py",
        "test_retail_decision_console_manual_acceptance_boundaries.py",
        "test_retail_decision_console_internal_preview_package_phase.py",
        "test_retail_decision_console_internal_preview_package_boundaries.py",
        "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 97 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 97 no micro audit sprawl", not bad, detail)


def _check_prompt_98_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
        "test_retail_decision_console_manual_acceptance_phase.py",
        "test_retail_decision_console_manual_acceptance_boundaries.py",
        "test_retail_decision_console_internal_preview_package_phase.py",
        "test_retail_decision_console_internal_preview_package_boundaries.py",
        "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 98 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 98 no micro audit sprawl", not bad, detail)


def _check_prompt_99_no_micro_audit_sprawl() -> AuditResult:
    docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RETAIL_DECISION_CONSOLE*.md")
    ]
    tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*retail_decision_console*.py")
        if path.name
        not in {
            "test_retail_decision_console_phase.py",
            "test_retail_decision_console_boundaries.py",
            "test_api_retail_decision_console.py",
            "test_retail_decision_console_ui_shell_phase.py",
            "test_retail_decision_console_ui_shell_boundaries.py",
            "test_desktop_retail_decision_console_shell.py",
            "test_retail_decision_console_demo_state_phase.py",
            "test_retail_decision_console_demo_state_boundaries.py",
            "test_api_retail_decision_console_demo_state.py",
            "test_retail_decision_console_static_state_wiring_phase.py",
            "test_retail_decision_console_static_state_wiring_boundaries.py",
            "test_desktop_retail_decision_console_static_state_wiring.py",
            "test_api_retail_decision_console_static_state_wiring.py",
            "test_retail_decision_console_local_preview_phase.py",
            "test_retail_decision_console_local_preview_boundaries.py",
            "test_preview_retail_decision_console_script.py",
            "test_retail_decision_console_visual_layout_phase.py",
            "test_retail_decision_console_visual_layout_boundaries.py",
            "test_desktop_retail_decision_console_visual_layout.py",
            "test_retail_decision_console_static_interactions_phase.py",
            "test_retail_decision_console_static_interactions_boundaries.py",
            "test_desktop_retail_decision_console_static_interactions.py",
            "test_retail_decision_console_preview_snapshot_phase.py",
            "test_retail_decision_console_preview_snapshot_boundaries.py",
            "test_preview_retail_decision_console_snapshot_script.py",
            "test_retail_decision_console_local_qa_bundle_phase.py",
            "test_retail_decision_console_local_qa_bundle_boundaries.py",
            "test_build_retail_decision_console_qa_bundle_script.py",
        "test_retail_decision_console_manual_acceptance_phase.py",
        "test_retail_decision_console_manual_acceptance_boundaries.py",
        "test_retail_decision_console_internal_preview_package_phase.py",
        "test_retail_decision_console_internal_preview_package_boundaries.py",
        "test_build_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_smoke_phase.py",
            "test_retail_decision_console_internal_preview_smoke_boundaries.py",
            "test_smoke_verify_retail_decision_console_internal_preview_script.py",
            "test_retail_decision_console_internal_preview_milestone_closure.py",
            "test_retail_decision_console_internal_preview_milestone_boundaries.py",
        }
    ]
    bad = docs + tests
    detail = ", ".join(bad) if bad else "Prompt 99 added no micro-audit doc/test sprawl"
    return AuditResult("prompt 99 no micro audit sprawl", not bad, detail)


def _check_analytics_modules_no_external_imports() -> AuditResult:
    bad: list[str] = []
    analytics_root = ROOT / "packages/analytics/stark_terminal_analytics"
    for path in analytics_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for phrase in ANALYTICS_EXTERNAL_IMPORT_PHRASES:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "analytics modules import no external-call clients"
    return AuditResult("analytics external imports", not bad, detail)


def _check_analytics_modules_no_action_terms() -> AuditResult:
    bad: list[str] = []
    analytics_root = ROOT / "packages/analytics/stark_terminal_analytics"
    for path in analytics_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for term in FORBIDDEN_ANALYTICS_ACTION_TERMS:
            if re.search(rf"\b{re.escape(term)}\b", text):
                bad.append(f"{path.relative_to(ROOT)}:{term}")
    detail = ", ".join(bad) if bad else "analytics modules expose no buy/sell/hold/watch/avoid action terms"
    return AuditResult("analytics action terms", not bad, detail)


def _check_heavy_analytics_dependencies_not_added() -> AuditResult:
    dependencies = _project_dependencies()
    bad = sorted(dependencies & FORBIDDEN_HEAVY_ANALYTICS_DEPENDENCIES)
    detail = ", ".join(bad) if bad else "no unexpected heavy analytics dependencies"
    return AuditResult("analytics dependencies", not bad, detail)


def _check_prompt_log() -> AuditResult:
    text = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    expected = [
        f"Prompt {number:02d}" for number in range(10)
    ] + [
        "Prompt 10",
        "Prompt 11",
        "Prompt 12",
        "Prompt 13",
        "Prompt 14",
        "Prompt 15",
        "Prompt 16",
        "Prompt 17",
        "Prompt 18",
        "Prompt 19",
        "Prompt 20",
        "Prompt 21",
        "Prompt 22",
        "Prompt 23",
        "Prompt 24",
        "Prompt 25",
        "Prompt 26",
        "Prompt 27",
        "Prompt 28",
        "Prompt 29",
        "Prompt 30",
        "Prompt 31",
        "Prompt 32",
        "Prompt 33",
        "Prompt 34",
        "Prompt 35",
        "Prompt 36",
        "Prompt 37",
        "Prompt 38",
        "Prompt 39",
        "Prompt 40",
        "Prompt 41",
        "Prompt 42",
        "Prompt 43",
        "Prompt 44",
        "Prompt 45",
        "Prompt 46",
        "Prompt 47",
        "Prompt 48",
        "Prompt 49",
        "Prompt 50",
        "Prompt 51",
        "Prompt 52",
        "Prompt 53",
        "Prompt 54",
        "Prompt 55",
        "Prompt 56",
        "Prompt 57",
        "Prompt 58",
        "Prompt 59",
        "Prompt 60",
        "Prompt 61",
        "Prompt 62",
        "Prompt 63",
        "Prompt 64",
        "Prompt 65",
        "Prompt 66",
        "Prompt 67",
        "Prompt 68",
        "Prompt 69",
        "Prompt 70",
        "Prompt 71",
        "Prompt 72",
        "Prompt 73",
        "Prompt 74",
        "Prompt 75",
        "Prompt 76",
        "Prompt 77",
        "Prompt 78",
        "Prompt 79",
        "Prompt 80",
        "Prompt 81",
        "Prompt 82",
        "Prompt 83",
        "Prompt 84",
        "Prompt 85",
        "Prompt 86",
        "Prompt 87",
        "Prompt 88",
        "Prompt 89",
        "Prompt 90",
        "Prompt 91",
        "Prompt 92",
        "Prompt 93",
        "Prompt 94",
        "Prompt 95",
        "Prompt 96",
        "Prompt 97",
        "Prompt 98",
        "Prompt 99",
        "Prompt 100",
        "Prompt 101",
        "Prompt 102",
        "Prompt 103",
        "Prompt 104",
        "Prompt 105",
        "Prompt 106",
        "Prompt 107",
        "Repo Documentation/Test Consolidation",
    ]
    missing = [entry for entry in expected if entry not in text]
    return AuditResult(
        "prompt log",
        not missing,
        ", ".join(missing) if missing else "Prompt 00 through Prompt 107 plus consolidation interlude present",
    )


def _check_north_star_status() -> AuditResult:
    text = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    required = [
        "Current Prompt: 107",
        "Completed Prompts: 108 after completion",
        "Current Milestone: Retail Decision Console Internal Preview - Closed",
        "Next Action: commit/push before starting next phase",
        "Next Focus: Retail Decision Console Post-Preview UX Backlog and Next Product Phase Selection",
        "Retail Decision Console Status: internal preview milestone closed; static/demo/unavailable/read-only only",
        "Audit Verdict: Retail Decision Console Internal Preview Milestone Closure complete; ready for commit/push before Prompt 108 only if tests pass",
        "Prompt 107 implements Retail Decision Console Internal Preview Milestone Closure",
        "Verifier lock: Retail Decision Console Status: internal preview milestone closed; static/demo/unavailable/read-only only; not production ready; not trading ready; not recommendation ready; not execution ready; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Historical verifier reference: Current Prompt: 106",
        "Historical verifier reference: Completed Prompts: 107 after completion",
        "Historical verifier reference: Current Milestone: Retail Decision Console Productization - Internal Preview Smoke Verification",
        "Historical verifier reference: Next Focus: Retail Decision Console Internal Preview Milestone Closure",
        "Historical verifier reference: Retail Decision Console Status: internal preview package smoke-verified; still static/demo/unavailable only",
        "Historical verifier reference: Audit Verdict: Retail Decision Console Internal Preview Package Smoke Verification complete; ready for Retail Decision Console Internal Preview Milestone Closure only if tests pass",
        "Prompt 106 implements Retail Decision Console Internal Preview Package Smoke Verification",
        "Verifier lock: Retail Decision Console Status: internal preview package smoke-verified; still static/demo/unavailable only; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Current Prompt: 105",
        "Completed Prompts: 106 after completion",
        "Current Milestone: Retail Decision Console Productization - Shareable Internal Preview Package",
        "Next Focus: Retail Decision Console Internal Preview Package Smoke Verification",
        "Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, local QA bundle, manual acceptance checklist, and shareable internal preview package",
        "Audit Verdict: Retail Decision Console Shareable Internal Preview Package complete; ready for Retail Decision Console Internal Preview Package Smoke Verification only if tests pass",
        "Prompt 105 implements Retail Decision Console Shareable Internal Preview Package",
        "Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, local QA bundle, manual acceptance checklist, and shareable internal preview package; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Current Prompt: 104",
        "Completed Prompts: 105 after completion",
        "Current Milestone: Retail Decision Console Productization - Manual Acceptance Checklist",
        "Next Focus: Retail Decision Console Shareable Internal Preview Package",
        "Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, local QA bundle, and manual acceptance checklist",
        "Audit Verdict: Retail Decision Console Manual Acceptance Checklist complete; ready for Retail Decision Console Shareable Internal Preview Package only if tests pass",
        "Prompt 104 implements Retail Decision Console Manual Acceptance Checklist",
        "Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, local QA bundle, and manual acceptance checklist; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Current Prompt: 103",
        "Completed Prompts: 104 after completion",
        "Current Milestone: Retail Decision Console Productization - Local QA Bundle",
        "Next Focus: Retail Decision Console Manual Acceptance Checklist",
        "Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, and local QA bundle",
        "Audit Verdict: Retail Decision Console Local QA Bundle complete; ready for Retail Decision Console Manual Acceptance Checklist only if tests pass",
        "Prompt 103 implements Retail Decision Console Local QA Bundle",
        "Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, snapshot export, and local QA bundle; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Current Prompt: 102",
        "Completed Prompts: 103 after completion",
        "Current Milestone: Retail Decision Console Productization - Preview Snapshot Export",
        "Next Focus: Retail Decision Console Local QA Bundle",
        "Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, and safe local snapshot export",
        "Audit Verdict: Retail Decision Console Preview Snapshot Export complete; ready for Retail Decision Console Local QA Bundle only if tests pass",
        "Prompt 102 implements Retail Decision Console Preview Snapshot Export",
        "Verifier lock: Retail Decision Console Status: static/demo shell with layout, local placeholder interactions, and safe local snapshot export; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Current Prompt: 101",
        "Completed Prompts: 102 after completion",
        "Current Milestone: Retail Decision Console Productization - Static Interaction Placeholders",
        "Next Focus: Retail Decision Console Preview Snapshot Export",
        "Retail Decision Console Status: static/demo shell with polished layout and local-only placeholder interactions",
        "Audit Verdict: Retail Decision Console Static Interaction Placeholders complete; ready for Retail Decision Console Preview Snapshot Export only if tests pass",
        "Prompt 101 implements Retail Decision Console Static Interaction Placeholders",
        "Verifier lock: Retail Decision Console Status: static/demo shell with polished layout and local-only placeholder interactions; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Current Prompt: 100",
        "Completed Prompts: 101 after completion",
        "Current Milestone: Retail Decision Console Productization - Visual Layout Pass",
        "Next Focus: Retail Decision Console Static Interaction Placeholders",
        "Retail Decision Console Status: static/demo shell with polished layout",
        "Audit Verdict: Retail Decision Console Visual Polish and Section Layout Pass complete; ready for Retail Decision Console Static Interaction Placeholders only if tests pass",
        "Prompt 100 implements Retail Decision Console Visual Polish and Section Layout Pass",
        "Verifier lock: Retail Decision Console Status: static/demo shell with polished layout; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Current Prompt: 99",
        "Completed Prompts: 100 after completion",
        "Current Milestone: Retail Decision Console Productization - Local Preview and Smoke Test",
        "Next Focus: Retail Decision Console Visual Polish and Section Layout Pass",
        "Retail Decision Console Status: static/demo shell previewable locally",
        "Audit Verdict: Retail Decision Console Local Preview Runbook and Manual Smoke Test complete; ready for Retail Decision Console Visual Polish and Section Layout Pass only if tests pass",
        "Prompt 99 implements Retail Decision Console Local Preview Runbook and Manual Smoke Test",
        "Verifier lock: Retail Decision Console Status: static/demo shell previewable locally; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Current Prompt: 98",
        "Completed Prompts: 99 after completion",
        "Current Milestone: Retail Decision Console Productization - Static State Wired into Desktop Shell",
        "Next Focus: Retail Decision Console Local Preview Runbook and Manual Smoke Test",
        "Retail Decision Console Status: UI shell skeleton with demo/static state wired",
        "Audit Verdict: Retail Decision Console Static State Wiring into Desktop Shell complete; ready for Retail Decision Console Local Preview Runbook and Manual Smoke Test only if tests pass",
        "Prompt 98 implements Retail Decision Console Static State Wiring into Desktop Shell",
        "Verifier lock: Retail Decision Console Status: UI shell skeleton with demo/static state wired; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Current Prompt: 97",
        "Completed Prompts: 98 after completion",
        "Current Milestone: Retail Decision Console Productization - Demo Static State",
        "Next Focus: Retail Decision Console Static State Wiring into Desktop Shell",
        "Retail Decision Console Status: UI shell skeleton plus demo/static state only",
        "Audit Verdict: Retail Decision Console Demo Data Contract and Static State Model complete; ready for Retail Decision Console Static State Wiring into Desktop Shell only if tests pass",
        "Prompt 97 implements Retail Decision Console Demo Data Contract and Static State Model",
        "Verifier lock: Retail Decision Console Status: UI shell skeleton plus demo/static state only; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Current Prompt: 96",
        "Completed Prompts: 97 after completion",
        "Current Milestone: Retail Decision Console Productization - UI Shell Skeleton",
        "Next Focus: Retail Decision Console Demo Data Contract and Static State Model",
        "Retail Decision Console Status: UI shell skeleton only",
        "Audit Verdict: Retail Decision Console UI Shell Skeleton complete; ready for Retail Decision Console Demo Data Contract and Static State Model only if tests pass",
        "Prompt 96 implements Retail Decision Console UI Shell Skeleton",
        "Verifier lock: Retail Decision Console Status: UI shell skeleton only; no live data, no generated recommendations, no confidence scoring, no active DecisionObject generation, no live market data claims, no broker controls, no order buttons, no execution APIs",
        "Current Prompt: 95",
        "Completed Prompts: 96 after completion",
        "Current Milestone: Retail Decision Console Productization",
        "Next Focus: Retail Decision Console UI Shell Skeleton",
        "Retail Decision Console Status: productization plan and UI shell boundary only",
        "Audit Verdict: Retail Decision Console Productization Plan and UI Shell Boundary complete; ready for Retail Decision Console UI Shell Skeleton only if tests pass",
        "Prompt 95 implements Retail Decision Console Productization Plan and UI Shell Boundary",
        "Current Prompt: 94",
        "Completed Prompts: 95 after completion",
        "Current Milestone: Product Surface Reorientation",
        "Next Focus: Retail Decision Console / Decision Desk productization",
        "Audit Verdict: Product Surface Reorientation complete; ready for Retail Decision Console Productization Plan and UI Shell Boundary only if tests pass",
        "Prompt 94 performs Product Surface Reorientation and Development Plan",
        "Current Prompt: 93",
        "Completed Prompts: 94 after completion",
        "Current Milestone: Research Knowledge Map Planning Phase - Phase Closure",
        "Research Knowledge Map Status: phase closed; planning/API/display/safety only",
        "Audit Verdict: Research Knowledge Map Phase Closure complete; ready for Product Surface Reorientation and Development Plan only if tests pass",
        "Prompt 93 performs Research Knowledge Map Phase Closure",
        "Current Prompt: 92",
        "Completed Prompts: 93 after completion",
        "Current Milestone: Research Knowledge Map Planning Phase - Safety Boundary Audit",
        "Research Knowledge Map Status: planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete",
        "Audit Verdict: Research Knowledge Map Safety Boundary Audit complete; ready for Research Knowledge Map Phase Closure only if tests pass",
        "Prompt 92 performs Research Knowledge Map Safety Boundary Audit",
        "Current Prompt: 91",
        "Completed Prompts: 92 after completion",
        "Current Milestone: Research Knowledge Map Planning Phase - Display Contract Skeleton",
        "Research Knowledge Map Status: planning/guardrails, API contract skeleton, and display contract skeleton only",
        "Audit Verdict: Research Knowledge Map Display Contract Skeleton complete; ready for Research Knowledge Map Safety Boundary Audit only if tests pass",
        "Prompt 91 implements Research Knowledge Map Display Contract Skeleton",
        "Current Prompt: 90",
        "Completed Prompts: 91 after completion",
        "Current Milestone: Research Knowledge Map Planning Phase - API Contract Skeleton",
        "Research Knowledge Map Status: planning/guardrails and API contract skeleton only",
        "Audit Verdict: Research Knowledge Map API Contract Skeleton complete; ready for Research Knowledge Map Display Contract Skeleton only if tests pass",
        "Prompt 90 implements Research Knowledge Map API Contract Skeleton",
        "Prompt 89 implements Research Knowledge Map Planning and Guardrails",
        "Research Metadata Graph Status: planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete; phase closed",
        "Prompt 88-B performs Research Metadata Graph Phase Closure and Forward Transition",
        "Current Prompt: 87",
        "Completed Prompts: 88 after completion",
        "Current Milestone: Research Metadata Graph Planning Phase - Safety Boundary Audit",
        "Research Metadata Graph Status: planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete",
        "Audit Verdict: ready for Research Metadata Graph Milestone Audit only if tests pass",
        "Prompt 87 performs Research Metadata Graph Safety Boundary Audit",
        "Current Prompt: 86",
        "Completed Prompts: 87 after completion",
        "Current Milestone: Research Metadata Graph Planning Phase - Display Contract Skeleton",
        "Research Metadata Graph Status: planning/guardrails, API contract skeleton, and display contract skeleton only",
        "Audit Verdict: ready for Research Metadata Graph Safety Boundary Audit only if tests pass",
        "Prompt 86 implements Research Metadata Graph Display Contract Skeleton",
        "Current Prompt: 85",
        "Completed Prompts: 86 after completion",
        "Current Milestone: Research Metadata Graph Planning Phase - API Contract Skeleton",
        "Research Metadata Graph Status: planning/guardrails and API contract skeleton only",
        "Audit Verdict: ready for Research Metadata Graph Display Contract Skeleton only if tests pass",
        "Prompt 85 implements Research Metadata Graph API Contract Skeleton",
        "Current Prompt: 84",
        "Completed Prompts: 85 after completion",
        "Current Milestone: Research Metadata Graph Planning Phase - Planning and Guardrails",
        "Prompt 84 implements Research Metadata Graph Planning and Guardrails",
        "Prompt 84 implements Research Metadata Graph Planning and Guardrails",
        "Current Prompt: 83",
        "Completed Prompts: 84 after completion",
        "Current Milestone: Research Artifact Index Planning Phase - API/Display Integration Readiness Audit",
        "Research Artifact Index API/display integration readiness audit complete",
        "Research Metadata Graph Status: ready for planning and guardrails only",
        "Audit Verdict: ready for Research Metadata Graph Planning and Guardrails only if tests pass",
        "Prompt 83 performs Research Artifact Index API/Display Integration Readiness",
        "Current Prompt: 82",
        "Completed Prompts: 83 after completion",
        "Current Milestone: Research Artifact Index Planning Phase - System Boundary Hardening",
        "Research Artifact Index Status: planning/guardrails, API contract skeleton",
        "system boundary hardening complete",
        "Audit Verdict: ready for Research Artifact Index API/Display Integration Readiness Audit only if tests pass",
        "Current Prompt: 81",
        "Completed Prompts: 82 after completion",
        "Historical verifier reference: Current Prompt: 80",
        "Historical verifier reference: Completed Prompts: 81 after completion",
        "Documentation/Test Policy",
        "phase-level audit consolidation",
        "prompt-level audit sprawl",
        "Historical verifier reference: Current Prompt: 79",
        "Historical verifier reference: Completed Prompts: 80 after completion",
        "Current Milestone: Research Artifact Index Planning Phase - Milestone Audit completed",
        "Backend Status: Foundation health surface + Research Artifact Index planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete",
        "Strategy Research Workspace Status: planning/API/display/safety/milestone/boundary/integration readiness complete; no active UI, no paper parsing, no strategy generation, no backtesting, no recommendations, no execution",
        "Research Artifact Registry Status: planning/guardrails, API/display contract skeletons, safety/milestone audits, system boundary hardening, and API/display integration readiness audit complete; no implementation, no active ingestion/storage, no upload/download, no active UI, no frontend/desktop, no paper parsing, no strategy generation, no backtesting, no recommendations, no execution",
        "Research Artifact Index Status: planning/guardrails, API contract skeleton, display contract skeleton, safety boundary audit, and milestone audit complete; no implementation, no active UI, no frontend/desktop, no indexing/search/ranking/retrieval, no embeddings/vector store, no ingestion/storage, no upload/download/preview, no paper parsing, no strategy generation, no backtesting, no recommendations, no execution",
        "Active Decision Architecture Target: documented as future target only; decision candidate is not a trade; execution APIs remain forbidden",
        "Audit Verdict: ready for Research Artifact Index System Boundary Hardening only if tests pass",
        "Prompt 81 Research Artifact Index Milestone Audit Status",
        "Prompt 81 - Research Artifact Index Milestone Audit",
        "Prompt 82 - Research Artifact Index System Boundary Hardening",
        "Prompt 80 performs Research Artifact Index Safety Boundary Audit",
        "Prompt 80 Research Artifact Index Safety Boundary Audit Status",
        "Prompt 79 implements Research Artifact Index Display Contract Skeleton",
        "Prompt 79 Research Artifact Index Display Status",
        "Prompt 78 implements Research Artifact Index API Contract Skeleton",
        "Prompt 78 Research Artifact Index API Status",
        "Prompt 77 implements Research Artifact Index Planning and Guardrails",
        "Prompt 76 performs Research Artifact Registry API/Display Integration Readiness Audit",
        "Prompt 75 implements Research Artifact Registry System Boundary Hardening",
        "Prompt 74 audits Research Artifact Registry Planning and Guardrails",
        "Prompt 73 audits Research Artifact Registry Planning and Guardrails",
        "Historical verifier reference: Completed Prompts: 74 after completion",
        "Prompt 73 audits Research Artifact Registry Planning and Guardrails",
        "Prompt 72 implements Research Artifact Registry Display Contract Skeleton",
        "Historical verifier reference: Completed Prompts: 73 after completion",
        "Historical verifier reference: Current Prompt: 68",
        "Historical verifier reference: Completed Prompts: 69 after completion",
        "Historical verifier reference: Current Prompt: 66",
        "Historical verifier reference: Completed Prompts: 67 after completion",
        "Historical verifier reference: Current Prompt: 65",
        "Historical verifier reference: Completed Prompts: 66 after completion",
        "Historical verifier reference: Current Prompt: 64",
        "Completed Prompts: 56 before this prompt, 57 after completion",
        "Completed Prompts: 58 after completion",
        "Completed Prompts: 59 after completion",
        "Historical verifier reference: Completed Prompts: 60 after completion",
        "Completed Prompts: 61 after completion",
        "Completed Prompts: 62 after completion",
        "Historical verifier reference: Completed Prompts: 65 after completion",
        "Historical verifier reference: Current Prompt: 63",
        "Historical verifier reference: Current Prompt: 62",
        "Historical verifier reference: Completed Prompts: 63 after completion",
        "Historical verifier reference: Current Prompt: 61",
        "Historical verifier reference: Current Prompt: 60",
        "Historical verifier reference: Current Prompt: 54",
        "Historical verifier reference: Completed Prompts: 54 before this prompt, 55 after completion",
        "Historical verifier reference: Completed Prompts: 55 after completion",
        "Historical verifier reference: Current Prompt: 53",
        "Historical verifier reference: Completed Prompts: 53 before this prompt, 54 after completion",
        "Historical verifier reference: Completed Prompts: 54 after completion",
        "Historical verifier reference: Current Prompt: 52",
        "Historical verifier reference: Completed Prompts: 52 before this prompt, 53 after completion",
        "Historical verifier reference: Completed Prompts: 53 after completion",
        "Historical verifier reference: Current Prompt: 51",
        "Historical verifier reference: Completed Prompts: 51 before this prompt, 52 after completion",
        "Historical verifier reference: Completed Prompts: 52 after completion",
        "Historical verifier reference: Current Prompt: 50",
        "Historical verifier reference: Completed Prompts: 50 before this prompt, 51 after completion",
        "Historical verifier reference: Completed Prompts: 51 after completion",
        "Historical verifier reference: Current Prompt: 49",
        "Historical verifier reference: Completed Prompts: 49 before this prompt, 50 after completion",
        "Historical verifier reference: Completed Prompts: 50 after completion",
        "Historical verifier reference: Current Prompt: 48",
        "Historical verifier reference: Completed Prompts: 48 before this prompt, 49 after completion",
        "Historical verifier reference: Completed Prompts: 49 after completion",
        "Historical verifier reference: Current Prompt: 47",
        "Historical verifier reference: Completed Prompts: 47 before this prompt, 48 after completion",
        "Historical verifier reference: Completed Prompts: 48 after completion",
        "Historical verifier reference: Current Prompt: 46",
        "Historical verifier reference: Completed Prompts: 46 before this prompt, 47 after completion",
        "Historical verifier reference: Completed Prompts: 47 after completion",
        "Historical verifier reference: Current Prompt: 45",
        "Historical verifier reference: Completed Prompts: 45 before this prompt, 46 after completion",
        "Historical verifier reference: Completed Prompts: 46 after completion",
        "Historical verifier reference: Current Prompt: 44",
        "Historical verifier reference: Completed Prompts: 44 before this prompt, 45 after completion",
        "Historical verifier reference: Completed Prompts: 45 after completion",
        "Historical verifier reference: Current Prompt: 43",
        "Historical verifier reference: Completed Prompts: 43 before this prompt, 44 after completion",
        "Historical verifier reference: Completed Prompts: 44 after completion",
        "Historical verifier reference: Current Prompt: 42",
        "Historical verifier reference: Completed Prompts: 42 before this prompt, 43 after completion",
        "Historical verifier reference: Completed Prompts: 43 after completion",
        "Historical verifier reference: Current Prompt: 41",
        "Historical verifier reference: Completed Prompts: 41 before this prompt, 42 after completion",
        "Historical verifier reference: Completed Prompts: 42 after completion",
        "Historical verifier reference: Current Prompt: 40",
        "Historical verifier reference: Completed Prompts: 40 before this prompt, 41 after completion",
        "Historical verifier reference: Current Prompt: 39",
        "Historical verifier reference: Completed Prompts: 39 before this prompt, 40 after completion",
        "Historical verifier reference: Current Prompt: 38",
        "Historical verifier reference: Completed Prompts: 38 before this prompt, 39 after completion",
        "Historical verifier reference: Current Prompt: 36",
        "Historical verifier reference: Completed Prompts: 36 before this prompt, 37 after completion",
        "Event Backbone Status: Kafka/Redpanda contracts/foundation only, no production pipelines",
        "Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening/dashboard/retail-trader-experience/strategy-research boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening/dashboard/API/display/safety-audit boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening/dashboard/API/display boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening/dashboard/API boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening/dashboard boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review/boundary-hardening boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation/human-review boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display/validation boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness/display boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API/readiness boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety/API boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence/safety boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision evidence boundaries",
        "Historical Data Quality Status: Validation framework active for synthetic/local provider and analytics/regime/decision-desk planning boundaries",
        "Fixture Status: Synthetic local-only test/dev fixtures implemented and audited",
        "Synthetic OHLCV Storage Status: Synthetic-only repository/service wiring implemented; no real market data",
        "Synthetic OHLCV Export Status: Synthetic-only Parquet export contract with DatasetManifest linkage implemented; no real market data",
        "Provider Status: Local Sample Provider and Local File Provider implemented; real provider implementation not started; no external calls",
        "Quant Engine Status: Descriptive analytics and regime planning complete; no signals, recommendations, decisions, backtests, or execution",
        "Historical Milestone Reference: Strategy Research Workspace Planning Phase - Safety Boundary Audit",
        "Historical Milestone Reference: Strategy Research Workspace Planning Phase - Safety Boundary Audit",
        "Historical Milestone Reference: Strategy Research Workspace Planning Phase - Display Contract Skeleton",
        "Historical Milestone Reference: Strategy Research Workspace Planning Phase - API Contract Skeleton",
        "Historical Milestone Reference: Retail Trader Experience Planning Phase - System Boundary Hardening",
        "Historical Milestone Reference: Retail Dashboard Planning Phase - System Boundary Hardening",
        "Historical Milestone Reference: Retail Dashboard Planning Phase - Milestone Audit completed",
        "Historical Milestone Reference: Retail Dashboard Planning Phase - Safety Boundary Audit",
        "Historical Milestone Reference: Retail Dashboard Planning Phase - Display Contract Skeleton",
        "Historical Milestone Reference: Retail Dashboard Planning Phase - API Contract Skeleton",
        "Historical Milestone Reference: Retail Dashboard Planning Phase - Planning and Guardrails",
        "Historical Milestone Reference: Retail Decision Desk Planning Phase - API/Display Integration Readiness Audit completed",
        "Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk System Boundary Hardening",
        "Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Milestone Audit 2 completed",
        "Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Human Review Workflow Skeleton",
        "Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Evidence Bundle Validation v0",
        "Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Display Contract Skeleton",
        "Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Readiness API Skeleton",
        "Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk Milestone Audit completed",
        "Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Desk API Contract Skeleton",
        "Historical Milestone Reference: Retail Decision Desk Planning Phase - Decision Safety and Human-Review Guardrails",
        "Historical Milestone Reference: Retail Decision Desk Planning Phase - DecisionObject Evidence Bundle Contracts",
        "Decision Engine Status: decision desk planning/contracts/safety/API/readiness/display/evidence/human-review/boundary/integration complete; no active decisions or execution",
        "Historical Decision Engine Status: Decision Desk planning/guardrails, evidence contracts, safety guardrails, API/readiness/display skeletons, evidence validation v0, human review workflow skeleton, and system boundary hardening implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no active UI, no active workflow, no execution",
        "Historical Decision Engine Status: Decision Desk planning/guardrails, evidence contracts, safety guardrails, API/readiness/display skeletons, evidence validation v0, and human review workflow skeleton implemented and audited; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no active workflow, no execution",
        "Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, Decision Desk API/readiness/display skeletons, evidence bundle validation v0, and human review workflow skeleton implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no active workflow, no execution",
        "Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, Decision Desk API/readiness/display skeletons, and evidence bundle validation v0 implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no execution",
        "Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, Decision Desk API skeleton, Decision Desk readiness API skeleton, and display contract skeleton implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no execution",
        "Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, Decision Desk API skeleton, and Decision Desk readiness API skeleton implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no readiness-to-trade, no approvals, no overrides, no execution",
        "Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, and Decision Desk API skeleton implemented and audited; no recommendations, no confidence scoring, no active DecisionObject generation, no approvals, no overrides, no execution",
        "Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, decision safety/human-review guardrails, and Decision Desk API skeleton implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no approvals, no overrides, no execution",
        "Historical Decision Engine Status: Decision Desk planning/guardrails, DecisionObject evidence bundle contracts, and Decision Safety human-review guardrails implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no approvals, no overrides, no execution",
        "Historical Decision Engine Status: Decision Desk planning/guardrails and DecisionObject evidence bundle contracts implemented; no recommendations, no confidence scoring, no active DecisionObject generation, no execution",
        "Historical Decision Engine Status: Decision Desk planning and guardrails implemented; no recommendations, no confidence scoring, no DecisionObject generation, no execution",
        "Retail Dashboard Status: complete through API/display integration readiness; no active UI, recommendations, broker controls, or execution",
        "Retail Trader Experience Status: complete through API/display integration readiness; no active UI, recommendations, suitability profiling, broker controls, or execution",
        "Historical Strategy Research Workspace Status: Planning/guardrails, API/display contract skeletons, and safety boundary audit complete; no active UI, no paper ingestion/parsing, no strategy generation, no backtesting, no recommendations, no broker controls, no execution",
        "Historical Strategy Research Workspace Status: Planning/guardrails, API contract skeleton, and display contract skeleton implemented; no active UI, no paper ingestion/parsing, no strategy generation, no backtesting, no recommendations, no broker controls, no execution",
        "Historical Strategy Research Workspace Status: Planning/guardrails and API contract skeleton implemented; no active UI, no paper ingestion/parsing, no strategy generation, no backtesting, no recommendations, no broker controls, no execution",
        "Historical Retail Trader Experience Status: Planning/guardrails, API contract skeleton, and display contract skeleton implemented; no active UI, no frontend/desktop implementation, no recommendations, no suitability profiling, no broker controls, no execution",
        "Historical Retail Trader Experience Status: Ready for planning and guardrails only; no implementation yet",
        "Historical Retail Dashboard Status: Planning/guardrails, API/display contract skeletons, safety/milestone audits, and system boundary hardening implemented; no active UI, no recommendation cards, no broker controls, no execution",
        "Historical Retail Dashboard Status: Planning/guardrails, API contract skeleton, display contract skeleton, safety boundary audit, and milestone audit complete; no active UI, no recommendation cards, no broker controls, no execution",
        "Historical Retail Dashboard Status: Planning/guardrails, API contract skeleton, display contract skeleton, and safety boundary audit complete; no active UI, no recommendation cards, no broker controls, no execution",
        "Historical Retail Dashboard Status: Planning/guardrails, API contract skeleton, and display contract skeleton implemented; no active UI, no recommendation cards, no broker controls, no execution",
        "Historical Retail Dashboard Status: Planning/guardrails and API contract skeleton implemented; no active UI, no recommendation cards, no broker controls, no execution",
        "Historical Retail Dashboard Status: Planning and guardrails implemented; no active UI, no recommendation cards, no broker controls, no execution",
        "Historical Retail Dashboard Status: Ready for planning and guardrails only; no implementation yet",
        "Historical Audit Verdict: Strategy Research Workspace Safety Boundary Audit complete; ready for Strategy Research Workspace Milestone Audit if tests pass",
        "Historical Audit Verdict: Strategy Research Workspace Display Contract Skeleton implemented; ready for Safety Boundary Audit if tests pass",
        "Historical Audit Verdict: Strategy Research Workspace API Contract Skeleton implemented; ready for Display Contract Skeleton if tests pass",
        "Historical Audit Verdict: Strategy Research Workspace Planning and Guardrails implemented; ready for API contract skeleton if tests pass",
        "Historical Audit Verdict: Ready for Strategy Research Workspace Planning and Guardrails only if tests pass",
        "Historical Audit Verdict: Retail Trader Experience Safety Boundary Audit complete; ready for Retail Trader Experience Milestone Audit if tests pass",
        "Historical Audit Verdict: Retail Trader Experience Display Contract Skeleton implemented; ready for Retail Trader Experience Safety Boundary Audit if tests pass",
        "Historical Audit Verdict: Ready for Retail Trader Experience Planning and Guardrails only if tests pass",
        "Historical Audit Verdict: Retail Dashboard System Boundary Hardening implemented; ready for API/display integration readiness audit if tests pass",
        "Historical Audit Verdict: Retail Dashboard planning phase ready for system boundary hardening if tests pass",
        "Historical Audit Verdict: Retail Dashboard Safety Boundary Audit complete; ready for Retail Dashboard Milestone Audit if tests pass",
        "Historical Audit Verdict: Retail Dashboard Display Contract Skeleton implemented; ready for Retail Dashboard Safety Boundary Audit if tests pass",
        "Historical Audit Verdict: Retail Dashboard API Contract Skeleton implemented; ready for Retail Dashboard Display Contract Skeleton if tests pass",
        "Historical Audit Verdict: Retail Dashboard Planning and Guardrails implemented; ready for Retail Dashboard API Contract Skeleton if tests pass",
        "Historical Audit Verdict: Ready for Retail Dashboard Planning and Guardrails only if tests pass",
        "Historical Audit Verdict: Decision Desk System Boundary Hardening implemented; ready for API/display integration readiness audit if tests pass",
        "Historical Audit Verdict: Decision Desk skeleton phase ready for system boundary hardening if tests pass",
        "Historical Audit Verdict: Decision Desk Human Review Workflow Skeleton implemented; ready for Decision Desk Milestone Audit 2 if tests pass",
        "Historical Audit Verdict: Decision Desk Evidence Bundle Validation v0 implemented; ready for Decision Desk Human Review Workflow Skeleton if tests pass",
        "Historical Audit Verdict: Decision Desk Display Contract Skeleton implemented; ready for Decision Desk Evidence Bundle Validation v0 if tests pass",
        "Historical Audit Verdict: Decision Desk Readiness API Skeleton implemented; ready for Decision Desk Display Contract Skeleton if tests pass",
        "Historical Audit Verdict: Decision Desk planning foundation ready for next read-only skeleton phase if tests pass",
        "Historical Audit Verdict: Decision Desk API Contract Skeleton implemented; ready for Decision Desk Milestone Audit if tests pass",
        "Historical Audit Verdict: Decision Safety and Human-Review Guardrails implemented; ready for Decision Desk API Contract Skeleton if tests pass",
        "Historical Audit Verdict: DecisionObject evidence bundle contracts implemented; ready for Decision Safety and Human-Review Guardrails if tests pass",
        "Historical Audit Verdict: Retail Decision Desk planning and guardrails implemented; ready for DecisionObject evidence bundle contracts if tests pass",
        "Feature Engine Status: Registry/contracts only; regime feature preparation contracts exist but no feature computation or registry writes",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    return AuditResult(
        "north star status",
        not missing,
        ", ".join(missing) if missing else "North Star Prompt 107 and consolidation status present",
    )


def run_audit() -> list[AuditResult]:
    return [
        _check_required_docs(),
        _check_required_dirs(),
        _check_required_routes(),
        _check_forbidden_route_names(),
        _check_required_data_foundation_files(),
        _check_required_analytics_foundation_files(),
        _check_required_numerical_analytics_files(),
        _check_required_returns_rolling_analytics_files(),
        _check_required_volatility_drawdown_analytics_files(),
        _check_required_analytics_milestone_audit_files(),
        _check_required_correlation_beta_analytics_files(),
        _check_required_time_series_diagnostics_files(),
        _check_required_regime_analytics_files(),
        _check_required_regime_feature_preparation_files(),
        _check_required_analytics_regime_milestone_audit_files(),
        _check_required_retail_decision_desk_files(),
        _check_required_decision_evidence_files(),
        _check_required_decision_safety_files(),
        _check_required_decision_api_files(),
        _check_required_decision_desk_milestone_audit_files(),
        _check_required_decision_readiness_api_files(),
        _check_required_decision_display_files(),
        _check_required_decision_evidence_validation_files(),
        _check_required_decision_human_review_files(),
        _check_required_decision_desk_milestone_audit_2_files(),
        _check_required_decision_boundary_files(),
        _check_required_decision_api_display_integration_audit_files(),
        _check_required_retail_dashboard_files(),
        _check_required_retail_dashboard_api_files(),
        _check_required_retail_dashboard_display_files(),
        _check_required_retail_dashboard_safety_audit_files(),
        _check_required_retail_dashboard_milestone_audit_files(),
        _check_required_retail_dashboard_boundary_files(),
        _check_required_retail_dashboard_api_display_integration_files(),
        _check_required_retail_trader_experience_files(),
        _check_required_retail_trader_experience_api_files(),
        _check_required_retail_trader_experience_display_files(),
        _check_required_retail_trader_experience_safety_audit_files(),
        _check_required_retail_trader_experience_milestone_audit_files(),
        _check_required_retail_trader_experience_boundary_files(),
        _check_required_retail_trader_experience_api_display_integration_files(),
        _check_required_strategy_research_workspace_files(),
        _check_required_strategy_research_workspace_api_files(),
        _check_required_strategy_research_workspace_display_files(),
        _check_required_strategy_research_workspace_safety_audit_files(),
        _check_required_strategy_research_workspace_milestone_audit_files(),
        _check_required_strategy_research_workspace_boundary_files(),
        _check_required_strategy_research_workspace_api_display_integration_files(),
        _check_required_research_artifact_registry_files(),
        _check_required_research_artifact_registry_api_files(),
        _check_required_research_artifact_registry_display_files(),
        _check_required_research_artifact_registry_safety_audit_files(),
        _check_required_research_artifact_registry_milestone_audit_files(),
        _check_required_research_artifact_registry_boundary_files(),
        _check_required_research_artifact_registry_api_display_integration_files(),
        _check_required_research_artifact_index_files(),
        _check_required_research_artifact_index_api_files(),
        _check_required_research_artifact_index_display_files(),
        _check_required_research_artifact_index_safety_audit_files(),
        _check_required_documentation_consolidation_files(),
        _check_required_research_artifact_index_milestone_audit_files(),
        _check_required_research_artifact_index_boundary_files(),
        _check_required_research_artifact_index_api_display_integration_files(),
        _check_required_research_metadata_graph_planning_files(),
        _check_required_research_metadata_graph_api_files(),
        _check_required_research_metadata_graph_display_files(),
        _check_required_research_metadata_graph_safety_audit_files(),
        _check_required_research_metadata_graph_phase_closure_files(),
        _check_required_research_knowledge_map_planning_files(),
        _check_required_research_knowledge_map_api_files(),
        _check_required_research_knowledge_map_display_files(),
        _check_required_research_knowledge_map_safety_files(),
        _check_required_research_knowledge_map_phase_closure_files(),
        _check_required_product_surface_reorientation_files(),
        _check_required_retail_decision_console_files(),
        _check_required_retail_decision_console_ui_shell_files(),
        _check_required_retail_decision_console_demo_state_files(),
        _check_required_retail_decision_console_static_state_wiring_files(),
        _check_required_retail_decision_console_local_preview_files(),
        _check_required_retail_decision_console_visual_layout_files(),
        _check_required_retail_decision_console_static_interaction_files(),
        _check_required_retail_decision_console_preview_snapshot_files(),
        _check_required_retail_decision_console_local_qa_bundle_files(),
        _check_required_retail_decision_console_manual_acceptance_files(),
        _check_required_retail_decision_console_internal_preview_files(),
        _check_required_retail_decision_console_internal_preview_smoke_files(),
        _check_required_retail_decision_console_internal_preview_milestone_files(),
        _check_forbidden_data_file_names(),
        _check_required_safety_phrases(),
        _check_provider_modules_no_external_imports(),
        _check_provider_dependency_boundaries(),
        _check_decision_phase2_dependency_boundaries(),
        _check_analytics_foundation_no_calculations(),
        _check_numerical_analytics_no_market_calculations(),
        _check_returns_rolling_no_forbidden_scope(),
        _check_volatility_drawdown_no_forbidden_scope(),
        _check_relationship_analytics_no_forbidden_scope(),
        _check_time_series_diagnostics_no_forbidden_scope(),
        _check_regime_analytics_no_forbidden_scope(),
        _check_regime_feature_preparation_no_forbidden_scope(),
        _check_retail_decision_desk_no_forbidden_scope(),
        _check_decision_evidence_no_forbidden_scope(),
        _check_decision_safety_no_forbidden_scope(),
        _check_decision_api_no_forbidden_scope(),
        _check_decision_readiness_api_no_forbidden_scope(),
        _check_decision_display_no_forbidden_scope(),
        _check_decision_evidence_validation_no_forbidden_scope(),
        _check_decision_human_review_no_forbidden_scope(),
        _check_decision_boundary_no_forbidden_scope(),
        _check_decision_api_display_integration_no_forbidden_scope(),
        _check_retail_dashboard_no_forbidden_scope(),
        _check_retail_dashboard_api_no_forbidden_scope(),
        _check_retail_dashboard_display_no_forbidden_scope(),
        _check_retail_dashboard_boundary_no_forbidden_scope(),
        _check_retail_dashboard_integration_no_boundary_bypass(),
        _check_retail_trader_experience_no_forbidden_scope(),
        _check_retail_trader_experience_api_no_forbidden_scope(),
        _check_retail_trader_experience_display_no_forbidden_scope(),
        _check_retail_trader_experience_boundary_no_forbidden_scope(),
        _check_retail_trader_experience_integration_no_boundary_bypass(),
        _check_strategy_research_workspace_no_forbidden_scope(),
        _check_strategy_research_workspace_api_no_forbidden_scope(),
        _check_strategy_research_workspace_display_no_forbidden_scope(),
        _check_strategy_research_workspace_boundary_no_forbidden_scope(),
        _check_strategy_research_workspace_safety_audit_docs_language(),
        _check_strategy_research_workspace_milestone_audit_docs_language(),
        _check_strategy_research_workspace_boundary_docs_language(),
        _check_strategy_research_workspace_api_display_integration_docs_language(),
        _check_research_artifact_registry_docs_language(),
        _check_research_artifact_registry_source_boundaries(),
        _check_research_artifact_registry_api_docs_language(),
        _check_research_artifact_registry_api_source_boundaries(),
        _check_research_artifact_registry_display_docs_language(),
        _check_research_artifact_registry_display_source_boundaries(),
        _check_research_artifact_registry_safety_audit_docs_language(),
        _check_research_artifact_registry_milestone_audit_docs_language(),
        _check_research_artifact_registry_boundary_docs_language(),
        _check_research_artifact_registry_boundary_source_boundaries(),
        _check_research_artifact_registry_api_display_integration_docs_language(),
        _check_research_artifact_index_docs_language(),
        _check_research_artifact_index_source_boundaries(),
        _check_research_artifact_index_api_docs_language(),
        _check_research_artifact_index_api_source_boundaries(),
        _check_research_artifact_index_display_docs_language(),
        _check_research_artifact_index_display_source_boundaries(),
        _check_research_artifact_index_safety_audit_docs_language(),
        _check_documentation_consolidation_docs_language(),
        _check_archived_prompt_audit_tests_not_collectable(),
        _check_research_artifact_index_milestone_audit_docs_language(),
        _check_research_artifact_index_safety_audit_source_boundaries(),
        _check_research_artifact_index_boundary_docs_language(),
        _check_research_artifact_index_boundary_source_boundaries(),
        _check_prompt_82_no_micro_audit_sprawl(),
        _check_research_artifact_index_api_display_integration_docs_language(),
        _check_prompt_83_no_micro_audit_sprawl(),
        _check_research_metadata_graph_docs_language(),
        _check_research_metadata_graph_source_boundaries(),
        _check_prompt_84_no_micro_audit_sprawl(),
        _check_prompt_85_no_micro_audit_sprawl(),
        _check_prompt_86_no_micro_audit_sprawl(),
        _check_prompt_87_no_micro_audit_sprawl(),
        _check_prompt_88_no_micro_audit_sprawl(),
        _check_research_knowledge_map_docs_language(),
        _check_research_knowledge_map_source_boundaries(),
        _check_prompt_89_no_micro_audit_sprawl(),
        _check_prompt_90_no_micro_audit_sprawl(),
        _check_prompt_91_no_micro_audit_sprawl(),
        _check_prompt_92_no_micro_audit_sprawl(),
        _check_prompt_93_no_micro_audit_sprawl(),
        _check_product_surface_reorientation_docs_language(),
        _check_product_surface_reorientation_no_runtime_capability(),
        _check_prompt_94_no_micro_audit_sprawl(),
        _check_retail_decision_console_docs_language(),
        _check_retail_decision_console_source_boundaries(),
        _check_retail_decision_console_ui_shell_docs_language(),
        _check_retail_decision_console_ui_shell_source_boundaries(),
        _check_retail_decision_console_demo_state_docs_language(),
        _check_retail_decision_console_demo_state_source_boundaries(),
        _check_retail_decision_console_static_state_wiring_docs_language(),
        _check_retail_decision_console_static_state_wiring_source_boundaries(),
        _check_retail_decision_console_local_preview_docs_language(),
        _check_retail_decision_console_local_preview_source_boundaries(),
        _check_retail_decision_console_visual_layout_docs_language(),
        _check_retail_decision_console_visual_layout_source_boundaries(),
        _check_retail_decision_console_static_interaction_docs_language(),
        _check_retail_decision_console_static_interaction_source_boundaries(),
        _check_retail_decision_console_preview_snapshot_docs_language(),
        _check_retail_decision_console_preview_snapshot_source_boundaries(),
        _check_retail_decision_console_local_qa_bundle_docs_language(),
        _check_retail_decision_console_local_qa_bundle_source_boundaries(),
        _check_retail_decision_console_manual_acceptance_docs_language(),
        _check_retail_decision_console_manual_acceptance_source_boundaries(),
        _check_retail_decision_console_internal_preview_docs_language(),
        _check_retail_decision_console_internal_preview_source_boundaries(),
        _check_retail_decision_console_internal_preview_smoke_docs_language(),
        _check_retail_decision_console_internal_preview_smoke_source_boundaries(),
        _check_retail_decision_console_internal_preview_milestone_docs_language(),
        _check_prompt_95_no_micro_audit_sprawl(),
        _check_prompt_96_no_micro_audit_sprawl(),
        _check_prompt_97_no_micro_audit_sprawl(),
        _check_prompt_98_no_micro_audit_sprawl(),
        _check_prompt_99_no_micro_audit_sprawl(),
        _check_prompt_100_no_micro_audit_sprawl(),
        _check_prompt_101_no_micro_audit_sprawl(),
        _check_prompt_102_no_micro_audit_sprawl(),
        _check_prompt_103_no_micro_audit_sprawl(),
        _check_prompt_104_no_micro_audit_sprawl(),
        _check_prompt_105_no_micro_audit_sprawl(),
        _check_prompt_106_no_micro_audit_sprawl(),
        _check_prompt_107_no_micro_audit_sprawl(),
        _check_analytics_modules_no_external_imports(),
        _check_analytics_modules_no_action_terms(),
        _check_heavy_analytics_dependencies_not_added(),
        _check_prompt_log(),
        _check_north_star_status(),
    ]


def main() -> int:
    print("Stark Terminal foundation and data foundation audit")
    results = run_audit()
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name}: {result.detail}")
    failures = [result for result in results if not result.passed]
    if failures:
        print(f"Audit failed: {len(failures)} failing checks")
        return 1
    print("Audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
