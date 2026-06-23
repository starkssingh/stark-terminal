from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_data_quality_docs_exist() -> None:
    for path in [
        "docs/DATA_QUALITY_FRAMEWORK.md",
        "docs/VALIDATION_RULE_SPEC.md",
        "docs/QUALITY_GATE_POLICY.md",
        "docs/DATA_QUALITY_REPORT_SPEC.md",
    ]:
        assert (ROOT / path).exists()


def test_data_quality_docs_and_status_are_current() -> None:
    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("*.md"))
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    for phrase in [
        "Data Quality",
        "validation framework",
        "validation rule",
        "quality gate",
        "validation report",
        "no execution APIs",
        "no market data ingestion",
        "no analytics signals",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text
    assert "Prompt 13" in prompt_log
    assert "Current Prompt: 36" in north_star
    assert "Data Quality + Validation Framework" in project_map
