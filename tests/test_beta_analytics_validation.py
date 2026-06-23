from pydantic import ValidationError
import pytest

from stark_terminal_analytics.beta.contracts import BetaMethod, create_beta_request, create_beta_result
from stark_terminal_analytics.beta.validation import (
    validate_beta_request,
    validate_beta_result,
    validate_paired_vectors_for_beta,
)
from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, create_vector_contract


def test_paired_vectors_for_beta_pass() -> None:
    asset = create_vector_contract("asset", "Asset Returns", [0.01, 0.02, 0.03])
    benchmark = create_vector_contract("benchmark", "Benchmark Returns", [0.02, 0.04, 0.06])

    result = validate_paired_vectors_for_beta(asset, benchmark)

    assert result.status == "ok"
    assert result.metrics["equal_lengths"] is True
    assert result.metrics["benchmark_variance_positive"] is True


def test_beta_validation_requires_enough_observations() -> None:
    asset = create_vector_contract("asset", "Asset Returns", [0.01])
    benchmark = create_vector_contract("benchmark", "Benchmark Returns", [0.02])

    result = validate_paired_vectors_for_beta(asset, benchmark)

    assert result.status == "failed"


def test_beta_validation_rejects_unequal_lengths_safely() -> None:
    asset = create_vector_contract("asset", "Asset Returns", [0.01, 0.02, 0.03])
    benchmark = create_vector_contract("benchmark", "Benchmark Returns", [0.02])

    result = validate_paired_vectors_for_beta(asset, benchmark)

    assert result.status == "failed"


def test_beta_validation_rejects_non_finite_values() -> None:
    with pytest.raises(ValidationError):
        create_vector_contract("asset", "Asset Returns", [0.01, float("inf")])


def test_beta_validation_rejects_real_market_source() -> None:
    source = NumericalSourceReference.model_construct(
        source_id="real",
        source_type="provider",
        source_data_reference="real",
        synthetic=False,
        real_market_data=True,
        schema_version="v1",
    )
    asset = create_vector_contract("asset", "Asset Returns", [0.01, 0.02, 0.03])
    benchmark = create_vector_contract("benchmark", "Benchmark Returns", [0.02, 0.04, 0.06])
    benchmark = benchmark.model_copy(update={"source": source})

    result = validate_paired_vectors_for_beta(asset, benchmark)

    assert result.status == "failed"


def test_beta_validation_rejects_zero_benchmark_variance() -> None:
    asset = create_vector_contract("asset", "Asset Returns", [0.01, 0.02, 0.03])
    benchmark = create_vector_contract("benchmark", "Benchmark Returns", [0.02, 0.02, 0.02])

    result = validate_paired_vectors_for_beta(asset, benchmark)

    assert result.status == "failed"


def test_beta_request_and_result_validation() -> None:
    asset = create_vector_contract("asset", "Asset Returns", [0.01, 0.02, 0.03])
    benchmark = create_vector_contract("benchmark", "Benchmark Returns", [0.02, 0.04, 0.06])
    request = create_beta_request("beta", asset, benchmark)
    result = create_beta_result(
        "beta_result",
        "beta",
        BetaMethod.SAMPLE_COVARIANCE,
        beta=0.5,
        covariance=0.0002,
        benchmark_variance=0.0004,
        asset_source=asset.source,
        benchmark_source=benchmark.source,
        observation_count=3,
    )

    assert validate_beta_request(request).status == "ok"
    assert validate_beta_result(result).status == "ok"
