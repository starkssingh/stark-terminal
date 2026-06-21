from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import DataLakeZone
from stark_terminal_data_platform.lake.zones import CANONICAL_LAKE_ZONES, ZONE_DIRECTORY_NAMES, normalize_zone


@dataclass(frozen=True)
class LakePaths:
    lake_root: Path
    parquet_root: Path
    research_artifacts_root: Path
    duckdb_database_path: Path


def _safe_component(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    path = Path(normalized)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field_name} must be relative and cannot contain traversal")
    return normalized


def build_lake_paths(settings: Settings | None = None) -> LakePaths:
    resolved_settings = settings or get_settings()
    return LakePaths(
        lake_root=Path(resolved_settings.lake_root),
        parquet_root=Path(resolved_settings.parquet_root),
        research_artifacts_root=Path(resolved_settings.research_artifacts_root),
        duckdb_database_path=Path(resolved_settings.duckdb_database_path),
    )


def zone_path(zone: DataLakeZone | str, settings: Settings | None = None) -> Path:
    paths = build_lake_paths(settings)
    normalized_zone = normalize_zone(zone)
    if normalized_zone == DataLakeZone.RESEARCH_ARTIFACTS:
        return paths.research_artifacts_root
    return paths.parquet_root / ZONE_DIRECTORY_NAMES[normalized_zone]


def _partition_parts_to_components(
    partition_parts: Sequence[str] | Mapping[str, str] | None,
) -> list[str]:
    if partition_parts is None:
        return []
    if isinstance(partition_parts, Mapping):
        return [
            _safe_component(f"{key}={value}", "partition_part")
            for key, value in partition_parts.items()
        ]
    return [_safe_component(part, "partition_part") for part in partition_parts]


def dataset_path(
    zone: DataLakeZone | str,
    dataset_name: str,
    version: str | None = None,
    partition_parts: Sequence[str] | Mapping[str, str] | None = None,
    settings: Settings | None = None,
) -> Path:
    safe_dataset_name = _safe_component(dataset_name, "dataset_name")
    path = zone_path(zone, settings) / safe_dataset_name
    if version is not None:
        path = path / _safe_component(version, "version")
    for partition_part in _partition_parts_to_components(partition_parts):
        path = path / partition_part
    return path


def ensure_lake_dirs(settings: Settings | None = None) -> list[Path]:
    paths = build_lake_paths(settings)
    directories = [
        paths.lake_root,
        paths.parquet_root,
        paths.research_artifacts_root,
        *[zone_path(zone, settings) for zone in CANONICAL_LAKE_ZONES],
        paths.duckdb_database_path.parent,
    ]
    unique_directories = list(dict.fromkeys(directories))
    for directory in unique_directories:
        directory.mkdir(parents=True, exist_ok=True)
    return unique_directories


def safe_relative_path(path: Path | str, root: Path | str) -> str:
    resolved_path = Path(path).resolve(strict=False)
    resolved_root = Path(root).resolve(strict=False)
    try:
        return str(resolved_path.relative_to(resolved_root))
    except ValueError as exc:
        raise ValueError("path is outside the configured root") from exc
