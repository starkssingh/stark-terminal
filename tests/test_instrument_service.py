from __future__ import annotations

from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.instrument import Instrument
from stark_terminal_data_platform.db.models.instrument import InstrumentORM
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.quality.enums import ValidationStatus
from stark_terminal_data_platform.repositories.instruments import InstrumentRepository
from stark_terminal_data_platform.services.instruments import (
    InstrumentMetadataService,
    InstrumentPersistenceError,
    InstrumentValidationError,
)


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


def _service(session: Session, settings: Settings | None = None) -> InstrumentMetadataService:
    return InstrumentMetadataService(InstrumentRepository(session), settings=settings or Settings())


def test_service_upsert_validates_and_persists(db_session: Session) -> None:
    service = _service(db_session)
    instrument = create_sample_instruments()[0]

    report = service.validate_instrument(instrument)
    persisted = service.upsert_instrument(instrument)

    assert report.status == ValidationStatus.PASS
    assert persisted == instrument
    assert service.health().repository_reachable is True
    assert service.health().instrument_count == 1


def test_service_blocks_invalid_instrument_before_persistence(db_session: Session) -> None:
    service = _service(db_session)
    valid = create_sample_instruments()[0]
    invalid = Instrument.model_construct(
        instrument_id=valid.instrument_id,
        display_name="",
        asset_class=valid.asset_class,
        status=valid.status,
        lot_size=valid.lot_size,
        tick_size=valid.tick_size,
        isin=None,
        sector=None,
        industry=None,
        metadata={},
    )

    with pytest.raises(InstrumentValidationError):
        service.upsert_instrument(invalid)

    assert service.repository.count() == 0


def test_service_upsert_many_and_seed_synthetic_are_idempotent(db_session: Session) -> None:
    service = _service(db_session)

    persisted = service.upsert_many(create_sample_instruments()[:2])
    seeded_once = service.seed_synthetic_instruments()
    seeded_twice = service.seed_synthetic_instruments()

    assert len(persisted) == 2
    assert len(seeded_once) == 6
    assert len(seeded_twice) == 6
    assert service.repository.count() == 6
    assert service.search_instruments("synthetic", limit=10)
    assert service.get_instrument("TCS", "NSE", "NSE_EQUITY") is not None


def test_service_respects_synthetic_seed_setting(db_session: Session) -> None:
    service = _service(db_session, Settings(instrument_persistence_allow_synthetic_seed=False))

    with pytest.raises(InstrumentPersistenceError):
        service.seed_synthetic_instruments()


def test_service_respects_persistence_enabled_setting(db_session: Session) -> None:
    service = _service(db_session, Settings(instrument_persistence_enabled=False))

    with pytest.raises(InstrumentPersistenceError):
        service.upsert_instrument(create_sample_instruments()[0])

    assert service.repository.count() == 0


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
    assert status.status == "unavailable"
    assert status.error == "InstrumentMetadataRepositoryUnavailable"
