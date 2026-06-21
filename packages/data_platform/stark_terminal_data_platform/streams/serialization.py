from __future__ import annotations

import json
from typing import Any

from stark_terminal_core.serialization.json import to_jsonable


class StreamSerializationError(ValueError):
    """Raised when a stream payload cannot be safely serialized."""


FORBIDDEN_PAYLOAD_KEY_PARTS = (
    "password",
    "secret",
    "token",
    "api_key",
    "database_url",
    "redis_url",
    "broker_token",
)


def _is_forbidden_payload_key(key: str) -> bool:
    normalized = key.lower()
    return any(part in normalized for part in FORBIDDEN_PAYLOAD_KEY_PARTS)


def _reject_forbidden_payload_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if _is_forbidden_payload_key(str(key)):
                raise StreamSerializationError("stream payload contains forbidden secret-like keys")
            _reject_forbidden_payload_keys(item)
    elif isinstance(value, list | tuple):
        for item in value:
            _reject_forbidden_payload_keys(item)


def ensure_stream_jsonable(value: Any) -> Any:
    _reject_forbidden_payload_keys(value)
    jsonable = to_jsonable(value)
    _reject_forbidden_payload_keys(jsonable)
    try:
        json.dumps(jsonable, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise StreamSerializationError("value is not JSON-serializable for stream storage") from exc
    return jsonable


def stream_dumps(value: Any) -> str:
    jsonable = ensure_stream_jsonable(value)
    try:
        return json.dumps(jsonable, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise StreamSerializationError("value is not JSON-serializable for stream storage") from exc


def stream_loads(payload: str | bytes | bytearray | None) -> Any:
    if payload is None:
        return None
    if isinstance(payload, bytes | bytearray):
        payload = bytes(payload).decode("utf-8")
    try:
        return json.loads(payload)
    except (TypeError, ValueError) as exc:
        raise StreamSerializationError("stream payload is not valid JSON") from exc
