from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from stark_terminal_core.domain.market_data_batch import metadata_from_batch
from stark_terminal_data_platform.db.models.market_data_batch import MarketDataBatchRecordORM
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.repositories.market_data_batches import MarketDataBatchRepository


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


def _metadata(fixture_id: str = "fixture_1"):
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
    return metadata_from_batch(batch, synthetic=True, fixture_id=fixture_id)


def test_repository_upsert_get_count_and_idempotent_update(db_session: Session) -> None:
    repository = MarketDataBatchRepository(db_session)
    metadata = _metadata()
    updated = metadata.model_copy(update={"row_count": 6, "notes": ["updated synthetic metadata"]})

    inserted = repository.upsert(metadata)
    roundtrip = repository.upsert(updated)

    assert inserted.batch_id == metadata.batch_id
    assert roundtrip.row_count == 6
    assert roundtrip.notes == ["updated synthetic metadata"]
    assert repository.get(metadata.batch_id) == roundtrip
    assert repository.count() == 1


def test_repository_list_by_instrument_search_by_fixture_and_delete(db_session: Session) -> None:
    repository = MarketDataBatchRepository(db_session)
    first = repository.upsert(_metadata("fixture_a"))
    second = repository.upsert(_metadata("fixture_b").model_copy(update={"batch_id": "batch_fixture_b"}))

    assert {item.batch_id for item in repository.list_all()} == {first.batch_id, second.batch_id}
    assert repository.list_by_instrument(first.instrument_id)[0].batch_id == first.batch_id
    assert repository.search_by_fixture("fixture_b")[0].batch_id == second.batch_id
    assert repository.delete(first.batch_id) is True
    assert repository.delete("missing") is False
    assert repository.count() == 1


@pytest.mark.parametrize("limit,offset", [(0, 0), (10, -1)])
def test_repository_rejects_invalid_limit_offset(db_session: Session, limit: int, offset: int) -> None:
    repository = MarketDataBatchRepository(db_session)

    with pytest.raises(ValueError):
        repository.list_all(limit=limit, offset=offset)


def test_repository_rejects_empty_batch_id_and_fixture_id(db_session: Session) -> None:
    repository = MarketDataBatchRepository(db_session)

    with pytest.raises(ValueError):
        repository.get("")
    with pytest.raises(ValueError):
        repository.search_by_fixture("")
