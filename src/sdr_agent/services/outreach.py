"""Call outcomes that lead to sequences: "Did not pick up" and "Wrong person".

Planned:
- no_answer(lead_id, sdr_slack_id)
    idempotency: already heyreach_enrolled -> "Already sequenced", stop
    log call, status called_no_answer ->
    in parallel: HeyReach no-answer campaign + Instantly (only if email valid) ->
    outreach_events rows, status sequenced -> HubSpot call log ->
    update the card -> expansion.start(lead_id)
- wrong_person(lead_id, sdr_slack_id)
    log call, status disqualified -> update the card -> expansion.start(lead_id)
- Both refuse to act on do_not_contact leads.

Phase: 4 · Tests: tests/integration/test_outreach.py
"""
