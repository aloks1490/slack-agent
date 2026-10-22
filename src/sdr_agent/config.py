"""Settings loaded from .env and validated at startup (pydantic-settings).

Why: one typed place for every key and knob; the app fails fast with a clear
message if something required is missing, instead of crashing mid-flow.

Planned:
- class Settings(BaseSettings)
    Slack:     slack_bot_token, slack_app_token
    Supabase:  supabase_url, supabase_service_role_key
    Deepline:  deepline_api_key
    Claude:    anthropic_api_key, claude_model (default "claude-opus-5-5")
    HubSpot:   hubspot_token                    (optional until Phase 3)
    HeyReach:  heyreach_api_key, heyreach_linkedin_account_id,
               heyreach_no_answer_campaign_id, heyreach_post_call_campaign_id  (Phase 4)
    Instantly: instantly_api_key, instantly_campaign_id                       (Phase 4)
    Behaviour: expansion_max_people, expansion_repeat_days,
               phone_lookup_min_seniority, log_level
- get_settings() -> Settings   cached, so .env is read once

Phase: 0
"""
