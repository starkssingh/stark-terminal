from __future__ import annotations

import base64
import json
from typing import Any

from stark_terminal_core.serialization.json import to_jsonable


class CacheSerializationError(ValueError):
    """Raised when a value cannot be safely serialized for cache storage."""


_BYTES_SENTINEL = "__stark_cache_bytes_b64__"


def _restore_special_values(value: Any) -> Any:
    if isinstance(value, dict):
        if set(value) == {_BYTES_SENTINEL}:
            return base64.b64decode(value[_BYTES_SENTINEL].encode("ascii"))
        return {key: _restore_special_values(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_restore_special_values(item) for item in value]
    return value


def ensure_cache_jsonable(value: Any) -> Any:
    if isinstance(value, bytes):
        return {_BYTES_SENTINEL: base64.b64encode(value).decode("ascii")}

    jsonable = to_jsonable(value)
    try:
        json.dumps(jsonable, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise CacheSerializationError("value is not JSON-serializable for cache storage") from exc
    return jsonable


def cache_dumps(value: Any) -> str:
    jsonable = ensure_cache_jsonable(value)
    try:
        return json.dumps(jsonable, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise CacheSerializationError("value is not JSON-serializable for cache storage") from exc


def cache_loads(payload: str | bytes | bytearray | None) -> Any:
    if payload is None:
        return None
    if isinstance(payload, bytes | bytearray):
        payload = bytes(payload).decode("utf-8")
    try:
        parsed = json.loads(payload)
    except (TypeError, ValueError) as exc:
        raise CacheSerializationError("cached payload is not valid JSON") from exc
    return _restore_special_values(parsed)

