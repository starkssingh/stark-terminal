from __future__ import annotations

from collections.abc import Generator, Iterator
from contextlib import contextmanager

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.db.engine import create_engine_from_settings


def get_engine(settings: Settings | None = None) -> Engine:
    return create_engine_from_settings(settings or get_settings())


def get_session_factory(settings: Settings | None = None) -> sessionmaker[Session]:
    return sessionmaker(
        bind=get_engine(settings),
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


@contextmanager
def session_scope(settings: Settings | None = None) -> Iterator[Session]:
    session_factory = get_session_factory(settings)
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db_session(settings: Settings | None = None) -> Generator[Session, None, None]:
    session_factory = get_session_factory(settings)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
