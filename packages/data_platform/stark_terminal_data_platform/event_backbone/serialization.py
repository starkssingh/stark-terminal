from __future__ import annotations

import json
from typing import Any

from stark_terminal_core.serialization.json import to_jsonable


class EventBackboneSerializationError(ValueError):
    """Raised when an event-backbone payload cannot be safely serialized."""


FORBIDDEN_PAYLOAD_KEY_PARTS = (
    "password",
    "secret",
    "token",
    "api_key",
    "database_url",
    "redis_url",
    "clickhouse_url",
    "kafka_bootstrap_servers",
    "broker_token",
    "broker_secret",
)

FORBIDDEN_EVENT_VALUE_PARTS = (
    "execution",
    "execute_order",
    "order_placement",
    "broker_credential",
    "broker_secret",
    "live_trading",
    "live-trading",
    "real_money",
    "real-money",
)


def _is_forbidden_payload_key(key: str) -> bool:
    normalized = key.lower()
    return any(part in normalized for part in FORBIDDEN_PAYLOAD_KEY_PARTS)


def _contains_forbidden_event_value(value: str) -> bool:
    normalized = value.lower()
    return any(part in normalized for part in FORBIDDEN_EVENT_VALUE_PARTS)


def _reject_forbidden_values(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            if _is_forbidden_payload_key(key_text):
                raise EventBackboneSerializationError(
                    "event-backbone payload contains forbidden secret-like keys"
                )
            if _contains_forbidden_event_value(key_text):
                raise EventBackboneSerializationError(
                    "event-backbone payload contains forbidden execution-like keys"
                )
            _reject_forbidden_values(item)
    elif isinstance(value, list | tuple):
        for item in value:
            _reject_forbidden_values(item)
    elif isinstance(value, str) and _contains_forbidden_event_value(value):
        raise EventBackboneSerializationError(
            "event-backbone payload contains forbidden execution-like values"
        )


def ensure_event_backbone_jsonable(value: Any) -> Any:
    _reject_forbidden_values(value)
    jsonable = to_jsonable(value)
    _reject_forbidden_values(jsonable)
    try:
        json.dumps(jsonable, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise EventBackboneSerializationError(
            "value is not JSON-serializable for event-backbone storage"
        ) from exc
    return jsonable


def event_backbone_dumps(value: Any) -> bytes:
    jsonable = ensure_event_backbone_jsonable(value)
    try:
        return json.dumps(jsonable, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise EventBackboneSerializationError(
            "value is not JSON-serializable for event-backbone storage"
        ) from exc


def event_backbone_loads(payload: bytes | bytearray | str | None) -> Any:
    if payload is None:
        return None
    if isinstance(payload, bytes | bytearray):
        payload = bytes(payload).decode("utf-8")
    try:
        return json.loads(payload)
    except (TypeError, ValueError) as exc:
        raise EventBackboneSerializationError(
            "event-backbone payload is not valid JSON"
        ) from exc

