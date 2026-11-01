import os
import json
from datetime import datetime
from pathlib import Path

# Base directory for all logs – placed inside the project root
LOG_ROOT = Path(__file__).resolve().parent / "logs"
LOG_ROOT.mkdir(exist_ok=True)

TEMPLATE_PATH = LOG_ROOT / "template.md"

def _ensure_log_file(log_file: Path) -> None:
    """Create the log file if it does not exist and write the template header.
    """
    if not log_file.exists():
        log_file.parent.mkdir(parents=True, exist_ok=True)
        # Write a simple markdown skeleton
        log_file.write_text(TEMPLATE_PATH.read_text() if TEMPLATE_PATH.exists() else "# Session Log\n\n## Events\n\n## Deadlines\n\n## Memory Summary\n")

def log_event(event: str, data: dict | None = None) -> None:
    """Append an event line to the current session log.

    Parameters
    ----------
    event: str
        Short description of what happened (e.g., "User asked a question").
    data: dict | None
        Optional extra information – will be JSON‑encoded.
    """
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log_file = LOG_ROOT / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    _ensure_log_file(log_file)
    line = f"- [{timestamp}] **{event}**"
    if data:
        line += f" – `{json.dumps(data, ensure_ascii=False)}`"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def add_deadline(date_str: str, description: str) -> None:
    """Add a deadline entry to the current session log.

    date_str: must be in DD-MM-YYYY format (per your project policy).
    """
    try:
        # Validate date format
        datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError as exc:
        raise ValueError(f"Invalid date format (expected DD-MM-YYYY): {date_str}") from exc

    log_file = LOG_ROOT / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    _ensure_log_file(log_file)
    line = f"- **Deadline**: {date_str} – {description}\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line)

def get_all_logs() -> list[Path]:
    """Return a list of all log files for the current project."""
    return list(LOG_ROOT.glob("*.md"))
