"""HubSpot sync: mirror an enriched lead into the CRM.

Planned:
- sync(lead_id)
    company by domain (create if missing) -> contact by email, then linkedin_url
    (create or update; owner from sdr_owners, never silently overwritten) ->
    associate -> note with the research summary ->
    save hubspot_contact_id / hubspot_company_id, status in_crm

Phase: 3
"""
