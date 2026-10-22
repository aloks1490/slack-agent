"""The AI-drafted LinkedIn message posted after a connected call.

Planned:
- draft_card(lead, draft_text) -> list[block]
    the draft text + character count;
    buttons: Send via HeyReach (send_message) · Edit (edit_message) ·
             Regenerate (regenerate_message) · Copy, I'll send it (copy_message)
- sent_card(lead, text, how) -> list[block]     after sending (buttons removed)

Phase: 6
"""
