from __future__ import annotations

import re
import tomllib

from pydantic import BaseModel, Field, field_validator, model_validator


BLOCKED_REGIME_FEATURE_DEPENDENCIES = [
    "numpy",
    "scipy",
    "statsmodels",
    "scikit-learn",
    "sklearn",
    "hmmlearn",
    "ruptures",
    "torch",
    "tensorflow",
    "xgboost",
    "lightgbm",
    "catboost",
    "ta-lib",
    "vectorbt",
    "backtrader",
]


class RegimeFeatureDependencyPlan(BaseModel):
    plan_id: str = "regime-feature-dependency-plan-v1"
    current_stage: str = "contracts_only"
    allowed_now: list[str] = Field(default_factory=list)
    blocked_now: list[str] = Field(default_factory=list)
    heavy_dependencies_blocked: bool = True
    feature_computation_allowed: bool = False
    schema_version: str = "v1"

    @field_validator("plan_id", "current_stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("regime feature dependency plan text fields cannot be empty")
        return normalized

    @model_validator(mode="after")
    def plan_must_block_feature_computation(self) -> RegimeFeatureDependencyPlan:
        if self.feature_computation_allowed:
            raise ValueError("feature computation dependencies are forbidden in Prompt 34")
        if not self.heavy_dependencies_blocked:
            raise ValueError("heavy dependencies must remain blocked in Prompt 34")
        return self


def default_regime_feature_dependency_plan() -> RegimeFeatureDependencyPlan:
    return RegimeFeatureDependencyPlan(
        allowed_now=[
            "standard-library",
            "datetime",
            "pydantic",
            "fastapi",
            "existing-project-packages",
        ],
        blocked_now=BLOCKED_REGIME_FEATURE_DEPENDENCIES.copy(),
    )


def regime_feature_dependency_allowed_now(name: str) -> bool:
    normalized = name.strip().lower().replace("_", "-")
    if not normalized:
        return False
    gate = default_regime_feature_dependency_plan()
    return normalized in {item.lower() for item in gate.allowed_now} and normalized not in set(gate.blocked_now)


def _dependency_names_from_pyproject(pyproject_text: str) -> set[str]:
    try:
        data = tomllib.loads(pyproject_text)
    except tomllib.TOMLDecodeError:
        return {
            match.group(1).lower()
            for match in re.finditer(r'["\']([A-Za-z0-9_.-]+)(?:\[|[<>=!~]|["\'])', pyproject_text)
        }
    dependencies = data.get("project", {}).get("dependencies", [])
    names: set[str] = set()
    for dependency in dependencies:
        normalized = (
            dependency.split("[", 1)[0]
            .split(">", 1)[0]
            .split("=", 1)[0]
            .split("<", 1)[0]
            .split("!", 1)[0]
            .split("~", 1)[0]
            .strip()
            .lower()
        )
        if normalized:
            names.add(normalized)
    return names


def assert_no_blocked_regime_feature_dependencies_added(pyproject_text: str) -> list[str]:
    dependencies = _dependency_names_from_pyproject(pyproject_text)
    aliases = {
        "scikit-learn": "sklearn",
        "tensorflow-cpu": "tensorflow",
        "tensorflow-macos": "tensorflow",
        "pytorch": "torch",
        "ta_lib": "ta-lib",
    }
    normalized = {aliases.get(name, name) for name in dependencies}
    return sorted(normalized & set(default_regime_feature_dependency_plan().blocked_now))
