from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any, Iterable

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import (
    AssetClass,
    DataProviderType,
    DataQualityStatus,
    DatasetFormat,
    Exchange,
    InstrumentStatus,
    MarketDataRequestKind,
    MarketSegment,
    ProviderCapability,
    ProviderStatus,
    Timeframe,
)
from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId
from stark_terminal_core.domain.instrument import Instrument
from stark_terminal_core.domain.market_data import MarketDataBar, normalize_datetime_to_utc
from stark_terminal_core.domain.market_data_contracts import MarketDataRequest, MarketDataResponse
from stark_terminal_data_platform.providers.approval import (
    approve_for_design,
    create_provider_approval_record,
)
from stark_terminal_data_platform.providers.base import MarketDataProvider
from stark_terminal_data_platform.providers.contracts import ProviderCapabilityReport
from stark_terminal_data_platform.providers.guardrails import (
    ProviderGuardrailDecision,
    ProviderGuardrailPolicy,
    ProviderGuardrailResult,
    ProviderIntegrationMode,
    default_provider_guardrail_policy,
    evaluate_provider_guardrails,
    sanitize_provider_notes,
)
from stark_terminal_data_platform.providers.readiness import ProviderComplianceChecklist
from stark_terminal_data_platform.quality.builtins import MarketDataResponseValidator
from stark_terminal_data_platform.quality.enums import ValidationStatus


LOCAL_FILE_SOURCE_REFERENCE = "local-file-test-dev-only"
LOCAL_FILE_PROVIDER_ID = DataProviderId(
    name="local_file",
    provider_type=DataProviderType.MANUAL,
    version="v0",
)
SUPPORTED_LOCAL_FILE_CAPABILITIES = [
    ProviderCapability.INSTRUMENT_MASTER,
    ProviderCapability.HISTORICAL_BARS,
    ProviderCapability.HEALTH_CHECK,
]
UNSUPPORTED_LOCAL_FILE_CAPABILITIES = [
    ProviderCapability.LATEST_BAR,
    ProviderCapability.OPTIONS_CHAIN,
    ProviderCapability.FUTURES_CHAIN,
    ProviderCapability.CORPORATE_ACTIONS,
]
SUPPORTED_LOCAL_FILE_FORMATS = {DatasetFormat.CSV, DatasetFormat.PARQUET}
INSTRUMENT_REQUIRED_COLUMNS = {
    "symbol",
    "exchange",
    "segment",
    "display_name",
    "asset_class",
}
OHLCV_REQUIRED_COLUMNS = {
    "symbol",
    "exchange",
    "segment",
    "timeframe",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
}
SENSITIVE_LOCAL_FILE_PATTERN = re.compile(
    r"(password|secret|token|api[_-]?key|credential|bearer|database_url|broker)",
    re.IGNORECASE,
)
NETWORK_PATH_PREFIXES = (
    "http://",
    "https://",
    "ftp://",
    "s3://",
    "gs://",
    "file://",
)


class LocalFileSource(BaseModel):
    source_id: str
    path: str
    file_format: DatasetFormat
    provider_name: str = "local_file"
    label: str = LOCAL_FILE_SOURCE_REFERENCE
    synthetic: bool = True
    real_market_data: bool = False
    schema_version: str = "v1"
    notes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("source_id", "path", "provider_name", "schema_version")
    @classmethod
    def text_fields_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("local file source text fields cannot be empty")
        if SENSITIVE_LOCAL_FILE_PATTERN.search(normalized):
            raise ValueError("local file source text fields must not contain secrets")
        return normalized

    @field_validator("file_format")
    @classmethod
    def file_format_must_be_supported(cls, value: DatasetFormat) -> DatasetFormat:
        if value not in SUPPORTED_LOCAL_FILE_FORMATS:
            raise ValueError("local file sources support only CSV and PARQUET")
        return value

    @field_validator("label")
    @classmethod
    def label_must_state_local_test_dev(cls, value: str) -> str:
        normalized = value.strip()
        lowered = normalized.lower()
        if not normalized:
            raise ValueError("local file source label cannot be empty")
        if "local" not in lowered or ("test" not in lowered and "dev" not in lowered):
            raise ValueError("local file source label must include local/test/dev semantics")
        return normalized

    @field_validator("notes")
    @classmethod
    def notes_must_be_sanitized(cls, value: list[str]) -> list[str]:
        return sanitize_provider_notes(value)

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_utc(cls, value: datetime) -> datetime:
        return normalize_datetime_to_utc(value)

    @model_validator(mode="after")
    def source_must_remain_local_only(self) -> LocalFileSource:
        reject_network_path(self.path)
        reject_path_traversal(self.path)
        if self.real_market_data:
            raise ValueError("local file source cannot claim real market data")
        return self


class LocalFileProviderHealthStatus(BaseModel):
    enabled: bool
    provider_name: str
    synthetic_or_local_only: bool = True
    real_data_claims_allowed: bool = False
    network_allowed: bool = False
    credentials_required: bool = False
    allowed_root: str
    csv_allowed: bool
    parquet_allowed: bool
    symlinks_allowed: bool
    max_rows: int
    status: str
    error: str | None = None


def reject_network_path(path: str | Path) -> None:
    raw = str(path).strip()
    lowered = raw.lower()
    if lowered.startswith(NETWORK_PATH_PREFIXES) or "://" in lowered:
        raise ValueError("network paths are forbidden for local file provider")
    if raw.startswith("\\\\") or raw.startswith("//"):
        raise ValueError("network paths are forbidden for local file provider")


def reject_path_traversal(path: str | Path) -> None:
    if ".." in Path(str(path)).parts:
        raise ValueError("path traversal is forbidden for local file provider")


def resolve_allowed_root(settings: Settings | None = None) -> Path:
    resolved_settings = settings or get_settings()
    root = Path(resolved_settings.local_file_provider_allowed_root).expanduser()
    return root.resolve(strict=False)


def _path_is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _path_contains_symlink(path: Path, allowed_root: Path) -> bool:
    try:
        relative = path.relative_to(allowed_root)
    except ValueError:
        return False
    current = allowed_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def reject_symlink_escape(path: str | Path, allowed_root: str | Path) -> None:
    candidate = Path(path)
    root = Path(allowed_root).resolve(strict=False)
    resolved = candidate.resolve(strict=True)
    if not _path_is_relative_to(resolved, root):
        raise ValueError("symlink escape outside allowed root is forbidden")


def validate_file_extension(path: str | Path, settings: Settings | None = None) -> str:
    resolved_settings = settings or get_settings()
    suffix = Path(path).suffix.lower()
    if suffix == ".csv" and resolved_settings.local_file_provider_allow_csv:
        return suffix
    if suffix == ".parquet" and resolved_settings.local_file_provider_allow_parquet:
        return suffix
    raise ValueError("local file provider supports only configured .csv and .parquet files")


def validate_local_file_path(
    path: str | Path,
    settings: Settings | None = None,
    allowed_root: Path | None = None,
) -> Path:
    resolved_settings = settings or get_settings()
    reject_network_path(path)
    reject_path_traversal(path)
    raw = str(path).strip()
    if SENSITIVE_LOCAL_FILE_PATTERN.search(raw):
        raise ValueError("local file path must not contain secret-like text")

    root = (allowed_root or resolve_allowed_root(resolved_settings)).resolve(strict=False)
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate_without_symlinks = candidate.resolve(strict=False)
    if not _path_is_relative_to(candidate_without_symlinks, root):
        raise ValueError("local file path must remain under the configured allowed root")
    validate_file_extension(candidate_without_symlinks, resolved_settings)
    if not candidate.exists():
        raise FileNotFoundError("local file path does not exist")
    if not candidate.is_file():
        raise ValueError("local file path must point to a file")
    if not resolved_settings.local_file_provider_allow_symlinks and _path_contains_symlink(
        candidate,
        root,
    ):
        raise ValueError("symlinks are forbidden for local file provider")
    resolved = candidate.resolve(strict=True)
    if not _path_is_relative_to(resolved, root):
        raise ValueError("local file path resolves outside the configured allowed root")
    return resolved


def _read_local_frame(source: LocalFileSource, settings: Settings | None = None):
    import polars as pl

    resolved_settings = settings or get_settings()
    path = validate_local_file_path(source.path, resolved_settings)
    suffix = validate_file_extension(path, resolved_settings)
    if source.file_format == DatasetFormat.CSV and suffix != ".csv":
        raise ValueError("local file source format does not match CSV extension")
    if source.file_format == DatasetFormat.PARQUET and suffix != ".parquet":
        raise ValueError("local file source format does not match PARQUET extension")

    frame = pl.read_csv(path) if source.file_format == DatasetFormat.CSV else pl.read_parquet(path)
    if frame.height > resolved_settings.local_file_provider_max_rows:
        raise ValueError("local file row count exceeds configured max_rows")
    return frame


def _require_columns(frame: Any, required: set[str]) -> None:
    columns = set(frame.columns)
    missing = sorted(required - columns)
    if missing:
        raise ValueError(f"local file missing required columns: {', '.join(missing)}")


def _optional_positive_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _optional_positive_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _parse_timestamp(value: Any) -> datetime:
    if isinstance(value, datetime):
        return normalize_datetime_to_utc(value)
    normalized = str(value).strip()
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"
    return normalize_datetime_to_utc(datetime.fromisoformat(normalized))


def _instrument_id_from_row(row: dict[str, Any]) -> InstrumentId:
    return InstrumentId(
        symbol=str(row["symbol"]),
        exchange=Exchange(str(row["exchange"]).strip().upper()),
        segment=MarketSegment(str(row["segment"]).strip().upper()),
    )


def read_local_instrument_master(
    source: LocalFileSource,
    settings: Settings | None = None,
) -> list[Instrument]:
    frame = _read_local_frame(source, settings)
    _require_columns(frame, INSTRUMENT_REQUIRED_COLUMNS)
    instruments: list[Instrument] = []
    for row in frame.iter_rows(named=True):
        instrument = Instrument(
            instrument_id=_instrument_id_from_row(row),
            display_name=str(row["display_name"]),
            asset_class=AssetClass(str(row["asset_class"]).strip().upper()),
            status=InstrumentStatus(str(row.get("status") or InstrumentStatus.UNKNOWN).strip().upper()),
            lot_size=_optional_positive_int(row.get("lot_size")),
            tick_size=_optional_positive_float(row.get("tick_size")),
            metadata={
                "source": LOCAL_FILE_SOURCE_REFERENCE,
                "provider": LOCAL_FILE_PROVIDER_ID.name,
            },
        )
        instruments.append(instrument)
    return instruments


def read_local_ohlcv_bars(
    source: LocalFileSource,
    request: MarketDataRequest,
    settings: Settings | None = None,
) -> list[MarketDataBar]:
    if request.instrument_id is None or request.timeframe is None:
        raise ValueError("local file historical bars require instrument_id and timeframe")
    frame = _read_local_frame(source, settings)
    _require_columns(frame, OHLCV_REQUIRED_COLUMNS)
    bars: list[MarketDataBar] = []
    for row in frame.iter_rows(named=True):
        instrument_id = _instrument_id_from_row(row)
        timeframe = Timeframe(str(row["timeframe"]).strip().upper())
        timestamp = _parse_timestamp(row["timestamp"])
        if instrument_id != request.instrument_id or timeframe != request.timeframe:
            continue
        if request.start and timestamp < request.start:
            continue
        if request.end and timestamp > request.end:
            continue
        bars.append(
            MarketDataBar(
                instrument_id=instrument_id,
                timeframe=timeframe,
                timestamp=timestamp,
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=_optional_positive_float(row.get("volume")),
                open_interest=_optional_positive_float(row.get("open_interest")),
                provider=LOCAL_FILE_PROVIDER_ID,
                quality_status=DataQualityStatus.RAW,
                source_data_reference=LOCAL_FILE_SOURCE_REFERENCE,
            )
        )
    return bars


def _local_file_approval_record(capabilities: Iterable[ProviderCapability]):
    record = create_provider_approval_record(
        provider_name=LOCAL_FILE_PROVIDER_ID.name,
        requested_capabilities=list(capabilities),
        requester="stark_terminal_prompt_24",
        requested_mode=ProviderIntegrationMode.LOCAL_FILE_ONLY,
        notes=[
            "Local File Provider Adapter v0 reads explicit local test/dev files only.",
            "No network calls, scraping, credentials, real ingestion, arbitrary file API, or execution behavior.",
        ],
    )
    return approve_for_design(record, reviewer="stark_terminal_guardrails")


def _local_file_compliance_checklist() -> ProviderComplianceChecklist:
    return ProviderComplianceChecklist(
        provider_name=LOCAL_FILE_PROVIDER_ID.name,
        terms_review_completed=True,
        redistribution_allowed=False,
        storage_allowed=False,
        scraping_prohibited=True,
        credential_handling_reviewed=False,
        rate_limits_documented=False,
        data_quality_plan_ready=True,
        audit_logging_plan_ready=True,
        notes=[
            "Local file test/dev adapter; no provider terms, credentials, network calls, or real data claims.",
        ],
    )


class LocalFileProviderAdapter(MarketDataProvider):
    provider_id = LOCAL_FILE_PROVIDER_ID

    def __init__(
        self,
        settings: Settings | None = None,
        source: LocalFileSource | None = None,
        guardrail_policy: ProviderGuardrailPolicy | None = None,
        approval=None,
        compliance: ProviderComplianceChecklist | None = None,
    ) -> None:
        resolved_settings = settings or get_settings()
        super().__init__(network_calls_allowed=False)
        self.settings = resolved_settings
        self.source = source
        self.guardrail_policy = guardrail_policy or default_provider_guardrail_policy(resolved_settings)
        self.approval = approval or _local_file_approval_record(SUPPORTED_LOCAL_FILE_CAPABILITIES)
        self.compliance = compliance or _local_file_compliance_checklist()
        self.response_validator = MarketDataResponseValidator(settings=resolved_settings)

    def evaluate_guardrails(self) -> ProviderGuardrailResult:
        return evaluate_provider_guardrails(
            provider_name=self.provider_id.name,
            requested_capabilities=SUPPORTED_LOCAL_FILE_CAPABILITIES,
            policy=self.guardrail_policy,
            approval=self.approval,
            compliance=self.compliance,
        )

    def capabilities(self) -> ProviderCapabilityReport:
        guardrail_result = self.evaluate_guardrails()
        enabled = (
            self.settings.local_file_provider_enabled
            and guardrail_result.decision == ProviderGuardrailDecision.ALLOW
            and not self.settings.local_file_provider_allow_network_paths
            and not self.settings.local_file_provider_allow_real_data_claims
        )
        return ProviderCapabilityReport(
            provider=self.provider_id,
            status=ProviderStatus.ENABLED if enabled else ProviderStatus.DISABLED,
            capabilities=SUPPORTED_LOCAL_FILE_CAPABILITIES if enabled else [ProviderCapability.HEALTH_CHECK],
            network_calls_allowed=False,
            schema_version=self.settings.local_file_provider_schema_version,
            notes=[
                "Local File Provider Adapter v0.",
                "Explicit local test/dev files only; no external provider, no live data, no credentials.",
                f"Guardrail decision: {guardrail_result.decision.value}.",
            ],
        )

    def health_check(self) -> LocalFileProviderHealthStatus:
        return check_local_file_provider_health(self.settings)

    def _guardrails_allow(self) -> tuple[bool, str | None]:
        if not self.settings.local_file_provider_enabled:
            return False, "Local file provider is disabled"
        if self.settings.local_file_provider_allow_network_paths:
            return False, "Local file provider network paths are forbidden"
        if self.settings.local_file_provider_allow_real_data_claims:
            return False, "Local file provider real data claims are forbidden"
        result = self.evaluate_guardrails()
        if result.decision != ProviderGuardrailDecision.ALLOW:
            return False, "; ".join(result.reasons)
        return True, None

    def _safe_error_response(self, request: MarketDataRequest, reason: str) -> MarketDataResponse:
        sanitized = sanitize_provider_notes([reason])
        if sanitized == ["[redacted]"]:
            sanitized = ["Local file provider request failed validation"]
        return MarketDataResponse(
            request_id=request.request_id,
            kind=request.kind,
            provider=self.provider_id,
            quality_status=DataQualityStatus.REJECTED,
            source_data_reference=LOCAL_FILE_SOURCE_REFERENCE,
            errors=sanitized or ["Local file provider request failed safely"],
        )

    def _source_or_error(self) -> tuple[LocalFileSource | None, str | None]:
        if self.source is None:
            return None, "Local file provider requires an explicit LocalFileSource"
        return self.source, None

    def _validate_response(self, response: MarketDataResponse) -> MarketDataResponse:
        report = self.response_validator.validate(response)
        if report.status in {ValidationStatus.FAIL, ValidationStatus.BLOCKED}:
            return MarketDataResponse(
                request_id=response.request_id,
                kind=response.kind,
                provider=self.provider_id,
                quality_status=DataQualityStatus.REJECTED,
                source_data_reference=LOCAL_FILE_SOURCE_REFERENCE,
                errors=["Local file provider response failed data quality validation"],
            )
        return response

    def get_instrument_master(self, request: MarketDataRequest) -> MarketDataResponse:
        allowed, reason = self._guardrails_allow()
        if not allowed:
            return self._safe_error_response(request, reason or "Local file provider guardrails blocked request")
        if request.kind not in {
            MarketDataRequestKind.INSTRUMENT_MASTER,
            MarketDataRequestKind.HEALTH_CHECK,
        }:
            return self._safe_error_response(
                request,
                "Local file instrument master supports only instrument master and health check requests",
            )
        source, source_error = self._source_or_error()
        if source_error or source is None:
            return self._safe_error_response(request, source_error or "Local file source missing")
        try:
            instruments = read_local_instrument_master(source, self.settings)
            response = MarketDataResponse(
                request_id=request.request_id,
                kind=request.kind,
                provider=self.provider_id,
                instruments=instruments,
                quality_status=DataQualityStatus.NORMALIZED,
                source_data_reference=LOCAL_FILE_SOURCE_REFERENCE,
            )
            return self._validate_response(response)
        except Exception as exc:
            return self._safe_error_response(request, str(exc))

    def get_historical_bars(self, request: MarketDataRequest) -> MarketDataResponse:
        allowed, reason = self._guardrails_allow()
        if not allowed:
            return self._safe_error_response(request, reason or "Local file provider guardrails blocked request")
        if request.kind != MarketDataRequestKind.HISTORICAL_BARS:
            return self._safe_error_response(
                request,
                "Local file historical bars require HISTORICAL_BARS request kind",
            )
        source, source_error = self._source_or_error()
        if source_error or source is None:
            return self._safe_error_response(request, source_error or "Local file source missing")
        try:
            bars = read_local_ohlcv_bars(source, request, self.settings)
            if not bars:
                return self._safe_error_response(request, "Local file provider found no matching historical bars")
            response = MarketDataResponse(
                request_id=request.request_id,
                kind=request.kind,
                provider=self.provider_id,
                bars=bars,
                quality_status=DataQualityStatus.RAW,
                source_data_reference=LOCAL_FILE_SOURCE_REFERENCE,
            )
            return self._validate_response(response)
        except Exception as exc:
            return self._safe_error_response(request, str(exc))

    def get_latest_bar(self, request: MarketDataRequest) -> MarketDataResponse:
        return self._safe_error_response(
            request,
            "Local file provider does not support real latest bars; use explicit local historical test files only",
        )

    def get_options_chain(self, request: MarketDataRequest) -> MarketDataResponse:
        return self._safe_error_response(
            request,
            "Local file provider does not support options chains; no real provider data is available",
        )

    def get_futures_chain(self, request: MarketDataRequest) -> MarketDataResponse:
        return self._safe_error_response(
            request,
            "Local file provider does not support futures chains; no real provider data is available",
        )


def check_local_file_provider_health(settings: Settings | None = None) -> LocalFileProviderHealthStatus:
    try:
        resolved_settings = settings or get_settings()
        dangerous_defaults_enabled = any(
            (
                resolved_settings.local_file_provider_allow_network_paths,
                resolved_settings.local_file_provider_allow_real_data_claims,
                resolved_settings.execution_apis_enabled,
                resolved_settings.allow_external_market_data_calls,
                resolved_settings.allow_provider_network_calls,
                resolved_settings.provider_credentials_allowed,
            )
        )
        status = "HEALTHY"
        if not resolved_settings.local_file_provider_enabled:
            status = "DISABLED"
        elif dangerous_defaults_enabled:
            status = "BLOCKED"
        return LocalFileProviderHealthStatus(
            enabled=resolved_settings.local_file_provider_enabled,
            provider_name=LOCAL_FILE_PROVIDER_ID.name,
            synthetic_or_local_only=True,
            real_data_claims_allowed=False,
            network_allowed=False,
            credentials_required=False,
            allowed_root=resolved_settings.local_file_provider_allowed_root,
            csv_allowed=resolved_settings.local_file_provider_allow_csv,
            parquet_allowed=resolved_settings.local_file_provider_allow_parquet,
            symlinks_allowed=resolved_settings.local_file_provider_allow_symlinks,
            max_rows=resolved_settings.local_file_provider_max_rows,
            status=status,
            error=None,
        )
    except Exception as exc:  # pragma: no cover - defensive safety path
        return LocalFileProviderHealthStatus(
            enabled=False,
            provider_name=LOCAL_FILE_PROVIDER_ID.name,
            synthetic_or_local_only=True,
            real_data_claims_allowed=False,
            network_allowed=False,
            credentials_required=False,
            allowed_root="data/local_files",
            csv_allowed=True,
            parquet_allowed=True,
            symlinks_allowed=False,
            max_rows=10000,
            status="UNHEALTHY",
            error=re.sub(r"://[^\s]+", "://[redacted]", str(exc)),
        )


def create_local_file_provider(
    settings: Settings | None = None,
    source: LocalFileSource | None = None,
) -> LocalFileProviderAdapter:
    return LocalFileProviderAdapter(settings=settings, source=source)


def sample_local_file_source_template(settings: Settings | None = None) -> LocalFileSource:
    resolved_settings = settings or get_settings()
    return LocalFileSource(
        source_id="local_file_template",
        path=str(Path(resolved_settings.local_file_provider_allowed_root) / "sample_ohlcv.csv"),
        file_format=DatasetFormat.CSV,
        notes=["Template only; not read by API endpoints."],
        schema_version=resolved_settings.local_file_provider_schema_version,
    )
