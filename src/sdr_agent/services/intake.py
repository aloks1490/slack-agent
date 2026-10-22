"""Intake: what happens when someone mentions the bot with a link.

Planned:
- handle_mention(text, user, channel, ts, thread_ts) -> Invalid | Existing | Created
    1. linkedin.normalise(text); no profile link -> Invalid
    2. find the lead by URL; found -> Existing(lead)   (do_not_contact is flagged)
    3. otherwise create the lead (status received, thread = thread_ts or ts) -> Created(lead)
  The Slack handler replies in the thread and, for Created, submits the enrichment job.

Phase: 1 · Tests: tests/integration/test_intake.py
"""
