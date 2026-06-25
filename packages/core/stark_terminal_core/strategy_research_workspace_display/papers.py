from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace_display.contracts import (
    StrategyResearchWorkspaceDisplayPaperKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_workspace_display_notes,
)


def _optional_trimmed(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


class StrategyResearchWorkspaceDisplayPaperPlaceholder(BaseModel):
    paper_reference_id: str
    paper_kind: StrategyResearchWorkspaceDisplayPaperKind
    title: str
    source: str | None = None
    display_contract_only: bool = True
    rendered_now: bool = False
    paper_ingested: bool = False
    paper_parsed: bool = False
    method_extracted: bool = False
    strategy_extracted: bool = False
    code_generated: bool = False
    backtest_generated: bool = False
    recommendation_generated: bool = False
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)
    notes: list[str] = Field(default_factory=list)

    @field_validator("paper_reference_id", "title", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "strategy research workspace display paper text fields")

    @field_validator("source")
    @classmethod
    def source_must_be_trimmed(cls, value: str | None) -> str | None:
        return _optional_trimmed(value)

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_workspace_display_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def paper_placeholder_must_fail_closed(self) -> StrategyResearchWorkspaceDisplayPaperPlaceholder:
        if self.paper_kind == StrategyResearchWorkspaceDisplayPaperKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research Workspace Display paper kind is not allowed")
        if not self.display_contract_only:
            raise ValueError("Strategy Research Workspace Display paper must remain display-contract-only")
        if (
            self.rendered_now
            or self.paper_ingested
            or self.paper_parsed
            or self.method_extracted
            or self.strategy_extracted
            or self.code_generated
            or self.backtest_generated
            or self.recommendation_generated
        ):
            raise ValueError("Strategy Research Workspace Display paper dangerous flags must be false")
        return self


def default_strategy_research_workspace_display_paper_placeholders() -> list[
    StrategyResearchWorkspaceDisplayPaperPlaceholder
]:
    return [
        StrategyResearchWorkspaceDisplayPaperPlaceholder(
            paper_reference_id="strategy-research-display-arxiv-reference-placeholder-v1",
            paper_kind=StrategyResearchWorkspaceDisplayPaperKind.ARXIV_REFERENCE_VISUAL_PLACEHOLDER,
            title="ArXiv Reference Visual Placeholder",
            source="reference-placeholder-only",
            notes=["No arXiv ingestion, PDF parsing, method extraction, or strategy extraction."],
        ),
        StrategyResearchWorkspaceDisplayPaperPlaceholder(
            paper_reference_id="strategy-research-display-doi-reference-placeholder-v1",
            paper_kind=StrategyResearchWorkspaceDisplayPaperKind.DOI_REFERENCE_VISUAL_PLACEHOLDER,
            title="DOI Reference Visual Placeholder",
            source="reference-placeholder-only",
        ),
        StrategyResearchWorkspaceDisplayPaperPlaceholder(
            paper_reference_id="strategy-research-display-method-summary-placeholder-v1",
            paper_kind=StrategyResearchWorkspaceDisplayPaperKind.METHOD_SUMMARY_VISUAL_PLACEHOLDER,
            title="Method Summary Visual Placeholder",
            source="summary-placeholder-only",
        ),
    ]
