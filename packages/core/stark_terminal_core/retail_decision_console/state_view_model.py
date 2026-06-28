from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.demo_state import (
    retail_decision_console_demo_state,
)
from stark_terminal_core.retail_decision_console.layout import (
    RetailDecisionConsoleLayoutDescriptor,
    RetailDecisionConsoleLayoutSection,
    RetailDecisionConsoleLayoutZone,
    retail_decision_console_default_layout,
)
from stark_terminal_core.retail_decision_console.interactions import (
    RetailDecisionConsoleInteractionDescriptor,
    retail_decision_console_static_interactions,
)
from stark_terminal_core.retail_decision_console.productization import (
    SERVICE_NAME,
    non_empty_text,
    normalize_datetime,
)
from stark_terminal_core.retail_decision_console.state_safety import (
    assert_retail_decision_console_demo_state_is_safe,
)
from stark_terminal_core.retail_decision_console.static_state import (
    RetailDecisionConsoleCardState,
    RetailDecisionConsoleProvenanceState,
    RetailDecisionConsoleSectionState,
    RetailDecisionConsoleStaticState,
)
from stark_terminal_core.retail_decision_console.ui_descriptors import (
    FORBIDDEN_ACTIVE_CONTROL_LABELS,
    SAFETY_BANNER,
    SHELL_TITLE,
    RetailDecisionConsoleShellDescriptor,
    retail_decision_console_ui_shell_descriptor,
)
from stark_terminal_core.retail_decision_console.ui_shell import (
    assert_retail_decision_console_ui_shell_is_safe,
)


STATIC_STATE_WIRING_STAGE = "static_state_wired_shell"
STATIC_STATE_SAFETY_BANNER = "Demo/static shell only — no live data, no recommendations, no execution"


def _enabled_flags(flags: dict[str, bool]) -> list[str]:
    return [name for name, value in flags.items() if value]


def _forbidden_active_labels(labels: list[str]) -> list[str]:
    forbidden = {label.casefold() for label in FORBIDDEN_ACTIVE_CONTROL_LABELS}
    return [label for label in labels if label.casefold() in forbidden]


def _safe_flag_snapshot() -> dict[str, bool]:
    return {
        "live_data_enabled": False,
        "recommendations_enabled": False,
        "action_generation_enabled": False,
        "confidence_scoring_enabled": False,
        "decision_object_generation_enabled": False,
        "broker_controls_enabled": False,
        "order_buttons_enabled": False,
        "execution_enabled": False,
    }


class RetailDecisionConsoleCardViewModel(BaseModel):
    card_id: str
    title: str
    placeholder_text: str
    unavailable_demo_label: str = "Demo only - unavailable placeholder"
    provenance_demo_label: str
    demo_only: bool = True
    unavailable: bool = True
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    active_control_labels: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=_safe_flag_snapshot)
    created_at: datetime

    @field_validator("card_id", "title", "placeholder_text", "unavailable_demo_label", "provenance_demo_label")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console card view-model text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def card_view_model_must_stay_demo_unavailable(self) -> RetailDecisionConsoleCardViewModel:
        if not self.demo_only or not self.unavailable:
            raise ValueError("retail decision console card view model must remain demo-only and unavailable")
        enabled = _enabled_flags(
            {
                **self.safety_flags,
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
            raise ValueError("retail decision console card view model cannot enable: " + ", ".join(enabled))
        forbidden_labels = _forbidden_active_labels(self.active_control_labels)
        if forbidden_labels:
            raise ValueError("retail decision console card view model cannot expose active controls: " + ", ".join(forbidden_labels))
        return self


class RetailDecisionConsoleSectionViewModel(BaseModel):
    section_id: str
    title: str
    placeholder_text: str
    layout_zone: RetailDecisionConsoleLayoutZone = RetailDecisionConsoleLayoutZone.CONTEXT
    layout_priority: int = Field(default=0, ge=0)
    layout_subtitle: str = "Static preview section"
    layout_safety_label: str = "Demo only - unavailable static preview"
    unavailable_demo_label: str = "Demo only - unavailable section"
    provenance_demo_label: str
    demo_only: bool = True
    unavailable: bool = True
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    active_control_labels: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=_safe_flag_snapshot)
    cards: list[RetailDecisionConsoleCardViewModel]
    created_at: datetime

    @field_validator(
        "section_id",
        "title",
        "placeholder_text",
        "layout_subtitle",
        "layout_safety_label",
        "unavailable_demo_label",
        "provenance_demo_label",
    )
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console section view-model text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def section_view_model_must_stay_demo_unavailable(self) -> RetailDecisionConsoleSectionViewModel:
        if not self.demo_only or not self.unavailable:
            raise ValueError("retail decision console section view model must remain demo-only and unavailable")
        if not self.cards:
            raise ValueError("retail decision console section view model requires demo cards")
        enabled = _enabled_flags(
            {
                **self.safety_flags,
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
            raise ValueError("retail decision console section view model cannot enable: " + ", ".join(enabled))
        forbidden_labels = _forbidden_active_labels(self.active_control_labels)
        if forbidden_labels:
            raise ValueError(
                "retail decision console section view model cannot expose active controls: " + ", ".join(forbidden_labels)
            )
        return self


class RetailDecisionConsoleShellViewModel(BaseModel):
    view_model_id: str
    shell_id: str
    title: str = SHELL_TITLE
    stage: str = STATIC_STATE_WIRING_STAGE
    service: str = SERVICE_NAME
    schema_version: str = "v1"
    static_state_wiring_only: bool = True
    static_interaction_placeholders_only: bool = True
    demo_only: bool = True
    unavailable: bool = True
    read_only: bool = True
    safety_banner: str = STATIC_STATE_SAFETY_BANNER
    provenance_demo_label: str
    shell_safety_banner: str = SAFETY_BANNER
    layout: RetailDecisionConsoleLayoutDescriptor
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    active_control_labels: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=_safe_flag_snapshot)
    interactions: list[RetailDecisionConsoleInteractionDescriptor] = Field(default_factory=list)
    sections: list[RetailDecisionConsoleSectionViewModel]
    created_at: datetime

    @field_validator("view_model_id", "shell_id", "title", "stage", "service", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console shell view-model text")

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def shell_view_model_must_stay_safe(self) -> RetailDecisionConsoleShellViewModel:
        if self.title != SHELL_TITLE:
            raise ValueError("retail decision console shell view model title is fixed")
        if self.stage != STATIC_STATE_WIRING_STAGE:
            raise ValueError("retail decision console shell view model stage must be static_state_wired_shell")
        if not (
            self.static_state_wiring_only
            and self.static_interaction_placeholders_only
            and self.demo_only
            and self.unavailable
            and self.read_only
        ):
            raise ValueError("retail decision console shell view model must remain wired demo/static state only")
        if not self.sections:
            raise ValueError("retail decision console shell view model requires sections")
        if not self.interactions:
            raise ValueError("retail decision console shell view model requires static interactions")
        if not self.layout.demo_only or not self.layout.unavailable or not self.layout.read_only:
            raise ValueError("retail decision console shell view model requires demo/unavailable layout")
        unsafe_interactions = [
            interaction.interaction_id
            for interaction in self.interactions
            if not (
                interaction.demo_only
                and interaction.unavailable
                and interaction.local_only
                and interaction.read_only
            )
        ]
        if unsafe_interactions:
            raise ValueError(
                "retail decision console shell view model cannot expose unsafe interactions: "
                + ", ".join(unsafe_interactions)
            )
        enabled = _enabled_flags(
            {
                **self.safety_flags,
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
            raise ValueError("retail decision console shell view model cannot enable: " + ", ".join(enabled))
        forbidden_labels = _forbidden_active_labels(self.active_control_labels)
        if forbidden_labels:
            raise ValueError("retail decision console shell view model cannot expose active controls: " + ", ".join(forbidden_labels))
        return self


def _provenance_label(provenance: RetailDecisionConsoleProvenanceState) -> str:
    return f"{provenance.label} ({provenance.source_type})"


def _layout_section_for(
    section: RetailDecisionConsoleSectionState,
    layout_by_section_id: dict[str, RetailDecisionConsoleLayoutSection],
) -> RetailDecisionConsoleLayoutSection:
    return layout_by_section_id.get(
        section.section_id,
        RetailDecisionConsoleLayoutSection(
            section_id=section.section_id,
            title=section.title,
            subtitle="Static preview section",
            zone=RetailDecisionConsoleLayoutZone.CONTEXT,
            priority=999,
            placeholder_text=section.body,
            created_at=section.created_at,
        ),
    )


def map_demo_cards_to_ui_cards(
    cards: list[RetailDecisionConsoleCardState] | None = None,
    provenance: RetailDecisionConsoleProvenanceState | None = None,
) -> list[RetailDecisionConsoleCardViewModel]:
    state = retail_decision_console_demo_state()
    current_cards = cards or [card for section in state.sections for card in section.cards]
    current_provenance = provenance or state.provenance
    provenance_label = _provenance_label(current_provenance)
    return [
        RetailDecisionConsoleCardViewModel(
            card_id=card.card_id,
            title=card.title,
            placeholder_text=card.body,
            provenance_demo_label=provenance_label,
            created_at=card.created_at,
        )
        for card in current_cards
    ]


def map_demo_sections_to_ui_sections(
    sections: list[RetailDecisionConsoleSectionState] | None = None,
    provenance: RetailDecisionConsoleProvenanceState | None = None,
    layout_sections: list[RetailDecisionConsoleLayoutSection] | None = None,
) -> list[RetailDecisionConsoleSectionViewModel]:
    state = retail_decision_console_demo_state()
    current_sections = sections or state.sections
    current_provenance = provenance or state.provenance
    provenance_label = _provenance_label(current_provenance)
    layout_by_section_id = {section.section_id: section for section in layout_sections or []}
    section_view_models: list[RetailDecisionConsoleSectionViewModel] = []
    for section in current_sections:
        layout_section = _layout_section_for(section, layout_by_section_id)
        section_view_models.append(
            RetailDecisionConsoleSectionViewModel(
                section_id=section.section_id,
                title=section.title,
                placeholder_text=section.body,
                layout_zone=layout_section.zone,
                layout_priority=layout_section.priority,
                layout_subtitle=layout_section.subtitle,
                layout_safety_label=layout_section.safety_label,
                provenance_demo_label=provenance_label,
                cards=map_demo_cards_to_ui_cards(section.cards, current_provenance),
                created_at=section.created_at,
            )
        )
    return section_view_models


def map_demo_state_to_shell_descriptor(
    state: RetailDecisionConsoleStaticState | None = None,
    descriptor: RetailDecisionConsoleShellDescriptor | None = None,
) -> RetailDecisionConsoleShellViewModel:
    current_state = state or retail_decision_console_demo_state()
    current_descriptor = descriptor or retail_decision_console_ui_shell_descriptor()
    layout = retail_decision_console_default_layout(current_state.created_at)
    interaction_state = retail_decision_console_static_interactions(current_state.created_at)
    assert_retail_decision_console_demo_state_is_safe(current_state)
    assert_retail_decision_console_ui_shell_is_safe(current_descriptor)
    return RetailDecisionConsoleShellViewModel(
        view_model_id="retail-decision-console-static-state-view-model-v1",
        shell_id=current_descriptor.shell_id,
        provenance_demo_label=_provenance_label(current_state.provenance),
        layout=layout,
        interactions=interaction_state.interactions,
        sections=map_demo_sections_to_ui_sections(current_state.sections, current_state.provenance, layout.sections),
        created_at=current_state.created_at,
    )


def retail_decision_console_state_view_model() -> RetailDecisionConsoleShellViewModel:
    return map_demo_state_to_shell_descriptor()
