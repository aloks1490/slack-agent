"""Data models shared across the app (Pydantic).

Planned:
- Lead                 mirrors a row in the `leads` table
- EnrichmentResult     everything Deepline returned for one person, plus what was missing
- Research             Claude output: summary (3 bullets), talking_points (3), icp_fit
- FitScore             Claude output for a suggested colleague: score 1-5, one-line reason
- LinkedInDraft        Claude output: the message text (under 300 characters)
- CallOutcome          enum: no_answer, connected, wrong_person, voicemail
- ConnectedOutcome     enum: meeting_booked, interested, not_now, not_interested
- MessageGoal          enum: recap_and_confirm, share_resource, soft_follow_up
- OutreachAction       enum: heyreach_enrolled, instantly_enrolled, message_drafted, message_sent

Phase: 1 onward (grow as needed)
"""
