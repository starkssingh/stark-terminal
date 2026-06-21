from __future__ import annotations

from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.instrument import Instrument
from stark_terminal_data_platform.db.models.instrument import InstrumentORM
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.quality.builtins import InstrumentValidator
from stark_terminal_data_platform.quality.enums import ValidationScope, ValidationSeverity
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.reports import ValidationReport, build_validation_report
from stark_terminal_data_platform.quality.results import fail_result
from stark_terminal_data_platform.repositories.instruments import InstrumentRepository
from stark_terminal_data_platform.services.instruments import InstrumentMetadataService, InstrumentValidationError


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


class SpyValidator:
    def __init__(self, report: ValidationReport | None = None) -> None:
        self.report = report
        self.calls = 0
        self.delegate = InstrumentValidator(settings=Settings())

    def validate(self, instrument: Instrument) -> ValidationReport:
        self.calls += 1
        return self.report or self.delegate.validate(instrument)


def _failure_report(instrument: Instrument) -> ValidationReport:
    issue = ValidationIssue(
        code="TEST_INSTRUMENT_BLOCKED",
        severity=ValidationSeverity.ERROR,
        message="instrument validation failed in test",
        scope=ValidationScope.INSTRUMENT,
    )
    result = fail_result(ValidationScope.INSTRUMENT, str(instrument.instrument_id), issue)
    return build_validation_report(ValidationScope.INSTRUMENT, str(instrument.instrument_id), [result], Settings())


def test_service_uses_data_quality_validator_before_persistence(db_session: Session) -> None:
    validator = SpyValidator()
    service = InstrumentMetadataService(
        InstrumentRepository(db_session),
        settings=Settings(),
        validator=validator,  # type: ignore[arg-type]
    )

    service.upsert_instrument(create_sample_instruments()[0])

    assert validator.calls == 1
    assert service.repository.count() == 1


def test_validation_failure_blocks_persistence(db_session: Session) -> None:
    instrument = create_sample_instruments()[0]
    validator = SpyValidator(_failure_report(instrument))
    service = InstrumentMetadataService(
        InstrumentRepository(db_session),
        settings=Settings(),
        validator=validator,  # type: ignore[arg-type]
    )

    with pytest.raises(InstrumentValidationError):
        service.upsert_instrument(instrument)

    assert validator.calls == 1
    assert service.repository.count() == 0


def test_validation_can_be_disabled_explicitly_for_safe_local_metadata(db_session: Session) -> None:
    instrument = create_sample_instruments()[0]
    validator = SpyValidator(_failure_report(instrument))
    service = InstrumentMetadataService(
        InstrumentRepository(db_session),
        settings=Settings(instrument_persistence_require_validation=False),
        validator=validator,  # type: ignore[arg-type]
    )

    service.upsert_instrument(instrument)

    assert validator.calls == 0
    assert service.repository.count() == 1
    assert service.get_instrument("RELIANCE", "NSE", "NSE_EQUITY") is not None
