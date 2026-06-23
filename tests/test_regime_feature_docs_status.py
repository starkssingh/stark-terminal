from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_DOCS = [
    "docs/REGIME_FEATURE_PREPARATION_CONTRACTS.md",
    "docs/REGIME_FEATURE_GROUPS.md",
    "docs/REGIME_FEATURE_PROVENANCE_POLICY.md",
    "docs/REGIME_FEATURE_EVIDENCE_MAPPING.md",
    "docs/REGIME_FEATURE_SAFETY_POLICY.md",
    "docs/REGIME_FEATURE_DEPENDENCY_STAGING.md",
]


def test_regime_feature_docs_exist() -> None:
    for doc in REQUIRED_DOCS:
        assert (ROOT / doc).exists(), doc


def test_regime_feature_docs_state_prompt_34_boundaries() -> None:
    combined = "\n".join((ROOT / doc).read_text(encoding="utf-8") for doc in REQUIRED_DOCS)

    for phrase in [
        "Regime Feature Preparation",
        "contracts-only",
        "feature groups",
        "provenance",
        "evidence mapping",
        "no feature computation",
        "no feature registry writes",
        "no classification",
        "no signals",
        "no recommendations",
        "no DecisionObject",
        "no execution APIs",
        "dependency staging",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in combined


def test_prompt_34_status_docs_are_current() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "## Prompt 34 - Regime Feature Preparation Contracts" in prompt_log
    assert "Current Prompt: 36" in north_star
    assert "Regime Feature Preparation Contracts" in project_map


def test_verify_and_audit_scripts_track_prompt_34_artifacts() -> None:
    verify_text = (ROOT / "scripts/verify_foundation.py").read_text(encoding="utf-8")
    audit_text = (ROOT / "scripts/audit_foundation.py").read_text(encoding="utf-8")

    assert "REGIME_FEATURE_PREPARATION_CONTRACTS.md" in verify_text
    assert "regime_features/contracts.py" in verify_text
    assert "Regime Feature Preparation" in verify_text
    assert "regime feature preparation" in audit_text.lower()

