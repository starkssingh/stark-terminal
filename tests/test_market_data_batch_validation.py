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
from stark_terminal_data_platform.quality.enums import ValidationStatus
from stark_terminal_data_platform.repositories.market_data_batches import MarketDataBatchRepository
from stark_terminal_data_platform.services.market_data_batches import MarketDataBatchMetadataService, MarketDataBatchValidationError


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


def test_generated_prompt_14_synthetic_batch_passes_validation(db_session: Session) -> None:
    service = MarketDataBatchMetadataService(MarketDataBatchRepository(db_session), settings=Settings())

    report = service.validate_batch(_batch())

    assert report.status == ValidationStatus.PASS
    assert report.source_data_reference == "synthetic-local-test-only"


def test_validation_failure_blocks_persistence(db_session: Session) -> None:
    service = MarketDataBatchMetadataService(MarketDataBatchRepository(db_session), settings=Settings())
    batch = _batch()
    bad_bar = MarketDataBar.model_construct(**{**batch.bars[0].model_dump(), "volume": -1.0})
    invalid_batch = MarketDataBatch.model_construct(bars=[bad_bar], provider=batch.provider, quality_status=batch.quality_status)

    with pytest.raises(MarketDataBatchValidationError):
        service.persist_synthetic_batch_metadata(invalid_batch)

    assert service.repository.count() == 0


def test_metadata_validation_rejects_bad_synthetic_reference(db_session: Session) -> None:
    service = MarketDataBatchMetadataService(MarketDataBatchRepository(db_session), settings=Settings())
    batch = _batch()
    bad_bar = MarketDataBar.model_construct(**{**batch.bars[0].model_dump(), "source_data_reference": "manual"})
    invalid_batch = MarketDataBatch.model_construct(bars=[bad_bar], provider=batch.provider, quality_status=batch.quality_status)

    with pytest.raises(Exception):
        service.persist_synthetic_batch_metadata(invalid_batch)
