from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit


DANGEROUS_KEYWORDS = (
    "drop ",
    "alter ",
    "truncate ",
    "create ",
    "insert ",
    "update ",
    "delete ",
    "merge ",
    "grant ",
    "revoke ",
    "execute ",
    "copy ",
)

PROMPT_INJECTION_PATTERNS = (
    "ignore previous instructions",
    "ignore all previous instructions",
    "override system",
    "reveal the api key",
    "reveal the secret",
    "system prompt",
    "developer message",
)


def contains_prompt_injection(value: str | None) -> bool:
    if value is None:
        return False

    normalized = re.sub(r"\s+", " ", str(value)).strip().lower()
    if not normalized:
        return False

    return any(pattern in normalized for pattern in PROMPT_INJECTION_PATTERNS)


def redact_sensitive_data(value: str | None) -> str:
    if value is None:
        return ""

    text = str(value).strip()
    if not text:
        return ""

    try:
        parsed = urlsplit(text)
        if parsed.scheme and parsed.hostname:
            username = parsed.username or ""
            password = parsed.password
            if username or password:
                host = parsed.hostname
                if parsed.port:
                    host = f"{host}:{parsed.port}"
                netloc = f"{username}:***@{host}" if username else f"***@{host}"
                rebuilt = parsed._replace(netloc=netloc)
                return urlunsplit(rebuilt)
    except ValueError:
        pass

    masked = re.sub(
        r"(?i)((?:api[_-]?key|token|secret|password)\s*[:=]\s*)([^\s,;]+)",
        r"\1***",
        text,
    )
    return masked


def validate_user_input(value: str | None, *, max_length: int = 2000) -> str:
    if value is None:
        raise ValueError("Input cannot be empty.")

    sanitized = str(value).strip()
    if not sanitized:
        raise ValueError("Input cannot be empty.")
    if len(sanitized) > max_length:
        raise ValueError(f"Input exceeds the maximum length of {max_length} characters.")
    if contains_prompt_injection(sanitized):
        raise ValueError("Input contains instruction-like content that is not allowed.")

    return sanitized


def validate_sql(query: str) -> str:
    if query is None:
        raise ValueError("SQL query cannot be empty.")

    sanitized = validate_user_input(query, max_length=20000)
    normalized = re.sub(r"\s+", " ", sanitized)
    lowered = normalized.lower()

    for keyword in DANGEROUS_KEYWORDS:
        if keyword in lowered:
            raise ValueError(f"Unsafe SQL statement detected: keyword '{keyword.strip()}' is not allowed.")

    if lowered.startswith("--") or lowered.startswith("/*"):
        raise ValueError("Only executable read-only queries are allowed.")

    if lowered.startswith(("select ", "with ", "show ", "describe ", "explain ")):
        return normalized

    raise ValueError("Only read-only SELECT/SHOW/DESCRIBE/EXPLAIN statements are allowed.")
