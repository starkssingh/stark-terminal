from __future__ import annotations

import re
import tomllib

from pydantic import BaseModel, Field, field_validator


BLOCKED_NUMERICAL_DEPENDENCIES = [
    "numpy",
    "scipy",
    "numba",
    "jax",
    "cupy",
    "torch",
    "tensorflow",
    "statsmodels",
    "arch",
    "ta-lib",
    "vectorbt",
    "backtrader",
    "quantlib",
    "xgboost",
    "lightgbm",
    "catboost",
    "scikit-learn",
]


class NumericalDependencyGate(BaseModel):
    stage: str = "contracts_and_safe_stdlib"
    allowed_now: list[str] = Field(default_factory=list)
    blocked_now: list[str] = Field(default_factory=list)
    heavy_dependencies_blocked: bool = True
    schema_version: str = "v1"

    @field_validator("stage", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("numerical dependency gate text fields cannot be empty")
        return normalized


def default_numerical_dependency_gate() -> NumericalDependencyGate:
    return NumericalDependencyGate(
        allowed_now=[
            "standard-library",
            "math",
            "statistics",
            "pydantic",
            "fastapi",
            "existing-project-packages",
            "polars-existing-data-io",
            "pyarrow-existing-data-io",
            "duckdb-existing-data-io",
        ],
        blocked_now=BLOCKED_NUMERICAL_DEPENDENCIES.copy(),
    )


def numerical_dependency_allowed_now(name: str) -> bool:
    normalized = name.strip().lower().replace("_", "-")
    if not normalized:
        return False
    blocked = set(default_numerical_dependency_gate().blocked_now)
    allowed = {item.lower() for item in default_numerical_dependency_gate().allowed_now}
    return normalized not in blocked and normalized in allowed


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


def assert_no_blocked_numerical_dependencies_added(pyproject_text: str) -> list[str]:
    dependencies = _dependency_names_from_pyproject(pyproject_text)
    blocked = set(default_numerical_dependency_gate().blocked_now)
    aliases = {
        "pytorch": "torch",
        "tensorflow-cpu": "tensorflow",
        "tensorflow-macos": "tensorflow",
        "quantlib-python": "quantlib",
        "ta_lib": "ta-lib",
    }
    normalized = {aliases.get(name, name) for name in dependencies}
    return sorted(normalized & blocked)
