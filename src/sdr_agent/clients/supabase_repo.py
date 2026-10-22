"""Supabase access: all reads and writes to the database go through here.

Planned (grouped by table):
- leads:            find_lead_by_url, get_lead, create_lead, update_lead,
                    set_status (checks domain.statuses.can_transition),
                    list_suggested(parent_lead_id), find_stuck(status, older_than)
- call_logs:        log_call(lead_id, sdr, outcome, notes)
- outreach_events:  has_event(lead_id, action), add_event(lead_id, channel, action, ...)
- expansion_runs:   recent_run_for_domain(domain, days), create_run, update_run
- workflow_errors:  log_error(workflow, step, lead_id, error, payload)
- sdr_owners:       hubspot_owner_for(slack_user_id)

Uses the service_role key (server-side only). Phase: 1
"""
