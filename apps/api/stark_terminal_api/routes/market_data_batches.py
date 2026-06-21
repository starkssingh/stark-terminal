from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from stark_terminal_core.domain.enums import Timeframe
from stark_terminal_core.domain.market_data_batch import metadata_from_batch
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.db.session import get_db_session
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import SyntheticOHLCVConfig, generate_synthetic_market_data_batch
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.repositories.market_data_batches import MarketDataBatchRepository
from stark_terminal_data_platform.services.market_data_batches import MarketDataBatchMetadataService

router = APIRouter()


def _service(session: Session) -> MarketDataBatchMetadataService:
    return MarketDataBatchMetadataService(MarketDataBatchRepository(session))


def _sample_metadata() -> dict[str, Any]:
    instrument = create_sample_instruments()[0]
    config = SyntheticOHLCVConfig(
        instrument_id=instrument.instrument_id,
        timeframe=Timeframe.DAILY,
        start_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        bar_count=5,
        start_price=100.0,
        seed=42,
        source_data_reference="synthetic-local-test-only",
    )
    batch = generate_synthetic_market_data_batch(config)
    metadata = metadata_from_batch(batch, synthetic=True, fixture_id="synthetic_reliance_daily")
    return to_jsonable(metadata)


@router.get("/market-data-batches/health")
def market_data_batches_health(session: Session = Depends(get_db_session)) -> dict[str, Any]:
    status = _service(session).health()
    return {
        "service": "stark-terminal-market-data-batches",
        **status.model_dump(),
    }


@router.get("/market-data-batches/sample")
def market_data_batches_sample() -> dict[str, Any]:
    return {
        "service": "stark-terminal-market-data-batches",
        "synthetic": True,
        "real_market_data": False,
        "stores_full_bars": False,
        "metadata": _sample_metadata(),
        "note": "synthetic metadata only; no full OHLCV bars are persisted or returned",
    }


@router.get("/market-data-batches/list")
def market_data_batches_list(
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    try:
        metadata = _service(session).list_metadata(limit=limit, offset=offset)
        return {
            "service": "stark-terminal-market-data-batches",
            "status": "ok",
            "metadata": to_jsonable(metadata),
            "count": len(metadata),
            "stores_full_bars": False,
            "real_market_data": False,
            "error": None,
        }
    except Exception:
        return {
            "service": "stark-terminal-market-data-batches",
            "status": "unavailable",
            "metadata": [],
            "count": 0,
            "stores_full_bars": False,
            "real_market_data": False,
            "error": "MarketDataBatchMetadataRepositoryUnavailable",
        }
