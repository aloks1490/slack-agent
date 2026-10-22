"""Scheduled tasks (APScheduler, inside the same process).

Planned:
- start(app)                        registers the jobs below
- sweep_stuck_leads()      every 10 min: enriching > 15 min -> retry once, then alert
- sweep_stuck_expansions() every 10 min: searching > 10 min -> post what has arrived
- daily_summary()          weekdays: leads per SDR, connect rate, sequenced,
                           suggestions added vs skipped, messages sent
- cleanup_skipped()        daily: delete skipped suggestions older than 90 days

Phase: 7
"""
