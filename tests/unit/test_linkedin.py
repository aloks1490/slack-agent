"""Unit tests for domain/linkedin.py -> normalise().

Planned cases:
- normal link; uppercase; trailing slash; ?utm_source=...; m.linkedin.com; /mwlite/in/
- Slack wrapping <url> and <url|label>; a mention token before the link
- company page -> None; Sales Navigator -> None; empty text -> None
- two links -> the first profile link
"""
