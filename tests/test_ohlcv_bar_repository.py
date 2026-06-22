from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from stark_terminal_core.domain.enums import Timeframe
from stark_terminal_core.domain.market_data import MarketDataBar
from stark_terminal_data_platform.db.models.timeseries import OHLCVBarORM
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_ohlcv_bars
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.repositories.ohlcv_bars import OHLCVBarRepository


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


def _bars(count: int = 5) -> list[MarketDataBar]:
    instrument = create_sample_instruments()[0]
    return generate_synthetic_ohlcv_bars(
        SyntheticOHLCVConfig(
            instrument_id=instrument.instrument_id,
            timeframe=Timeframe.DAILY,
            start_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            bar_count=count,
            start_price=100.0,
            source_data_reference="synthetic-local-test-only",
        )
    )


def test_repository_upsert_get_count_and_idempotent_update(db_session: Session) -> None:
    repository = OHLCVBarRepository(db_session)
    bar = _bars(1)[0]
    updated = bar.model_copy(update={"close": bar.close + 1.0, "high": bar.close + 2.0})

    inserted = repository.upsert_bar(bar)
    roundtrip = repository.upsert_bar(updated)

    assert inserted.timestamp == bar.timestamp
    assert roundtrip.close == updated.close
    assert repository.get_bar(bar.instrument_id, bar.timeframe, bar.timestamp, bar.provider) == roundtrip
    assert repository.count() == 1


def test_repository_upsert_many_list_filters_and_delete(db_session: Session) -> None:
    repository = OHLCVBarRepository(db_session)
    bars = repository.upsert_many(_bars(5))
    instrument_id = bars[0].instrument_id
    timeframe = bars[0].timeframe

    assert repository.count(instrument_id=instrument_id, timeframe=timeframe) == 5
    assert [bar.timestamp for bar in repository.list_bars(instrument_id, timeframe, limit=2)] == [
        bars[0].timestamp,
        bars[1].timestamp,
    ]
    filtered = repository.list_bars(instrument_id, timeframe, start=bars[1].timestamp, end=bars[3].timestamp)
    assert [bar.timestamp for bar in filtered] == [bars[1].timestamp, bars[2].timestamp, bars[3].timestamp]
    assert repository.delete_synthetic_bars("synthetic-local-test-only") == 5
    assert repository.count() == 0


def test_repository_rejects_invalid_query_arguments(db_session: Session) -> None:
    repository = OHLCVBarRepository(db_session)
    bars = _bars(2)

    with pytest.raises(ValueError):
        repository.list_bars(bars[0].instrument_id, bars[0].timeframe, limit=0)
    with pytest.raises(ValueError):
        repository.list_bars(bars[0].instrument_id, bars[0].timeframe, offset=-1)
    with pytest.raises(ValueError):
        repository.list_bars(bars[0].instrument_id, bars[0].timeframe, start=bars[1].timestamp, end=bars[0].timestamp)


def test_repository_does_not_share_global_state_between_sessions() -> None:
    first_engine = create_engine("sqlite+pysqlite:///:memory:")
    second_engine = create_engine("sqlite+pysqlite:///:memory:")
    OHLCVBarORM.__table__.create(first_engine)
    OHLCVBarORM.__table__.create(second_engine)
    try:
        FirstSession = sessionmaker(bind=first_engine, autoflush=False, autocommit=False, expire_on_commit=False)
        SecondSession = sessionmaker(bind=second_engine, autoflush=False, autocommit=False, expire_on_commit=False)
        with FirstSession() as first_session, SecondSession() as second_session:
            OHLCVBarRepository(first_session).upsert_bar(_bars(1)[0])
            assert OHLCVBarRepository(first_session).count() == 1
            assert OHLCVBarRepository(second_session).count() == 0
    finally:
        first_engine.dispose()
        second_engine.dispose()
