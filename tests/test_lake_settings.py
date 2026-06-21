from pydantic import ValidationError
import pytest

from stark_terminal_core.config.settings import Settings


def test_lake_settings_defaults_are_valid() -> None:
    settings = Settings()

    assert settings.lake_root == "data/lake"
    assert settings.duckdb_database_path == "data/lake/stark_terminal.duckdb"
    assert settings.duckdb_read_only is False
    assert settings.parquet_compression == "zstd"
    assert settings.create_lake_dirs is False


def test_lake_safe_snapshot_includes_safe_fields_and_excludes_urls() -> None:
    settings = Settings(
        database_url="postgresql+psycopg://user:secret@localhost/stark",
        timescale_database_url="postgresql+psycopg://user:secret@localhost/ts",
        redis_url="redis://:secret@localhost:6379",
        clickhouse_url="http://secret@localhost:8123",
        kafka_bootstrap_servers="secret-host:9092",
    )

    snapshot = settings.safe_settings_snapshot()

    assert snapshot["lake_root"] == "data/lake"
    assert snapshot["parquet_root"] == "data/parquet"
    assert snapshot["research_artifacts_root"] == "data/research_artifacts"
    assert snapshot["duckdb_database_configured"] is True
    assert snapshot["parquet_compression"] == "zstd"
    assert snapshot["create_lake_dirs"] is False
    for raw_key in [
        "database_url",
        "timescale_database_url",
        "redis_url",
        "clickhouse_url",
        "kafka_bootstrap_servers",
    ]:
        assert raw_key not in snapshot


@pytest.mark.parametrize("compression", ["brotli", "", "zip"])
def test_invalid_parquet_compression_rejected(compression: str) -> None:
    with pytest.raises(ValidationError):
        Settings(parquet_compression=compression)


@pytest.mark.parametrize("field", ["lake_root", "duckdb_database_path", "parquet_root"])
def test_empty_lake_path_settings_rejected(field: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: " "})
