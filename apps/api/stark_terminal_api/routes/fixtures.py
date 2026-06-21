from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.fixtures.catalog import create_default_synthetic_fixture_catalog
from stark_terminal_data_platform.fixtures.health import check_fixture_health

router = APIRouter()


@router.get("/fixtures/health")
def fixtures_health() -> dict[str, Any]:
    status = check_fixture_health()
    return {
        "service": "stark-terminal-fixtures",
        **status.model_dump(),
    }


@router.get("/fixtures/catalog")
def fixtures_catalog() -> dict[str, Any]:
    settings = get_settings()
    catalog = create_default_synthetic_fixture_catalog(settings=settings)
    manifests = catalog.list_manifests()
    return {
        "service": "stark-terminal-fixtures",
        "label": settings.synthetic_fixture_label,
        "synthetic": True,
        "real_market_data": False,
        "count": len(manifests),
        "manifests": to_jsonable(manifests),
    }
