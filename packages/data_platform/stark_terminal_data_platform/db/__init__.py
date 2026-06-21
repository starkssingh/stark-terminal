"""Database foundation for Stark Terminal."""

from stark_terminal_data_platform.db.base import Base
from stark_terminal_data_platform.db.engine import build_database_url, create_engine_from_settings
from stark_terminal_data_platform.db.health import DatabaseHealthStatus, check_database_health
from stark_terminal_data_platform.db.session import (
    get_db_session,
    get_engine,
    get_session_factory,
    session_scope,
)

__all__ = [
    "Base",
    "DatabaseHealthStatus",
    "build_database_url",
    "check_database_health",
    "create_engine_from_settings",
    "get_db_session",
    "get_engine",
    "get_session_factory",
    "session_scope",
]
