from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.strategy_research_workspace.planning import (
    StrategyResearchPaperReferenceKind,
    _non_empty_text,
    _utc_datetime,
    _utc_now,
    sanitize_strategy_research_notes,
)


class StrategyResearchPaperReferencePlaceholder(BaseModel):
    paper_reference_id: str
    paper_kind: StrategyResearchPaperReferenceKind
    title: str
    source: str | None = None
    planning_only: bool = True
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
        return _non_empty_text(value, "strategy research paper reference text fields")

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_strategy_research_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def paper_reference_must_remain_placeholder(self) -> StrategyResearchPaperReferencePlaceholder:
        if self.paper_kind == StrategyResearchPaperReferenceKind.UNKNOWN:
            raise ValueError("UNKNOWN Strategy Research paper reference kind is not allowed")
        if not self.planning_only:
            raise ValueError("Strategy Research paper reference must remain planning-only")
        forbidden = {
            "paper ingested": self.paper_ingested,
            "paper parsed": self.paper_parsed,
            "method extracted": self.method_extracted,
            "strategy extracted": self.strategy_extracted,
            "code generated": self.code_generated,
            "backtest generated": self.backtest_generated,
            "recommendation generated": self.recommendation_generated,
        }
        enabled = [name for name, value in forbidden.items() if value]
        if enabled:
            raise ValueError("Strategy Research paper reference cannot be: " + ", ".join(enabled))
        return self


def default_strategy_research_paper_reference_placeholders() -> list[StrategyResearchPaperReferencePlaceholder]:
    return [
        StrategyResearchPaperReferencePlaceholder(
            paper_reference_id="strategy-research-arxiv-reference-placeholder-v1",
            paper_kind=StrategyResearchPaperReferenceKind.ARXIV_REFERENCE_PLACEHOLDER,
            title="ArXiv Reference Placeholder",
            source=None,
            notes=["This is a reference placeholder only; no arXiv client or paper ingestion exists."],
        ),
        StrategyResearchPaperReferencePlaceholder(
            paper_reference_id="strategy-research-doi-reference-placeholder-v1",
            paper_kind=StrategyResearchPaperReferenceKind.DOI_REFERENCE_PLACEHOLDER,
            title="DOI Reference Placeholder",
            source=None,
            notes=["This is a reference placeholder only; no DOI lookup or method extraction exists."],
        ),
        StrategyResearchPaperReferencePlaceholder(
            paper_reference_id="strategy-research-method-summary-placeholder-v1",
            paper_kind=StrategyResearchPaperReferenceKind.METHOD_SUMMARY_PLACEHOLDER,
            title="Method Summary Placeholder",
            source=None,
            notes=["No method summary is extracted or interpreted as a strategy."],
        ),
    ]
