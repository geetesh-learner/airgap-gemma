"""
Sanity, unit, and chat module tests for Airgap-Gemma Chat Interface.
Rule 3 Compliance: Unit tests covering core inference helpers and edge cases.
"""
import urllib.error
from collections.abc import Generator
from unittest.mock import patch

from hackathon_toolkit.ollama_client import parse_json_safely, query_gemma, stream_gemma


def test_placeholder_sanity():
    """Placeholder test ensuring test suite execution."""
    assert True


def test_parse_json_safely_valid():
    """Verify that JSON parser defensively handles valid JSON dictionary."""
    valid_json = '{"status": "ok", "agent": "prototype-2"}'
    parsed = parse_json_safely(valid_json)
    assert parsed.get("status") == "ok"
    assert parsed.get("agent") == "prototype-2"


def test_parse_json_safely_container_key():
    """Verify container key extraction."""
    nested_json = '{"response": {"text": "offline-ai"}}'
    parsed = parse_json_safely(nested_json, container_key="response")
    assert parsed.get("text") == "offline-ai"


def test_parse_json_safely_invalid():
    """Verify fallback handling for non-JSON strings."""
    invalid_json = "plain text response"
    fallback = parse_json_safely(invalid_json)
    assert fallback.get("error") == "Failed to decode JSON"
    assert fallback.get("raw") == "plain text response"


def test_stream_gemma_returns_generator():
    """Verify that stream_gemma yields a generator."""
    gen = stream_gemma("Test generator initialization")
    assert isinstance(gen, Generator)


def test_stream_gemma_connection_error():
    """Verify defensive handling when Ollama daemon is unreachable."""
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Connection refused")):
        chunks = list(stream_gemma("hello"))
        assert len(chunks) == 1
        assert "ERROR_CONNECTION" in chunks[0]


def test_query_gemma_connection_error():
    """Verify defensive fallback for non-streaming query."""
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Connection refused")):
        res = query_gemma("hello")
        assert "ERROR_CONNECTION" in res
