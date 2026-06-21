from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_data_platform.warehouse.memory import InMemoryWarehouseQueryRecorder


class WarehouseUnavailableError(RuntimeError):
    """Raised when the ClickHouse warehouse is unavailable by configuration or connection."""


def _sanitize_error(error: BaseException | str) -> str:
    text = error.__class__.__name__ if isinstance(error, BaseException) else str(error)
    lowered = text.lower()
    if any(term in lowered for term in ("password", "secret", "token", "credential", "clickhouse_url")):
        return "SanitizedWarehouseError"
    return text


def _configured(settings: Settings) -> bool:
    return bool(settings.clickhouse_url) or bool(settings.clickhouse_host)


class ClickHouseWarehouseClient:
    def __init__(
        self,
        settings: Settings | None = None,
        recorder: InMemoryWarehouseQueryRecorder | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.recorder = recorder
        self._client: Any | None = None
        self._closed = False
        if not self.settings.clickhouse_enabled or not _configured(self.settings):
            if self.settings.clickhouse_use_memory_fallback:
                self.recorder = self.recorder or InMemoryWarehouseQueryRecorder()
            else:
                self.recorder = None

    @property
    def backend(self) -> str:
        if self.recorder is not None and (not self.settings.clickhouse_enabled or self._client is None):
            return "memory"
        if self.settings.clickhouse_enabled:
            return "clickhouse"
        return "none"

    def _connection_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "host": self.settings.clickhouse_host,
            "port": self.settings.clickhouse_port,
            "database": self.settings.clickhouse_database,
            "username": self.settings.clickhouse_user,
            "password": self.settings.clickhouse_password,
            "secure": self.settings.clickhouse_secure,
            "connect_timeout": self.settings.clickhouse_connect_timeout_seconds,
            "send_receive_timeout": self.settings.clickhouse_send_receive_timeout_seconds,
        }
        if self.settings.clickhouse_url:
            parsed = urlparse(self.settings.clickhouse_url)
            if parsed.scheme not in {"http", "https", "clickhouse"}:
                raise WarehouseUnavailableError("ClickHouse URL scheme is unsupported")
            if parsed.hostname:
                kwargs["host"] = parsed.hostname
            if parsed.port:
                kwargs["port"] = parsed.port
            if parsed.username:
                kwargs["username"] = parsed.username
            if parsed.password:
                kwargs["password"] = parsed.password
            if parsed.path and parsed.path != "/":
                kwargs["database"] = parsed.path.strip("/")
            kwargs["secure"] = parsed.scheme == "https" or self.settings.clickhouse_secure
        return {key: value for key, value in kwargs.items() if value is not None}

    def _get_clickhouse_client(self) -> Any:
        if not self.settings.clickhouse_enabled:
            raise WarehouseUnavailableError("ClickHouse warehouse is disabled")
        if self._client is None:
            try:
                import clickhouse_connect

                self._client = clickhouse_connect.get_client(**self._connection_kwargs())
            except WarehouseUnavailableError:
                raise
            except Exception as exc:
                raise WarehouseUnavailableError(_sanitize_error(exc)) from exc
        return self._client

    def ping(self) -> bool:
        if self.recorder is not None and not self.settings.clickhouse_enabled:
            return True
        client = self._get_clickhouse_client()
        try:
            result = client.query("SELECT 1")
            return result is not None
        except Exception as exc:
            raise WarehouseUnavailableError(_sanitize_error(exc)) from exc

    def execute(self, query: str, parameters: dict[str, Any] | None = None) -> Any:
        if self.recorder is not None and not self.settings.clickhouse_enabled:
            self.recorder.record(query, parameters)
            return None
        client = self._get_clickhouse_client()
        try:
            return client.command(query, parameters=parameters)
        except Exception as exc:
            raise WarehouseUnavailableError(_sanitize_error(exc)) from exc

    def query(self, query: str, parameters: dict[str, Any] | None = None) -> Any:
        if self.recorder is not None and not self.settings.clickhouse_enabled:
            self.recorder.record(query, parameters)
            return []
        client = self._get_clickhouse_client()
        try:
            return client.query(query, parameters=parameters)
        except Exception as exc:
            raise WarehouseUnavailableError(_sanitize_error(exc)) from exc

    def close(self) -> None:
        if self._client is not None and hasattr(self._client, "close"):
            self._client.close()
        self._closed = True

    def __enter__(self) -> ClickHouseWarehouseClient:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()
