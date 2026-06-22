from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import ProviderCapability
from stark_terminal_data_platform.providers.guardrails import (
    ProviderApprovalStatus,
    ProviderIntegrationMode,
    reject_execution_capabilities,
    sanitize_provider_notes,
)


class ProviderApprovalRecord(BaseModel):
    provider_name: str
    requested_mode: ProviderIntegrationMode
    approval_status: ProviderApprovalStatus = ProviderApprovalStatus.DRAFT
    requested_capabilities: list[ProviderCapability]
    approved_capabilities: list[ProviderCapability] = Field(default_factory=list)
    requester: str
    reviewer: str | None = None
    terms_review_completed: bool = False
    credentials_required: bool = False
    network_calls_required: bool = False
    scraping_required: bool = False
    execution_required: bool = False
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reviewed_at: datetime | None = None
    schema_version: str = "v1"

    @field_validator("provider_name", "requester", "reviewer", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("provider approval text fields cannot be empty")
        return normalized

    @field_validator("requested_capabilities")
    @classmethod
    def requested_capabilities_must_be_present(
        cls,
        value: list[ProviderCapability],
    ) -> list[ProviderCapability]:
        if not value:
            raise ValueError("requested_capabilities cannot be empty")
        return value

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_provider_notes(value)

    @model_validator(mode="after")
    def approval_record_must_obey_guardrails(self) -> ProviderApprovalRecord:
        if self.execution_required:
            raise ValueError("provider execution is always forbidden")
        forbidden = reject_execution_capabilities(self.requested_capabilities)
        if forbidden:
            raise ValueError("execution/order/broker capabilities are forbidden")
        if self.approved_capabilities:
            requested = set(self.requested_capabilities)
            approved = set(self.approved_capabilities)
            if not approved.issubset(requested):
                raise ValueError("approved capabilities must be a subset of requested capabilities")
        if self.scraping_required and self.approval_status == ProviderApprovalStatus.APPROVED_FOR_PRODUCTION:
            raise ValueError("scraping-based providers cannot be approved for production by default")
        return self


def create_provider_approval_record(
    provider_name: str,
    requested_capabilities: Iterable[ProviderCapability],
    requester: str,
    requested_mode: ProviderIntegrationMode = ProviderIntegrationMode.SYNTHETIC_ONLY,
    notes: Iterable[str] | None = None,
) -> ProviderApprovalRecord:
    return ProviderApprovalRecord(
        provider_name=provider_name,
        requested_mode=requested_mode,
        requested_capabilities=list(requested_capabilities),
        requester=requester,
        notes=list(notes or []),
    )


def approve_for_design(record: ProviderApprovalRecord, reviewer: str) -> ProviderApprovalRecord:
    normalized_reviewer = reviewer.strip()
    if not normalized_reviewer:
        raise ValueError("reviewer cannot be empty")
    return record.model_copy(
        update={
            "approval_status": ProviderApprovalStatus.APPROVED_FOR_DESIGN,
            "approved_capabilities": list(record.requested_capabilities),
            "reviewer": normalized_reviewer,
            "reviewed_at": datetime.now(timezone.utc),
            "notes": sanitize_provider_notes(
                [*record.notes, "Approved for design contracts only; no external calls."]
            ),
        }
    )


def block_provider(record: ProviderApprovalRecord, reviewer: str, reason: str) -> ProviderApprovalRecord:
    normalized_reviewer = reviewer.strip()
    if not normalized_reviewer:
        raise ValueError("reviewer cannot be empty")
    sanitized_reason = sanitize_provider_notes([reason])
    return record.model_copy(
        update={
            "approval_status": ProviderApprovalStatus.BLOCKED,
            "approved_capabilities": [],
            "reviewer": normalized_reviewer,
            "reviewed_at": datetime.now(timezone.utc),
            "notes": sanitize_provider_notes([*record.notes, *sanitized_reason]),
        }
    )
