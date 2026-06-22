from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import (
    DataLakeZone,
    DataProviderType,
    DatasetFormat,
    DatasetKind,
    Timeframe,
)
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.market_data import MarketDataBar, normalize_datetime_to_utc
from stark_terminal_data_platform.fixtures.manifests import (
    text_implies_real_market_data,
    text_mentions_synthetic_local_test,
)
from stark_terminal_data_platform.lake.duckdb_client import DuckDBClient
from stark_terminal_data_platform.lake.manifest import (
    DatasetManifest,
    DatasetPartition,
    create_dataset_manifest,
)
from stark_terminal_data_platform.lake.parquet_io import (
    count_parquet_rows,
    inspect_parquet_schema,
    read_parquet_frame,
    write_parquet_frame,
)
from stark_terminal_data_platform.lake.zones import ZONE_DIRECTORY_NAMES, normalize_zone
from stark_terminal_data_platform.quality.builtins import MarketDataBarValidator
from stark_terminal_data_platform.quality.enums import ValidationScope, ValidationSeverity, ValidationStatus
from stark_terminal_data_platform.quality.issues import ValidationIssue
from stark_terminal_data_platform.quality.reports import ValidationReport, build_validation_report
from stark_terminal_data_platform.quality.results import fail_result, pass_result
from stark_terminal_data_platform.repositories.ohlcv_bars import OHLCVBarRepository

_SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
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
        return "SyntheticOHLCVExportError"
    return normalized[:240]


def _safe_name(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    candidate = Path(normalized)
    if candidate.is_absolute() or ".." in candidate.parts or "/" in normalized or "\\" in normalized:
        raise ValueError(f"{field_name} cannot be absolute or contain traversal")
    if not _SAFE_NAME_RE.fullmatch(normalized):
        raise ValueError(f"{field_name} must be a safe dataset identifier")
    return normalized


def _requires_synthetic_source(value: str | None, field_name: str) -> str:
    normalized = (value or "").strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    if not text_mentions_synthetic_local_test(normalized) or text_implies_real_market_data(normalized):
        raise ValueError(f"{field_name} must clearly describe synthetic local test data")
    return normalized


def _manifest_relative_path(path: Path) -> Path:
    if not path.is_absolute():
        return path
    parts = list(path.parts)
    for marker in ("research_artifacts", "raw", "cleaned", "normalized", "feature_ready", "backtest_ready"):
        if marker in parts:
            return Path(*parts[parts.index(marker):])
    return Path(*parts[-4:]) if len(parts) >= 4 else Path(path.name)


class SyntheticOHLCVExportError(RuntimeError):
    """Base error for synthetic OHLCV research lake export failures."""


class SyntheticOHLCVExportValidationError(SyntheticOHLCVExportError):
    def __init__(self, report: ValidationReport) -> None:
        super().__init__("synthetic OHLCV export validation failed")
        self.report = report


class SyntheticOHLCVExportRequest(BaseModel):
    export_id: str
    instrument_id: InstrumentId
    timeframe: Timeframe
    start: datetime | None = None
    end: datetime | None = None
    zone: DataLakeZone = DataLakeZone.RESEARCH_ARTIFACTS
    dataset_name: str
    version: str = "v1"
    synthetic: bool = True
    source_data_reference: str
    schema_version: str = "v1"
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("export_id", "dataset_name", "version", "schema_version", mode="before")
    @classmethod
    def text_fields_must_be_safe(cls, value: str) -> str:
        return _safe_name(str(value), "synthetic OHLCV export field")

    @field_validator("source_data_reference", mode="before")
    @classmethod
    def source_reference_must_be_synthetic(cls, value: str) -> str:
        return _requires_synthetic_source(str(value), "source_data_reference")

    @field_validator("start", "end", "created_at")
    @classmethod
    def timestamps_must_be_utc(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        return normalize_datetime_to_utc(value)

    @field_validator("zone", mode="before")
    @classmethod
    def zone_must_be_known(cls, value: DataLakeZone | str) -> DataLakeZone:
        return normalize_zone(value)

    @model_validator(mode="after")
    def request_must_be_synthetic_and_ordered(self) -> SyntheticOHLCVExportRequest:
        if not self.synthetic:
            raise ValueError("synthetic OHLCV export requests must remain synthetic")
        if self.start is not None and self.end is not None and self.start > self.end:
            raise ValueError("start must be before or equal to end")
        return self


class SyntheticOHLCVExportResult(BaseModel):
    export_id: str
    exported: bool
    synthetic: bool = True
    real_market_data: bool = False
    row_count: int = Field(ge=0)
    dataset_manifest: DatasetManifest | None = None
    output_path: str | None = None
    validation_report_id: str | None = None
    status: str
    error: str | None = None
    created_at: datetime = Field(default_factory=_utc_now)

    @field_validator("export_id", "validation_report_id", "status")
    @classmethod
    def result_text_must_be_safe(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("synthetic OHLCV export result text fields cannot be empty")
        if _SENSITIVE_ERROR_RE.search(normalized):
            raise ValueError("synthetic OHLCV export result text fields cannot contain secrets or raw URLs")
        return normalized

    @field_validator("output_path")
    @classmethod
    def output_path_must_not_contain_secrets(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("output_path cannot be empty")
        if _SENSITIVE_ERROR_RE.search(normalized):
            raise ValueError("output_path cannot contain secrets or raw URLs")
        return normalized

    @field_validator("error", mode="before")
    @classmethod
    def error_must_be_sanitized(cls, value: str | None) -> str | None:
        return _safe_error(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_datetime_to_utc(value)

    @model_validator(mode="after")
    def result_must_remain_synthetic(self) -> SyntheticOHLCVExportResult:
        if not self.synthetic:
            raise ValueError("synthetic OHLCV export result must remain synthetic")
        if self.real_market_data:
            raise ValueError("synthetic OHLCV export cannot represent real market data")
        return self


class SyntheticOHLCVExportHealthStatus(BaseModel):
    enabled: bool
    validation_required: bool
    disk_writes_allowed: bool
    default_zone: str
    max_rows: int
    synthetic_only: bool = True
    real_market_data_allowed: bool = False
    duckdb_available: bool
    parquet_engine_available: bool
    status: str
    error: str | None = None


def build_synthetic_ohlcv_dataset_name(
    instrument_id: InstrumentId,
    timeframe: Timeframe,
    version: str = "v1",
) -> str:
    version_part = _safe_name(version, "version").lower()
    return (
        f"synthetic_ohlcv_{instrument_id.exchange.value.lower()}_"
        f"{instrument_id.symbol.lower()}_{instrument_id.segment.value.lower()}_"
        f"{Timeframe(timeframe).value.lower()}_{version_part}"
    )


def create_synthetic_ohlcv_export_request(
    *,
    instrument_id: InstrumentId,
    timeframe: Timeframe,
    source_data_reference: str,
    export_id: str | None = None,
    dataset_name: str | None = None,
    version: str = "v1",
    start: datetime | None = None,
    end: datetime | None = None,
    zone: DataLakeZone | str = DataLakeZone.RESEARCH_ARTIFACTS,
    schema_version: str = "v1",
) -> SyntheticOHLCVExportRequest:
    return SyntheticOHLCVExportRequest(
        export_id=export_id or f"synthetic_ohlcv_export_{uuid4().hex}",
        instrument_id=instrument_id,
        timeframe=timeframe,
        start=start,
        end=end,
        zone=normalize_zone(zone),
        dataset_name=dataset_name or build_synthetic_ohlcv_dataset_name(instrument_id, timeframe, version),
        version=version,
        synthetic=True,
        source_data_reference=source_data_reference,
        schema_version=schema_version,
    )


def validate_export_request(request: SyntheticOHLCVExportRequest) -> SyntheticOHLCVExportRequest:
    return SyntheticOHLCVExportRequest.model_validate(request)


class SyntheticOHLCVResearchLakeExportService:
    """Exports stored synthetic OHLCV bars to temp/test Parquet research artifacts."""

    def __init__(
        self,
        repository: OHLCVBarRepository | None = None,
        *,
        settings: Settings | None = None,
        bar_validator: MarketDataBarValidator | None = None,
    ) -> None:
        self.repository = repository
        self.settings = settings or get_settings()
        self.bar_validator = bar_validator or MarketDataBarValidator(settings=self.settings)

    def validate_export_request(self, request: SyntheticOHLCVExportRequest) -> ValidationReport:
        results = [
            pass_result(
                ValidationScope.DATASET_MANIFEST,
                request.export_id,
                rule_id="SYNTHETIC_OHLCV_EXPORT_REQUEST",
                metadata={"dataset_name": request.dataset_name, "synthetic": True},
            )
        ]
        if not request.synthetic or text_implies_real_market_data(request.source_data_reference):
            results.append(
                fail_result(
                    ValidationScope.DATASET_MANIFEST,
                    request.export_id,
                    ValidationIssue(
                        code="EXPORT_REQUEST_NOT_SYNTHETIC",
                        severity=ValidationSeverity.ERROR,
                        message="synthetic OHLCV export requests must remain synthetic",
                        scope=ValidationScope.DATASET_MANIFEST,
                    ),
                )
            )
        return build_validation_report(
            ValidationScope.DATASET_MANIFEST,
            request.export_id,
            results,
            self.settings,
            source_data_reference=request.source_data_reference,
            notes=["validation-before-export for synthetic OHLCV research lake contract"],
        )

    def validate_bars_for_export(self, bars: list[MarketDataBar]) -> ValidationReport:
        results = []
        if not bars:
            results.append(
                fail_result(
                    ValidationScope.MARKET_DATA_BAR,
                    "synthetic_ohlcv_export",
                    ValidationIssue(
                        code="SYNTHETIC_OHLCV_EXPORT_EMPTY",
                        severity=ValidationSeverity.ERROR,
                        message="synthetic OHLCV export requires at least one stored bar",
                        scope=ValidationScope.MARKET_DATA_BAR,
                    ),
                )
            )
        if len(bars) > self.settings.synthetic_ohlcv_export_max_rows:
            results.append(
                fail_result(
                    ValidationScope.MARKET_DATA_BAR,
                    "synthetic_ohlcv_export",
                    ValidationIssue(
                        code="SYNTHETIC_OHLCV_EXPORT_TOO_LARGE",
                        severity=ValidationSeverity.ERROR,
                        message="synthetic OHLCV export exceeds configured max rows",
                        scope=ValidationScope.MARKET_DATA_BAR,
                    ),
                )
            )

        for bar in bars:
            subject_id = self._bar_subject_id(bar)
            results.extend(self.bar_validator.validate(bar).results)
            source = bar.source_data_reference
            if not source or not text_mentions_synthetic_local_test(source) or text_implies_real_market_data(source):
                results.append(
                    fail_result(
                        ValidationScope.MARKET_DATA_BAR,
                        subject_id,
                        ValidationIssue(
                            code="SYNTHETIC_EXPORT_SOURCE_REFERENCE_REQUIRED",
                            severity=ValidationSeverity.ERROR,
                            message="exported OHLCV bars require synthetic local test source references",
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
                            code="SYNTHETIC_EXPORT_PROVIDER_REQUIRED",
                            severity=ValidationSeverity.ERROR,
                            message="exported OHLCV bars require LOCAL_SAMPLE provider identity",
                            field="provider",
                            scope=ValidationScope.MARKET_DATA_BAR,
                        ),
                    )
                )

        return build_validation_report(
            ValidationScope.MARKET_DATA_BAR,
            "synthetic_ohlcv_export",
            results,
            self.settings,
            source_data_reference=bars[0].source_data_reference if bars else None,
            notes=["validation-before-export for synthetic-only research lake Parquet output"],
        )

    def export_bars_to_parquet(
        self,
        request: SyntheticOHLCVExportRequest,
        output_root: Path | None = None,
    ) -> SyntheticOHLCVExportResult:
        self._ensure_enabled()
        repository = self._require_repository()
        request_report = self.validate_export_request(request)
        if request_report.status != ValidationStatus.PASS:
            raise SyntheticOHLCVExportValidationError(request_report)

        bars = repository.list_bars(
            request.instrument_id,
            request.timeframe,
            start=request.start,
            end=request.end,
            limit=self.settings.synthetic_ohlcv_export_max_rows + 1,
        )
        bar_report = self.validate_bars_for_export(bars)
        if self.settings.synthetic_ohlcv_export_require_validation and bar_report.status != ValidationStatus.PASS:
            raise SyntheticOHLCVExportValidationError(bar_report)

        root = self._resolve_output_root(output_root)
        relative_path = self._relative_export_path(request)
        output_path = root / relative_path
        try:
            rows = self._bars_to_rows(bars)
            write_parquet_frame(rows, output_path, compression=self.settings.parquet_compression)
            manifest = self.create_manifest_for_export(
                request,
                relative_path,
                row_count=len(rows),
                schema_json=inspect_parquet_schema(output_path),
            )
            return SyntheticOHLCVExportResult(
                export_id=request.export_id,
                exported=True,
                synthetic=True,
                real_market_data=False,
                row_count=count_parquet_rows(output_path),
                dataset_manifest=manifest,
                output_path=str(output_path),
                validation_report_id=bar_report.report_id,
                status="exported",
                error=None,
            )
        except Exception as exc:
            return SyntheticOHLCVExportResult(
                export_id=request.export_id,
                exported=False,
                synthetic=True,
                real_market_data=False,
                row_count=len(bars),
                dataset_manifest=None,
                output_path=str(output_path),
                validation_report_id=bar_report.report_id,
                status="failed",
                error=_safe_error(str(exc)) or "SyntheticOHLCVExportUnavailable",
            )

    def create_manifest_for_export(
        self,
        request: SyntheticOHLCVExportRequest,
        path: str | Path,
        row_count: int,
        schema_json: dict[str, str] | None = None,
    ) -> DatasetManifest:
        manifest_path = _manifest_relative_path(Path(path))
        return create_dataset_manifest(
            dataset_id=request.export_id,
            name=request.dataset_name,
            kind=DatasetKind.OHLCV,
            zone=request.zone,
            path=manifest_path,
            format=DatasetFormat.PARQUET,
            version=request.version,
            partitions=[
                DatasetPartition(key="exchange", value=request.instrument_id.exchange.value),
                DatasetPartition(key="symbol", value=request.instrument_id.symbol),
                DatasetPartition(key="timeframe", value=request.timeframe.value),
            ],
            row_count=row_count,
            schema_json=schema_json or self._default_schema_map(),
            source_data_reference=request.source_data_reference,
            notes=[
                "synthetic-only OHLCV research lake export",
                "not real market data",
                "no analytics, signals, decisions, or execution APIs",
            ],
        )

    def read_export_with_duckdb(self, path: str | Path) -> Any:
        with DuckDBClient() as client:
            return client.query_parquet(path)

    def health(self) -> SyntheticOHLCVExportHealthStatus:
        try:
            parquet_engine_available = True
            duckdb_available = True
            return SyntheticOHLCVExportHealthStatus(
                enabled=self.settings.synthetic_ohlcv_export_enabled,
                validation_required=self.settings.synthetic_ohlcv_export_require_validation,
                disk_writes_allowed=self.settings.synthetic_ohlcv_export_allow_disk_writes,
                default_zone=self.settings.synthetic_ohlcv_export_default_zone,
                max_rows=self.settings.synthetic_ohlcv_export_max_rows,
                synthetic_only=True,
                real_market_data_allowed=False,
                duckdb_available=duckdb_available,
                parquet_engine_available=parquet_engine_available,
                status="healthy" if self.settings.synthetic_ohlcv_export_enabled else "disabled",
                error=None,
            )
        except Exception:
            return SyntheticOHLCVExportHealthStatus(
                enabled=self.settings.synthetic_ohlcv_export_enabled,
                validation_required=self.settings.synthetic_ohlcv_export_require_validation,
                disk_writes_allowed=self.settings.synthetic_ohlcv_export_allow_disk_writes,
                default_zone=self.settings.synthetic_ohlcv_export_default_zone,
                max_rows=self.settings.synthetic_ohlcv_export_max_rows,
                synthetic_only=True,
                real_market_data_allowed=False,
                duckdb_available=False,
                parquet_engine_available=False,
                status="unavailable",
                error="SyntheticOHLCVExportHealthUnavailable",
            )

    def _ensure_enabled(self) -> None:
        if not self.settings.synthetic_ohlcv_export_enabled:
            raise SyntheticOHLCVExportError("synthetic OHLCV export is disabled")

    def _require_repository(self) -> OHLCVBarRepository:
        if self.repository is None:
            raise SyntheticOHLCVExportError("synthetic OHLCV export repository is not configured")
        return self.repository

    def _resolve_output_root(self, output_root: Path | None) -> Path:
        if output_root is None:
            if not self.settings.synthetic_ohlcv_export_allow_disk_writes:
                raise SyntheticOHLCVExportError("explicit output_root is required when export disk writes are disabled")
            return Path(self.settings.research_artifacts_root)
        return Path(output_root)

    def _relative_export_path(self, request: SyntheticOHLCVExportRequest) -> Path:
        zone_dir = ZONE_DIRECTORY_NAMES[request.zone]
        filename = f"{request.export_id}.parquet"
        return Path(zone_dir) / request.dataset_name / request.version / filename

    @staticmethod
    def _bars_to_rows(bars: list[MarketDataBar]) -> list[dict[str, Any]]:
        return [
            {
                "instrument_id": str(bar.instrument_id),
                "symbol": bar.instrument_id.symbol,
                "exchange": bar.instrument_id.exchange.value,
                "segment": bar.instrument_id.segment.value,
                "timeframe": bar.timeframe.value,
                "timestamp": bar.timestamp,
                "open": bar.open,
                "high": bar.high,
                "low": bar.low,
                "close": bar.close,
                "volume": bar.volume,
                "open_interest": bar.open_interest,
                "provider": bar.provider.name if bar.provider is not None else None,
                "provider_type": bar.provider.provider_type.value if bar.provider is not None else None,
                "quality_status": bar.quality_status.value,
                "source_data_reference": bar.source_data_reference,
            }
            for bar in bars
        ]

    @staticmethod
    def _default_schema_map() -> dict[str, str]:
        return {
            "instrument_id": "string",
            "symbol": "string",
            "exchange": "string",
            "segment": "string",
            "timeframe": "string",
            "timestamp": "datetime[utc]",
            "open": "float",
            "high": "float",
            "low": "float",
            "close": "float",
            "volume": "float",
            "open_interest": "float",
            "provider": "string",
            "provider_type": "string",
            "quality_status": "string",
            "source_data_reference": "string",
        }

    @staticmethod
    def _bar_subject_id(bar: MarketDataBar) -> str:
        return f"{bar.instrument_id}:{bar.timeframe.value}:{bar.timestamp.isoformat()}"
