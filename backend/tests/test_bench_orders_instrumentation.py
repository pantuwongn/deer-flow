"""Tests for order-desk OpenTelemetry to LangSmith attributes."""

from __future__ import annotations

from deerflow.bench import orders


class _RecordingSpan:
    def __init__(self) -> None:
        self.attributes = {}
        self.events = []
        self.status = None

    def is_recording(self) -> bool:
        return True

    def set_attribute(self, key, value) -> None:
        self.attributes[key] = value

    def record_exception(self, exc) -> None:
        self.events.append(exc)

    def set_status(self, status) -> None:
        self.status = status


def test_root_metadata_is_bounded_and_comes_from_request(monkeypatch) -> None:
    root = _RecordingSpan()
    monkeypatch.setattr(orders.trace, "get_current_span", lambda: root)

    orders._stamp_root_metadata(
        {
            "configurable": {
                "thread_id": "thread-1",
                "user_id": "user-1",
                "graph": "not-a-graph",
            },
            "metadata": {"environment": "staging"},
        },
        {},
    )

    assert root.attributes["metadata.thread_id"] == "thread-1"
    assert root.attributes["metadata.user_id"] == "user-1"
    assert root.attributes["metadata.environment"] == "staging"
    assert root.attributes["metadata.graph"] == "recent"


def test_error_mapping_preserves_exception_event_and_run_fields() -> None:
    span = _RecordingSpan()
    error = RuntimeError("failed step")

    orders._record_error(span, error)

    assert span.events == [error]
    assert span.attributes["status"] == "error"
    assert span.attributes["error"] == "failed step"
    assert span.attributes["error.type"] == "RuntimeError"
    assert span.attributes["error.message"] == "failed step"
    assert span.status is not None
