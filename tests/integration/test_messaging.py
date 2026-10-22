"""Integration tests for services/messaging.py.

Planned cases:
- modal opens before any other work (call order)
- not interested -> call logged, no draft
- draft -> Send -> HeyReach post-call with the exact text, message_sent, HubSpot note
- Regenerate -> previous draft passed to the LLM
"""
