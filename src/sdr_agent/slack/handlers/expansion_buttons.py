"""Handles the expansion card's per-person buttons.

Planned:
- on_add_suggested_lead(ack, body)   ack() -> job: services.expansion.add_suggested
- on_skip_suggested_lead(ack, body)  ack() -> services.expansion.skip_suggested,
                                     grey the person out with chat.update

Button value = the suggested person's lead id. Phase: 5
"""
