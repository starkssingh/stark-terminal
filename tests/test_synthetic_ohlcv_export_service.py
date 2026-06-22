from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from stark_terminal_core.domain.enums import DatasetFormat, DatasetKind, Timeframe
from stark_terminal_data_platform.db.models.timeseries import OHLCVBarORM
from stark_terminal_data_platform.exports.synthetic_ohlcv import (
    SyntheticOHLCVResearchLakeExportService,
    create_synthetic_ohlcv_export_request,
)
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
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


def _batch(bar_count: int = 5):
    instrument = create_sample_instruments()[0]
    return generate_synthetic_market_data_batch(
        SyntheticOHLCVConfig(
            instrument_id=instrument.instrument_id,
            timeframe=Timeframe.DAILY,
            start_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            bar_count=bar_count,
            start_price=100.0,
            source_data_reference="synthetic-local-test-only",
        )
    )


def test_export_service_exports_stored_synthetic_bars_to_tmp_parquet(db_session: Session, tmp_path) -> None:
    repository = OHLCVBarRepository(db_session)
    batch = _batch(5)
    SyntheticOHLCVStorageService(repository).store_synthetic_batch(
        batch,
        batch_id="batch_synthetic_reliance",
        fixture_id="fixture_reliance",
    )
    request = create_synthetic_ohlcv_export_request(
        export_id="synthetic_ohlcv_export_reliance_daily",
        instrument_id=batch.bars[0].instrument_id,
        timeframe=batch.bars[0].timeframe,
        dataset_name="synthetic_ohlcv_reliance_daily",
        source_data_reference="synthetic-local-test-only",
    )
    service = SyntheticOHLCVResearchLakeExportService(repository)

    result = service.export_bars_to_parquet(request, output_root=tmp_path)

    assert result.exported is True
    assert result.synthetic is True
    assert result.real_market_data is False
    assert result.row_count == 5
    assert result.dataset_manifest is not None
    assert result.dataset_manifest.kind == DatasetKind.OHLCV
    assert result.dataset_manifest.format == DatasetFormat.PARQUET
    assert result.dataset_manifest.row_count == 5
    assert result.output_path is not None
    assert tmp_path in (tmp_path / result.dataset_manifest.path).parents or result.output_path.startswith(str(tmp_path))


def test_export_service_creates_manifest_with_source_and_partitions(db_session: Session, tmp_path) -> None:
    repository = OHLCVBarRepository(db_session)
    batch = _batch(2)
    SyntheticOHLCVStorageService(repository).store_synthetic_batch(batch)
    request = create_synthetic_ohlcv_export_request(
        export_id="synthetic_ohlcv_export_reliance_manifest",
        instrument_id=batch.bars[0].instrument_id,
        timeframe=batch.bars[0].timeframe,
        dataset_name="synthetic_ohlcv_reliance_manifest",
        source_data_reference="synthetic-local-test-only",
    )

    result = SyntheticOHLCVResearchLakeExportService(repository).export_bars_to_parquet(request, output_root=tmp_path)

    manifest = result.dataset_manifest
    assert manifest is not None
    assert manifest.dataset_id == request.export_id
    assert manifest.name == request.dataset_name
    assert manifest.source_data_reference == "synthetic-local-test-only"
    assert {partition.key for partition in manifest.partitions} == {"exchange", "symbol", "timeframe"}
    assert not result.dataset_manifest.path.startswith("/")
