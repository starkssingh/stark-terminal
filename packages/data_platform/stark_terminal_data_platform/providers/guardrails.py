from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
import re
from typing import Any, Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import ProviderCapability


FORBIDDEN_PROVIDER_CONCEPTS = (
    "execution",
    "execute",
    "order",
    "order placement",
    "broker",
    "broker credential",
    "broker secret",
    "live trading",
    "live-trading",
    "real money",
    "real-money",
    "routing",
    "trade execution",
)
SENSITIVE_PROVIDER_CONCEPTS = (
    "password",
    "secret",
    "token",
    "api_key",
    "apikey",
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "kafka_bootstrap_servers",
    "provider_url",
    "broker_secret",
)
APPROVED_PROVIDER_STATUSES = {
    "APPROVED_FOR_DESIGN",
    "APPROVED_FOR_LOCAL_TESTS",
    "APPROVED_FOR_NETWORK_TESTS",
    "APPROVED_FOR_PRODUCTION",
}


class ProviderApprovalStatus(StrEnum):
    DRAFT = "DRAFT"
    BLOCKED = "BLOCKED"
    APPROVED_FOR_DESIGN = "APPROVED_FOR_DESIGN"
    APPROVED_FOR_LOCAL_TESTS = "APPROVED_FOR_LOCAL_TESTS"
    APPROVED_FOR_NETWORK_TESTS = "APPROVED_FOR_NETWORK_TESTS"
    APPROVED_FOR_PRODUCTION = "APPROVED_FOR_PRODUCTION"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"


class ProviderRiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    EXTREME = "EXTREME"
    UNKNOWN = "UNKNOWN"


class ProviderIntegrationMode(StrEnum):
    SYNTHETIC_ONLY = "SYNTHETIC_ONLY"
    LOCAL_FILE_ONLY = "LOCAL_FILE_ONLY"
    SANDBOX_NETWORK = "SANDBOX_NETWORK"
    READ_ONLY_PRODUCTION = "READ_ONLY_PRODUCTION"
    DISABLED = "DISABLED"


class ProviderGuardrailDecision(StrEnum):
    ALLOW = "ALLOW"
    WARN = "WARN"
    BLOCK = "BLOCK"


def sanitize_provider_notes(notes: Iterable[str] | None) -> list[str]:
    if notes is None:
        return []
    sanitized: list[str] = []
    for note in notes:
        normalized = str(note).strip()
        if not normalized:
            continue
        lowered = normalized.lower()
        if "://" in lowered or any(part in lowered for part in SENSITIVE_PROVIDER_CONCEPTS):
            sanitized.append("[redacted]")
        else:
            sanitized.append(normalized[:240])
    return sanitized


def _text(value: Any) -> str:
    if hasattr(value, "value"):
        return str(value.value)
    return str(value)


def _capability_texts(capabilities: Iterable[Any]) -> list[str]:
    return [_text(capability).strip() for capability in capabilities]


def _contains_forbidden_provider_concept(value: str) -> bool:
    normalized = value.lower().replace("_", " ").replace("-", " ")
    return any(concept in normalized for concept in FORBIDDEN_PROVIDER_CONCEPTS)


def reject_execution_capabilities(capabilities: Iterable[Any]) -> list[str]:
    rejected = [
        capability
        for capability in _capability_texts(capabilities)
        if _contains_forbidden_provider_concept(capability)
    ]
    if not rejected:
        return []
    return [f"execution/order/broker capability is forbidden: {capability}" for capability in rejected]


def reject_scraping_without_approval(scraping_required: bool, policy: ProviderGuardrailPolicy) -> list[str]:
    if scraping_required and not policy.scraping_allowed:
        return ["scraping is disallowed by the provider guardrail policy"]
    return []


class ProviderGuardrailPolicy(BaseModel):
    policy_id: str
    name: str
    network_calls_allowed: bool = False
    scraping_allowed: bool = False
    credentials_allowed: bool = False
    execution_allowed: bool = False
    real_ingestion_allowed: bool = False
    synthetic_only: bool = True
    terms_review_required: bool = True
    approval_required: bool = True
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @field_validator("policy_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("provider guardrail text fields cannot be empty")
        return normalized

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_provider_notes(value)

    @model_validator(mode="after")
    def dangerous_policy_flags_are_rejected(self) -> ProviderGuardrailPolicy:
        if self.execution_allowed:
            raise ValueError("provider execution is always forbidden")
        if self.real_ingestion_allowed and self.synthetic_only:
            raise ValueError("real ingestion cannot be allowed while synthetic_only is true")
        if self.real_ingestion_allowed and not (self.approval_required and self.terms_review_required):
            raise ValueError("real ingestion requires approval and terms review")
        return self


class ProviderGuardrailResult(BaseModel):
    decision: ProviderGuardrailDecision
    policy_id: str
    provider_name: str
    reasons: list[str]
    risk_level: ProviderRiskLevel
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = "v1"

    @field_validator("policy_id", "provider_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("provider guardrail result text fields cannot be empty")
        return normalized

    @field_validator("reasons")
    @classmethod
    def reasons_must_be_present_and_sanitized(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_provider_notes(value)
        if not sanitized:
            raise ValueError("provider guardrail result requires at least one reason")
        return sanitized


class ProviderGuardrailHealthStatus(BaseModel):
    enabled: bool
    approval_required: bool
    terms_review_required: bool
    network_calls_default_allowed: bool
    scraping_default_allowed: bool
    credentials_allowed: bool
    execution_allowed: bool = False
    schema_version: str
    status: str
    error: str | None = None


def default_provider_guardrail_policy(settings: Settings | None = None) -> ProviderGuardrailPolicy:
    resolved_settings = settings or get_settings()
    return ProviderGuardrailPolicy(
        policy_id="provider_guardrails_default",
        name="Default provider implementation guardrails",
        network_calls_allowed=resolved_settings.provider_network_calls_default_allowed,
        scraping_allowed=resolved_settings.provider_scraping_default_allowed,
        credentials_allowed=resolved_settings.provider_credentials_allowed,
        execution_allowed=False,
        real_ingestion_allowed=False,
        synthetic_only=True,
        terms_review_required=resolved_settings.provider_terms_review_required,
        approval_required=resolved_settings.provider_implementation_approval_required,
        schema_version=resolved_settings.provider_guardrail_schema_version,
        notes=[
            "Prompt 20 allows provider planning contracts only.",
            "Current allowed mode is synthetic-only/local fixtures with no external calls.",
        ],
    )


def _approval_status(approval: Any) -> str:
    status = getattr(approval, "approval_status", ProviderApprovalStatus.UNKNOWN)
    return _text(status).strip().upper()


def _approval_mode(approval: Any) -> str:
    mode = getattr(approval, "requested_mode", ProviderIntegrationMode.DISABLED)
    return _text(mode).strip().upper()


def _compliance_terms_completed(compliance: Any) -> bool:
    return bool(getattr(compliance, "terms_review_completed", False))


def _requested_network(approval: Any | None) -> bool:
    return bool(getattr(approval, "network_calls_required", False)) if approval is not None else False


def _requested_scraping(approval: Any | None) -> bool:
    return bool(getattr(approval, "scraping_required", False)) if approval is not None else False


def _requested_credentials(approval: Any | None) -> bool:
    return bool(getattr(approval, "credentials_required", False)) if approval is not None else False


def _requested_execution(approval: Any | None) -> bool:
    return bool(getattr(approval, "execution_required", False)) if approval is not None else False


def _provider_name_has_forbidden_concepts(provider_name: str) -> bool:
    return _contains_forbidden_provider_concept(provider_name)


def evaluate_provider_guardrails(
    provider_name: str,
    requested_capabilities: Iterable[ProviderCapability | str],
    policy: ProviderGuardrailPolicy,
    approval: Any | None = None,
    compliance: Any | None = None,
) -> ProviderGuardrailResult:
    normalized_provider = provider_name.strip()
    if not normalized_provider:
        raise ValueError("provider_name cannot be empty")

    reasons: list[str] = []
    risk_level = ProviderRiskLevel.LOW
    capabilities = list(requested_capabilities)
    if not capabilities:
        reasons.append("requested capabilities cannot be empty")
        risk_level = ProviderRiskLevel.MEDIUM

    forbidden_capability_reasons = reject_execution_capabilities(capabilities)
    if forbidden_capability_reasons:
        reasons.extend(forbidden_capability_reasons)
        risk_level = ProviderRiskLevel.EXTREME

    if _provider_name_has_forbidden_concepts(normalized_provider):
        reasons.append("provider name contains execution/order/broker concepts")
        risk_level = ProviderRiskLevel.EXTREME

    if _requested_execution(approval):
        reasons.append("provider approval record requests execution behavior")
        risk_level = ProviderRiskLevel.EXTREME

    if policy.approval_required:
        if approval is None:
            reasons.append("provider implementation approval is required")
            risk_level = max(risk_level, ProviderRiskLevel.HIGH, key=lambda level: list(ProviderRiskLevel).index(level))
        elif _approval_status(approval) not in APPROVED_PROVIDER_STATUSES:
            reasons.append("provider approval status is not approved for the requested phase")
            risk_level = max(risk_level, ProviderRiskLevel.HIGH, key=lambda level: list(ProviderRiskLevel).index(level))

    if policy.terms_review_required:
        if compliance is None or not _compliance_terms_completed(compliance):
            reasons.append("provider terms review is required before implementation")
            risk_level = max(risk_level, ProviderRiskLevel.HIGH, key=lambda level: list(ProviderRiskLevel).index(level))

    if _requested_network(approval) and not policy.network_calls_allowed:
        reasons.append("provider network calls are disabled by default")
        risk_level = ProviderRiskLevel.HIGH

    if _requested_scraping(approval) and not policy.scraping_allowed:
        reasons.append("scraping is disallowed by default")
        risk_level = ProviderRiskLevel.HIGH

    if _requested_credentials(approval) and not policy.credentials_allowed:
        reasons.append("provider credentials are disallowed in the current phase")
        risk_level = ProviderRiskLevel.HIGH

    if policy.synthetic_only and approval is not None:
        allowed_modes = {ProviderIntegrationMode.SYNTHETIC_ONLY.value, ProviderIntegrationMode.LOCAL_FILE_ONLY.value}
        if _approval_mode(approval) not in allowed_modes:
            reasons.append("current provider guardrail policy allows only synthetic/local-file modes")
            risk_level = ProviderRiskLevel.HIGH

    if policy.real_ingestion_allowed:
        reasons.append("real ingestion is outside Prompt 20 scope and requires a future explicit prompt")
        risk_level = ProviderRiskLevel.HIGH

    if reasons:
        return ProviderGuardrailResult(
            decision=ProviderGuardrailDecision.BLOCK,
            policy_id=policy.policy_id,
            provider_name=normalized_provider,
            reasons=reasons,
            risk_level=risk_level,
            schema_version=policy.schema_version,
        )

    return ProviderGuardrailResult(
        decision=ProviderGuardrailDecision.ALLOW,
        policy_id=policy.policy_id,
        provider_name=normalized_provider,
        reasons=["synthetic-only local provider design is within current guardrails"],
        risk_level=ProviderRiskLevel.LOW,
        schema_version=policy.schema_version,
    )


def check_provider_guardrail_health(settings: Settings | None = None) -> ProviderGuardrailHealthStatus:
    try:
        resolved_settings = settings or get_settings()
        dangerous_defaults_enabled = any(
            (
                resolved_settings.provider_network_calls_default_allowed,
                resolved_settings.provider_scraping_default_allowed,
                resolved_settings.provider_credentials_allowed,
                resolved_settings.execution_apis_enabled,
                resolved_settings.broker_integrations_enabled,
                resolved_settings.live_trading_enabled,
            )
        )
        status = "HEALTHY"
        if not resolved_settings.provider_guardrails_enabled:
            status = "DISABLED"
        elif dangerous_defaults_enabled:
            status = "BLOCKED"
        return ProviderGuardrailHealthStatus(
            enabled=resolved_settings.provider_guardrails_enabled,
            approval_required=resolved_settings.provider_implementation_approval_required,
            terms_review_required=resolved_settings.provider_terms_review_required,
            network_calls_default_allowed=resolved_settings.provider_network_calls_default_allowed,
            scraping_default_allowed=resolved_settings.provider_scraping_default_allowed,
            credentials_allowed=resolved_settings.provider_credentials_allowed,
            execution_allowed=False,
            schema_version=resolved_settings.provider_guardrail_schema_version,
            status=status,
            error=None,
        )
    except Exception as exc:  # pragma: no cover - defensive safety path
        return ProviderGuardrailHealthStatus(
            enabled=False,
            approval_required=True,
            terms_review_required=True,
            network_calls_default_allowed=False,
            scraping_default_allowed=False,
            credentials_allowed=False,
            execution_allowed=False,
            schema_version="v1",
            status="UNHEALTHY",
            error=re.sub(r"://[^\\s]+", "://[redacted]", str(exc)),
        )
