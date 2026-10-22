"""Lead statuses and which status may follow which.

Why: every step checks the status before acting and sets it after. Central rules
stop impossible jumps (e.g. re-enrolling a lead that is already sequenced).

Planned:
- LeadStatus enum: received, enriching, enriched, in_crm, called_no_answer, sequenced,
  called_connected, message_drafted, message_sent, suggested, skipped,
  disqualified, do_not_contact, error
- ALLOWED_TRANSITIONS: dict of status -> set of next statuses
- can_transition(current, new) -> bool
- blocks_outreach(status) -> bool     True for do_not_contact (and disqualified)

Phase: 1 · Tests: tests/unit/test_statuses.py
"""
