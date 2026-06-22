from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone
import inspect

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import DataProviderType, Timeframe
from stark_terminal_core.domain.identifiers import DataProviderId
from stark_terminal_data_platform.db.models.timeseries import OHLCVBarORM
from stark_terminal_data_platform.exports.synthetic_ohlcv import (
    SyntheticOHLCVExportValidationError,
    SyntheticOHLCVResearchLakeExportService,
    create_synthetic_ohlcv_export_request,
)
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.repositories.ohlcv_bars import OHLCVBarRepository
from stark_terminal_data_platform.services.synthetic_ohlcv_storage import SyntheticOHLCVStorageService


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


def _batch(bar_count: int = 3):
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


def _request(batch):
    return create_synthetic_ohlcv_export_request(
        export_id="synthetic_ohlcv_export_validation",
        instrument_id=batch.bars[0].instrument_id,
        timeframe=batch.bars[0].timeframe,
        dataset_name="synthetic_ohlcv_validation",
        source_data_reference="synthetic-local-test-only",
    )


def test_export_with_no_bars_fails_safely(db_session: Session, tmp_path) -> None:
    batch = _batch(1)
    repository = OHLCVBarRepository(db_session)
    service = SyntheticOHLCVResearchLakeExportService(repository)

    with pytest.raises(SyntheticOHLCVExportValidationError) as exc_info:
        service.export_bars_to_parquet(_request(batch), output_root=tmp_path)

    assert exc_info.value.report.status == "FAIL"


def test_export_blocks_invalid_or_non_synthetic_bars(db_session: Session, tmp_path) -> None:
    batch = _batch(1)
    bad_bar = batch.bars[0].model_copy(update={"source_data_reference": "synthetic-local-test-only"})
    object.__setattr__(bad_bar, "low", -1.0)
    repository = OHLCVBarRepository(db_session)
    service = SyntheticOHLCVResearchLakeExportService(repository)

    assert service.validate_bars_for_export([bad_bar]).status == "FAIL"

    non_synthetic = batch.bars[0].model_copy(update={"source_data_reference": "local-test-only"})
    repository.upsert_bar(non_synthetic)
    db_session.commit()

    with pytest.raises(SyntheticOHLCVExportValidationError):
        service.export_bars_to_parquet(_request(batch), output_root=tmp_path)


def test_export_blocks_non_local_sample_provider_and_max_rows(db_session: Session, tmp_path) -> None:
    batch = _batch(3)
    manual_bar = batch.bars[0].model_copy(
        update={"provider": DataProviderId(name="manual_fixture", provider_type=DataProviderType.MANUAL)}
    )
    repository = OHLCVBarRepository(db_session)
    repository.upsert_bar(manual_bar)
    db_session.commit()

    with pytest.raises(SyntheticOHLCVExportValidationError):
        SyntheticOHLCVResearchLakeExportService(repository).export_bars_to_parquet(_request(batch), output_root=tmp_path)

    repository.delete_synthetic_bars("synthetic-local-test-only")
    SyntheticOHLCVStorageService(repository).store_synthetic_batch(batch)
    settings = Settings(synthetic_ohlcv_export_max_rows=2)
    with pytest.raises(SyntheticOHLCVExportValidationError):
        SyntheticOHLCVResearchLakeExportService(repository, settings=settings).export_bars_to_parquet(
            _request(batch),
            output_root=tmp_path,
        )


def test_export_service_does_not_publish_events_or_call_external_systems() -> None:
    source = inspect.getsource(SyntheticOHLCVResearchLakeExportService)
    forbidden_terms = ("EventBackboneProducer", "StreamProducer", "redis", "kafka", "clickhouse", "requests.")

    assert all(term not in source for term in forbidden_terms)
