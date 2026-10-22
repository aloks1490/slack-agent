"""Integration tests for services/enrichment.py.

Planned cases:
- full data -> enriched (then in_crm), card posted with every field
- no email -> "Not found" on the card, pipeline continues
- junior title -> phone lookup not called; no phone -> hint on the card
- Deepline 500 on one step -> retried, then continues without that data
- crash -> workflow_errors row, status error, Retry alert; Retry succeeds
"""
