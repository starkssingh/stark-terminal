from __future__ import annotations

from datetime import datetime
from typing import Any

from stark_terminal_core.domain.instrument import Instrument
from stark_terminal_core.domain.market_data import MarketDataBar
from stark_terminal_core.domain.market_data_contracts import MarketDataRequest, MarketDataResponse
from stark_terminal_core.domain.options import OptionsChainSnapshot
from stark_terminal_data_platform.features.quality import FeatureQualityReport
from stark_terminal_data_platform.features.values import FeatureSnapshot
from stark_terminal_data_platform.instruments.universe import InstrumentUniverseSnapshot
from stark_terminal_data_platform.lake.manifest import DatasetManifest
from stark_terminal_data_platform.quality.enums import ValidationScope, ValidationSeverity
from stark_terminal_data_platform.quality.results import ValidationResult
from stark_terminal_data_platform.quality.validators import BaseValidator
from stark_terminal_data_platform.warehouse.tables import WarehouseTableContract, validate_table_identifier


def _has_source_reference(subject: object) -> bool:
    source = getattr(subject, "source_data_reference", None)
    sources = getattr(subject, "source_data_references", None)
    return bool(source) or bool(sources)


def _is_synthetic_allowed(subject: object, allow_synthetic: bool) -> bool:
    if not allow_synthetic:
        return False
    provider = getattr(subject, "provider", None)
    provider_name = getattr(provider, "name", "")
    if isinstance(provider_name, str) and "sample" in provider_name.lower():
        return True
    metadata = getattr(subject, "metadata", {})
    if isinstance(metadata, dict) and str(metadata.get("fixture", "")).lower() == "synthetic":
        return True
    return provider is None


def _is_timezone_aware(value: datetime | None) -> bool:
    return value is not None and value.tzinfo is not None and value.utcoffset() is not None


class InstrumentValidator(BaseValidator):
    scope = ValidationScope.INSTRUMENT
    name = "instrument_validator"
    expected_type = Instrument

    def subject_id(self, subject: object) -> str:
        return str(getattr(subject, "instrument_id", "instrument"))

    def _validate(self, subject: Instrument) -> Any:
        results: list[ValidationResult] = []
        if not subject.display_name.strip():
            results.append(self._fail(subject, "INSTRUMENT_DISPLAY_NAME_EMPTY", "display_name is required", "display_name"))
        if subject.lot_size is not None and subject.lot_size <= 0:
            results.append(self._fail(subject, "INSTRUMENT_LOT_SIZE_INVALID", "lot_size must be positive", "lot_size"))
        if subject.tick_size is not None and subject.tick_size <= 0:
            results.append(self._fail(subject, "INSTRUMENT_TICK_SIZE_INVALID", "tick_size must be positive", "tick_size"))
        if str(subject.instrument_id) != f"{subject.instrument_id.exchange.value}:{subject.instrument_id.symbol}:{subject.instrument_id.segment.value}":
            results.append(self._fail(subject, "INSTRUMENT_KEY_UNSTABLE", "instrument key is not stable", "instrument_id"))
        return self._report(subject, results or [self._pass(subject)])


class InstrumentUniverseValidator(BaseValidator):
    scope = ValidationScope.INSTRUMENT_UNIVERSE
    name = "instrument_universe_validator"
    expected_type = InstrumentUniverseSnapshot

    def _validate(self, subject: InstrumentUniverseSnapshot) -> Any:
        results: list[ValidationResult] = []
        if not subject.source.strip():
            results.append(self._fail(subject, "UNIVERSE_SOURCE_EMPTY", "universe source is required", "source"))
        if not subject.instruments:
            results.append(self._fail(subject, "UNIVERSE_EMPTY", "instrument universe cannot be empty", "instruments"))
        keys = [str(item.instrument_id) for item in subject.instruments]
        if len(keys) != len(set(keys)):
            results.append(self._fail(subject, "UNIVERSE_DUPLICATE_KEYS", "duplicate instrument keys found", "instruments"))
        return self._report(subject, results or [self._pass(subject)])


class MarketDataBarValidator(BaseValidator):
    scope = ValidationScope.MARKET_DATA_BAR
    name = "market_data_bar_validator"
    expected_type = MarketDataBar

    def subject_id(self, subject: object) -> str:
        instrument = getattr(subject, "instrument_id", "unknown")
        timestamp = getattr(subject, "timestamp", "unknown")
        return f"{instrument}:{timestamp}"

    def _validate(self, subject: MarketDataBar) -> Any:
        results: list[ValidationResult] = []
        for field_name in ("open", "high", "low", "close"):
            if getattr(subject, field_name) <= 0:
                results.append(self._fail(subject, "BAR_PRICE_NON_POSITIVE", "OHLC prices must be positive", field_name))
        if subject.high < max(subject.open, subject.close, subject.low):
            results.append(self._fail(subject, "BAR_HIGH_LOW_INCONSISTENT", "high must cover open/close/low", "high"))
        if subject.low > min(subject.open, subject.close, subject.high):
            results.append(self._fail(subject, "BAR_HIGH_LOW_INCONSISTENT", "low must be below open/close/high", "low"))
        if subject.volume is not None and subject.volume < 0:
            results.append(self._fail(subject, "BAR_VOLUME_NEGATIVE", "volume cannot be negative", "volume"))
        if subject.open_interest is not None and subject.open_interest < 0:
            results.append(self._fail(subject, "BAR_OPEN_INTEREST_NEGATIVE", "open_interest cannot be negative", "open_interest"))
        if self.settings.data_quality_require_timezone_aware_timestamps and not _is_timezone_aware(subject.timestamp):
            results.append(self._fail(subject, "BAR_TIMESTAMP_NOT_AWARE", "timestamp must be timezone-aware", "timestamp"))
        if (
            self.settings.data_quality_require_source_reference
            and not _has_source_reference(subject)
            and not _is_synthetic_allowed(subject, self.settings.data_quality_allow_synthetic_data)
        ):
            results.append(self._fail(subject, "BAR_SOURCE_REFERENCE_MISSING", "source_data_reference is required", "source_data_reference"))
        return self._report(subject, results or [self._pass(subject)], subject.source_data_reference)


class MarketDataRequestValidator(BaseValidator):
    scope = ValidationScope.MARKET_DATA_REQUEST
    name = "market_data_request_validator"
    expected_type = MarketDataRequest

    def _validate(self, subject: MarketDataRequest) -> Any:
        results: list[ValidationResult] = []
        if subject.start and subject.end and subject.start >= subject.end:
            results.append(self._fail(subject, "REQUEST_RANGE_INVALID", "start must be before end", "start"))
        if subject.kind == "HISTORICAL_BARS":
            missing = [
                name
                for name in ("instrument_id", "timeframe", "start", "end")
                if getattr(subject, name) is None
            ]
            for field_name in missing:
                results.append(self._fail(subject, "REQUEST_REQUIRED_FIELD_MISSING", "historical bars request missing required field", field_name))
        return self._report(subject, results or [self._pass(subject)])


class MarketDataResponseValidator(BaseValidator):
    scope = ValidationScope.MARKET_DATA_RESPONSE
    name = "market_data_response_validator"
    expected_type = MarketDataResponse

    def _validate(self, subject: MarketDataResponse) -> Any:
        results: list[ValidationResult] = []
        if not subject.bars and not subject.instruments and not subject.errors:
            results.append(self._fail(subject, "RESPONSE_EMPTY", "market data response must contain bars, instruments, or errors"))
        bar_validator = MarketDataBarValidator(settings=self.settings)
        for bar in subject.bars:
            bar_report = bar_validator.validate(bar)
            if bar_report.status in {"FAIL", "BLOCKED"}:
                results.append(self._fail(subject, "RESPONSE_BAR_INVALID", "response contains invalid bar", "bars"))
        for error in subject.errors:
            if any(token in error.lower() for token in ("password", "secret", "token", "api_key")):
                results.append(self._fail(subject, "RESPONSE_ERROR_UNSANITIZED", "response error appears unsanitized", "errors"))
        return self._report(subject, results or [self._pass(subject)], subject.source_data_reference)


class OptionsChainSnapshotValidator(BaseValidator):
    scope = ValidationScope.OPTIONS_CHAIN_SNAPSHOT
    name = "options_chain_snapshot_validator"
    expected_type = OptionsChainSnapshot

    def subject_id(self, subject: object) -> str:
        return f"{getattr(subject, 'underlying', 'unknown')}:{getattr(subject, 'expiry', 'unknown')}"

    def _validate(self, subject: OptionsChainSnapshot) -> Any:
        results: list[ValidationResult] = []
        if not subject.contracts:
            results.append(self._fail(subject, "OPTIONS_CHAIN_EMPTY", "options chain contracts cannot be empty", "contracts"))
        for contract in subject.contracts:
            if contract.underlying != subject.underlying:
                results.append(self._fail(subject, "OPTIONS_CHAIN_UNDERLYING_MISMATCH", "contract underlying mismatch", "contracts"))
            if contract.expiry != subject.expiry:
                results.append(self._fail(subject, "OPTIONS_CHAIN_EXPIRY_MISMATCH", "contract expiry mismatch", "contracts"))
        if self.settings.data_quality_require_timezone_aware_timestamps and not _is_timezone_aware(subject.timestamp):
            results.append(self._fail(subject, "OPTIONS_CHAIN_TIMESTAMP_NOT_AWARE", "timestamp must be timezone-aware", "timestamp"))
        if (
            self.settings.data_quality_require_source_reference
            and not _has_source_reference(subject)
            and not _is_synthetic_allowed(subject, self.settings.data_quality_allow_synthetic_data)
        ):
            results.append(self._fail(subject, "OPTIONS_CHAIN_SOURCE_REFERENCE_MISSING", "source_data_reference is required", "source_data_reference"))
        return self._report(subject, results or [self._pass(subject)], subject.source_data_reference)


class DatasetManifestValidator(BaseValidator):
    scope = ValidationScope.DATASET_MANIFEST
    name = "dataset_manifest_validator"
    expected_type = DatasetManifest

    def subject_id(self, subject: object) -> str:
        return str(getattr(subject, "dataset_id", "dataset_manifest"))

    def _validate(self, subject: DatasetManifest) -> Any:
        results: list[ValidationResult] = []
        if not subject.path.strip() or "../" in subject.path or "..\\" in subject.path:
            results.append(self._fail(subject, "MANIFEST_PATH_UNSAFE", "manifest path is empty or contains traversal", "path"))
        if subject.row_count is not None and subject.row_count < 0:
            results.append(self._fail(subject, "MANIFEST_ROW_COUNT_NEGATIVE", "row_count cannot be negative", "row_count"))
        if not all(isinstance(value, str) for value in subject.schema_map.values()):
            results.append(self._fail(subject, "MANIFEST_SCHEMA_INVALID", "schema_json values must be strings", "schema_json"))
        return self._report(subject, results or [self._pass(subject)], subject.source_data_reference)


class FeatureSnapshotValidator(BaseValidator):
    scope = ValidationScope.FEATURE_SNAPSHOT
    name = "feature_snapshot_validator"
    expected_type = FeatureSnapshot

    def subject_id(self, subject: object) -> str:
        return str(getattr(subject, "snapshot_id", "feature_snapshot"))

    def _validate(self, subject: FeatureSnapshot) -> Any:
        results: list[ValidationResult] = []
        if not subject.values:
            results.append(self._fail(subject, "FEATURE_SNAPSHOT_EMPTY", "feature snapshot values cannot be empty", "values"))
        if self.settings.data_quality_require_source_reference and not subject.source_data_references:
            results.append(self._fail(subject, "FEATURE_SNAPSHOT_SOURCE_MISSING", "source references are required", "source_data_references"))
        for value in subject.values:
            if self.settings.data_quality_require_timezone_aware_timestamps and not _is_timezone_aware(value.event_timestamp):
                results.append(self._fail(subject, "FEATURE_VALUE_TIMESTAMP_NOT_AWARE", "feature value event_timestamp must be timezone-aware", "values"))
        source_ref = subject.source_data_references[0] if subject.source_data_references else None
        return self._report(subject, results or [self._pass(subject)], source_ref)


class FeatureQualityReportValidator(BaseValidator):
    scope = ValidationScope.FEATURE_QUALITY_REPORT
    name = "feature_quality_report_validator"
    expected_type = FeatureQualityReport

    def subject_id(self, subject: object) -> str:
        return str(getattr(subject, "report_id", "feature_quality_report"))

    def _validate(self, subject: FeatureQualityReport) -> Any:
        results: list[ValidationResult] = []
        for field_name in ("row_count", "missing_value_count", "stale_value_count", "invalid_value_count"):
            value = getattr(subject, field_name)
            if value is not None and value < 0:
                results.append(self._fail(subject, "FEATURE_QUALITY_COUNT_NEGATIVE", "quality counts cannot be negative", field_name))
        if subject.status == "PASS" and subject.errors:
            results.append(self._fail(subject, "FEATURE_QUALITY_PASS_WITH_ERRORS", "PASS reports cannot contain errors", "errors"))
        return self._report(subject, results or [self._pass(subject)], subject.source_data_reference)


class WarehouseTableContractValidator(BaseValidator):
    scope = ValidationScope.WAREHOUSE_TABLE_CONTRACT
    name = "warehouse_table_contract_validator"
    expected_type = WarehouseTableContract

    def subject_id(self, subject: object) -> str:
        return str(getattr(subject, "table_name", "warehouse_table_contract"))

    def _validate(self, subject: WarehouseTableContract) -> Any:
        results: list[ValidationResult] = []
        try:
            validate_table_identifier(subject.table_name)
        except Exception:
            results.append(self._fail(subject, "WAREHOUSE_TABLE_NAME_UNSAFE", "table_name is unsafe", "table_name"))
        if not subject.columns:
            results.append(self._fail(subject, "WAREHOUSE_COLUMNS_EMPTY", "columns cannot be empty", "columns"))
        if not subject.order_by:
            results.append(self._fail(subject, "WAREHOUSE_ORDER_BY_EMPTY", "order_by cannot be empty", "order_by"))
        column_names = {column.name for column in subject.columns}
        for column_name in subject.order_by:
            if column_name not in column_names:
                results.append(self._fail(subject, "WAREHOUSE_ORDER_BY_MISSING_COLUMN", "order_by column not found", "order_by"))
        return self._report(subject, results or [self._pass(subject)])


BUILTIN_VALIDATOR_CLASSES = [
    InstrumentValidator,
    InstrumentUniverseValidator,
    MarketDataBarValidator,
    MarketDataRequestValidator,
    MarketDataResponseValidator,
    OptionsChainSnapshotValidator,
    DatasetManifestValidator,
    FeatureSnapshotValidator,
    FeatureQualityReportValidator,
    WarehouseTableContractValidator,
]


def create_builtin_validators(settings=None) -> list[BaseValidator]:
    return [validator_cls(settings=settings) for validator_cls in BUILTIN_VALIDATOR_CLASSES]
