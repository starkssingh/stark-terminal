from pathlib import Path

import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import DataLakeZone
from stark_terminal_data_platform.lake.paths import (
    dataset_path,
    ensure_lake_dirs,
    safe_relative_path,
    zone_path,
)
from stark_terminal_data_platform.lake.zones import CANONICAL_LAKE_ZONES, ZONE_DIRECTORY_NAMES, normalize_zone


def temp_settings(tmp_path: Path) -> Settings:
    return Settings(
        lake_root=str(tmp_path / "lake"),
        parquet_root=str(tmp_path / "parquet"),
        research_artifacts_root=str(tmp_path / "research_artifacts"),
        duckdb_database_path=str(tmp_path / "lake" / "stark.duckdb"),
    )


def test_canonical_zones_are_present() -> None:
    assert set(CANONICAL_LAKE_ZONES) == {
        DataLakeZone.RAW,
        DataLakeZone.CLEANED,
        DataLakeZone.NORMALIZED,
        DataLakeZone.FEATURE_READY,
        DataLakeZone.BACKTEST_READY,
        DataLakeZone.RESEARCH_ARTIFACTS,
    }
    assert ZONE_DIRECTORY_NAMES[DataLakeZone.FEATURE_READY] == "feature_ready"
    assert normalize_zone("backtest_ready") == DataLakeZone.BACKTEST_READY


def test_zone_path_returns_path(tmp_path: Path) -> None:
    settings = temp_settings(tmp_path)

    path = zone_path(DataLakeZone.RAW, settings)

    assert isinstance(path, Path)
    assert path == tmp_path / "parquet" / "raw"


def test_dataset_path_supports_version_and_partitions(tmp_path: Path) -> None:
    settings = temp_settings(tmp_path)

    path = dataset_path(
        DataLakeZone.NORMALIZED,
        "nifty_bars",
        version="v1",
        partition_parts={"exchange": "NSE", "timeframe": "1D"},
        settings=settings,
    )

    assert path == tmp_path / "parquet" / "normalized" / "nifty_bars" / "v1" / "exchange=NSE" / "timeframe=1D"


@pytest.mark.parametrize("dataset_name", ["", "../escape", "/absolute"])
def test_dataset_path_rejects_unsafe_dataset_names(tmp_path: Path, dataset_name: str) -> None:
    with pytest.raises(ValueError):
        dataset_path(DataLakeZone.RAW, dataset_name, settings=temp_settings(tmp_path))


def test_ensure_lake_dirs_creates_expected_dirs_only_when_called(tmp_path: Path) -> None:
    settings = temp_settings(tmp_path)
    assert not (tmp_path / "parquet").exists()

    created = ensure_lake_dirs(settings)

    assert (tmp_path / "parquet" / "raw").exists()
    assert (tmp_path / "research_artifacts").exists()
    assert (tmp_path / "lake").exists()
    assert tmp_path / "parquet" / "raw" in created


def test_safe_relative_path_rejects_outside_root(tmp_path: Path) -> None:
    inside = tmp_path / "lake" / "file.parquet"
    outside = tmp_path / "other" / "file.parquet"

    assert safe_relative_path(inside, tmp_path / "lake") == "file.parquet"
    with pytest.raises(ValueError):
        safe_relative_path(outside, tmp_path / "lake")
