"""DuckDB + Parquet research lake foundation."""

from stark_terminal_data_platform.lake.health import (
    ResearchLakeHealthStatus,
    check_research_lake_health,
)
from stark_terminal_data_platform.lake.paths import (
    LakePaths,
    build_lake_paths,
    dataset_path,
    ensure_lake_dirs,
    safe_relative_path,
    zone_path,
)

__all__ = [
    "LakePaths",
    "ResearchLakeHealthStatus",
    "build_lake_paths",
    "check_research_lake_health",
    "dataset_path",
    "ensure_lake_dirs",
    "safe_relative_path",
    "zone_path",
]
