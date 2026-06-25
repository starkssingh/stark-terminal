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
    "docs/STRATEGY_RESEARCH_WORKSPACE_NO_ACTIVE_UI_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_NO_PAPER_PARSING_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_NO_STRATEGY_GENERATION_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_NO_BACKTESTING_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_NO_RECOMMENDATION_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_NO_EXECUTION_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_MILESTONE_READINESS.md",
    "tests/test_strategy_research_workspace_safety_boundary_audit_docs.py",
    "tests/test_strategy_research_workspace_api_boundary_audit.py",
    "tests/test_strategy_research_workspace_display_boundary_audit.py",
    "tests/test_strategy_research_workspace_no_active_ui_audit.py",
    "tests/test_strategy_research_workspace_no_paper_parsing_audit.py",
    "tests/test_strategy_research_workspace_no_strategy_generation_audit.py",
    "tests/test_strategy_research_workspace_no_backtesting_audit.py",
    "tests/test_strategy_research_workspace_no_recommendation_audit.py",
    "tests/test_strategy_research_workspace_no_execution_audit.py",
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
    return "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("*.md"))


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
    ]
    missing = [entry for entry in expected if entry not in text]
    return AuditResult("prompt log", not missing, ", ".join(missing) if missing else "Prompt 00 through Prompt 67 present")


def _check_north_star_status() -> AuditResult:
    text = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    required = [
        "Current Prompt: 67",
        "Completed Prompts: 68 after completion",
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
        "Current Milestone: Strategy Research Workspace Planning Phase - Milestone Audit completed",
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
        "Backend Status: Foundation health surface + Strategy Research Workspace planning/API/display/safety boundary audited",
        "Strategy Research Workspace Status: planning/guardrails, API/display contract skeletons, safety boundary audit, and milestone audit complete; no active UI, no paper ingestion/parsing, no strategy generation, no backtesting, no recommendations, no broker controls, no execution",
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
        "Audit Verdict: Strategy Research Workspace planning phase ready for system boundary hardening only if tests pass",
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
    return AuditResult("north star status", not missing, ", ".join(missing) if missing else "North Star Prompt 67 status present")


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
        _check_strategy_research_workspace_safety_audit_docs_language(),
        _check_strategy_research_workspace_milestone_audit_docs_language(),
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
