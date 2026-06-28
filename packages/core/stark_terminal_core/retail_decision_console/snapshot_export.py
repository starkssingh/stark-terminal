from __future__ import annotations

import json
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.retail_decision_console.productization import (
    SERVICE_NAME,
    non_empty_text,
    normalize_datetime,
)
from stark_terminal_core.retail_decision_console.state_view_model import (
    STATIC_STATE_SAFETY_BANNER,
    RetailDecisionConsoleShellViewModel,
    retail_decision_console_state_view_model,
)


PREVIEW_SNAPSHOT_STAGE = "preview_snapshot_export"


class RetailDecisionConsoleSnapshotFormat(StrEnum):
    JSON = "json"
    MARKDOWN = "markdown"
    TEXT = "text"


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


def _enabled_flags(flags: dict[str, bool]) -> list[str]:
    return [name for name, enabled in flags.items() if enabled]


class RetailDecisionConsolePreviewSnapshot(BaseModel):
    snapshot_id: str = "retail-decision-console-preview-snapshot-v1"
    generated_at_utc: datetime
    service: str = SERVICE_NAME
    stage: str = PREVIEW_SNAPSHOT_STAGE
    schema_version: str = "v1"
    demo_only: bool = True
    unavailable: bool = True
    local_only: bool = True
    read_only: bool = True
    safety_banner: str = STATIC_STATE_SAFETY_BANNER
    layout_summary: dict[str, Any]
    section_summary: list[dict[str, Any]]
    card_summary: list[dict[str, Any]]
    static_interaction_summary: list[dict[str, Any]]
    provenance_demo_label: str
    live_data_enabled: bool = False
    recommendations_enabled: bool = False
    action_generation_enabled: bool = False
    confidence_scoring_enabled: bool = False
    decision_object_generation_enabled: bool = False
    broker_controls_enabled: bool = False
    order_buttons_enabled: bool = False
    execution_enabled: bool = False
    no_secrets_marker: str = "no secrets included"
    no_credentials_marker: str = "no credentials included"
    no_live_data_marker: str = "no live data included"
    no_recommendation_marker: str = "no recommendations included"
    no_execution_marker: str = "no execution controls included"
    safety_flags: dict[str, bool] = Field(default_factory=_safe_flag_snapshot)

    @field_validator(
        "snapshot_id",
        "service",
        "stage",
        "schema_version",
        "safety_banner",
        "provenance_demo_label",
        "no_secrets_marker",
        "no_credentials_marker",
        "no_live_data_marker",
        "no_recommendation_marker",
        "no_execution_marker",
    )
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return non_empty_text(value, "retail decision console preview snapshot text")

    @field_validator("generated_at_utc")
    @classmethod
    def generated_at_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_datetime(value)

    @model_validator(mode="after")
    def snapshot_must_remain_local_static_safe(self) -> RetailDecisionConsolePreviewSnapshot:
        if self.stage != PREVIEW_SNAPSHOT_STAGE:
            raise ValueError("retail decision console preview snapshot stage must be preview_snapshot_export")
        if not (self.demo_only and self.unavailable and self.local_only and self.read_only):
            raise ValueError("retail decision console preview snapshot must remain demo, unavailable, local, and read-only")
        if not self.layout_summary or not self.section_summary or not self.card_summary or not self.static_interaction_summary:
            raise ValueError("retail decision console preview snapshot requires layout, section, card, and interaction summaries")
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
            raise ValueError("retail decision console preview snapshot cannot enable: " + ", ".join(enabled))
        return self


def _layout_summary(view_model: RetailDecisionConsoleShellViewModel) -> dict[str, Any]:
    return {
        "layout_id": view_model.layout.layout_id,
        "title": view_model.layout.title,
        "stage": view_model.layout.stage,
        "zones": [zone.value for zone in view_model.layout.zones],
        "section_count": len(view_model.sections),
        "demo_only": view_model.layout.demo_only,
        "unavailable": view_model.layout.unavailable,
        "read_only": view_model.layout.read_only,
        "safety_banner": view_model.layout.safety_banner,
    }


def _section_summary(view_model: RetailDecisionConsoleShellViewModel) -> list[dict[str, Any]]:
    return [
        {
            "section_id": section.section_id,
            "title": section.title,
            "zone": section.layout_zone.value,
            "priority": section.layout_priority,
            "placeholder_text": section.placeholder_text,
            "unavailable_demo_label": section.unavailable_demo_label,
            "provenance_demo_label": section.provenance_demo_label,
            "demo_only": section.demo_only,
            "unavailable": section.unavailable,
            "safety_flags": section.safety_flags,
        }
        for section in sorted(
            view_model.sections,
            key=lambda item: (
                list(view_model.layout.zones).index(item.layout_zone),
                item.layout_priority,
            ),
        )
    ]


def _card_summary(view_model: RetailDecisionConsoleShellViewModel) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for section in view_model.sections:
        for card in section.cards:
            cards.append(
                {
                    "section_id": section.section_id,
                    "card_id": card.card_id,
                    "title": card.title,
                    "placeholder_text": card.placeholder_text,
                    "unavailable_demo_label": card.unavailable_demo_label,
                    "provenance_demo_label": card.provenance_demo_label,
                    "demo_only": card.demo_only,
                    "unavailable": card.unavailable,
                    "safety_flags": card.safety_flags,
                }
            )
    return cards


def _interaction_summary(view_model: RetailDecisionConsoleShellViewModel) -> list[dict[str, Any]]:
    return [
        {
            "interaction_id": interaction.interaction_id,
            "label": interaction.label,
            "interaction_type": interaction.interaction_type.value,
            "target_section_id": interaction.target_section_id,
            "demo_only": interaction.demo_only,
            "unavailable": interaction.unavailable,
            "local_only": interaction.local_only,
            "read_only": interaction.read_only,
            "safety_note": interaction.safety_note,
            "safety_flags": interaction.safety_flags,
        }
        for interaction in view_model.interactions
    ]


def retail_decision_console_preview_snapshot(
    view_model: RetailDecisionConsoleShellViewModel | None = None,
    generated_at_utc: datetime | None = None,
) -> RetailDecisionConsolePreviewSnapshot:
    current_view_model = view_model or retail_decision_console_state_view_model()
    return RetailDecisionConsolePreviewSnapshot(
        generated_at_utc=generated_at_utc or current_view_model.created_at,
        layout_summary=_layout_summary(current_view_model),
        section_summary=_section_summary(current_view_model),
        card_summary=_card_summary(current_view_model),
        static_interaction_summary=_interaction_summary(current_view_model),
        provenance_demo_label=current_view_model.provenance_demo_label,
    )


def retail_decision_console_snapshot_to_dict(
    snapshot: RetailDecisionConsolePreviewSnapshot | None = None,
) -> dict[str, Any]:
    current_snapshot = snapshot or retail_decision_console_preview_snapshot()
    return current_snapshot.model_dump(mode="json")


def retail_decision_console_snapshot_to_markdown(
    snapshot: RetailDecisionConsolePreviewSnapshot | None = None,
) -> str:
    current_snapshot = snapshot or retail_decision_console_preview_snapshot()
    lines = [
        "# Retail Decision Console Preview Snapshot",
        "",
        current_snapshot.safety_banner,
        "",
        f"- Stage: {current_snapshot.stage}",
        f"- Demo only: {current_snapshot.demo_only}",
        f"- Unavailable: {current_snapshot.unavailable}",
        f"- Local only: {current_snapshot.local_only}",
        f"- Read only: {current_snapshot.read_only}",
        f"- {current_snapshot.no_secrets_marker}",
        f"- {current_snapshot.no_credentials_marker}",
        f"- {current_snapshot.no_live_data_marker}",
        f"- {current_snapshot.no_recommendation_marker}",
        f"- {current_snapshot.no_execution_marker}",
        "",
        "## Layout",
        f"- Title: {current_snapshot.layout_summary['title']}",
        f"- Zones: {', '.join(current_snapshot.layout_summary['zones'])}",
        f"- Sections: {current_snapshot.layout_summary['section_count']}",
        "",
        "## Sections",
    ]
    lines.extend(
        f"- {section['zone']} / {section['title']}: {section['unavailable_demo_label']}"
        for section in current_snapshot.section_summary
    )
    lines.extend(["", "## Static Interactions"])
    lines.extend(
        f"- {interaction['interaction_type']} / {interaction['label']}: demo-only unavailable local-only"
        for interaction in current_snapshot.static_interaction_summary
    )
    return "\n".join(lines) + "\n"


def retail_decision_console_snapshot_to_text(
    snapshot: RetailDecisionConsolePreviewSnapshot | None = None,
) -> str:
    current_snapshot = snapshot or retail_decision_console_preview_snapshot()
    lines = [
        "Retail Decision Console Preview Snapshot",
        current_snapshot.safety_banner,
        f"Stage: {current_snapshot.stage}",
        "State: demo-only, unavailable, local-only, read-only",
        current_snapshot.no_secrets_marker,
        current_snapshot.no_credentials_marker,
        current_snapshot.no_live_data_marker,
        current_snapshot.no_recommendation_marker,
        current_snapshot.no_execution_marker,
        f"Layout zones: {', '.join(current_snapshot.layout_summary['zones'])}",
        f"Sections: {len(current_snapshot.section_summary)}",
        f"Cards: {len(current_snapshot.card_summary)}",
        f"Static interactions: {len(current_snapshot.static_interaction_summary)}",
    ]
    return "\n".join(lines) + "\n"


def _snapshot_payload(
    snapshot: RetailDecisionConsolePreviewSnapshot,
    snapshot_format: RetailDecisionConsoleSnapshotFormat,
) -> str:
    if snapshot_format is RetailDecisionConsoleSnapshotFormat.JSON:
        return json.dumps(retail_decision_console_snapshot_to_dict(snapshot), indent=2, sort_keys=True) + "\n"
    if snapshot_format is RetailDecisionConsoleSnapshotFormat.MARKDOWN:
        return retail_decision_console_snapshot_to_markdown(snapshot)
    return retail_decision_console_snapshot_to_text(snapshot)


def write_retail_decision_console_snapshot(
    path: str | Path,
    snapshot: RetailDecisionConsolePreviewSnapshot | None = None,
    snapshot_format: RetailDecisionConsoleSnapshotFormat | str = RetailDecisionConsoleSnapshotFormat.JSON,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    current_snapshot = snapshot or retail_decision_console_preview_snapshot()
    current_format = RetailDecisionConsoleSnapshotFormat(snapshot_format)
    output_path.write_text(_snapshot_payload(current_snapshot, current_format), encoding="utf-8")
    return output_path
