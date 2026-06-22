from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.domain.enums import Timeframe
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.db.session import get_db_session
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.repositories.ohlcv_bars import OHLCVBarRepository
from stark_terminal_data_platform.services.synthetic_ohlcv_storage import (
    SyntheticOHLCVStorageResult,
    SyntheticOHLCVStorageService,
)

router = APIRouter()


def _service(session: Session) -> SyntheticOHLCVStorageService:
    return SyntheticOHLCVStorageService(OHLCVBarRepository(session))


def _sample_batch():
    instrument = create_sample_instruments()[0]
    config = SyntheticOHLCVConfig(
        instrument_id=instrument.instrument_id,
        timeframe=Timeframe.DAILY,
        start_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        bar_count=3,
        start_price=100.0,
        seed=42,
        source_data_reference="synthetic-local-test-only",
    )
    return generate_synthetic_market_data_batch(config)


@router.get("/synthetic-ohlcv-storage/health")
def synthetic_ohlcv_storage_health(session: Session = Depends(get_db_session)) -> dict[str, Any]:
    status = _service(session).health()
    return {
        "service": "stark-terminal-synthetic-ohlcv-storage",
        **status.model_dump(),
    }


@router.get("/synthetic-ohlcv-storage/sample")
def synthetic_ohlcv_storage_sample(session: Session = Depends(get_db_session)) -> dict[str, Any]:
    batch = _sample_batch()
    report = _service(session).validate_bars(batch.bars)
    sample_result = SyntheticOHLCVStorageResult(
        batch_id=None,
        stored=False,
        synthetic=True,
        bar_count=len(batch.bars),
        validation_status=report.status.value,
        source_data_reference=batch.bars[0].source_data_reference,
        fixture_id="synthetic_reliance_daily",
        stores_real_data=False,
        status="sample-not-stored",
        error=None,
    )
    return {
        "service": "stark-terminal-synthetic-ohlcv-storage",
        "synthetic": True,
        "real_market_data": False,
        "stores_real_data": False,
        "timescale_required_for_tests": False,
        "sample_result": to_jsonable(sample_result),
        "note": "synthetic/test-only sample metadata; no live market data and no storage write",
    }


@router.get("/synthetic-ohlcv-storage/contracts")
def synthetic_ohlcv_storage_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-synthetic-ohlcv-storage",
        "schema_version": settings.synthetic_ohlcv_storage_schema_version,
        "idempotency_key_description": "instrument_id + timeframe + timestamp + provider_id",
        "storage_scope": "synthetic-only OHLCV operational storage foundation",
        "real_market_data": False,
        "stores_real_data": False,
        "timescale_required_for_tests": False,
    }
