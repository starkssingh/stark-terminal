from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_timeseries_migration_exists() -> None:
    assert (ROOT / "alembic/versions/0002_operational_timeseries_tables.py").exists()


def test_timeseries_migration_references_expected_tables_and_timescale_sql() -> None:
    migration = (ROOT / "alembic/versions/0002_operational_timeseries_tables.py").read_text(
        encoding="utf-8"
    )

    for table_name in [
        "ohlcv_bars",
        "options_chain_snapshots",
        "futures_basis_snapshots",
        "market_state_snapshots",
        "regime_snapshots",
    ]:
        assert table_name in migration
    assert "CREATE EXTENSION IF NOT EXISTS timescaledb" in migration
    assert "create_hypertable" in migration
    assert "broker" not in migration.lower()
    assert "execution" not in migration.lower()
    assert "trading" not in migration.lower()
