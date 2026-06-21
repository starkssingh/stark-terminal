from __future__ import annotations

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import make_url

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.db.engine import create_engine_from_settings


class TimescaleHealthStatus(BaseModel):
    configured: bool
    enabled: bool
    reachable: bool
    extension_available: bool | None = None
    hypertables_enabled: bool
    dialect: str | None = None
    error: str | None = None


def check_timescale_health(settings: Settings | None = None) -> TimescaleHealthStatus:
    resolved_settings = settings or get_settings()
    configured = bool(resolved_settings.timescale_database_url)

    if not resolved_settings.timescale_enabled:
        return TimescaleHealthStatus(
            configured=configured,
            enabled=False,
            reachable=False,
            extension_available=None,
            hypertables_enabled=resolved_settings.timescale_create_hypertables,
        )

    if not resolved_settings.timescale_database_url:
        return TimescaleHealthStatus(
            configured=False,
            enabled=True,
            reachable=False,
            extension_available=None,
            hypertables_enabled=resolved_settings.timescale_create_hypertables,
            error="TimescaleDB URL is not configured",
        )

    dialect = None
    try:
        dialect = make_url(resolved_settings.timescale_database_url).drivername.split("+")[0]
        timescale_settings = resolved_settings.model_copy(
            update={"database_url": resolved_settings.timescale_database_url}
        )
        engine = create_engine_from_settings(timescale_settings)
        extension_available: bool | None = None
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            if dialect == "postgresql":
                result = connection.execute(
                    text("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = :name)"),
                    {"name": resolved_settings.timescale_extension_name},
                )
                extension_available = bool(result.scalar())
        engine.dispose()
        return TimescaleHealthStatus(
            configured=True,
            enabled=True,
            reachable=True,
            extension_available=extension_available,
            hypertables_enabled=resolved_settings.timescale_create_hypertables,
            dialect=dialect,
        )
    except Exception as exc:
        return TimescaleHealthStatus(
            configured=configured,
            enabled=True,
            reachable=False,
            extension_available=None,
            hypertables_enabled=resolved_settings.timescale_create_hypertables,
            dialect=dialect,
            error=exc.__class__.__name__,
        )
