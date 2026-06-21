from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.lake.duckdb_client import DuckDBClient
from stark_terminal_data_platform.lake.paths import build_lake_paths, ensure_lake_dirs, zone_path
from stark_terminal_data_platform.lake.zones import CANONICAL_LAKE_ZONES, ZONE_DIRECTORY_NAMES


class ResearchLakeHealthStatus(BaseModel):
    configured: bool
    lake_root_exists: bool
    parquet_root_exists: bool
    research_artifacts_root_exists: bool
    duckdb_available: bool
    duckdb_reachable: bool
    parquet_engine_available: bool
    zones: dict[str, bool]
    error: str | None = None


def check_research_lake_health(
    settings: Settings | None = None,
    create_dirs: bool | None = None,
) -> ResearchLakeHealthStatus:
    resolved_settings = settings or get_settings()
    should_create_dirs = resolved_settings.create_lake_dirs if create_dirs is None else create_dirs
    error: str | None = None

    if should_create_dirs:
        try:
            ensure_lake_dirs(resolved_settings)
        except Exception as exc:
            error = exc.__class__.__name__

    paths = build_lake_paths(resolved_settings)
    zones = {
        ZONE_DIRECTORY_NAMES[zone]: zone_path(zone, resolved_settings).exists()
        for zone in CANONICAL_LAKE_ZONES
    }

    duckdb_available = True
    duckdb_reachable = False
    duckdb_health_path = paths.duckdb_database_path if should_create_dirs else ":memory:"
    try:
        with DuckDBClient(duckdb_health_path, read_only=resolved_settings.duckdb_read_only) as client:
            client.execute("SELECT 1")
            duckdb_reachable = True
    except Exception as exc:
        duckdb_reachable = False
        error = error or exc.__class__.__name__

    try:
        import pyarrow.parquet  # noqa: F401

        parquet_engine_available = True
    except Exception as exc:
        parquet_engine_available = False
        error = error or exc.__class__.__name__

    return ResearchLakeHealthStatus(
        configured=bool(resolved_settings.lake_root and resolved_settings.parquet_root),
        lake_root_exists=paths.lake_root.exists(),
        parquet_root_exists=paths.parquet_root.exists(),
        research_artifacts_root_exists=paths.research_artifacts_root.exists(),
        duckdb_available=duckdb_available,
        duckdb_reachable=duckdb_reachable,
        parquet_engine_available=parquet_engine_available,
        zones=zones,
        error=error,
    )
