from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_data_platform.providers.local_file import (
    SUPPORTED_LOCAL_FILE_CAPABILITIES,
    SUPPORTED_LOCAL_FILE_FORMATS,
    UNSUPPORTED_LOCAL_FILE_CAPABILITIES,
    check_local_file_provider_health,
    sample_local_file_source_template,
)

router = APIRouter()


@router.get("/local-file-provider/health")
def local_file_provider_health() -> dict[str, Any]:
    status = check_local_file_provider_health(get_settings())
    return {
        "service": "stark-terminal-local-file-provider",
        **status.model_dump(),
    }


@router.get("/local-file-provider/contracts")
def local_file_provider_contracts() -> dict[str, Any]:
    settings = get_settings()
    template = sample_local_file_source_template(settings)
    return {
        "service": "stark-terminal-local-file-provider",
        "provider_name": "local_file",
        "local_file_only": True,
        "real_market_data": False,
        "network_calls": False,
        "credentials_required": False,
        "supported_formats": sorted(format_.value for format_ in SUPPORTED_LOCAL_FILE_FORMATS),
        "supported_capabilities": [capability.value for capability in SUPPORTED_LOCAL_FILE_CAPABILITIES],
        "unsupported_capabilities": [capability.value for capability in UNSUPPORTED_LOCAL_FILE_CAPABILITIES],
        "path_safety": {
            "allowed_root": settings.local_file_provider_allowed_root,
            "path_traversal_rejected": True,
            "network_paths_allowed": False,
            "symlinks_allowed": settings.local_file_provider_allow_symlinks,
            "api_file_path_parameters": False,
            "arbitrary_file_read_api": False,
        },
        "template_source": {
            "source_id": template.source_id,
            "path": template.path,
            "file_format": template.file_format.value,
            "label": template.label,
            "real_market_data": template.real_market_data,
        },
        "schema_version": settings.local_file_provider_schema_version,
        "note": "Local file provider contracts are local/test/dev only; this endpoint does not read files.",
    }
