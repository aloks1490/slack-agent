"""Background job runner (thread pool) with central error handling.

Why: Slack needs an answer within 3 seconds; enrichment takes minutes. Handlers
submit work here and return immediately.

Planned:
- submit(fn, lead_id, step_name, **kwargs)
    runs fn in a ThreadPoolExecutor; on any exception:
      log to workflow_errors, set lead status error,
      post "Something failed at <step>" in the lead's thread with a Retry button
- Supabase statuses make work recoverable: after a restart the sweeper
  (jobs.scheduled) finds anything left half-done.

Upgrade path if it ever grows: swap the thread pool for Redis + RQ; services stay the same.

Phase: 2
"""
