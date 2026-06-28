from __future__ import annotations

from datetime import datetime, timezone

from stark_terminal_core.retail_decision_console.static_state import (
    RetailDecisionConsoleCardState,
    RetailDecisionConsoleProvenanceState,
    RetailDecisionConsoleSectionState,
    RetailDecisionConsoleStaticState,
)


DEMO_CREATED_AT = datetime(2026, 1, 1, tzinfo=timezone.utc)

DEMO_SECTION_DEFINITIONS = (
    (
        "header-status-banner",
        "Header/status banner",
        "Demo only and unavailable. No live data, recommendation, action generation, confidence score, active DecisionObject, broker control, order button, or execution.",
    ),
    (
        "instrument-selector",
        "Instrument selector placeholder",
        "Demo only and unavailable. No instrument lookup, live data, recommendation, confidence score, broker control, order button, or execution.",
    ),
    (
        "timeframe-selector",
        "Timeframe selector placeholder",
        "Demo only and unavailable. No timeframe data fetch, live data, recommendation, confidence score, broker control, order button, or execution.",
    ),
    (
        "market-session",
        "Market/session placeholder",
        "Demo only and unavailable. No market session lookup, live data, recommendation, confidence score, broker control, order button, or execution.",
    ),
    (
        "refresh-placeholder",
        "Disabled refresh placeholder",
        "Demo only and unavailable. No data refresh, live data, recommendation, confidence score, broker control, order button, or execution.",
    ),
    (
        "decision-summary",
        "Decision summary placeholder",
        "Demo only and unavailable. No generated action state, recommendation, confidence score, active DecisionObject, broker control, order button, or execution.",
    ),
    (
        "regime-state",
        "Regime/state placeholder",
        "Demo only and unavailable. No regime detection, live data, recommendation, confidence score, broker control, order button, or execution.",
    ),
    (
        "evidence-panel",
        "Evidence panel placeholder",
        "Demo only and unavailable. No validated evidence bundle, recommendation, confidence score, active DecisionObject, broker control, order button, or execution.",
    ),
    (
        "risk-invalidation",
        "Risk/invalidation placeholder",
        "Demo only and unavailable. No live risk calculation, recommendation, confidence score, broker control, order button, or execution.",
    ),
    (
        "options-context",
        "Options context placeholder",
        "Demo only and unavailable. No options analytics, recommendation, confidence score, broker control, order button, or execution.",
    ),
    (
        "research-context",
        "Research context placeholder",
        "Demo only and unavailable. No retrieval, strategy generation, recommendation, confidence score, broker control, order button, or execution.",
    ),
    (
        "journal",
        "Journal placeholder",
        "Demo only and unavailable. No active workflow, broker control, order button, recommendation, confidence score, or execution.",
    ),
    (
        "settings",
        "Settings placeholder",
        "Demo only and unavailable. No broker control, live data, recommendation, confidence score, order button, or execution.",
    ),
)


def retail_decision_console_demo_cards(section_id: str | None = None) -> list[RetailDecisionConsoleCardState]:
    target = section_id or "retail-decision-console"
    return [
        RetailDecisionConsoleCardState(
            card_id=f"{target}-demo-unavailable-card",
            title="Demo unavailable card",
            body=(
                "Demo only and unavailable. No live data, recommendation, action generation, "
                "confidence score, active DecisionObject, broker control, order button, or execution."
            ),
            created_at=DEMO_CREATED_AT,
        )
    ]


def retail_decision_console_demo_sections() -> list[RetailDecisionConsoleSectionState]:
    return [
        RetailDecisionConsoleSectionState(
            section_id=section_id,
            title=title,
            body=body,
            cards=retail_decision_console_demo_cards(section_id),
            created_at=DEMO_CREATED_AT,
        )
        for section_id, title, body in DEMO_SECTION_DEFINITIONS
    ]


def retail_decision_console_demo_state() -> RetailDecisionConsoleStaticState:
    return RetailDecisionConsoleStaticState(
        state_id="retail-decision-console-demo-static-state-v1",
        provenance=RetailDecisionConsoleProvenanceState(
            provenance_id="retail-decision-console-demo-static-provenance-v1",
            notes=[
                "Demo static unavailable placeholder only.",
                "No source validation or data-quality validation is implied.",
                "No live market intelligence is present.",
            ],
            created_at=DEMO_CREATED_AT,
        ),
        sections=retail_decision_console_demo_sections(),
        created_at=DEMO_CREATED_AT,
    )
