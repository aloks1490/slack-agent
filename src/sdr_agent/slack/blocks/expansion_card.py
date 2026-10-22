"""The account-expansion card: "Found N more people at <company> who match your persona".

Planned:
- expansion_card(company, people) -> list[block]
    one section per person, sorted by fit: name, title, fit reason, email found?,
    LinkedIn link; buttons Add as lead (add_suggested_lead) / Skip (skip_suggested_lead)
- mark_person(blocks, lead_id, state) -> list[block]   grey out skipped / tick added

Phase: 5
"""
