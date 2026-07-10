"""EML (email) text extraction from headers and body."""

from email import message_from_file
from email.message import Message


def extract_text_from_eml(file_path: str) -> str:
    """Extract sender, subject, date, and plain-text body from an .eml file."""
    with open(file_path, encoding="utf-8", errors="ignore") as f:
        msg: Message = message_from_file(f)

    header_lines = [
        f"From: {msg.get('From', '')}",
        f"To: {msg.get('To', '')}",
        f"Subject: {msg.get('Subject', '')}",
        f"Date: {msg.get('Date', '')}",
    ]

    body = _extract_body(msg)
    return "\n".join(header_lines) + "\n\n" + body


def _extract_body(msg: Message) -> str:
    if msg.is_multipart():
        parts: list[str] = []
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    parts.append(payload.decode(part.get_content_charset() or "utf-8", errors="ignore"))
        return "\n".join(parts)

    payload = msg.get_payload(decode=True)
    if isinstance(payload, bytes):
        return payload.decode(msg.get_content_charset() or "utf-8", errors="ignore")
    return str(payload or "")
