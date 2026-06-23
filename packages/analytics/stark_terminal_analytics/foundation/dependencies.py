from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_analytics.foundation.contracts import sanitize_analytics_notes


class AnalyticsDependencyStage(StrEnum):
    CONTRACTS_ONLY = "CONTRACTS_ONLY"
    NUMERICAL_CORE = "NUMERICAL_CORE"
    STATISTICAL_MODELS = "STATISTICAL_MODELS"
    ML_MODELS = "ML_MODELS"
    GPU_ACCELERATION = "GPU_ACCELERATION"
    UNKNOWN = "UNKNOWN"


class AnalyticsDependency(BaseModel):
    name: str
    category: str
    stage: AnalyticsDependencyStage
    required_now: bool = False
    planned_for_prompt: str | None = None
    reason: str
    heavy: bool = False
    optional: bool = True

    @field_validator("name", "category", "reason")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("analytics dependency text fields cannot be empty")
        return normalized

    @model_validator(mode="after")
    def heavy_dependencies_are_not_required_now(self) -> AnalyticsDependency:
        if self.heavy and self.required_now:
            raise ValueError("heavy analytics dependencies cannot be required in Prompt 26")
        return self


class AnalyticsDependencyPlan(BaseModel):
    plan_id: str
    schema_version: str = "v1"
    dependencies: list[AnalyticsDependency]
    current_stage: AnalyticsDependencyStage = AnalyticsDependencyStage.CONTRACTS_ONLY
    notes: list[str] = Field(default_factory=list)

    @field_validator("plan_id", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("analytics dependency plan text fields cannot be empty")
        return normalized

    @field_validator("dependencies")
    @classmethod
    def dependencies_must_be_present(
        cls,
        value: list[AnalyticsDependency],
    ) -> list[AnalyticsDependency]:
        if not value:
            raise ValueError("analytics dependency plan cannot be empty")
        return value

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_analytics_notes(value)

    @model_validator(mode="after")
    def prompt_26_stage_must_be_contracts_only(self) -> AnalyticsDependencyPlan:
        if self.current_stage != AnalyticsDependencyStage.CONTRACTS_ONLY:
            raise ValueError("Prompt 26 dependency stage must remain CONTRACTS_ONLY")
        return self


def _dependency(
    name: str,
    category: str,
    stage: AnalyticsDependencyStage,
    planned_for_prompt: str,
    reason: str,
    heavy: bool,
) -> AnalyticsDependency:
    return AnalyticsDependency(
        name=name,
        category=category,
        stage=stage,
        planned_for_prompt=planned_for_prompt,
        reason=reason,
        heavy=heavy,
        required_now=False,
        optional=True,
    )


def default_analytics_dependency_plan() -> AnalyticsDependencyPlan:
    dependencies = [
        _dependency("NumPy", "numerical", AnalyticsDependencyStage.NUMERICAL_CORE, "Prompt 27+", "Future array math baseline.", True),
        _dependency("SciPy", "numerical", AnalyticsDependencyStage.STATISTICAL_MODELS, "Prompt 31+", "Future scientific/statistical routines.", True),
        _dependency("pandas", "tabular", AnalyticsDependencyStage.NUMERICAL_CORE, "future evaluation", "Future compatibility with tabular research workflows.", True),
        _dependency("Polars", "tabular", AnalyticsDependencyStage.NUMERICAL_CORE, "already available for data IO", "Existing project dependency, but not required for Prompt 26 calculations.", False),
        _dependency("Numba", "performance", AnalyticsDependencyStage.NUMERICAL_CORE, "future evaluation", "Future acceleration candidate.", True),
        _dependency("JAX", "ml/gpu", AnalyticsDependencyStage.GPU_ACCELERATION, "future evaluation", "Future differentiable/GPU analytics candidate.", True),
        _dependency("CuPy", "gpu", AnalyticsDependencyStage.GPU_ACCELERATION, "future evaluation", "Future GPU array candidate.", True),
        _dependency("statsmodels", "statistical", AnalyticsDependencyStage.STATISTICAL_MODELS, "future evaluation", "Future statistical model candidate.", True),
        _dependency("arch", "statistical", AnalyticsDependencyStage.STATISTICAL_MODELS, "future evaluation", "Future volatility model candidate.", True),
        _dependency("scikit-learn", "ml", AnalyticsDependencyStage.ML_MODELS, "future evaluation", "Future ML baseline candidate.", True),
        _dependency("XGBoost", "ml", AnalyticsDependencyStage.ML_MODELS, "future evaluation", "Future gradient boosting candidate.", True),
        _dependency("LightGBM", "ml", AnalyticsDependencyStage.ML_MODELS, "future evaluation", "Future gradient boosting candidate.", True),
        _dependency("CatBoost", "ml", AnalyticsDependencyStage.ML_MODELS, "future evaluation", "Future gradient boosting candidate.", True),
        _dependency("PyTorch", "ml", AnalyticsDependencyStage.ML_MODELS, "future evaluation", "Future deep learning candidate.", True),
        _dependency("TensorFlow", "ml", AnalyticsDependencyStage.ML_MODELS, "future evaluation", "Future deep learning candidate.", True),
        _dependency("QuantLib", "options", AnalyticsDependencyStage.STATISTICAL_MODELS, "future options phase", "Future options analytics candidate.", True),
        _dependency("vectorbt", "backtesting", AnalyticsDependencyStage.STATISTICAL_MODELS, "future evaluation", "Future backtesting reference candidate.", True),
        _dependency("backtrader", "backtesting", AnalyticsDependencyStage.STATISTICAL_MODELS, "future evaluation", "Future backtesting reference candidate.", True),
    ]
    return AnalyticsDependencyPlan(
        plan_id="analytics_dependency_staging_v1",
        dependencies=dependencies,
        notes=[
            "Prompt 26 is contracts-only.",
            "Heavy numerical, statistical, ML, GPU, options, and backtesting dependencies are planned, not required now.",
        ],
    )


def list_blocked_heavy_dependencies_for_prompt_26() -> list[str]:
    return [
        dependency.name
        for dependency in default_analytics_dependency_plan().dependencies
        if dependency.heavy
    ]


def dependency_is_allowed_now(name: str) -> bool:
    normalized = name.strip().lower()
    if not normalized:
        return False
    blocked = {dependency.lower() for dependency in list_blocked_heavy_dependencies_for_prompt_26()}
    return normalized not in blocked and normalized in {"standard library", "pydantic", "fastapi", "polars"}
