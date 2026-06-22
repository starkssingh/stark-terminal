from __future__ import annotations

from datetime import datetime, timezone
import re

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import DataProviderType, Timeframe
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.market_data import MarketDataBar, MarketDataBatch
from stark_terminal_data_platform.fixtures.manifests import (
    text_implies_real_market_data,
    text_mentions_synthetic_local_test,
)
from stark_terminal_data_platform.quality.builtins import MarketDataBarValidator
from stark_terminal_data_platform.quality.enums import ValidationScope, ValidationSeverity, ValidationStatus
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.reports import ValidationReport, build_validation_report
from stark_terminal_data_platform.quality.results import fail_result
from stark_terminal_data_platform.repositories.ohlcv_bars import OHLCVBarRepository

_SENSITIVE_ERROR_RE = re.compile(
    r"(password|secret|token|api_key|database_url|redis_url|clickhouse_url|kafka|broker|://)",
    re.IGNORECASE,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _safe_error(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    if _SENSITIVE_ERROR_RE.search(normalized):
        return "SyntheticOHLCVStorageError"
    return normalized[:240]


class SyntheticOHLCVStorageError(RuntimeError):
    """Base error for synthetic-only OHLCV storage failures."""


class SyntheticOHLCVStorageValidationError(SyntheticOHLCVStorageError):
    def __init__(self, report: ValidationReport) -> None:
        super().__init__("synthetic OHLCV storage validation failed")
        self.report = report


class SyntheticOHLCVStorageResult(BaseModel):
    batch_id: str | None = None
    stored: bool
    synthetic: bool = True
    bar_count: int = Field(ge=0)
    validation_status: str | None = None
    source_data_reference: str | None = None
    fixture_id: str | None = None
    stores_real_data: bool = False
    status: str
    error: str | None = None
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("batch_id", "validation_status", "source_data_reference", "fixture_id", "status")
    @classmethod
    def text_fields_must_be_sanitized(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("synthetic OHLCV storage text fields cannot be empty")
        if _SENSITIVE_ERROR_RE.search(normalized):
            raise ValueError("synthetic OHLCV storage text fields cannot contain secrets or raw URLs")
        return normalized

    @field_validator("error", mode="before")
    @classmethod
    def error_must_be_sanitized(cls, value: str | None) -> str | None:
        return _safe_error(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def result_must_remain_synthetic(self) -> SyntheticOHLCVStorageResult:
        if not self.synthetic:
            raise ValueError("synthetic OHLCV storage result must remain synthetic")
        if self.stores_real_data:
            raise ValueError("synthetic OHLCV storage cannot store real market data")
        return self


class SyntheticOHLCVStorageHealthStatus(BaseModel):
    enabled: bool
    validation_required: bool
    sqlite_allowed: bool
    repository_reachable: bool
    stored_bar_count: int | None
    stores_real_data: bool = False
    timescale_required_for_tests: bool = False
    status: str
    error: str | None = None


class SyntheticOHLCVStorageService:
    """Synthetic-only OHLCV storage service with deterministic validation gates."""

    def __init__(
        self,
        repository: OHLCVBarRepository,
        *,
        settings: Settings | None = None,
        bar_validator: MarketDataBarValidator | None = None,
    ) -> None:
        self.repository = repository
        self.settings = settings or get_settings()
        self.bar_validator = bar_validator or MarketDataBarValidator(settings=self.settings)

    def validate_bars(self, bars: list[MarketDataBar]) -> ValidationReport:
        results = []
        if not bars:
            results.append(
                fail_result(
                    ValidationScope.MARKET_DATA_BAR,
                    "synthetic_ohlcv_storage",
                    ValidationIssue(
                        code="SYNTHETIC_OHLCV_EMPTY",
                        severity=ValidationSeverity.ERROR,
                        message="synthetic OHLCV storage requires at least one bar",
                        scope=ValidationScope.MARKET_DATA_BAR,
                    ),
                )
            )
        if len(bars) > self.settings.synthetic_ohlcv_storage_max_bars_per_batch:
            results.append(
                fail_result(
                    ValidationScope.MARKET_DATA_BAR,
                    "synthetic_ohlcv_storage",
                    ValidationIssue(
                        code="SYNTHETIC_OHLCV_BATCH_TOO_LARGE",
                        severity=ValidationSeverity.ERROR,
                        message="synthetic OHLCV batch exceeds configured max bars",
                        scope=ValidationScope.MARKET_DATA_BAR,
                    ),
                )
            )

        for bar in bars:
            results.extend(self.bar_validator.validate(bar).results)
            subject_id = self._bar_subject_id(bar)
            source = bar.source_data_reference
            if not source or not text_mentions_synthetic_local_test(source) or text_implies_real_market_data(source):
                results.append(
                    fail_result(
                        ValidationScope.MARKET_DATA_BAR,
                        subject_id,
                        ValidationIssue(
                            code="SYNTHETIC_SOURCE_REFERENCE_REQUIRED",
                            severity=ValidationSeverity.ERROR,
                            message="stored OHLCV bars require synthetic local test source references",
                            field="source_data_reference",
                            scope=ValidationScope.MARKET_DATA_BAR,
                        ),
                    )
                )
            if bar.provider is None or bar.provider.provider_type != DataProviderType.LOCAL_SAMPLE:
                results.append(
                    fail_result(
                        ValidationScope.MARKET_DATA_BAR,
                        subject_id,
                        ValidationIssue(
                            code="SYNTHETIC_PROVIDER_REQUIRED",
                            severity=ValidationSeverity.ERROR,
                            message="stored synthetic OHLCV bars require LOCAL_SAMPLE provider identity",
                            field="provider",
                            scope=ValidationScope.MARKET_DATA_BAR,
                        ),
                    )
                )

        return build_validation_report(
            ValidationScope.MARKET_DATA_BAR,
            "synthetic_ohlcv_storage",
            results,
            self.settings,
            source_data_reference=bars[0].source_data_reference if bars else None,
            notes=["validation-before-storage for synthetic-only TimescaleDB OHLCV foundation"],
        )

    def store_synthetic_bars(
        self,
        bars: list[MarketDataBar],
        batch_id: str | None = None,
        fixture_id: str | None = None,
    ) -> SyntheticOHLCVStorageResult:
        self._ensure_enabled()
        report = self.validate_bars(bars)
        if report.status != ValidationStatus.PASS:
            raise SyntheticOHLCVStorageValidationError(report)
        try:
            stored = self.repository.upsert_many(bars)
            self.repository.session.commit()
            return SyntheticOHLCVStorageResult(
                batch_id=batch_id,
                stored=True,
                synthetic=True,
                bar_count=len(stored),
                validation_status=report.status.value,
                source_data_reference=bars[0].source_data_reference if bars else None,
                fixture_id=fixture_id,
                stores_real_data=False,
                status="stored",
                error=None,
            )
        except Exception as exc:
            self.repository.session.rollback()
            return SyntheticOHLCVStorageResult(
                batch_id=batch_id,
                stored=False,
                synthetic=True,
                bar_count=len(bars),
                validation_status=report.status.value,
                source_data_reference=bars[0].source_data_reference if bars else None,
                fixture_id=fixture_id,
                stores_real_data=False,
                status="failed",
                error=_safe_error(str(exc)) or "SyntheticOHLCVStorageUnavailable",
            )

    def store_synthetic_batch(
        self,
        batch: MarketDataBatch,
        batch_id: str | None = None,
        fixture_id: str | None = None,
    ) -> SyntheticOHLCVStorageResult:
        return self.store_synthetic_bars(batch.bars, batch_id=batch_id, fixture_id=fixture_id)

    def list_bars(
        self,
        instrument_id: InstrumentId,
        timeframe: Timeframe,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int = 1000,
        offset: int = 0,
    ) -> list[MarketDataBar]:
        return self.repository.list_bars(
            instrument_id,
            timeframe,
            start=start,
            end=end,
            limit=limit,
            offset=offset,
        )

    def count_bars(self, instrument_id: InstrumentId | None = None, timeframe: Timeframe | None = None) -> int:
        return self.repository.count(instrument_id=instrument_id, timeframe=timeframe)

    def health(self) -> SyntheticOHLCVStorageHealthStatus:
        try:
            count = self.repository.count()
            return SyntheticOHLCVStorageHealthStatus(
                enabled=self.settings.synthetic_ohlcv_storage_enabled,
                validation_required=self.settings.synthetic_ohlcv_storage_require_validation,
                sqlite_allowed=self.settings.synthetic_ohlcv_storage_allow_sqlite,
                repository_reachable=True,
                stored_bar_count=count,
                stores_real_data=False,
                timescale_required_for_tests=False,
                status="healthy" if self.settings.synthetic_ohlcv_storage_enabled else "disabled",
                error=None,
            )
        except Exception:
            return SyntheticOHLCVStorageHealthStatus(
                enabled=self.settings.synthetic_ohlcv_storage_enabled,
                validation_required=self.settings.synthetic_ohlcv_storage_require_validation,
                sqlite_allowed=self.settings.synthetic_ohlcv_storage_allow_sqlite,
                repository_reachable=False,
                stored_bar_count=None,
                stores_real_data=False,
                timescale_required_for_tests=False,
                status="unavailable",
                error="SyntheticOHLCVStorageRepositoryUnavailable",
            )

    def _ensure_enabled(self) -> None:
        if not self.settings.synthetic_ohlcv_storage_enabled:
            raise SyntheticOHLCVStorageError("synthetic OHLCV storage is disabled")

    @staticmethod
    def _bar_subject_id(bar: MarketDataBar) -> str:
        return f"{bar.instrument_id}:{bar.timeframe.value}:{bar.timestamp.isoformat()}"
