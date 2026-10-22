"""Integration tests for services/outreach.py.

Planned cases:
- no answer -> HeyReach + Instantly once each, two outreach_events, sequenced,
  HubSpot call logged, card updated, expansion started
- double click -> enrolled exactly once
- invalid email -> HeyReach only, "email skipped" logged
- wrong person -> disqualified, expansion started
"""
