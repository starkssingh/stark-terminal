from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_event_backbone_docs_exist_and_prompt_status_is_current() -> None:
    assert (ROOT / "docs/KAFKA_REDPANDA_FOUNDATION.md").exists()
    assert (ROOT / "docs/EVENT_BACKBONE_TOPIC_POLICY.md").exists()
    assert (ROOT / "docs/DURABLE_EVENT_ENVELOPE_SPEC.md").exists()

    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 12 - Kafka/Redpanda Event Backbone Foundation" in prompt_log
    assert "Current Prompt: 36" in north_star
    assert "Completed Prompts: 35 before this prompt, 36 after completion" in north_star
    assert "event_backbone/topics.py" in project_map
    assert "Kafka/Redpanda Event Backbone foundation" in project_map


def test_event_backbone_docs_state_boundaries() -> None:
    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("*.md"))

    assert "durable event backbone" in docs_text
    assert "topic policy" in docs_text
    assert "DurableEventEnvelope" in docs_text
    assert "memory fallback" in docs_text
    assert "no execution APIs" in docs_text
    assert "no market data ingestion" in docs_text
    assert "Mac mini M2" in docs_text
    assert "Windows-native" in docs_text
