"""LinkedIn link cleaning: turn any version of a profile link into one standard form.

Why: dedupe only works if the same person always produces the same URL.

Planned:
- normalise(text: str) -> str | None
    Find the first linkedin.com/in/<slug> link in a Slack message and rebuild it as
    https://www.linkedin.com/in/<slug> (lowercase, no query string, no trailing slash).
    Handles Slack's <url> and <url|label> wrapping, m.linkedin.com and /mwlite/in/.
    Returns None for company pages, Sales Navigator links or no link at all.

Phase: 1 · Tests: tests/unit/test_linkedin.py
"""
