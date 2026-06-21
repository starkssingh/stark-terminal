from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from stark_terminal_core.domain.market_data import MarketDataBar, MarketDataBatch
from stark_terminal_core.domain.market_data_batch import (
    MarketDataBatchMetadata,
    MarketDataBatchPersistenceResult,
    batch_metadata_key,
    metadata_from_batch,
)
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments


def _sample_batch() -> MarketDataBatch:
    instrument = create_sample_instruments()[0]
    return generate_synthetic_market_data_batch(
        SyntheticOHLCVConfig(
            instrument_id=instrument.instrument_id,
            timeframe="DAILY",
            start_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            bar_count=5,
            start_price=100.0,
            seed=42,
            source_data_reference="synthetic-local-test-only",
        )
    )


def test_valid_market_data_batch_metadata_creation() -> None:
    metadata = metadata_from_batch(_sample_batch(), synthetic=True, fixture_id="fixture_1")

    assert metadata.batch_id.startswith("batch_")
    assert metadata.row_count == 5
    assert metadata.start_timestamp <= metadata.end_timestamp
    assert metadata.synthetic is True
    assert metadata.fixture_id == "fixture_1"
    assert batch_metadata_key(metadata)


@pytest.mark.parametrize(
    "field,value",
    [
        ("batch_id", ""),
        ("row_count", 0),
        ("source_data_reference", ""),
        ("schema_version", ""),
    ],
)
def test_market_data_batch_metadata_rejects_invalid_fields(field: str, value: object) -> None:
    metadata = metadata_from_batch(_sample_batch(), synthetic=True)
    payload = metadata.model_dump()
    payload[field] = value

    with pytest.raises(ValidationError):
        MarketDataBatchMetadata(**payload)


def test_market_data_batch_metadata_rejects_invalid_time_range() -> None:
    metadata = metadata_from_batch(_sample_batch(), synthetic=True)
    payload = metadata.model_dump()
    payload["start_timestamp"], payload["end_timestamp"] = payload["end_timestamp"], payload["start_timestamp"]

    with pytest.raises(ValidationError):
        MarketDataBatchMetadata(**payload)


def test_synthetic_metadata_requires_synthetic_local_test_reference() -> None:
    metadata = metadata_from_batch(_sample_batch(), synthetic=False)
    payload = metadata.model_dump()
    payload["synthetic"] = True
    payload["source_data_reference"] = "manual"

    with pytest.raises(ValidationError):
        MarketDataBatchMetadata(**payload)


def test_metadata_from_batch_requires_single_instrument_and_timeframe() -> None:
    batch = _sample_batch()
    other_bar = batch.bars[0].model_copy(
        update={"instrument_id": create_sample_instruments()[1].instrument_id}
    )

    with pytest.raises(ValueError):
        metadata_from_batch(MarketDataBatch(bars=[batch.bars[0], other_bar], provider=batch.provider), synthetic=True)


def test_metadata_from_batch_requires_source_reference() -> None:
    batch = _sample_batch()
    bad_bar = MarketDataBar.model_construct(**{**batch.bars[0].model_dump(), "source_data_reference": None})

    with pytest.raises(ValueError):
        metadata_from_batch(MarketDataBatch(bars=[bad_bar], provider=batch.provider), synthetic=True)


def test_persistence_result_sanitizes_errors() -> None:
    result = MarketDataBatchPersistenceResult(
        batch_id="batch_1",
        persisted=False,
        status="failed",
        error="password leaked",
    )

    assert result.error == "sanitized_error"
