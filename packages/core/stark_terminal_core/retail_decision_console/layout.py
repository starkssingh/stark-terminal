from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    SERVICE_NAME,
    non_empty_text,
    normalize_datetime,
    utc_now,
)
from stark_terminal_core.retail_decision_console.ui_descriptors import SHELL_TITLE


VISUAL_LAYOUT_STAGE = "visual_layout_pass"
VISUAL_LAYOUT_SAFETY_BANNER = "Demo/static preview only - no live data, no recommendations, no execution"


class RetailDecisionConsoleLayoutZone(StrEnum):
    HEADER = "HEADER"
    CONTROLS = "CONTROLS"
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    CONTEXT = "CONTEXT"
    FOOTER = "FOOTER"


def _enabled_flags(flags: dict[str, bool]) -> list[str]:
    return [name for name, value in flags.items() if value]


class RetailDecisionConsoleLayoutSection(BaseModel):
    section_id: str
    title: str
    subtitle: str
    zone: RetailDecisionConsoleLayoutZone
    priority: int = Field(default=0, ge=0)
    placeholder_text: str
    demo_only: bool = True
    unavailable: bool = True
    safety_label: str = "Demo only - unavailable static preview"
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("section_id", "title", "subtitle", "placeholder_text", "safety_label")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console layout section text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def section_must_remain_demo_unavailable(self) -> RetailDecisionConsoleLayoutSection:
        if not self.demo_only or not self.unavailable:
            raise ValueError("retail decision console layout sections must remain demo-only and unavailable")
        enabled = _enabled_flags(
            {
                "live data": self.live_data_enabled,
                "recommendations": self.recommendations_enabled,
                "action generation": self.action_generation_enabled,
                "confidence scoring": self.confidence_scoring_enabled,
                "DecisionObject generation": self.decision_object_generation_enabled,
                "broker controls": self.broker_controls_enabled,
                "order buttons": self.order_buttons_enabled,
                "execution": self.execution_enabled,
            }
        )
        if enabled:
            raise ValueError("retail decision console layout section cannot enable: " + ", ".join(enabled))
        return self


class RetailDecisionConsoleLayoutDescriptor(BaseModel):
    layout_id: str = "retail-decision-console-visual-layout-v1"
    title: str = SHELL_TITLE
    service: str = SERVICE_NAME
    schema_version: str = "v1"
    stage: str = VISUAL_LAYOUT_STAGE
    demo_only: bool = True
    unavailable: bool = True
    read_only: bool = True
    safety_banner: str = VISUAL_LAYOUT_SAFETY_BANNER
    zones: list[RetailDecisionConsoleLayoutZone] = Field(
        default_factory=lambda: list(RetailDecisionConsoleLayoutZone)
    )
    sections: list[RetailDecisionConsoleLayoutSection]
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("layout_id", "title", "service", "schema_version", "stage", "safety_banner")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console layout text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def layout_must_remain_static_safe(self) -> RetailDecisionConsoleLayoutDescriptor:
        if self.title != SHELL_TITLE:
            raise ValueError("retail decision console layout title is fixed")
        if self.stage != VISUAL_LAYOUT_STAGE:
            raise ValueError("retail decision console layout stage must be visual_layout_pass")
        if not self.zones:
            raise ValueError("retail decision console layout requires zones")
        if not self.sections:
            raise ValueError("retail decision console layout requires sections")
        if not self.demo_only or not self.unavailable or not self.read_only:
            raise ValueError("retail decision console layout must remain demo-only, unavailable, and read-only")
        section_zones = {section.zone for section in self.sections}
        missing_zones = [zone.value for zone in self.zones if zone not in section_zones]
        if missing_zones:
            raise ValueError("retail decision console layout sections must cover zones: " + ", ".join(missing_zones))
        enabled = _enabled_flags(
            {
                "live data": self.live_data_enabled,
                "recommendations": self.recommendations_enabled,
                "action generation": self.action_generation_enabled,
                "confidence scoring": self.confidence_scoring_enabled,
                "DecisionObject generation": self.decision_object_generation_enabled,
                "broker controls": self.broker_controls_enabled,
                "order buttons": self.order_buttons_enabled,
                "execution": self.execution_enabled,
            }
        )
        if enabled:
            raise ValueError("retail decision console layout cannot enable: " + ", ".join(enabled))
        return self


def retail_decision_console_default_layout(
    created_at: datetime | None = None,
) -> RetailDecisionConsoleLayoutDescriptor:
    timestamp = created_at or utc_now()
    sections = [
        RetailDecisionConsoleLayoutSection(
            section_id="header-status-banner",
            title="Status banner",
            subtitle="Global safety posture",
            zone=RetailDecisionConsoleLayoutZone.HEADER,
            priority=0,
            placeholder_text="Static preview header. Demo-only and unavailable.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="instrument-selector",
            title="Instrument placeholder",
            subtitle="Selection shell",
            zone=RetailDecisionConsoleLayoutZone.CONTROLS,
            priority=10,
            placeholder_text="Unavailable selector placeholder. No lookup or live data.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="timeframe-selector",
            title="Timeframe placeholder",
            subtitle="Horizon shell",
            zone=RetailDecisionConsoleLayoutZone.CONTROLS,
            priority=11,
            placeholder_text="Unavailable timeframe placeholder. No fetch or computation.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="market-session",
            title="Market/session placeholder",
            subtitle="Session shell",
            zone=RetailDecisionConsoleLayoutZone.CONTROLS,
            priority=12,
            placeholder_text="Unavailable market/session placeholder. No live status claim.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="refresh-placeholder",
            title="Refresh placeholder",
            subtitle="Disabled static control",
            zone=RetailDecisionConsoleLayoutZone.CONTROLS,
            priority=13,
            placeholder_text="Disabled placeholder. No network call, no API fetch, no data refresh.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="decision-summary",
            title="Decision summary placeholder",
            subtitle="Primary unavailable summary",
            zone=RetailDecisionConsoleLayoutZone.PRIMARY,
            priority=20,
            placeholder_text="Unavailable decision-support shell. No generated action state.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="regime-state",
            title="Regime/state placeholder",
            subtitle="Context shell",
            zone=RetailDecisionConsoleLayoutZone.PRIMARY,
            priority=21,
            placeholder_text="Unavailable context panel. No live regime detection.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="evidence-panel",
            title="Evidence panel placeholder",
            subtitle="Evidence shell",
            zone=RetailDecisionConsoleLayoutZone.SECONDARY,
            priority=30,
            placeholder_text="Unavailable evidence panel. No validated bundle.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="risk-invalidation",
            title="Risk/invalidation placeholder",
            subtitle="Risk shell",
            zone=RetailDecisionConsoleLayoutZone.SECONDARY,
            priority=31,
            placeholder_text="Unavailable risk and invalidation shell. No live risk calculation.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="options-context",
            title="Options context placeholder",
            subtitle="Options shell",
            zone=RetailDecisionConsoleLayoutZone.CONTEXT,
            priority=40,
            placeholder_text="Unavailable options context. No analytics output.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="research-context",
            title="Research context placeholder",
            subtitle="Research shell",
            zone=RetailDecisionConsoleLayoutZone.CONTEXT,
            priority=41,
            placeholder_text="Unavailable research context. No retrieval or strategy output.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="journal",
            title="Journal placeholder",
            subtitle="Notebook shell",
            zone=RetailDecisionConsoleLayoutZone.FOOTER,
            priority=50,
            placeholder_text="Unavailable journal link placeholder. No active workflow.",
            created_at=timestamp,
        ),
        RetailDecisionConsoleLayoutSection(
            section_id="settings",
            title="Settings/help placeholder",
            subtitle="Preference shell",
            zone=RetailDecisionConsoleLayoutZone.FOOTER,
            priority=51,
            placeholder_text="Unavailable settings and help placeholder. No external connection.",
            created_at=timestamp,
        ),
    ]
    return RetailDecisionConsoleLayoutDescriptor(sections=sections, created_at=timestamp)
