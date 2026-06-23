from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes
from stark_terminal_analytics.foundation.dependencies import AnalyticsDependencyStage


class AnalyticsRoadmapItem(BaseModel):
    prompt: str
    title: str
    scope: str
    forbidden: list[str]
    dependencies_stage: AnalyticsDependencyStage
    status: str = "planned"

    @field_validator("prompt", "title", "scope", "status")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("analytics roadmap text fields cannot be empty")
        return normalized

    @field_validator("forbidden")
    @classmethod
    def forbidden_items_must_be_present(cls, value: list[str]) -> list[str]:
        sanitized = sanitize_analytics_notes(value)
        if not sanitized:
            raise ValueError("analytics roadmap items must list forbidden scope")
        return sanitized


DEFAULT_FORBIDDEN = [
    "trading signals",
    "recommendations",
    "decision generation",
    "execution APIs",
    "broker integration",
    "real market ingestion",
]


def default_analytics_roadmap() -> list[AnalyticsRoadmapItem]:
    return [
        AnalyticsRoadmapItem(
            prompt="Prompt 27",
            title="Numerical Analytics Core Contracts",
            scope="Define safe numerical input/output contracts and dependency gates.",
            forbidden=DEFAULT_FORBIDDEN,
            dependencies_stage=AnalyticsDependencyStage.NUMERICAL_CORE,
            status="completed",
        ),
        AnalyticsRoadmapItem(
            prompt="Prompt 28",
            title="Returns and Rolling Window Analytics v0",
            scope="Implement tiny deterministic descriptive returns and rolling-window calculations if allowed.",
            forbidden=DEFAULT_FORBIDDEN,
            dependencies_stage=AnalyticsDependencyStage.NUMERICAL_CORE,
            status="completed",
        ),
        AnalyticsRoadmapItem(
            prompt="Prompt 29",
            title="Volatility and Drawdown Analytics v0",
            scope="Implement descriptive risk metrics with validation and source references if allowed.",
            forbidden=DEFAULT_FORBIDDEN,
            dependencies_stage=AnalyticsDependencyStage.NUMERICAL_CORE,
            status="completed",
        ),
        AnalyticsRoadmapItem(
            prompt="Prompt 30",
            title="Analytics Milestone Audit",
            scope="Audit numerical/returns/volatility/drawdown analytics boundaries.",
            forbidden=DEFAULT_FORBIDDEN,
            dependencies_stage=AnalyticsDependencyStage.CONTRACTS_ONLY,
            status="completed",
        ),
        AnalyticsRoadmapItem(
            prompt="Prompt 31",
            title="Correlation and Beta Analytics v0",
            scope="Plan or implement descriptive correlation and beta analytics under audit gates.",
            forbidden=DEFAULT_FORBIDDEN,
            dependencies_stage=AnalyticsDependencyStage.STATISTICAL_MODELS,
            status="completed",
        ),
        AnalyticsRoadmapItem(
            prompt="Prompt 32",
            title="Time-Series Diagnostics Foundation",
            scope="Introduce diagnostics contracts and quality checks for time-series assumptions.",
            forbidden=DEFAULT_FORBIDDEN,
            dependencies_stage=AnalyticsDependencyStage.STATISTICAL_MODELS,
            status="completed",
        ),
        AnalyticsRoadmapItem(
            prompt="Prompt 33",
            title="Regime Analytics Planning and Guardrails",
            scope="Plan regime analytics boundaries without hidden decision logic.",
            forbidden=DEFAULT_FORBIDDEN,
            dependencies_stage=AnalyticsDependencyStage.STATISTICAL_MODELS,
            status="completed",
        ),
        AnalyticsRoadmapItem(
            prompt="Prompt 34",
            title="Regime Feature Preparation Contracts",
            scope="Define feature preparation contracts for future regime analytics without feature computation.",
            forbidden=DEFAULT_FORBIDDEN,
            dependencies_stage=AnalyticsDependencyStage.STATISTICAL_MODELS,
            status="next",
        ),
        AnalyticsRoadmapItem(
            prompt="Prompt 35",
            title="Analytics/Regime Milestone Audit",
            scope="Audit correlation and beta, diagnostics, and regime planning boundaries.",
            forbidden=DEFAULT_FORBIDDEN,
            dependencies_stage=AnalyticsDependencyStage.CONTRACTS_ONLY,
        ),
    ]
