from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.candidates import (
    ProviderCandidateChecklist,
    ProviderCandidateProfile,
    ProviderDataAccessMethod,
)
from stark_terminal_data_platform.providers.guardrails import (
    ProviderRiskLevel,
    sanitize_provider_notes,
)


class ProviderSelectionDecision(StrEnum):
    SHORTLIST = "SHORTLIST"
    WATCHLIST = "WATCHLIST"
    REJECT = "REJECT"
    BLOCK = "BLOCK"
    UNKNOWN = "UNKNOWN"


class ProviderSelectionCriteria(BaseModel):
    criteria_id: str
    name: str
    required_capabilities: list[ProviderCapability]
    preferred_data_access_methods: list[ProviderDataAccessMethod]
    allow_network_required_candidates: bool = False
    allow_scraping_candidates: bool = False
    allow_credential_required_candidates: bool = False
    require_terms_review: bool = True
    require_data_quality_plan: bool = True
    require_no_execution_scope: bool = True
    schema_version: str = "v1"

    @field_validator("criteria_id", "name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("provider selection criteria text fields cannot be empty")
        return normalized

    @field_validator("required_capabilities")
    @classmethod
    def required_capabilities_must_be_present(
        cls,
        value: list[ProviderCapability],
    ) -> list[ProviderCapability]:
        if not value:
            raise ValueError("required_capabilities cannot be empty")
        return value

    @field_validator("preferred_data_access_methods")
    @classmethod
    def preferred_methods_must_be_present(
        cls,
        value: list[ProviderDataAccessMethod],
    ) -> list[ProviderDataAccessMethod]:
        if not value:
            raise ValueError("preferred_data_access_methods cannot be empty")
        return value


class ProviderCapabilityGap(BaseModel):
    capability: ProviderCapability
    required: bool
    present: bool
    gap: bool
    notes: str | None = None


class ProviderCandidateScore(BaseModel):
    candidate_id: str
    provider_name: str
    score: int = Field(ge=0, le=100)
    decision: ProviderSelectionDecision
    risk_level: ProviderRiskLevel
    gaps: list[ProviderCapabilityGap]
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = "v1"

    @field_validator("candidate_id", "provider_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("provider score text fields cannot be empty")
        return normalized

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_provider_notes(value)

    @field_validator("generated_at")
    @classmethod
    def generated_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def shortlist_cannot_have_blockers(self) -> ProviderCandidateScore:
        if self.decision == ProviderSelectionDecision.SHORTLIST and self.blockers:
            raise ValueError("blocked provider candidates cannot be shortlisted")
        return self


class ProviderReadinessHealthStatus(BaseModel):
    enabled: bool
    schema_version: str
    real_implementation_allowed: bool
    network_checks_allowed: bool
    scraping_checks_allowed: bool
    credentials_allowed: bool
    minimum_score_for_design: int
    minimum_score_for_network_tests: int
    minimum_score_for_production: int
    status: str
    error: str | None = None


def default_provider_selection_criteria() -> ProviderSelectionCriteria:
    return ProviderSelectionCriteria(
        criteria_id="default_provider_selection_v1",
        name="Default provider candidate selection criteria",
        required_capabilities=[
            ProviderCapability.INSTRUMENT_MASTER,
            ProviderCapability.HISTORICAL_BARS,
            ProviderCapability.HEALTH_CHECK,
        ],
        preferred_data_access_methods=[
            ProviderDataAccessMethod.SYNTHETIC_ONLY,
            ProviderDataAccessMethod.LOCAL_FILE,
        ],
    )


def analyze_capability_gaps(
    profile: ProviderCandidateProfile,
    criteria: ProviderSelectionCriteria,
) -> list[ProviderCapabilityGap]:
    requested = set(profile.requested_capabilities)
    return [
        ProviderCapabilityGap(
            capability=capability,
            required=True,
            present=capability in requested,
            gap=capability not in requested,
            notes=None if capability in requested else "required capability missing",
        )
        for capability in criteria.required_capabilities
    ]


def readiness_thresholds_from_settings(settings: Settings | None = None) -> dict[str, int]:
    resolved_settings = settings or get_settings()
    return {
        "design": resolved_settings.provider_candidate_minimum_score_for_design,
        "network_tests": resolved_settings.provider_candidate_minimum_score_for_network_tests,
        "production": resolved_settings.provider_candidate_minimum_score_for_production,
    }


def _bounded_score(value: int) -> int:
    return max(0, min(100, value))


def _settings_value(settings: Settings | None, name: str) -> bool:
    resolved_settings = settings or get_settings()
    return bool(getattr(resolved_settings, name))


def score_provider_candidate(
    profile: ProviderCandidateProfile,
    checklist: ProviderCandidateChecklist,
    criteria: ProviderSelectionCriteria,
    settings: Settings | None = None,
) -> ProviderCandidateScore:
    thresholds = readiness_thresholds_from_settings(settings)
    gaps = analyze_capability_gaps(profile, criteria)
    score = 100
    blockers: list[str] = []
    warnings: list[str] = []

    for gap in gaps:
        if gap.gap:
            score -= 20
            blockers.append(f"missing required capability: {gap.capability.value}")

    if profile.data_access_method not in criteria.preferred_data_access_methods:
        score -= 10
        warnings.append("candidate uses a non-preferred data access method")

    if profile.provides_execution or not checklist.no_execution_scope_confirmed:
        score -= 100
        blockers.append("execution scope is forbidden")

    network_allowed = criteria.allow_network_required_candidates or _settings_value(
        settings,
        "provider_candidate_network_checks_allowed",
    )
    if profile.requires_network_calls and not network_allowed:
        score -= 25
        blockers.append("network checks are not allowed in the current provider readiness phase")
    elif profile.requires_network_calls:
        score -= 10
        warnings.append("network requirements need future explicit approval")

    scraping_allowed = criteria.allow_scraping_candidates or _settings_value(
        settings,
        "provider_candidate_scraping_checks_allowed",
    )
    if (
        profile.requires_scraping
        or profile.data_access_method == ProviderDataAccessMethod.SCRAPING
    ) and not scraping_allowed:
        score -= 40
        blockers.append("scraping candidates are blocked by default")
    elif profile.requires_scraping:
        score -= 20
        warnings.append("scraping requires separate legal and compliance review")

    credentials_allowed = criteria.allow_credential_required_candidates or _settings_value(
        settings,
        "provider_candidate_credentials_allowed",
    )
    if profile.requires_credentials and not credentials_allowed:
        score -= 30
        blockers.append("credential-required candidates are blocked in the current phase")
    elif profile.requires_credentials and not checklist.credential_handling_plan_ready:
        score -= 15
        blockers.append("credential handling plan is not ready")

    if criteria.require_terms_review and not checklist.terms_review_available:
        score -= 20
        blockers.append("terms review metadata is missing")
    if not checklist.storage_rights_known:
        score -= 10
        blockers.append("storage rights are unknown")
    if not checklist.redistribution_rights_known:
        score -= 10
        blockers.append("redistribution rights are unknown")
    if not checklist.rate_limits_known:
        score -= 5
        warnings.append("rate limits are not documented")
    if not checklist.attribution_requirements_known:
        score -= 5
        warnings.append("attribution requirements are not documented")
    if not checklist.delayed_data_requirements_known:
        score -= 5
        warnings.append("delayed data requirements are not documented")
    if criteria.require_data_quality_plan and not checklist.data_quality_plan_ready:
        score -= 15
        blockers.append("data quality plan is not ready")
    if not checklist.audit_logging_plan_ready:
        score -= 10
        blockers.append("audit logging plan is not ready")
    if not checklist.fallback_plan_ready:
        score -= 5
        warnings.append("fallback plan is not ready")
    if profile.requires_scraping and not checklist.no_scraping_or_approved_scraping:
        score -= 15
        blockers.append("scraping has not been explicitly prohibited or separately approved")

    score = _bounded_score(score)
    if blockers:
        decision = ProviderSelectionDecision.BLOCK
        risk_level = ProviderRiskLevel.EXTREME
    elif score >= thresholds["design"]:
        decision = ProviderSelectionDecision.SHORTLIST
        risk_level = ProviderRiskLevel.LOW if not warnings else ProviderRiskLevel.MEDIUM
    elif score >= 50:
        decision = ProviderSelectionDecision.WATCHLIST
        risk_level = ProviderRiskLevel.HIGH
    else:
        decision = ProviderSelectionDecision.REJECT
        risk_level = ProviderRiskLevel.HIGH

    if score >= thresholds["production"]:
        warnings.append("production approval remains unavailable in Prompt 23")

    return ProviderCandidateScore(
        candidate_id=profile.candidate_id,
        provider_name=profile.provider_name,
        score=score,
        decision=decision,
        risk_level=risk_level,
        gaps=gaps,
        blockers=blockers,
        warnings=warnings,
        schema_version=profile.schema_version,
    )


class ProviderCandidateRegistry:
    def __init__(self) -> None:
        self._profiles: dict[str, ProviderCandidateProfile] = {}
        self._checklists: dict[str, ProviderCandidateChecklist] = {}

    def register(
        self,
        profile: ProviderCandidateProfile,
        checklist: ProviderCandidateChecklist | None = None,
        *,
        replace: bool = False,
    ) -> ProviderCandidateProfile:
        if profile.candidate_id in self._profiles and not replace:
            raise ValueError("provider candidate already registered")
        if checklist is not None and checklist.candidate_id != profile.candidate_id:
            raise ValueError("candidate checklist id must match profile id")
        self._profiles[profile.candidate_id] = profile
        if checklist is not None:
            self._checklists[profile.candidate_id] = checklist
        return profile

    def get(self, candidate_id: str) -> ProviderCandidateProfile | None:
        return self._profiles.get(candidate_id)

    def get_checklist(self, candidate_id: str) -> ProviderCandidateChecklist | None:
        return self._checklists.get(candidate_id)

    def list_candidates(self) -> list[ProviderCandidateProfile]:
        return list(self._profiles.values())

    def score_candidate(
        self,
        profile: ProviderCandidateProfile,
        checklist: ProviderCandidateChecklist,
        criteria: ProviderSelectionCriteria,
        settings: Settings | None = None,
    ) -> ProviderCandidateScore:
        return score_provider_candidate(profile, checklist, criteria, settings=settings)

    def list_shortlist(
        self,
        criteria: ProviderSelectionCriteria,
        settings: Settings | None = None,
    ) -> list[ProviderCandidateScore]:
        scores: list[ProviderCandidateScore] = []
        for profile in self._profiles.values():
            checklist = self._checklists.get(profile.candidate_id)
            if checklist is None:
                continue
            score = self.score_candidate(profile, checklist, criteria, settings=settings)
            if score.decision == ProviderSelectionDecision.SHORTLIST:
                scores.append(score)
        return scores

    def clear(self) -> None:
        self._profiles.clear()
        self._checklists.clear()


def check_provider_readiness_health(settings: Settings | None = None) -> ProviderReadinessHealthStatus:
    try:
        resolved_settings = settings or get_settings()
        dangerous_flags = any(
            (
                resolved_settings.provider_candidate_real_implementation_allowed,
                resolved_settings.provider_candidate_network_checks_allowed,
                resolved_settings.provider_candidate_scraping_checks_allowed,
                resolved_settings.provider_candidate_credentials_allowed,
                resolved_settings.execution_apis_enabled,
                resolved_settings.broker_integrations_enabled,
                resolved_settings.live_trading_enabled,
            )
        )
        status = "HEALTHY"
        if not resolved_settings.provider_readiness_enabled:
            status = "DISABLED"
        elif dangerous_flags:
            status = "BLOCKED"
        return ProviderReadinessHealthStatus(
            enabled=resolved_settings.provider_readiness_enabled,
            schema_version=resolved_settings.provider_candidate_selection_schema_version,
            real_implementation_allowed=resolved_settings.provider_candidate_real_implementation_allowed,
            network_checks_allowed=resolved_settings.provider_candidate_network_checks_allowed,
            scraping_checks_allowed=resolved_settings.provider_candidate_scraping_checks_allowed,
            credentials_allowed=resolved_settings.provider_candidate_credentials_allowed,
            minimum_score_for_design=resolved_settings.provider_candidate_minimum_score_for_design,
            minimum_score_for_network_tests=resolved_settings.provider_candidate_minimum_score_for_network_tests,
            minimum_score_for_production=resolved_settings.provider_candidate_minimum_score_for_production,
            status=status,
            error=None,
        )
    except Exception as exc:  # pragma: no cover - defensive safety path
        return ProviderReadinessHealthStatus(
            enabled=False,
            schema_version="v1",
            real_implementation_allowed=False,
            network_checks_allowed=False,
            scraping_checks_allowed=False,
            credentials_allowed=False,
            minimum_score_for_design=70,
            minimum_score_for_network_tests=85,
            minimum_score_for_production=95,
            status="UNHEALTHY",
            error=str(exc).replace("://", "://[redacted]"),
        )
