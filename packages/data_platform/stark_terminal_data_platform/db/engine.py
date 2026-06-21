from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool

from stark_terminal_core.config.settings import Settings, get_settings


SQLITE_DEV_URL = "sqlite+pysqlite:///./stark_terminal_dev.db"


def build_database_url(settings: Settings) -> str:
    if settings.database_url:
        return settings.database_url
    return SQLITE_DEV_URL


def _connect_args_for_url(database_url: str, settings: Settings) -> dict[str, object]:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {"connect_timeout": settings.database_connect_timeout_seconds}


def create_engine_from_settings(settings: Settings | None = None) -> Engine:
    resolved_settings = settings or get_settings()
    database_url = build_database_url(resolved_settings)
    kwargs: dict[str, object] = {
        "echo": resolved_settings.database_echo,
        "pool_pre_ping": resolved_settings.database_pool_pre_ping,
        "connect_args": _connect_args_for_url(database_url, resolved_settings),
    }

    if database_url.startswith("sqlite"):
        if database_url == "sqlite+pysqlite:///:memory:":
            kwargs["poolclass"] = StaticPool
    else:
        kwargs["pool_size"] = resolved_settings.database_pool_size
        kwargs["max_overflow"] = resolved_settings.database_max_overflow

    return create_engine(database_url, **kwargs)
