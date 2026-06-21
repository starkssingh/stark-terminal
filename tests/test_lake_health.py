from pathlib import Path

from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.lake.health import check_research_lake_health


def temp_settings(tmp_path: Path, create_lake_dirs: bool = False) -> Settings:
    return Settings(
        lake_root=str(tmp_path / "lake"),
        parquet_root=str(tmp_path / "parquet"),
        research_artifacts_root=str(tmp_path / "research_artifacts"),
        duckdb_database_path=str(tmp_path / "lake" / "research.duckdb"),
        create_lake_dirs=create_lake_dirs,
    )


def test_research_lake_health_does_not_create_dirs_by_default(tmp_path: Path) -> None:
    settings = temp_settings(tmp_path)

    status = check_research_lake_health(settings)

    assert status.configured is True
    assert status.lake_root_exists is False
    assert status.parquet_root_exists is False
    assert status.duckdb_available is True
    assert status.parquet_engine_available is True
    assert not (tmp_path / "lake").exists()


def test_research_lake_health_create_dirs_true_creates_expected_dirs(tmp_path: Path) -> None:
    settings = temp_settings(tmp_path)

    status = check_research_lake_health(settings, create_dirs=True)

    assert status.lake_root_exists is True
    assert status.parquet_root_exists is True
    assert status.research_artifacts_root_exists is True
    assert status.zones["raw"] is True
    assert (tmp_path / "lake").exists()


def test_research_lake_health_reports_zone_statuses(tmp_path: Path) -> None:
    status = check_research_lake_health(temp_settings(tmp_path))

    assert set(status.zones) == {
        "raw",
        "cleaned",
        "normalized",
        "feature_ready",
        "backtest_ready",
        "research_artifacts",
    }
