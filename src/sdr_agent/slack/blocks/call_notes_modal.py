"""Slack modals for the connected-call flow.

Planned:
- call_notes_modal(lead_id) -> dict        callback_id call_notes_submit
    call outcome (Meeting booked / Interested, follow up / Not now / Not interested)
    call notes (multi-line)
    message goal (Recap and meeting confirmation / Share a resource / Soft follow-up)
    private_metadata = lead id
- edit_message_modal(lead_id, draft) -> dict   callback_id edit_message_submit

Phase: 6
"""
