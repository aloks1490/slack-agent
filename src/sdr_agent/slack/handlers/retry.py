"""Handles the Retry button on "Something failed at <step>" messages.

Planned:
- on_retry_step(ack, body)   ack() -> re-submit the failed job for that lead
                             (step and lead id carried in the button value)

Phase: 2 (with the job runner)
"""
