from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_dashboard.planning import _non_empty_text, _utc_datetime, _utc_now


class RetailDashboardDataSourceReference(BaseModel):
    reference_id: str
    source_name: str
    required: bool = True
    real_market_data: bool = False
    validated: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "source_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard data source reference text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def data_source_reference_must_fail_closed(self) -> RetailDashboardDataSourceReference:
        if self.real_market_data:
            raise ValueError("Retail Dashboard real market data display is forbidden in Prompt 49")
        if self.display_ready:
            raise ValueError("Retail Dashboard data source references are not display-ready in Prompt 49")
        return self


class RetailDashboardDecisionReference(BaseModel):
    reference_id: str
    decision_object_id: str | None = None
    required: bool = False
    active_decision_object: bool = False
    recommendation_available: bool = False
    readiness_to_trade_available: bool = False
    display_ready: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("reference_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail dashboard decision reference text fields")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def decision_reference_must_fail_closed(self) -> RetailDashboardDecisionReference:
        if self.active_decision_object:
            raise ValueError("Retail Dashboard active DecisionObject references are forbidden in Prompt 49")
        if self.recommendation_available:
            raise ValueError("Retail Dashboard recommendation references are forbidden in Prompt 49")
        if self.readiness_to_trade_available:
            raise ValueError("Retail Dashboard readiness-to-trade references are forbidden in Prompt 49")
        if self.display_ready:
            raise ValueError("Retail Dashboard decision references are not display-ready in Prompt 49")
        return self


def default_retail_dashboard_data_source_references() -> list[RetailDashboardDataSourceReference]:
    return [
        RetailDashboardDataSourceReference(
            reference_id="retail-dashboard-data-source-synthetic-local-placeholder-v1",
            source_name="synthetic-local-placeholder",
            required=True,
            validated=False,
        ),
        RetailDashboardDataSourceReference(
            reference_id="retail-dashboard-data-source-quality-placeholder-v1",
            source_name="data-quality-placeholder",
            required=True,
            validated=False,
        ),
    ]


def default_retail_dashboard_decision_reference() -> RetailDashboardDecisionReference:
    return RetailDashboardDecisionReference(
        reference_id="retail-dashboard-decision-reference-placeholder-v1",
        required=False,
    )
