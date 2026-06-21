from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine

from stark_terminal_data_platform.db.base import Base
from stark_terminal_data_platform.db.models.market_data_batch import MarketDataBatchRecordORM
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_core.domain.market_data_batch import metadata_from_batch
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments


ROOT = Path(__file__).resolve().parents[1]


def _metadata():
    instrument = create_sample_instruments()[0]
    batch = generate_synthetic_market_data_batch(
        SyntheticOHLCVConfig(
            instrument_id=instrument.instrument_id,
            timeframe="DAILY",
            start_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            bar_count=5,
            start_price=100.0,
            source_data_reference="synthetic-local-test-only",
        )
    )
    return metadata_from_batch(batch, synthetic=True, fixture_id="fixture_1")


def test_base_metadata_contains_market_data_batch_table() -> None:
    assert "market_data_batch_records" in Base.metadata.tables


def test_market_data_batch_orm_has_no_reserved_metadata_or_full_bar_columns() -> None:
    columns = set(MarketDataBatchRecordORM.__table__.columns.keys())

    assert "metadata" not in columns
    assert "notes_json" in columns
    for full_bar_column in {"open", "high", "low", "close", "volume", "open_interest"}:
        assert full_bar_column not in columns


def test_market_data_batch_orm_roundtrip() -> None:
    metadata = _metadata()
    orm = MarketDataBatchRecordORM.from_domain(metadata)
    roundtrip = orm.to_domain()

    assert roundtrip == metadata
    assert orm.batch_id == metadata.batch_id
    assert orm.synthetic is True


def test_market_data_batch_table_constraints_and_indexes() -> None:
    table = MarketDataBatchRecordORM.__table__
    constraint_names = {constraint.name for constraint in table.constraints}
    index_names = {index.name for index in table.indexes}

    assert "uq_market_data_batch_records_batch_id" in constraint_names
    assert "ix_market_data_batch_records_instrument_time_range" in index_names
    assert "ix_market_data_batch_records_synthetic_fixture" in index_names


def test_market_data_batch_table_can_be_created_in_sqlite() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    try:
        MarketDataBatchRecordORM.__table__.create(engine)
        assert "market_data_batch_records" in Base.metadata.tables
    finally:
        engine.dispose()


def test_alembic_0003_market_data_batch_metadata_exists() -> None:
    migration = ROOT / "alembic/versions/0003_market_data_batch_metadata.py"
    text = migration.read_text(encoding="utf-8")

    assert "market_data_batch_records" in text
    assert "uq_market_data_batch_records_batch_id" in text
    assert "ohlcv_bars" not in text
    assert "broker" not in text.lower()
