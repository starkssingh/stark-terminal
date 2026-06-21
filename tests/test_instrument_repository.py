from __future__ import annotations

from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from stark_terminal_core.domain.enums import Exchange, MarketSegment
from stark_terminal_data_platform.db.models.instrument import InstrumentORM
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.repositories.instruments import InstrumentRepository


@pytest.fixture()
def db_session() -> Iterator[Session]:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    InstrumentORM.__table__.create(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def test_repository_upsert_get_count_and_idempotent_update(db_session: Session) -> None:
    repository = InstrumentRepository(db_session)
    instrument = create_sample_instruments()[0]

    inserted = repository.upsert(instrument)
    updated = repository.upsert(instrument.model_copy(update={"display_name": "Reliance Updated Synthetic"}))

    assert str(inserted.instrument_id) == "NSE:RELIANCE:NSE_EQUITY"
    assert updated.display_name == "Reliance Updated Synthetic"
    assert repository.count() == 1
    assert repository.get(" reliance ", "NSE", "NSE_EQUITY") == updated
    assert repository.get_by_id(instrument.instrument_id) == updated


def test_repository_list_search_and_delete(db_session: Session) -> None:
    repository = InstrumentRepository(db_session)
    for instrument in create_sample_instruments()[:3]:
        repository.upsert(instrument)

    assert [item.instrument_id.symbol for item in repository.list_all(limit=2)] == ["HDFCBANK", "RELIANCE"]
    assert [item.instrument_id.symbol for item in repository.list_all(limit=2, offset=2)] == ["TCS"]
    assert [item.instrument_id.symbol for item in repository.search("hdfc")] == ["HDFCBANK"]

    assert repository.delete("HDFCBANK", Exchange.NSE, MarketSegment.NSE_EQUITY) is True
    assert repository.delete("MISSING", Exchange.NSE, MarketSegment.NSE_EQUITY) is False
    assert repository.count() == 2


@pytest.mark.parametrize(
    "limit,offset",
    [
        (0, 0),
        (10, -1),
    ],
)
def test_repository_rejects_invalid_limit_offset(db_session: Session, limit: int, offset: int) -> None:
    repository = InstrumentRepository(db_session)

    with pytest.raises(ValueError):
        repository.list_all(limit=limit, offset=offset)


def test_repository_rejects_invalid_search_args(db_session: Session) -> None:
    repository = InstrumentRepository(db_session)

    with pytest.raises(ValueError):
        repository.search("", limit=20)
    with pytest.raises(ValueError):
        repository.search("RELIANCE", limit=0)
