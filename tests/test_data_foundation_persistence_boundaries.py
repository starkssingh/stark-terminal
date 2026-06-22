from pathlib import Path

from stark_terminal_data_platform.db.models.instrument import InstrumentORM
from stark_terminal_data_platform.db.models.market_data_batch import MarketDataBatchRecordORM


ROOT = Path(__file__).resolve().parents[1]

FULL_BAR_COLUMNS = {"open", "high", "low", "close", "volume", "open_interest", "bar_payload", "bars_json"}


def test_instrument_metadata_table_does_not_store_bars() -> None:
    column_names = set(InstrumentORM.__table__.columns.keys())

    assert FULL_BAR_COLUMNS.isdisjoint(column_names)


def test_market_data_batch_records_do_not_store_full_bars() -> None:
    column_names = set(MarketDataBatchRecordORM.__table__.columns.keys())

    assert FULL_BAR_COLUMNS.isdisjoint(column_names)
    assert "row_count" in column_names
    assert "source_data_reference" in column_names
    assert "synthetic" in column_names


def test_batch_metadata_docs_and_timeseries_docs_preserve_boundary() -> None:
    docs = "\n".join(
        [
            (ROOT / "docs/MARKET_DATA_BATCH_PERSISTENCE.md").read_text(encoding="utf-8"),
            (ROOT / "docs/BATCH_METADATA_POLICY.md").read_text(encoding="utf-8"),
            (ROOT / "docs/TIMESERIES_SCHEMA.md").read_text(encoding="utf-8"),
            (ROOT / "docs/DATA_PERSISTENCE_BOUNDARY.md").read_text(encoding="utf-8"),
        ]
    )

    for phrase in [
        "metadata-only",
        "no full OHLCV",
        "TimescaleDB",
        "future operational",
        "No store currently receives real market data",
    ]:
        assert phrase in docs


def test_prompt_14_to_16_services_do_not_write_other_stores_or_publish_events() -> None:
    service_text = "\n".join(
        [
            (ROOT / "packages/data_platform/stark_terminal_data_platform/services/instruments.py").read_text(
                encoding="utf-8"
            ),
            (
                ROOT / "packages/data_platform/stark_terminal_data_platform/services/market_data_batches.py"
            ).read_text(encoding="utf-8"),
            (ROOT / "packages/data_platform/stark_terminal_data_platform/repositories/instruments.py").read_text(
                encoding="utf-8"
            ),
            (
                ROOT / "packages/data_platform/stark_terminal_data_platform/repositories/market_data_batches.py"
            ).read_text(encoding="utf-8"),
        ]
    )

    forbidden = [
        "OHLCVBarORM",
        "ClickHouse",
        "DuckDB",
        "Redis",
        "Kafka",
        "publish(",
        "write_fixture_bars_to_parquet",
        "write_parquet",
        "to_parquet",
    ]

    for phrase in forbidden:
        assert phrase not in service_text
