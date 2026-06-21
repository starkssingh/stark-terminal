from __future__ import annotations

from pydantic import BaseModel

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments
from stark_terminal_data_platform.instruments.master import InstrumentMaster, LocalInstrumentMaster


class InstrumentMasterHealthStatus(BaseModel):
    configured: bool
    mode: str
    source: str
    instrument_count: int
    external_calls_allowed: bool
    provider_network_calls_allowed: bool
    status: str
    error: str | None = None


def _default_master(settings: Settings) -> InstrumentMaster | None:
    if settings.instrument_master_mode != "local":
        return None
    return LocalInstrumentMaster(
        create_sample_instruments(),
        source=settings.instrument_master_source,
        schema_version=settings.market_data_contract_schema_version,
    )


def check_instrument_master_health(
    settings: Settings | None = None,
    instrument_master: InstrumentMaster | None = None,
) -> InstrumentMasterHealthStatus:
    resolved_settings = settings or get_settings()
    status = "DISABLED"
    count = 0
    error: str | None = None

    try:
        master = instrument_master or _default_master(resolved_settings)
        if master is not None:
            count = len(master.list_instruments())
            status = "HEALTHY"
        elif resolved_settings.instrument_master_mode == "external_planned":
            status = "PLANNED"
        else:
            status = "DISABLED"
    except Exception:
        status = "UNHEALTHY"
        error = "InstrumentMasterHealthCheckFailed"

    return InstrumentMasterHealthStatus(
        configured=resolved_settings.instrument_master_mode != "disabled",
        mode=resolved_settings.instrument_master_mode,
        source=resolved_settings.instrument_master_source,
        instrument_count=count,
        external_calls_allowed=resolved_settings.allow_external_market_data_calls,
        provider_network_calls_allowed=resolved_settings.allow_provider_network_calls,
        status=status,
        error=error,
    )
