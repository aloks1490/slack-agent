"""Unit tests for slack/blocks/lead_card.py.

Planned cases:
- full lead -> expected blocks (snapshot)
- no phone -> hint shown; do_not_contact -> no call buttons; "already" note rendered
- Slack limits: <= 10 fields per section, header <= 150 chars,
  section text <= 3000 chars, <= 50 blocks
- every call button's value is the lead id
"""
