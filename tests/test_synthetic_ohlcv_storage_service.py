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
from stark_terminal_core.domain.market_data import MarketDataBar
from stark_terminal_data_platform.db.models.timeseries import OHLCVBarORM
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.repositories.ohlcv_bars import OHLCVBarRepository
from stark_terminal_data_platform.services.synthetic_ohlcv_storage import (
    SyntheticOHLCVStorageService,
    SyntheticOHLCVStorageValidationError,
)


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


def _service(session: Session, settings: Settings | None = None) -> SyntheticOHLCVStorageService:
    return SyntheticOHLCVStorageService(OHLCVBarRepository(session), settings=settings or Settings())


def test_service_stores_valid_synthetic_batch_idempotently(db_session: Session) -> None:
    service = _service(db_session)
    batch = _batch(5)

    first = service.store_synthetic_batch(batch, batch_id="batch_synthetic_reliance", fixture_id="fixture_reliance")
    second = service.store_synthetic_batch(batch, batch_id="batch_synthetic_reliance", fixture_id="fixture_reliance")

    assert first.stored is True
    assert second.stored is True
    assert first.stores_real_data is False
    assert service.count_bars(batch.bars[0].instrument_id, batch.bars[0].timeframe) == 5
    assert len(service.list_bars(batch.bars[0].instrument_id, batch.bars[0].timeframe)) == 5


def test_service_rejects_invalid_and_non_synthetic_bars(db_session: Session) -> None:
    service = _service(db_session)
    valid = _batch(1).bars[0]
    invalid_price = valid.model_copy()
    object.__setattr__(invalid_price, "low", -1.0)
    non_synthetic = valid.model_copy(update={"source_data_reference": "local-test-only"})

    with pytest.raises(SyntheticOHLCVStorageValidationError):
        service.store_synthetic_bars([invalid_price])
    with pytest.raises(SyntheticOHLCVStorageValidationError):
        service.store_synthetic_bars([non_synthetic])

    assert service.count_bars() == 0


def test_service_requires_local_sample_provider(db_session: Session) -> None:
    service = _service(db_session)
    bar = _batch(1).bars[0].model_copy(
        update={"provider": DataProviderId(name="manual_fixture", provider_type=DataProviderType.MANUAL)}
    )

    with pytest.raises(SyntheticOHLCVStorageValidationError) as exc_info:
        service.store_synthetic_bars([bar])

    assert exc_info.value.report.status == "FAIL"
    assert service.count_bars() == 0


def test_service_enforces_max_bars_setting(db_session: Session) -> None:
    settings = Settings(synthetic_ohlcv_storage_max_bars_per_batch=2)
    service = _service(db_session, settings=settings)

    with pytest.raises(SyntheticOHLCVStorageValidationError):
        service.store_synthetic_batch(_batch(3))


def test_service_health_reports_synthetic_boundary(db_session: Session) -> None:
    service = _service(db_session)
    health = service.health()

    assert health.repository_reachable is True
    assert health.stores_real_data is False
    assert health.timescale_required_for_tests is False
    assert health.sqlite_allowed is True


def test_service_does_not_publish_events_or_call_external_systems() -> None:
    source = inspect.getsource(SyntheticOHLCVStorageService)
    forbidden_terms = ("EventBackboneProducer", "StreamProducer", "redis", "kafka", "clickhouse", "duckdb", "requests.")

    assert all(term not in source for term in forbidden_terms)
