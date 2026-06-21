from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.instruments.health import check_instrument_master_health
from stark_terminal_data_platform.providers.health import check_provider_contract_health

router = APIRouter()


@router.get("/instruments/health")
def instruments_health() -> dict[str, Any]:
    status = check_instrument_master_health()
    return {
        "service": "stark-terminal-instruments",
        **status.model_dump(),
    }


@router.get("/providers/health")
def providers_health() -> dict[str, Any]:
    status = check_provider_contract_health()
    return {
        "service": "stark-terminal-providers",
        **status.model_dump(),
    }


@router.get("/instruments/sample")
def sample_instruments() -> dict[str, Any]:
    instruments = create_sample_instruments()
    return {
        "service": "stark-terminal-instruments",
        "source": "synthetic",
        "instruments": to_jsonable(instruments),
        "count": len(instruments),
        "live_data": False,
    }
