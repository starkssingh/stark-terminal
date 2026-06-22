import os
from pathlib import Path

import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.providers.local_file import (
    reject_network_path,
    reject_path_traversal,
    resolve_allowed_root,
    validate_file_extension,
    validate_local_file_path,
)


def _settings(root: Path, **overrides) -> Settings:
    return Settings(local_file_provider_allowed_root=str(root), **overrides)


def test_allowed_root_resolves_with_pathlib(tmp_path: Path) -> None:
    settings = _settings(tmp_path)

    assert resolve_allowed_root(settings) == tmp_path.resolve()


def test_valid_file_under_allowed_root_is_accepted(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.csv"
    file_path.write_text("symbol,exchange,segment,display_name,asset_class\nABC,NSE,NSE_EQUITY,ABC,EQUITY\n")

    resolved = validate_local_file_path(file_path, _settings(tmp_path))

    assert resolved == file_path.resolve()
    assert validate_file_extension(file_path, _settings(tmp_path)) == ".csv"


def test_relative_file_under_allowed_root_is_accepted(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.csv"
    file_path.write_text("symbol,exchange,segment,display_name,asset_class\nABC,NSE,NSE_EQUITY,ABC,EQUITY\n")

    resolved = validate_local_file_path("sample.csv", _settings(tmp_path))

    assert resolved == file_path.resolve()


def test_traversal_and_missing_files_are_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        reject_path_traversal("../outside.csv")

    with pytest.raises(FileNotFoundError):
        validate_local_file_path("missing.csv", _settings(tmp_path))


def test_unsupported_extension_and_network_paths_are_rejected(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.txt"
    file_path.write_text("x\n")

    with pytest.raises(ValueError):
        validate_local_file_path(file_path, _settings(tmp_path))

    for path in ["https://example.com/data.csv", "s3://bucket/data.csv", "//server/share/data.csv"]:
        with pytest.raises(ValueError):
            reject_network_path(path)


def test_absolute_path_outside_allowed_root_is_rejected(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside_local_file_provider.csv"
    outside.write_text("x\n")
    try:
        with pytest.raises(ValueError):
            validate_local_file_path(outside, _settings(tmp_path))
    finally:
        outside.unlink(missing_ok=True)


def test_symlink_escape_is_rejected_where_supported(tmp_path: Path) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlink not supported")

    outside = tmp_path.parent / "outside_symlink_escape.csv"
    outside.write_text("x\n")
    link = tmp_path / "escape.csv"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        outside.unlink(missing_ok=True)
        pytest.skip("symlink creation not supported")

    try:
        with pytest.raises(ValueError):
            validate_local_file_path(link, _settings(tmp_path))
    finally:
        link.unlink(missing_ok=True)
        outside.unlink(missing_ok=True)
