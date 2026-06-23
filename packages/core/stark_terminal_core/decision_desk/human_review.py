from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.decision_desk.planning import _non_empty_text, sanitize_decision_notes


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class RetailHumanReviewRequirement(BaseModel):
    review_id: str
    title: str
    description: str
    required: bool = True
    reviewer_role: str = "human_operator"
    blocks_recommendations: bool = True
    blocks_decision_objects: bool = True
    blocks_execution: bool = True
    schema_version: str = "v1"

    @field_validator("review_id", "title", "description", "reviewer_role", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail human review requirement text fields")

    @model_validator(mode="after")
    def review_must_block_dangerous_outputs(self) -> RetailHumanReviewRequirement:
        if not self.blocks_recommendations:
            raise ValueError("human review must block recommendations in Prompt 36")
        if not self.blocks_decision_objects:
            raise ValueError("human review must block DecisionObjects in Prompt 36")
        if not self.blocks_execution:
            raise ValueError("human review must block execution in Prompt 36")
        return self


class RetailHumanReviewChecklist(BaseModel):
    checklist_id: str
    requirements: list[RetailHumanReviewRequirement]
    complete: bool = False
    recommendations_allowed: bool = False
    decision_objects_allowed: bool = False
    execution_allowed: bool = False
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("checklist_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        return _non_empty_text(value, "retail human review checklist text fields")

    @field_validator("requirements")
    @classmethod
    def requirements_must_be_present(
        cls,
        value: list[RetailHumanReviewRequirement],
    ) -> list[RetailHumanReviewRequirement]:
        if not value:
            raise ValueError("retail human review checklist requirements cannot be empty")
        return value

    @field_validator("blockers", "warnings")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_decision_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        return _utc_datetime(value)

    @model_validator(mode="after")
    def checklist_must_remain_blocking(self) -> RetailHumanReviewChecklist:
        if self.recommendations_allowed:
            raise ValueError("human review cannot allow recommendations in Prompt 36")
        if self.decision_objects_allowed:
            raise ValueError("human review cannot allow DecisionObjects in Prompt 36")
        if self.execution_allowed:
            raise ValueError("human review cannot allow execution in Prompt 36")
        if self.complete and self.blockers:
            raise ValueError("complete retail human review checklist cannot have blockers")
        return self


def default_retail_human_review_requirements() -> list[RetailHumanReviewRequirement]:
    return [
        RetailHumanReviewRequirement(
            review_id="retail-human-review-evidence-chain",
            title="Evidence Chain Review",
            description="Human operator must review the evidence chain before future Decision Desk outputs are allowed.",
        ),
        RetailHumanReviewRequirement(
            review_id="retail-human-review-risk-language",
            title="Risk Language Review",
            description="Human operator must verify that future display copy does not imply advice, certainty, or execution readiness.",
        ),
        RetailHumanReviewRequirement(
            review_id="retail-human-review-no-execution",
            title="Execution Boundary Review",
            description="Human operator must verify that no broker, order, or execution pathway exists.",
        ),
    ]


def build_retail_human_review_checklist(
    requirements: list[RetailHumanReviewRequirement] | None = None,
    completed_review_ids: set[str] | None = None,
    warnings: list[str] | None = None,
) -> RetailHumanReviewChecklist:
    resolved_requirements = requirements or default_retail_human_review_requirements()
    completed = completed_review_ids or set()
    blockers = [
        f"missing required human review: {requirement.review_id}"
        for requirement in resolved_requirements
        if requirement.required and requirement.review_id not in completed
    ]
    return RetailHumanReviewChecklist(
        checklist_id="retail-human-review-checklist-v1",
        requirements=resolved_requirements,
        complete=not blockers,
        blockers=blockers,
        warnings=warnings or [],
    )


def evaluate_retail_human_review_checklist(
    checklist: RetailHumanReviewChecklist,
) -> RetailHumanReviewChecklist:
    if checklist.complete:
        return checklist
    blockers = checklist.blockers or ["required retail human review remains incomplete"]
    return checklist.model_copy(update={"blockers": sanitize_decision_notes(blockers), "complete": False})
