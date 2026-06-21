from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.market_data import MarketDataBar, MarketDataBatch
from stark_terminal_data_platform.db.models.market_data_batch import MarketDataBatchRecordORM
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.repositories.market_data_batches import MarketDataBatchRepository
from stark_terminal_data_platform.services.market_data_batches import (
    MarketDataBatchMetadataService,
    MarketDataBatchPersistenceError,
    MarketDataBatchValidationError,
)


@pytest.fixture()
def db_session() -> Iterator[Session]:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    MarketDataBatchRecordORM.__table__.create(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def _batch() -> MarketDataBatch:
    instrument = create_sample_instruments()[0]
    return generate_synthetic_market_data_batch(
        SyntheticOHLCVConfig(
            instrument_id=instrument.instrument_id,
            timeframe="DAILY",
            start_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            bar_count=5,
            start_price=100.0,
            source_data_reference="synthetic-local-test-only",
        )
    )


def _service(session: Session, settings: Settings | None = None) -> MarketDataBatchMetadataService:
    return MarketDataBatchMetadataService(MarketDataBatchRepository(session), settings=settings or Settings())


def test_service_creates_and_persists_synthetic_batch_metadata(db_session: Session) -> None:
    service = _service(db_session)
    batch = _batch()

    metadata = service.create_metadata_from_batch(batch, synthetic=True, fixture_id="fixture_1")
    result = service.persist_synthetic_batch_metadata(batch, fixture_id="fixture_1")

    assert metadata.row_count == len(batch.bars)
    assert result.persisted is True
    assert result.row_count == len(batch.bars)
    assert service.repository.count() == 1
    assert service.get_metadata(result.batch_id) is not None
    assert service.health().stores_full_bars is False


def test_service_list_by_instrument_delegates(db_session: Session) -> None:
    service = _service(db_session)
    result = service.persist_synthetic_batch_metadata(_batch(), fixture_id="fixture_1")
    metadata = service.get_metadata(result.batch_id)

    assert metadata is not None
    assert service.list_metadata()[0].batch_id == result.batch_id
    assert service.list_by_instrument(metadata.instrument_id)[0].batch_id == result.batch_id


def test_service_rejects_invalid_batch_before_persistence(db_session: Session) -> None:
    service = _service(db_session)
    batch = _batch()
    bad_bar = MarketDataBar.model_construct(**{**batch.bars[0].model_dump(), "high": 1.0})
    invalid_batch = MarketDataBatch.model_construct(bars=[bad_bar], provider=batch.provider, quality_status=batch.quality_status)

    with pytest.raises(MarketDataBatchValidationError):
        service.persist_synthetic_batch_metadata(invalid_batch, fixture_id="fixture_bad")

    assert service.repository.count() == 0


def test_service_respects_synthetic_allowed_and_enabled_settings(db_session: Session) -> None:
    synthetic_disabled = _service(db_session, Settings(market_data_batch_persistence_allow_synthetic=False))
    with pytest.raises(MarketDataBatchPersistenceError):
        synthetic_disabled.persist_synthetic_batch_metadata(_batch(), fixture_id="fixture_1")

    disabled = _service(db_session, Settings(market_data_batch_persistence_enabled=False))
    with pytest.raises(MarketDataBatchPersistenceError):
        disabled.persist_synthetic_batch_metadata(_batch(), fixture_id="fixture_1")


def test_service_health_fails_safely_when_table_unavailable() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    session = SessionLocal()
    try:
        status = _service(session).health()
    finally:
        session.close()
        engine.dispose()

    assert status.repository_reachable is False
    assert status.stores_full_bars is False
    assert status.error == "MarketDataBatchMetadataRepositoryUnavailable"
