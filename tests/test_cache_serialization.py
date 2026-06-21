from datetime import datetime, timezone

import pytest

from stark_terminal_core.domain.decision_object import DecisionObject
from stark_terminal_core.domain.enums import ActionState, MarketSegment, RiskLevel
from stark_terminal_data_platform.cache.serialization import (
    CacheSerializationError,
    cache_dumps,
    cache_loads,
)


def test_cache_serializes_primitives_and_collections() -> None:
    payload = {"count": 1, "items": ["a", "b"], "active": True}

    assert cache_loads(cache_dumps(payload)) == payload


def test_cache_serializes_enums_datetimes_and_pydantic_models() -> None:
    decision = DecisionObject(
        instrument="RELIANCE",
        exchange="NSE",
        segment=MarketSegment.NSE_EQUITY,
        timeframe="DAILY",
        regime=None,
        state=None,
        action_state=ActionState.WATCH,
        confidence=55.0,
        risk=RiskLevel.MEDIUM,
        evidence=[],
        invalidation=None,
        horizon=None,
        source_data_reference=None,
        generated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    restored = cache_loads(cache_dumps({"decision": decision, "state": ActionState.WATCH}))

    assert restored["state"] == "WATCH"
    assert restored["decision"]["instrument"] == "RELIANCE"
    assert restored["decision"]["generated_at"] == "2026-01-01T00:00:00+00:00"


def test_cache_serializes_bytes_with_sentinel_roundtrip() -> None:
    assert cache_loads(cache_dumps(b"abc")) == b"abc"


def test_cache_rejects_unserializable_objects() -> None:
    with pytest.raises(CacheSerializationError):
        cache_dumps(object())

