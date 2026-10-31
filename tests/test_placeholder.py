"""
Sanity and unit tests for Airgap-Gemma Prototype 1.
"""
from hackathon_toolkit.ollama_client import parse_json_safely


def test_placeholder_sanity():
    """Placeholder test ensuring test suite execution."""
    assert True


def test_parse_json_safely():
    """Verify that JSON parser defensively handles raw text."""
    valid_json = '{"status": "ok", "agent": "prototype-1"}'
    parsed = parse_json_safely(valid_json)
    assert parsed.get("status") == "ok"
    assert parsed.get("agent") == "prototype-1"

    invalid_json = "plain text response"
    fallback = parse_json_safely(invalid_json)
    assert fallback.get("error") == "Failed to decode JSON"
