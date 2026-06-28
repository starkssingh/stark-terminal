from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    SERVICE_NAME,
    non_empty_text,
    normalize_datetime,
    sanitized_text_list,
    utc_now,
)


SHELL_TITLE = "Stark Terminal — Retail Decision Console"
SAFETY_BANNER = "Skeleton only — no live data, no recommendations, no execution"

FORBIDDEN_ACTIVE_CONTROL_LABELS = (
    "Buy",
    "Sell",
    "Execute",
    "Place Order",
    "Broker",
    "Connect Broker",
    "Trade Now",
    "Auto Trade",
    "Approve Trade",
    "Override",
    "Live Signal",
    "Strong Buy",
    "Strong Sell",
    "Ready to Trade",
)

SAFE_CONTROL_LABELS = (
    "Settings placeholder",
    "Journal placeholder",
    "Help/About placeholder",
)

DEFAULT_SECTION_DEFINITIONS = (
    ("header-status-banner", "Header/status banner", "Unavailable skeleton banner; no live data."),
    ("instrument-selector", "Instrument selector placeholder", "Static placeholder; no market data request."),
    ("timeframe-selector", "Timeframe selector placeholder", "Static placeholder; no data fetch."),
    ("market-session", "Market/session placeholder", "Static placeholder; no live session claim."),
    ("refresh-placeholder", "Disabled refresh placeholder", "Static disabled placeholder; no data refresh."),
    ("decision-summary", "Decision summary placeholder", "Unavailable summary; no generated action state."),
    ("regime-state", "Regime/state placeholder", "Unavailable context; no live regime classification."),
    ("evidence-panel", "Evidence panel placeholder", "Unavailable evidence shell; no validated evidence bundle."),
    ("risk-invalidation", "Risk/invalidation placeholder", "Unavailable risk shell; no live risk signal."),
    ("options-context", "Options context placeholder", "Unavailable options shell; no options recommendation."),
    ("research-context", "Research context placeholder", "Unavailable research shell; no retrieval."),
    ("journal", "Journal placeholder", "Static journal placeholder; no trade workflow."),
    ("settings", "Settings placeholder", "Static settings placeholder; no broker controls."),
)


def _dangerous_flags_enabled(flags: dict[str, bool]) -> list[str]:
    return [name for name, value in flags.items() if value]


def _contains_forbidden_label(labels: list[str]) -> list[str]:
    normalized_forbidden = {label.casefold() for label in FORBIDDEN_ACTIVE_CONTROL_LABELS}
    return [label for label in labels if label.casefold() in normalized_forbidden]


class RetailDecisionConsolePlaceholderState(BaseModel):
    state_id: str
    unavailable: bool = True
    skeleton_only: bool = True
    demo_only: bool = True
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    message: str = SAFETY_BANNER
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("state_id", "message")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console placeholder state text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def placeholder_state_must_stay_unavailable(self) -> RetailDecisionConsolePlaceholderState:
        if not self.unavailable or not self.skeleton_only or not self.demo_only:
            raise ValueError("retail decision console placeholder state must remain unavailable skeleton/demo only")
        enabled = _dangerous_flags_enabled(
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
            raise ValueError("retail decision console placeholder state cannot enable: " + ", ".join(enabled))
        return self


class RetailDecisionConsoleSectionDescriptor(BaseModel):
    section_id: str
    title: str
    description: str
    placeholder_state: RetailDecisionConsolePlaceholderState
    active_control_labels: list[str] = Field(default_factory=list)
    skeleton_only: bool = True
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("section_id", "title", "description")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console section descriptor text")

    @field_validator("active_control_labels")
    @classmethod
    def active_control_labels_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def section_must_remain_static_placeholder(self) -> RetailDecisionConsoleSectionDescriptor:
        if not self.skeleton_only:
            raise ValueError("retail decision console section descriptor must remain skeleton-only")
        forbidden_labels = _contains_forbidden_label(self.active_control_labels)
        if forbidden_labels:
            raise ValueError("retail decision console section cannot expose active controls: " + ", ".join(forbidden_labels))
        enabled = _dangerous_flags_enabled(
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
            raise ValueError("retail decision console section descriptor cannot enable: " + ", ".join(enabled))
        return self


class RetailDecisionConsoleShellDescriptor(BaseModel):
    shell_id: str
    title: str = SHELL_TITLE
    stage: str = "ui_shell_skeleton"
    service: str = SERVICE_NAME
    schema_version: str = "v1"
    skeleton_only: bool = True
    unavailable_by_default: bool = True
    safety_banner: str = SAFETY_BANNER
    safe_control_labels: tuple[str, ...] = SAFE_CONTROL_LABELS
    active_control_labels: list[str] = Field(default_factory=list)
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    sections: list[RetailDecisionConsoleSectionDescriptor]
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("shell_id", "title", "stage", "service", "schema_version", "safety_banner")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console shell descriptor text")

    @field_validator("safe_control_labels")
    @classmethod
    def safe_control_labels_must_be_clean(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(sanitized_text_list(list(value)))

    @field_validator("active_control_labels")
    @classmethod
    def active_control_labels_must_be_clean(cls, value: list[str]) -> list[str]:
        return sanitized_text_list(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def shell_must_remain_skeleton_only(self) -> RetailDecisionConsoleShellDescriptor:
        if self.title != SHELL_TITLE:
            raise ValueError("retail decision console shell title is fixed")
        if self.stage != "ui_shell_skeleton":
            raise ValueError("retail decision console shell stage must be ui_shell_skeleton")
        if not self.skeleton_only or not self.unavailable_by_default:
            raise ValueError("retail decision console shell must remain skeleton-only and unavailable by default")
        if not self.sections:
            raise ValueError("retail decision console shell requires placeholder sections")
        forbidden_labels = _contains_forbidden_label(self.active_control_labels)
        if forbidden_labels:
            raise ValueError("retail decision console shell cannot expose active controls: " + ", ".join(forbidden_labels))
        enabled = _dangerous_flags_enabled(
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
            raise ValueError("retail decision console shell descriptor cannot enable: " + ", ".join(enabled))
        return self


def default_placeholder_state(section_id: str) -> RetailDecisionConsolePlaceholderState:
    return RetailDecisionConsolePlaceholderState(state_id=f"{section_id}-unavailable-state")


def retail_decision_console_section_descriptors() -> list[RetailDecisionConsoleSectionDescriptor]:
    return [
        RetailDecisionConsoleSectionDescriptor(
            section_id=section_id,
            title=title,
            description=description,
            placeholder_state=default_placeholder_state(section_id),
        )
        for section_id, title, description in DEFAULT_SECTION_DEFINITIONS
    ]


def retail_decision_console_ui_shell_descriptor() -> RetailDecisionConsoleShellDescriptor:
    return RetailDecisionConsoleShellDescriptor(
        shell_id="retail-decision-console-ui-shell-skeleton-v1",
        sections=retail_decision_console_section_descriptors(),
    )


def retail_decision_console_ui_forbidden_labels() -> tuple[str, ...]:
    return FORBIDDEN_ACTIVE_CONTROL_LABELS
