import pytest

from stark_terminal_analytics.regime.contracts import RegimeEvidenceKind
from stark_terminal_analytics.regime.evidence import (
    RegimeEvidenceChecklist,
    RegimeEvidenceRequirement,
    build_regime_evidence_checklist,
    default_regime_evidence_requirements,
    evaluate_evidence_readiness,
)


def test_default_regime_evidence_requirements_exist() -> None:
    requirements = default_regime_evidence_requirements()

    assert requirements
    assert {requirement.evidence_kind for requirement in requirements} >= {
        RegimeEvidenceKind.RETURNS,
        RegimeEvidenceKind.VOLATILITY,
        RegimeEvidenceKind.DRAWDOWN,
        RegimeEvidenceKind.CORRELATION,
        RegimeEvidenceKind.BETA,
        RegimeEvidenceKind.TIME_SERIES_DIAGNOSTICS,
    }
    assert all(requirement.source_reference_required for requirement in requirements)
    assert all(requirement.validation_required for requirement in requirements)


def test_regime_evidence_requirement_rejects_unknown_or_invalid_minimum() -> None:
    with pytest.raises(ValueError):
        RegimeEvidenceRequirement(
            requirement_id="unknown",
            evidence_kind=RegimeEvidenceKind.UNKNOWN,
            description="Invalid.",
        )

    with pytest.raises(ValueError):
        RegimeEvidenceRequirement(
            requirement_id="bad-minimum",
            evidence_kind=RegimeEvidenceKind.RETURNS,
            description="Invalid.",
            minimum_observations=0,
        )


def test_missing_required_evidence_produces_blockers() -> None:
    checklist = build_regime_evidence_checklist()

    assert checklist.complete is False
    assert checklist.blockers
    assert checklist.classification_allowed is False


def test_completed_evidence_checklist_has_no_blockers() -> None:
    requirements = default_regime_evidence_requirements()
    completed = {requirement.requirement_id for requirement in requirements}

    checklist = build_regime_evidence_checklist(requirements=requirements, completed_requirement_ids=completed)

    assert checklist.complete is True
    assert checklist.blockers == []


def test_complete_checklist_cannot_have_blockers() -> None:
    with pytest.raises(ValueError):
        RegimeEvidenceChecklist(
            checklist_id="invalid",
            requirements=default_regime_evidence_requirements(),
            complete=True,
            blockers=["missing evidence"],
        )


def test_evaluate_evidence_readiness_remains_planning_only() -> None:
    checklist = evaluate_evidence_readiness(build_regime_evidence_checklist())

    assert checklist.complete is False
    assert checklist.blockers
    assert checklist.classification_allowed is False
