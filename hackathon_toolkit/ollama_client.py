# Local Ollama Inference Client (Defensive Implementation)
# DBC Compliance: DBC-001, DBC-002

import json
import urllib.error
import urllib.request
from collections.abc import Generator

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma2:2b"


def query_gemma(
    prompt: str,
    system_prompt: str = "",
    model: str = DEFAULT_MODEL,
    as_json: bool = False,
) -> str:
    """Sends a query to local Ollama instance with timeout and defensive error handling."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if system_prompt:
        payload["system"] = system_prompt
    if as_json:
        payload["format"] = "json"

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "")
    except urllib.error.URLError:
        return f"ERROR_CONNECTION: Cannot connect to Ollama at {OLLAMA_URL}. Is 'ollama serve' running?"
    except Exception as err:  # noqa: BLE001
        return f"ERROR_UNEXPECTED: {err!s}"


def stream_gemma(
    prompt: str,
    system_prompt: str = "",
    model: str = DEFAULT_MODEL,
) -> Generator[str, None, None]:
    """Streams response tokens from local Ollama instance in real time."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
    }
    if system_prompt:
        payload["system"] = system_prompt

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            for line in response:
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    yield chunk.get("response", "")
    except urllib.error.URLError:
        yield f"ERROR_CONNECTION: Cannot connect to Ollama at {OLLAMA_URL}. Is 'ollama serve' running?"
    except Exception as err:  # noqa: BLE001
        yield f"ERROR_UNEXPECTED: {err!s}"


def parse_json_safely(raw_text: str, container_key: str | None = None) -> list | dict:
    """Defensively normalizes JSON string from LLMs to prevent DBC-001 type errors."""
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        return {"error": "Failed to decode JSON", "raw": raw_text}

    if container_key and isinstance(data, dict):
        return data.get(container_key, data)
    return data
