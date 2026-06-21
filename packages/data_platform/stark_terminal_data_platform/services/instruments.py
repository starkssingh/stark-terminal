from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import Exchange, MarketSegment
from stark_terminal_core.domain.instrument import Instrument
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.quality.builtins import InstrumentValidator
from stark_terminal_data_platform.quality.enums import ValidationStatus
from stark_terminal_data_platform.quality.reports import ValidationReport
from stark_terminal_data_platform.repositories.instruments import InstrumentRepository


class InstrumentPersistenceError(RuntimeError):
    """Base error for safe instrument metadata persistence failures."""


class InstrumentValidationError(InstrumentPersistenceError):
    def __init__(self, report: ValidationReport) -> None:
        super().__init__("instrument validation failed")
        self.report = report


class InstrumentNotFoundError(InstrumentPersistenceError):
    """Raised by callers that choose exception semantics for missing instruments."""


class InstrumentPersistenceHealthStatus(BaseModel):
    enabled: bool
    validation_required: bool
    synthetic_seed_allowed: bool
    repository_reachable: bool
    instrument_count: int | None
    status: str
    error: str | None = None


class InstrumentMetadataService:
    def __init__(
        self,
        repository: InstrumentRepository,
        *,
        settings: Settings | None = None,
        validator: InstrumentValidator | None = None,
    ) -> None:
        self.repository = repository
        self.settings = settings or get_settings()
        self.validator = validator or InstrumentValidator(settings=self.settings)

    def validate_instrument(self, instrument: Instrument) -> ValidationReport:
        return self.validator.validate(instrument)

    def upsert_instrument(self, instrument: Instrument) -> Instrument:
        try:
            self._ensure_enabled()
            if self.settings.instrument_persistence_require_validation:
                report = self.validate_instrument(instrument)
                if report.status != ValidationStatus.PASS:
                    raise InstrumentValidationError(report)
            persisted = self.repository.upsert(instrument)
            self.repository.session.commit()
            return persisted
        except Exception:
            self.repository.session.rollback()
            raise

    def upsert_many(self, instruments: list[Instrument]) -> list[Instrument]:
        persisted: list[Instrument] = []
        try:
            self._ensure_enabled()
            for instrument in instruments:
                if self.settings.instrument_persistence_require_validation:
                    report = self.validate_instrument(instrument)
                    if report.status != ValidationStatus.PASS:
                        raise InstrumentValidationError(report)
                persisted.append(self.repository.upsert(instrument))
            self.repository.session.commit()
        except Exception:
            self.repository.session.rollback()
            raise
        return persisted

    def seed_synthetic_instruments(self, instruments: list[Instrument] | None = None) -> list[Instrument]:
        if not self.settings.instrument_persistence_allow_synthetic_seed:
            raise InstrumentPersistenceError("synthetic instrument seeding is disabled")
        return self.upsert_many(instruments or create_sample_instruments())

    def list_instruments(self, limit: int = 100, offset: int = 0) -> list[Instrument]:
        return self.repository.list_all(limit=limit, offset=offset)

    def get_instrument(
        self,
        symbol: str,
        exchange: str | Exchange,
        segment: str | MarketSegment,
    ) -> Instrument | None:
        return self.repository.get(symbol, exchange, segment)

    def search_instruments(self, query: str, limit: int = 20) -> list[Instrument]:
        return self.repository.search(query, limit=limit)

    def health(self) -> InstrumentPersistenceHealthStatus:
        try:
            count = self.repository.count()
            return InstrumentPersistenceHealthStatus(
                enabled=self.settings.instrument_persistence_enabled,
                validation_required=self.settings.instrument_persistence_require_validation,
                synthetic_seed_allowed=self.settings.instrument_persistence_allow_synthetic_seed,
                repository_reachable=True,
                instrument_count=count,
                status="healthy" if self.settings.instrument_persistence_enabled else "disabled",
                error=None,
            )
        except Exception:
            return InstrumentPersistenceHealthStatus(
                enabled=self.settings.instrument_persistence_enabled,
                validation_required=self.settings.instrument_persistence_require_validation,
                synthetic_seed_allowed=self.settings.instrument_persistence_allow_synthetic_seed,
                repository_reachable=False,
                instrument_count=None,
                status="unavailable",
                error="InstrumentMetadataRepositoryUnavailable",
            )

    def _ensure_enabled(self) -> None:
        if not self.settings.instrument_persistence_enabled:
            raise InstrumentPersistenceError("instrument metadata persistence is disabled")
