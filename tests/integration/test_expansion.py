"""Integration tests for services/expansion.py.

Planned cases:
- 8 found incl. the original person + one existing lead -> card shows 6
- nobody found -> "No other matching people found", run empty
- same domain searched 10 days ago -> no Deepline call, link to the old thread
- Add as lead -> received + full enrichment with phone; Skip -> skipped, never enrolled
"""
