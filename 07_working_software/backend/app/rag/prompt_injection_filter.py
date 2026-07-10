"""Detects and rejects prompt-injection / malicious patterns in user input (VR-2.2, E010)."""

import re

from app.config.constants import PROMPT_INJECTION_PATTERNS

_compiled_patterns = [re.compile(p) for p in PROMPT_INJECTION_PATTERNS]


def detect_injection(text: str) -> bool:
    """Return True if the text matches a known prompt-injection or SQL-injection pattern."""
    return any(pattern.search(text) for pattern in _compiled_patterns)
