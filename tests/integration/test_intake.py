"""Integration tests for services/intake.py (fake clients, no real APIs).

Planned cases:
- new link -> one lead (received), "Enriching…" in the right thread, enrichment job submitted
- same link twice / link variants -> still one lead; second time posts the "already" card
- invalid link -> reply only, nothing saved
- do_not_contact lead -> blocked, no call buttons
"""
