"""Handles the lead card's call-outcome buttons.

Planned:
- on_call_no_answer(ack, body)   ack() -> job: services.outreach.no_answer
- on_wrong_person(ack, body)     ack() -> job: services.outreach.wrong_person
- on_call_connected(ack, body, client)
    ack() and open the call-notes modal IMMEDIATELY (trigger_id expires in 3 s);
    the rest happens on modal submit (handlers.modals)
- on_open_linkedin(ack)          link button; just ack()

Button value = lead id. Phase: 2 ("coming soon" replies) -> 4 -> 6
"""
