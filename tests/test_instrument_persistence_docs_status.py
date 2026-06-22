from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_prompt_15_docs_exist() -> None:
    assert (ROOT / "docs/INSTRUMENT_PERSISTENCE_FOUNDATION.md").exists()
    assert (ROOT / "docs/INSTRUMENT_REPOSITORY_POLICY.md").exists()


def test_prompt_15_docs_contain_required_boundaries() -> None:
    combined = "\n".join(
        [
            (ROOT / "docs/INSTRUMENT_PERSISTENCE_FOUNDATION.md").read_text(encoding="utf-8"),
            (ROOT / "docs/INSTRUMENT_REPOSITORY_POLICY.md").read_text(encoding="utf-8"),
        ]
    )

    for phrase in [
        "Instrument Metadata Persistence",
        "InstrumentRepository",
        "InstrumentMetadataService",
        "validation-before-persistence",
        "synthetic",
        "no real market ingestion",
        "no external calls",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in combined


def test_prompt_15_status_docs_updated() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Current Prompt: 25" in north_star
    assert "Completed Prompts: 25 before this prompt, 26 after completion" in north_star
    assert "Instrument Persistence Status" in north_star
    assert "Prompt 15 - Instrument Metadata Persistence Wiring" in prompt_log
    assert "InstrumentRepository" in project_map
    assert "InstrumentMetadataService" in project_map
