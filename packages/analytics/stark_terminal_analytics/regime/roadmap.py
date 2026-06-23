from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes


class RegimeRoadmapItem(BaseModel):
    prompt: str
    title: str
    scope: str
    forbidden: list[str]
    status: str = "planned"

    @field_validator("prompt", "title", "scope", "status")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("regime roadmap text fields cannot be empty")
        return normalized

    @field_validator("forbidden")
    @classmethod
    def forbidden_scope_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_analytics_notes(value)
        if not sanitized:
            raise ValueError("regime roadmap items must include forbidden scope")
        return sanitized


DEFAULT_REGIME_FORBIDDEN = [
    "classification",
    "feature computation",
    "feature registry writes",
    "signals",
    "recommendations",
    "DecisionObject generation",
    "execution APIs",
    "broker integration",
    "real market ingestion",
]


def default_regime_roadmap() -> list[RegimeRoadmapItem]:
    return [
        RegimeRoadmapItem(
            prompt="Prompt 34",
            title="Regime Feature Preparation Contracts",
            scope="Define candidate feature group contracts and evidence mapping without feature computation.",
            forbidden=DEFAULT_REGIME_FORBIDDEN,
            status="completed",
        ),
        RegimeRoadmapItem(
            prompt="Prompt 35",
            title="Analytics/Regime Milestone Audit",
            scope="Audit diagnostics, relationship analytics, regime planning, and feature-preparation boundaries.",
            forbidden=DEFAULT_REGIME_FORBIDDEN,
            status="next",
        ),
        RegimeRoadmapItem(
            prompt="Prompt 36",
            title="Retail Decision Desk Planning and Guardrails",
            scope="Plan future decision desk contracts and user-facing safety boundaries.",
            forbidden=DEFAULT_REGIME_FORBIDDEN,
        ),
        RegimeRoadmapItem(
            prompt="Prompt 37",
            title="DecisionObject Evidence Bundle Contracts",
            scope="Define future evidence bundle contracts without generating DecisionObjects.",
            forbidden=DEFAULT_REGIME_FORBIDDEN,
        ),
        RegimeRoadmapItem(
            prompt="Prompt 38",
            title="Decision Safety and Human-Review Guardrails",
            scope="Define human-review and safety gates before any future decision logic.",
            forbidden=DEFAULT_REGIME_FORBIDDEN,
        ),
    ]
