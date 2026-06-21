from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.market_data import MarketDataBatch
from stark_terminal_core.domain.market_data_batch import (
    MarketDataBatchMetadata,
    MarketDataBatchPersistenceResult,
    metadata_from_batch,
)
from stark_terminal_data_platform.quality.builtins import MarketDataBarValidator
from stark_terminal_data_platform.quality.enums import ValidationScope, ValidationSeverity, ValidationStatus
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.reports import ValidationReport, build_validation_report
from stark_terminal_data_platform.quality.results import fail_result
from stark_terminal_data_platform.repositories.market_data_batches import MarketDataBatchRepository


class MarketDataBatchPersistenceError(RuntimeError):
    """Base error for safe market data batch metadata persistence failures."""


class MarketDataBatchValidationError(MarketDataBatchPersistenceError):
    def __init__(self, report: ValidationReport) -> None:
        super().__init__("market data batch validation failed")
        self.report = report


class MarketDataBatchNotFoundError(MarketDataBatchPersistenceError):
    """Raised by callers that choose exception semantics for missing batch metadata."""


class MarketDataBatchPersistenceHealthStatus(BaseModel):
    enabled: bool
    validation_required: bool
    synthetic_allowed: bool
    repository_reachable: bool
    batch_count: int | None
    stores_full_bars: bool = False
    status: str
    error: str | None = None


class MarketDataBatchMetadataService:
    def __init__(
        self,
        repository: MarketDataBatchRepository,
        *,
        settings: Settings | None = None,
        bar_validator: MarketDataBarValidator | None = None,
    ) -> None:
        self.repository = repository
        self.settings = settings or get_settings()
        self.bar_validator = bar_validator or MarketDataBarValidator(settings=self.settings)

    def validate_batch(self, batch: MarketDataBatch) -> ValidationReport:
        results = []
        if not batch.bars:
            results.append(
                fail_result(
                    ValidationScope.MARKET_DATA_BAR,
                    "market_data_batch",
                    ValidationIssue(
                        code="MARKET_DATA_BATCH_EMPTY",
                        severity=ValidationSeverity.ERROR,
                        message="market data batch bars cannot be empty",
                        scope=ValidationScope.MARKET_DATA_BAR,
                    ),
                )
            )
        for bar in batch.bars:
            results.extend(self.bar_validator.validate(bar).results)
        return build_validation_report(
            ValidationScope.MARKET_DATA_BAR,
            "market_data_batch",
            results,
            self.settings,
            source_data_reference=batch.bars[0].source_data_reference if batch.bars else None,
            notes=["market data batch metadata validation; full bars are not persisted"],
        )

    def create_metadata_from_batch(
        self,
        batch: MarketDataBatch,
        batch_id: str | None = None,
        synthetic: bool = False,
        fixture_id: str | None = None,
        dataset_manifest_id: str | None = None,
    ) -> MarketDataBatchMetadata:
        report = self.validate_batch(batch)
        return metadata_from_batch(
            batch,
            batch_id=batch_id,
            synthetic=synthetic,
            fixture_id=fixture_id,
            dataset_manifest_id=dataset_manifest_id,
            validation_report_id=report.report_id,
            schema_version=self.settings.market_data_batch_persistence_schema_version,
        )

    def persist_batch_metadata(self, metadata: MarketDataBatchMetadata) -> MarketDataBatchPersistenceResult:
        try:
            self._ensure_enabled()
            if metadata.synthetic and not self.settings.market_data_batch_persistence_allow_synthetic:
                raise MarketDataBatchPersistenceError("synthetic market data batch metadata persistence is disabled")
            persisted = self.upsert_metadata(metadata)
            return MarketDataBatchPersistenceResult(
                batch_id=persisted.batch_id,
                persisted=True,
                status="persisted",
                validation_status="PASS" if metadata.validation_report_id else None,
                row_count=persisted.row_count,
                error=None,
            )
        except MarketDataBatchPersistenceError:
            self.repository.session.rollback()
            raise
        except Exception as exc:
            self.repository.session.rollback()
            return MarketDataBatchPersistenceResult(
                batch_id=metadata.batch_id,
                persisted=False,
                status="failed",
                row_count=metadata.row_count,
                error=str(exc) or "market data batch metadata persistence failed",
            )

    def persist_synthetic_batch_metadata(
        self,
        batch: MarketDataBatch,
        fixture_id: str | None = None,
    ) -> MarketDataBatchPersistenceResult:
        if not self.settings.market_data_batch_persistence_allow_synthetic:
            raise MarketDataBatchPersistenceError("synthetic market data batch metadata persistence is disabled")
        report = self.validate_batch(batch)
        if self.settings.market_data_batch_persistence_require_validation and report.status != ValidationStatus.PASS:
            raise MarketDataBatchValidationError(report)
        metadata = metadata_from_batch(
            batch,
            synthetic=True,
            fixture_id=fixture_id,
            validation_report_id=report.report_id,
            schema_version=self.settings.market_data_batch_persistence_schema_version,
        )
        return self.persist_batch_metadata(metadata)

    def upsert_metadata(self, metadata: MarketDataBatchMetadata) -> MarketDataBatchMetadata:
        self._ensure_enabled()
        try:
            persisted = self.repository.upsert(metadata)
            self.repository.session.commit()
            return persisted
        except Exception:
            self.repository.session.rollback()
            raise

    def get_metadata(self, batch_id: str) -> MarketDataBatchMetadata | None:
        return self.repository.get(batch_id)

    def list_metadata(self, limit: int = 100, offset: int = 0) -> list[MarketDataBatchMetadata]:
        return self.repository.list_all(limit=limit, offset=offset)

    def list_by_instrument(
        self,
        instrument_id: InstrumentId,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MarketDataBatchMetadata]:
        return self.repository.list_by_instrument(instrument_id, limit=limit, offset=offset)

    def health(self) -> MarketDataBatchPersistenceHealthStatus:
        try:
            count = self.repository.count()
            return MarketDataBatchPersistenceHealthStatus(
                enabled=self.settings.market_data_batch_persistence_enabled,
                validation_required=self.settings.market_data_batch_persistence_require_validation,
                synthetic_allowed=self.settings.market_data_batch_persistence_allow_synthetic,
                repository_reachable=True,
                batch_count=count,
                stores_full_bars=False,
                status="healthy" if self.settings.market_data_batch_persistence_enabled else "disabled",
                error=None,
            )
        except Exception:
            return MarketDataBatchPersistenceHealthStatus(
                enabled=self.settings.market_data_batch_persistence_enabled,
                validation_required=self.settings.market_data_batch_persistence_require_validation,
                synthetic_allowed=self.settings.market_data_batch_persistence_allow_synthetic,
                repository_reachable=False,
                batch_count=None,
                stores_full_bars=False,
                status="unavailable",
                error="MarketDataBatchMetadataRepositoryUnavailable",
            )

    def _ensure_enabled(self) -> None:
        if not self.settings.market_data_batch_persistence_enabled:
            raise MarketDataBatchPersistenceError("market data batch metadata persistence is disabled")
