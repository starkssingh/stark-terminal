from datetime import timezone

import pytest
from pydantic import ValidationError

from stark_terminal_core.domain.enums import DatasetFormat
from stark_terminal_data_platform.providers.local_file import (
    LOCAL_FILE_SOURCE_REFERENCE,
    LocalFileSource,
)


def test_valid_local_file_source_contract() -> None:
    source = LocalFileSource(
        source_id="source_csv",
        path="sample.csv",
        file_format=DatasetFormat.CSV,
        notes=["local test/dev source"],
    )

    assert source.source_id == "source_csv"
    assert source.file_format == DatasetFormat.CSV
    assert source.label == LOCAL_FILE_SOURCE_REFERENCE
    assert source.synthetic is True
    assert source.real_market_data is False
    assert source.created_at.tzinfo == timezone.utc


def test_local_file_source_rejects_empty_required_text() -> None:
    with pytest.raises(ValidationError):
        LocalFileSource(source_id="", path="sample.csv", file_format=DatasetFormat.CSV)

    with pytest.raises(ValidationError):
        LocalFileSource(source_id="source_csv", path="", file_format=DatasetFormat.CSV)


def test_local_file_source_rejects_unsupported_format() -> None:
    with pytest.raises(ValidationError):
        LocalFileSource(
            source_id="source_json",
            path="sample.jsonl",
            file_format=DatasetFormat.JSONL,
        )


def test_local_file_source_label_must_state_local_test_or_dev() -> None:
    with pytest.raises(ValidationError):
        LocalFileSource(
            source_id="source_csv",
            path="sample.csv",
            file_format=DatasetFormat.CSV,
            label="manual-upload",
        )


def test_local_file_source_rejects_real_market_data_claims() -> None:
    with pytest.raises(ValidationError):
        LocalFileSource(
            source_id="source_csv",
            path="sample.csv",
            file_format=DatasetFormat.CSV,
            real_market_data=True,
        )


def test_local_file_source_rejects_secret_like_path_and_sanitizes_notes() -> None:
    with pytest.raises(ValidationError):
        LocalFileSource(
            source_id="source_csv",
            path="provider_token_sample.csv",
            file_format=DatasetFormat.CSV,
        )

    source = LocalFileSource(
        source_id="source_csv",
        path="sample.csv",
        file_format=DatasetFormat.CSV,
        notes=["api_key should not appear"],
    )

    assert source.notes == ["[redacted]"]
