from __future__ import annotations

import re

from stark_terminal_core.domain.enums import Exchange, MarketSegment
from stark_terminal_core.domain.identifiers import InstrumentId


SAFE_SYMBOL_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9._&-]*$")


def validate_symbol(symbol: str) -> str:
    if not isinstance(symbol, str):
        raise TypeError("symbol must be a string")
    normalized = symbol.strip().upper()
    if not normalized:
        raise ValueError("symbol cannot be empty")
    if any(ord(char) < 32 for char in normalized):
        raise ValueError("symbol cannot contain control characters")
    if "../" in normalized or "..\\" in normalized or "/" in normalized or "\\" in normalized:
        raise ValueError("symbol cannot contain path traversal or path separators")
    if "://" in normalized:
        raise ValueError("symbol cannot be URL-like")
    if ".." in normalized:
        raise ValueError("symbol cannot contain path traversal-like segments")
    if not SAFE_SYMBOL_PATTERN.fullmatch(normalized):
        raise ValueError("symbol contains unsupported characters")
    return normalized


def normalize_symbol(symbol: str) -> str:
    return validate_symbol(symbol)


def normalize_exchange(exchange: str | Exchange) -> Exchange:
    if isinstance(exchange, Exchange):
        return exchange
    if not isinstance(exchange, str):
        raise TypeError("exchange must be a string or Exchange")
    normalized = exchange.strip().upper()
    if not normalized:
        raise ValueError("exchange cannot be empty")
    return Exchange(normalized)


def normalize_segment(segment: str | MarketSegment) -> MarketSegment:
    if isinstance(segment, MarketSegment):
        return segment
    if not isinstance(segment, str):
        raise TypeError("segment must be a string or MarketSegment")
    normalized = segment.strip().upper()
    if not normalized:
        raise ValueError("segment cannot be empty")
    return MarketSegment(normalized)


def build_instrument_key(
    symbol: str,
    exchange: str | Exchange,
    segment: str | MarketSegment,
) -> str:
    instrument_id = InstrumentId(
        symbol=normalize_symbol(symbol),
        exchange=normalize_exchange(exchange),
        segment=normalize_segment(segment),
    )
    return str(instrument_id)


def parse_instrument_key(key: str) -> InstrumentId:
    if not isinstance(key, str):
        raise TypeError("instrument key must be a string")
    parts = key.strip().split(":")
    if len(parts) != 3:
        raise ValueError("instrument key must use EXCHANGE:SYMBOL:SEGMENT format")
    exchange, symbol, segment = parts
    return InstrumentId(
        symbol=normalize_symbol(symbol),
        exchange=normalize_exchange(exchange),
        segment=normalize_segment(segment),
    )
