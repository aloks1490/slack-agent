"""HubSpot client (official SDK: hubspot-api-client).

Planned:
- find_company_by_domain(domain) / create_company(...)
- find_contact(email=None, linkedin_url=None) / create_contact(...) / update_contact(...)
- associate_contact_company(contact_id, company_id)
- add_note(contact_id, text)
- log_call(contact_id, outcome, notes)
- contact_url(contact_id) -> str      link shown on the lead card

Custom contact properties to create once in HubSpot: linkedin_url,
linkedin_followers, linkedin_connections, research_summary.

Phase: 3
"""
