"""HeyReach client: LinkedIn sequences and sending post-call messages.

API: header X-API-KEY; endpoint "Add Leads to Campaign (V2)" (AddLeadsToCampaignV2).
Confirm field names against HeyReach's current API docs before building.

Planned:
- add_to_campaign(campaign_id, lead, custom_fields) -> external_id
    no-answer campaign: custom field talking_point   -> {talking_point} in HeyReach
    post-call campaign: custom field custom_message  -> {custom_message} in HeyReach

Phase: 4 (no-answer), 6 (post-call)
"""
