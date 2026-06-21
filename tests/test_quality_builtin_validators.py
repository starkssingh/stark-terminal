from datetime import date, datetime, timezone

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import (
    AdjustmentMode,
    DataLakeZone,
    DataProviderType,
    DatasetFormat,
    DatasetKind,
    Exchange,
    FeatureComputationMode,
    FeatureEntityType,
    FeatureQualityStatus,
    FeatureValueType,
    MarketDataRequestKind,
    OptionType,
    Timeframe,
)
from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId
from stark_terminal_core.domain.market_data import MarketDataBar
from stark_terminal_core.domain.market_data_contracts import (
    MarketDataRequest,
    MarketDataResponse,
)
from stark_terminal_core.domain.options import OptionContract, OptionsChainSnapshot
from stark_terminal_data_platform.features.quality import FeatureQualityReport
from stark_terminal_data_platform.features.values import FeatureEntity, FeatureSnapshot, FeatureValue
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.instruments.universe import (
    InstrumentUniverseSnapshot,
    create_universe_snapshot,
)
from stark_terminal_data_platform.lake.manifest import DatasetManifest
from stark_terminal_data_platform.quality.builtins import (
    DatasetManifestValidator,
    FeatureQualityReportValidator,
    FeatureSnapshotValidator,
    InstrumentUniverseValidator,
    InstrumentValidator,
    MarketDataBarValidator,
    MarketDataRequestValidator,
    MarketDataResponseValidator,
    OptionsChainSnapshotValidator,
    WarehouseTableContractValidator,
)
from stark_terminal_data_platform.quality.enums import ValidationStatus
from stark_terminal_data_platform.warehouse.tables import analytical_ohlcv_table_contract


def _instrument():
    return create_sample_instruments()[0]


def _bar() -> MarketDataBar:
    return MarketDataBar(
        instrument_id=_instrument().instrument_id,
        timeframe=Timeframe.DAILY,
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        open=100,
        high=110,
        low=95,
        close=105,
        volume=1000,
        provider=DataProviderId(name="local_sample", provider_type=DataProviderType.LOCAL_SAMPLE),
        source_data_reference="fixture://ohlcv",
    )


def test_instrument_validator_validates_synthetic_instrument() -> None:
    report = InstrumentValidator().validate(_instrument())

    assert report.status == ValidationStatus.PASS


def test_instrument_validator_catches_invalid_constructed_values() -> None:
    instrument = _instrument().model_copy(update={"lot_size": -1})

    report = InstrumentValidator().validate(instrument)

    assert report.status == ValidationStatus.FAIL
    assert report.error_count == 1


def test_instrument_universe_validator_catches_duplicate_keys() -> None:
    instrument = _instrument()
    snapshot = InstrumentUniverseSnapshot.model_construct(
        snapshot_id="dup",
        source="synthetic",
        instruments=[instrument, instrument],
        created_at=datetime.now(timezone.utc),
        schema_version="v1",
        notes=[],
    )

    report = InstrumentUniverseValidator().validate(snapshot)

    assert report.status == ValidationStatus.FAIL


def test_market_data_bar_validator_validates_valid_bar_and_bad_ohlc() -> None:
    valid_report = MarketDataBarValidator().validate(_bar())
    bad = _bar().model_copy(update={"high": 90})

    bad_report = MarketDataBarValidator().validate(bad)

    assert valid_report.status == ValidationStatus.PASS
    assert bad_report.status == ValidationStatus.FAIL


def test_market_data_bar_validator_requires_source_when_synthetic_not_allowed() -> None:
    bar = _bar().model_copy(update={"source_data_reference": None, "provider": DataProviderId(name="vendor", provider_type=DataProviderType.VENDOR)})

    report = MarketDataBarValidator(
        settings=Settings(data_quality_allow_synthetic_data=False)
    ).validate(bar)

    assert report.status == ValidationStatus.FAIL


def test_market_data_request_validator_catches_missing_historical_fields() -> None:
    request = MarketDataRequest.model_construct(
        request_id="bad",
        kind=MarketDataRequestKind.HISTORICAL_BARS,
        instrument_id=None,
        timeframe=None,
        start=None,
        end=None,
        provider=None,
        adjustment_mode=AdjustmentMode.RAW,
        schema_version="v1",
        created_at=datetime.now(timezone.utc),
    )

    report = MarketDataRequestValidator().validate(request)

    assert report.status == ValidationStatus.FAIL


def test_market_data_response_validator_checks_empty_response() -> None:
    response = MarketDataResponse.model_construct(
        request_id="resp",
        kind=MarketDataRequestKind.HISTORICAL_BARS,
        provider=None,
        bars=[],
        instruments=[],
        quality_status="UNKNOWN",
        source_data_reference=None,
        received_at=datetime.now(timezone.utc),
        errors=[],
    )

    report = MarketDataResponseValidator().validate(response)

    assert report.status == ValidationStatus.FAIL


def test_options_chain_snapshot_validator_validates_snapshot_and_catches_empty() -> None:
    underlying = _instrument().instrument_id
    contract = OptionContract(
        underlying=underlying,
        contract_symbol="RELIANCE26JAN100CE",
        expiry=date(2026, 1, 29),
        strike=100,
        option_type=OptionType.CALL,
        lot_size=1,
    )
    snapshot = OptionsChainSnapshot(
        underlying=underlying,
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        expiry=date(2026, 1, 29),
        contracts=[contract],
        source_data_reference="fixture://options",
    )
    empty = OptionsChainSnapshot.model_construct(
        underlying=underlying,
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        expiry=date(2026, 1, 29),
        contracts=[],
        provider=None,
        source_data_reference="fixture://options",
    )

    assert OptionsChainSnapshotValidator().validate(snapshot).status == ValidationStatus.PASS
    assert OptionsChainSnapshotValidator().validate(empty).status == ValidationStatus.FAIL


def test_dataset_manifest_validator_validates_and_catches_bad_constructed_values() -> None:
    manifest = DatasetManifest(
        dataset_id="dataset",
        name="dataset",
        kind=DatasetKind.OHLCV,
        zone=DataLakeZone.RAW,
        format=DatasetFormat.PARQUET,
        path="raw/dataset",
        row_count=1,
        schema_json={"close": "float"},
        source_data_reference="fixture://dataset",
    )
    bad = DatasetManifest.model_construct(
        dataset_id="bad",
        name="bad",
        kind=DatasetKind.OHLCV,
        zone=DataLakeZone.RAW,
        format=DatasetFormat.PARQUET,
        version="v1",
        path="../bad",
        partitions=[],
        row_count=-1,
        schema_map={"close": 1},
        source_data_reference=None,
        created_at=datetime.now(timezone.utc),
        notes=[],
    )

    assert DatasetManifestValidator().validate(manifest).status == ValidationStatus.PASS
    assert DatasetManifestValidator().validate(bad).status == ValidationStatus.FAIL


def test_feature_snapshot_validator_validates_snapshot() -> None:
    entity = FeatureEntity(entity_type=FeatureEntityType.INSTRUMENT, keys={"instrument_id": "NSE:RELIANCE:NSE_EQUITY"})
    value = FeatureValue(
        feature_name="close_value",
        entity=entity,
        value=100.0,
        value_type=FeatureValueType.FLOAT,
        event_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        source_data_reference="fixture://features",
    )
    snapshot = FeatureSnapshot(
        snapshot_id="snap",
        feature_set_name="price_features",
        values=[value],
        source_data_references=["fixture://features"],
        computation_mode=FeatureComputationMode.MANUAL,
    )

    report = FeatureSnapshotValidator().validate(snapshot)

    assert report.status == ValidationStatus.PASS


def test_feature_quality_report_validator_catches_pass_with_errors() -> None:
    report_obj = FeatureQualityReport.model_construct(
        report_id="q",
        feature_set_name="features",
        feature_set_version="v1",
        status=FeatureQualityStatus.PASS,
        row_count=1,
        missing_value_count=0,
        stale_value_count=0,
        invalid_value_count=0,
        warnings=[],
        errors=["bad"],
        generated_at=datetime.now(timezone.utc),
        source_data_reference="fixture://features",
    )

    report = FeatureQualityReportValidator().validate(report_obj)

    assert report.status == ValidationStatus.FAIL


def test_warehouse_table_contract_validator_validates_default_contract() -> None:
    report = WarehouseTableContractValidator().validate(analytical_ohlcv_table_contract())

    assert report.status == ValidationStatus.PASS


def test_builtin_validator_invalid_type_returns_blocked_report() -> None:
    report = MarketDataBarValidator().validate({"not": "a bar"})

    assert report.status == ValidationStatus.BLOCKED
