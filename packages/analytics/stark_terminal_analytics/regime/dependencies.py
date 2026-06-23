from __future__ import annotations

import re
import tomllib

from pydantic import BaseModel, Field, field_validator


BLOCKED_REGIME_DEPENDENCIES = [
    "statsmodels",
    "scipy",
    "numpy",
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


class RegimeDependencyPlan(BaseModel):
    plan_id: str = "regime-dependency-plan-v1"
    current_stage: str = "planning_only"
    allowed_now: list[str] = Field(default_factory=list)
    blocked_now: list[str] = Field(default_factory=list)
    heavy_dependencies_blocked: bool = True
    schema_version: str = "v1"

    @field_validator("plan_id", "current_stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("regime dependency plan text fields cannot be empty")
        return normalized


def default_regime_dependency_plan() -> RegimeDependencyPlan:
    return RegimeDependencyPlan(
        allowed_now=[
            "standard-library",
            "datetime",
            "pydantic",
            "fastapi",
            "existing-project-packages",
        ],
        blocked_now=BLOCKED_REGIME_DEPENDENCIES.copy(),
    )


def regime_dependency_allowed_now(name: str) -> bool:
    normalized = name.strip().lower().replace("_", "-")
    if not normalized:
        return False
    gate = default_regime_dependency_plan()
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


def assert_no_blocked_regime_dependencies_added(pyproject_text: str) -> list[str]:
    dependencies = _dependency_names_from_pyproject(pyproject_text)
    aliases = {
        "scikit-learn": "sklearn",
        "tensorflow-cpu": "tensorflow",
        "tensorflow-macos": "tensorflow",
        "pytorch": "torch",
        "ta_lib": "ta-lib",
    }
    normalized = {aliases.get(name, name) for name in dependencies}
    return sorted(normalized & set(default_regime_dependency_plan().blocked_now))
