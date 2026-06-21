from __future__ import annotations

import re
from enum import Enum

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import CacheNamespace


_CONTROL_CHARACTER_RE = re.compile(r"[\x00-\x1f\x7f]")
_SAFE_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def validate_cache_key_part(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("cache key parts must be strings")

    normalized = value.strip()
    if not normalized:
        raise ValueError("cache key parts cannot be empty")
    if _CONTROL_CHARACTER_RE.search(normalized):
        raise ValueError("cache key parts cannot contain control characters")
    if "../" in normalized or "..\\" in normalized:
        raise ValueError("cache key parts cannot contain path traversal")
    if "://" in normalized:
        raise ValueError("cache key parts cannot contain URL-like values")
    if ":" in normalized:
        raise ValueError("cache key parts cannot contain ':'")
    return normalized


def _validate_slug(value: str, field_name: str) -> str:
    normalized = value.strip().lower()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    if not _SAFE_SLUG_RE.fullmatch(normalized):
        raise ValueError(f"{field_name} must be a safe slug-like string")
    return normalized


def normalize_namespace(namespace: CacheNamespace | Enum | str) -> str:
    if isinstance(namespace, CacheNamespace):
        value = namespace.value
    elif isinstance(namespace, Enum):
        value = str(namespace.value)
    elif isinstance(namespace, str):
        value = namespace
    else:
        raise TypeError("cache namespace must be an enum or string")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    return _validate_slug(normalized, "cache namespace")


def build_cache_key(
    namespace: CacheNamespace | Enum | str,
    *parts: str,
    settings: Settings | None = None,
) -> str:
    resolved_settings = settings or get_settings()
    prefix = _validate_slug(resolved_settings.cache_key_prefix, "cache key prefix")
    environment = _validate_slug(
        resolved_settings.cache_environment_namespace,
        "cache environment namespace",
    )
    normalized_namespace = normalize_namespace(namespace)
    normalized_parts = [validate_cache_key_part(part) for part in parts]
    return ":".join([prefix, environment, normalized_namespace, *normalized_parts])


class CacheKeyBuilder:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def build(self, namespace: CacheNamespace | Enum | str, *parts: str) -> str:
        return build_cache_key(namespace, *parts, settings=self.settings)

