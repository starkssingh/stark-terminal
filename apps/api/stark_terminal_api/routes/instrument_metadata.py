from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.db.session import get_db_session
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.repositories.instruments import InstrumentRepository
from stark_terminal_data_platform.services.instruments import InstrumentMetadataService

router = APIRouter()


def _service(session: Session) -> InstrumentMetadataService:
    return InstrumentMetadataService(InstrumentRepository(session))


@router.get("/instrument-metadata/health")
def instrument_metadata_health(session: Session = Depends(get_db_session)) -> dict[str, Any]:
    status = _service(session).health()
    return {
        "service": "stark-terminal-instrument-metadata",
        **status.model_dump(),
    }


@router.get("/instrument-metadata/sample")
def instrument_metadata_sample() -> dict[str, Any]:
    instruments = create_sample_instruments()
    return {
        "service": "stark-terminal-instrument-metadata",
        "synthetic": True,
        "real_market_data": False,
        "instruments": to_jsonable(instruments),
        "count": len(instruments),
    }


@router.get("/instrument-metadata/list")
def instrument_metadata_list(
    limit: int = 100,
    offset: int = 0,
    session: Session = Depends(get_db_session),
) -> dict[str, Any]:
    try:
        instruments = _service(session).list_instruments(limit=limit, offset=offset)
        return {
            "service": "stark-terminal-instrument-metadata",
            "status": "ok",
            "instruments": to_jsonable(instruments),
            "count": len(instruments),
            "synthetic_seeded": False,
            "real_market_data": False,
            "error": None,
        }
    except Exception:
        return {
            "service": "stark-terminal-instrument-metadata",
            "status": "unavailable",
            "instruments": [],
            "count": 0,
            "synthetic_seeded": False,
            "real_market_data": False,
            "error": "InstrumentMetadataRepositoryUnavailable",
        }
