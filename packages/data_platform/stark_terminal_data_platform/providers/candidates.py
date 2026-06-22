from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
import re
from typing import Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.guardrails import (
    FORBIDDEN_PROVIDER_CONCEPTS,
    sanitize_provider_notes,
)


SENSITIVE_REFERENCE_PATTERN = re.compile(
    r"(password|secret|token|api[_-]?key|credential|bearer|client_secret)",
    re.IGNORECASE,
)


class ProviderCandidateStatus(StrEnum):
    DRAFT = "DRAFT"
    REJECTED = "REJECTED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    DESIGN_CANDIDATE = "DESIGN_CANDIDATE"
    LOCAL_FILE_CANDIDATE = "LOCAL_FILE_CANDIDATE"
    NETWORK_TEST_CANDIDATE = "NETWORK_TEST_CANDIDATE"
    PRODUCTION_CANDIDATE_BLOCKED = "PRODUCTION_CANDIDATE_BLOCKED"
    UNKNOWN = "UNKNOWN"


class ProviderDataAccessMethod(StrEnum):
    SYNTHETIC_ONLY = "SYNTHETIC_ONLY"
    LOCAL_FILE = "LOCAL_FILE"
    OFFICIAL_API = "OFFICIAL_API"
    VENDOR_API = "VENDOR_API"
    BROKER_READ_ONLY_API = "BROKER_READ_ONLY_API"
    SCRAPING = "SCRAPING"
    UNKNOWN = "UNKNOWN"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _non_empty_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    return normalized


def _contains_forbidden_text(value: str) -> bool:
    normalized = value.lower().replace("_", " ").replace("-", " ")
    return any(concept in normalized for concept in FORBIDDEN_PROVIDER_CONCEPTS)


def _safe_reference(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    if SENSITIVE_REFERENCE_PATTERN.search(normalized):
        return "[redacted]"
    return normalized[:240]


class ProviderCandidateProfile(BaseModel):
    candidate_id: str
    provider_name: str
    display_name: str
    data_access_method: ProviderDataAccessMethod
    requested_capabilities: list[ProviderCapability]
    claimed_exchanges: list[str] = Field(default_factory=list)
    claimed_segments: list[str] = Field(default_factory=list)
    requires_credentials: bool = False
    requires_network_calls: bool = False
    requires_scraping: bool = False
    provides_execution: bool = False
    terms_url_reference: str | None = None
    documentation_reference: str | None = None
    notes: list[str] = Field(default_factory=list)
    status: ProviderCandidateStatus = ProviderCandidateStatus.DRAFT
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("candidate_id", "provider_name", "display_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "provider candidate text fields")

    @field_validator("requested_capabilities")
    @classmethod
    def requested_capabilities_must_be_present(
        cls,
        value: list[ProviderCapability],
    ) -> list[ProviderCapability]:
        if not value:
            raise ValueError("requested_capabilities cannot be empty")
        return value

    @field_validator("claimed_exchanges", "claimed_segments")
    @classmethod
    def claimed_fields_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return [item.strip().upper() for item in value if item and item.strip()]

    @field_validator("terms_url_reference", "documentation_reference")
    @classmethod
    def references_must_not_contain_secrets(cls, value: str | None) -> str | None:
        return _safe_reference(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_provider_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def candidate_must_not_represent_execution(self) -> ProviderCandidateProfile:
        if self.provides_execution:
            raise ValueError("provider candidates cannot provide execution")
        if _contains_forbidden_text(self.provider_name) or _contains_forbidden_text(self.display_name):
            raise ValueError("provider candidate names cannot contain execution/order/broker concepts")
        if self.data_access_method == ProviderDataAccessMethod.SCRAPING and not self.requires_scraping:
            raise ValueError("scraping access method requires requires_scraping=true")
        return self


class ProviderCandidateChecklist(BaseModel):
    candidate_id: str
    terms_review_available: bool = False
    storage_rights_known: bool = False
    redistribution_rights_known: bool = False
    rate_limits_known: bool = False
    attribution_requirements_known: bool = False
    delayed_data_requirements_known: bool = False
    credential_handling_plan_ready: bool = False
    data_quality_plan_ready: bool = False
    audit_logging_plan_ready: bool = False
    fallback_plan_ready: bool = False
    no_execution_scope_confirmed: bool = True
    no_scraping_or_approved_scraping: bool = False
    notes: list[str] = Field(default_factory=list)
    schema_version: str = "v1"

    @field_validator("candidate_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "provider candidate checklist text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_provider_notes(value)

    @model_validator(mode="after")
    def checklist_must_confirm_no_execution_scope(self) -> ProviderCandidateChecklist:
        if not self.no_execution_scope_confirmed:
            raise ValueError("provider candidate checklist must confirm no-execution scope")
        return self


def create_provider_candidate_profile(
    *,
    candidate_id: str,
    provider_name: str,
    display_name: str,
    data_access_method: ProviderDataAccessMethod,
    requested_capabilities: Iterable[ProviderCapability],
    **kwargs,
) -> ProviderCandidateProfile:
    return ProviderCandidateProfile(
        candidate_id=candidate_id,
        provider_name=provider_name,
        display_name=display_name,
        data_access_method=data_access_method,
        requested_capabilities=list(requested_capabilities),
        **kwargs,
    )


def create_default_candidate_checklist(candidate_id: str) -> ProviderCandidateChecklist:
    return ProviderCandidateChecklist(candidate_id=candidate_id)


def candidate_requires_guardrail_block(profile: ProviderCandidateProfile) -> list[str]:
    blockers: list[str] = []
    if profile.provides_execution:
        blockers.append("provider candidates cannot provide execution")
    if _contains_forbidden_text(profile.provider_name) or _contains_forbidden_text(profile.display_name):
        blockers.append("provider candidate names contain execution/order/broker concepts")
    if profile.requires_network_calls:
        blockers.append("network checks are disabled by default for provider candidates")
    if profile.requires_scraping or profile.data_access_method == ProviderDataAccessMethod.SCRAPING:
        blockers.append("scraping candidates are blocked by default")
    if profile.requires_credentials:
        blockers.append("credential-required candidates are blocked by default")
    return blockers
