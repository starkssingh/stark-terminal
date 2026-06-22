from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from stark_terminal_core.domain.enums import Timeframe
from stark_terminal_data_platform.db.models.timeseries import OHLCVBarORM
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.quality.enums import ValidationStatus
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


def _batch():
    instrument = create_sample_instruments()[0]
    return generate_synthetic_market_data_batch(
        SyntheticOHLCVConfig(
            instrument_id=instrument.instrument_id,
            timeframe=Timeframe.DAILY,
            start_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            bar_count=2,
            start_price=100.0,
            source_data_reference="synthetic-local-test-only",
        )
    )


def test_generated_synthetic_batch_passes_storage_validation(db_session: Session) -> None:
    service = SyntheticOHLCVStorageService(OHLCVBarRepository(db_session))

    report = service.validate_bars(_batch().bars)

    assert report.status == ValidationStatus.PASS
    assert report.issue_count == 0
    assert report.source_data_reference == "synthetic-local-test-only"


def test_bad_ohlc_and_negative_volume_fail_storage_validation(db_session: Session) -> None:
    service = SyntheticOHLCVStorageService(OHLCVBarRepository(db_session))
    bar = _batch().bars[0].model_copy()
    object.__setattr__(bar, "high", 1.0)
    object.__setattr__(bar, "volume", -1.0)

    report = service.validate_bars([bar])

    assert report.status == ValidationStatus.FAIL
    assert {issue.code for result in report.results for issue in result.issues}.issuperset(
        {"BAR_HIGH_LOW_INCONSISTENT", "BAR_VOLUME_NEGATIVE"}
    )
