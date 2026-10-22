"""Connected-call flow: call notes -> AI draft -> SDR approves -> send.

Planned:
- record_connected_call(lead_id, sdr, outcome, notes, goal)
    log call, status called_connected, HubSpot call with notes;
    "not interested" -> close out, no draft
- create_draft(lead_id, ...) -> LinkedInDraft      status message_drafted
- regenerate_draft(lead_id, previous_draft) -> LinkedInDraft
- send_via_heyreach(lead_id, text)    post-call campaign, status message_sent, HubSpot note
- mark_sent_manually(lead_id, text)   logged as message_sent with action manual

Phase: 6 · Tests: tests/integration/test_messaging.py
"""
