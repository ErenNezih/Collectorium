import os
import re


EMAIL_RE = re.compile(r"\b[a-z0-9._%+-]+@(?:gmail|hotmail|outlook|yahoo|icloud|proton|yandex|[\w-]+)\.[a-z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?:\+?90|\b0)?\s*(?:\(?\d{3}\)?[\s\-.]?\d{3}[\s\-.]?\d{2}[\s\-.]?\d{2})")
LINK_RE = re.compile(r"https?://|wa\.me|whatsapp\.com|t\.me|instagram\.com|x\.com|twitter\.com|facebook\.com|@[\w\.]{3,}", re.I)
KEYWORDS_RE = re.compile(r"gmail|whatsapp|\bwp\b|tel|telefon|numara|no[:\s]|dot\s?com|\.\s?com", re.I)


def redact_text(raw_text: str, strict: bool = True) -> tuple[str, bool]:
    """Return (redacted_text, has_violation). If not strict, returns (raw_text, False)."""
    if not strict:
        return raw_text, False
    if not raw_text:
        return raw_text, False
    has = False
    text = raw_text
    for pattern in (EMAIL_RE, PHONE_RE, LINK_RE, KEYWORDS_RE):
        if pattern.search(text):
            has = True
            text = pattern.sub("[…]", text)
    return text, has


