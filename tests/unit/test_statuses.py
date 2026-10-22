"""Unit tests for domain/statuses.py.

Planned cases:
- allowed transitions pass (received -> enriching -> enriched -> in_crm ...)
- illegal transitions are rejected (sequenced -> received)
- do_not_contact blocks outreach
"""
