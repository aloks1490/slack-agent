"""The lead card posted in the thread.

Planned:
- lead_card(lead, note=None) -> list[block]
    header: name
    optional context note (e.g. "Already in the pipeline · owner · status")
    fields: title, company, email (+status), phone, location, company size,
            industry, followers, connections, status
    research summary + talking points
    "No phone found, start on LinkedIn" hint when there is no phone
    buttons: Picked up (call_connected) · Did not pick up (call_no_answer) ·
             Wrong person (wrong_person) · LinkedIn (link); value = lead id
    no call buttons for do_not_contact leads
- lead_card_outcome(lead, text) -> list[block]   card after a button (buttons replaced)

Phase: 1 (simple) -> 2 (full) · Tests: tests/unit/test_lead_card.py
"""
