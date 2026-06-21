from __future__ import annotations

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import make_url

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.db.engine import build_database_url, create_engine_from_settings


class DatabaseHealthStatus(BaseModel):
    configured: bool
    reachable: bool
    dialect: str | None
    database_url_present: bool
    error: str | None = None


def check_database_health(settings: Settings | None = None) -> DatabaseHealthStatus:
    resolved_settings = settings or get_settings()
    database_url_present = bool(resolved_settings.database_url)
    database_url = build_database_url(resolved_settings)
    dialect = None

    try:
        dialect = make_url(database_url).drivername.split("+")[0]
        engine = create_engine_from_settings(resolved_settings)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        engine.dispose()
        return DatabaseHealthStatus(
            configured=database_url_present,
            reachable=True,
            dialect=dialect,
            database_url_present=database_url_present,
        )
    except Exception as exc:
        return DatabaseHealthStatus(
            configured=database_url_present,
            reachable=False,
            dialect=dialect,
            database_url_present=database_url_present,
            error=exc.__class__.__name__,
        )
