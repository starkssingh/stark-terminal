from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone

import polars as pl
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from stark_terminal_core.domain.enums import Timeframe
from stark_terminal_data_platform.db.models.timeseries import OHLCVBarORM
from stark_terminal_data_platform.exports.synthetic_ohlcv import (
    SyntheticOHLCVResearchLakeExportService,
    create_synthetic_ohlcv_export_request,
)
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.lake.parquet_io import read_parquet_frame
from stark_terminal_data_platform.repositories.ohlcv_bars import OHLCVBarRepository
from stark_terminal_data_platform.services.synthetic_ohlcv_storage import SyntheticOHLCVStorageService

import pytest


@pytest.fixture()
def db_session() -> Iterator[Session]:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    OHLCVBarORM.__table__.create(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def _export_result(db_session: Session, tmp_path):
    instrument = create_sample_instruments()[0]
    batch = generate_synthetic_market_data_batch(
        SyntheticOHLCVConfig(
            instrument_id=instrument.instrument_id,
            timeframe=Timeframe.DAILY,
            start_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            bar_count=4,
            start_price=100.0,
            source_data_reference="synthetic-local-test-only",
        )
    )
    repository = OHLCVBarRepository(db_session)
    SyntheticOHLCVStorageService(repository).store_synthetic_batch(batch)
    request = create_synthetic_ohlcv_export_request(
        export_id="synthetic_ohlcv_export_parquet",
        instrument_id=batch.bars[0].instrument_id,
        timeframe=batch.bars[0].timeframe,
        dataset_name="synthetic_ohlcv_parquet",
        source_data_reference="synthetic-local-test-only",
    )
    service = SyntheticOHLCVResearchLakeExportService(repository)
    return service, service.export_bars_to_parquet(request, output_root=tmp_path)


def test_exported_parquet_schema_and_row_count(db_session: Session, tmp_path) -> None:
    _service, result = _export_result(db_session, tmp_path)
    output_path = result.output_path
    assert output_path is not None
    frame = read_parquet_frame(output_path)

    assert frame.height == 4
    assert set(
        [
            "instrument_id",
            "symbol",
            "exchange",
            "segment",
            "timeframe",
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "open_interest",
            "provider",
            "source_data_reference",
        ]
    ).issubset(set(frame.columns))
    assert all(str(path_part) not in output_path for path_part in [".."])
    assert str(tmp_path) in output_path


def test_duckdb_reads_exported_parquet(db_session: Session, tmp_path) -> None:
    service, result = _export_result(db_session, tmp_path)
    frame = service.read_export_with_duckdb(result.output_path)

    assert isinstance(frame, pl.DataFrame)
    assert frame.height == result.row_count
    assert frame["source_data_reference"].to_list() == ["synthetic-local-test-only"] * result.row_count
