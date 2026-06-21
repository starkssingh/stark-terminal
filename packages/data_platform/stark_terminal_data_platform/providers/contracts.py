from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from stark_terminal_core.domain.enums import ProviderCapability, ProviderStatus
from stark_terminal_core.domain.identifiers import DataProviderId


class ProviderCapabilityReport(BaseModel):
    provider: DataProviderId
    status: ProviderStatus
    capabilities: list[ProviderCapability] = Field(default_factory=list)
    network_calls_allowed: bool
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def enabled_providers_must_report_capabilities(self) -> ProviderCapabilityReport:
        if self.status == ProviderStatus.ENABLED and not self.capabilities:
            raise ValueError("enabled providers must report at least one capability")
        if not self.schema_version.strip():
            raise ValueError("schema_version cannot be empty")
        return self
