from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


SENSITIVE_KEY_PARTS = (
    "password",
    "secret",
    "token",
    "credential",
    "database_url",
    "timescale_database_url",
    "redis_url",
    "clickhouse_url",
    "kafka_bootstrap_servers",
)


def _is_sensitive_key(key: str) -> bool:
    normalized = key.lower()
    if normalized.endswith("_configured") or normalized.endswith("_present"):
        return False
    return any(part in normalized for part in SENSITIVE_KEY_PARTS)


def model_to_dict(model: BaseModel) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump(by_alias=True)
    return model.dict()


def to_jsonable(obj: Any) -> Any:
    if hasattr(obj, "safe_settings_snapshot"):
        return to_jsonable(obj.safe_settings_snapshot())

    if isinstance(obj, BaseModel):
        return to_jsonable(model_to_dict(obj))

    if isinstance(obj, Enum):
        return obj.value

    if isinstance(obj, datetime | date):
        return obj.isoformat()

    if isinstance(obj, list):
        return [to_jsonable(item) for item in obj]

    if isinstance(obj, tuple):
        return [to_jsonable(item) for item in obj]

    if isinstance(obj, dict):
        return {
            str(key): to_jsonable(value)
            for key, value in obj.items()
            if not _is_sensitive_key(str(key))
        }

    return obj
