"""Account expansion: suggest more people to call at the same company.

Planned:
- start(lead_id)
    same domain searched within EXPANSION_REPEAT_DAYS -> post link to that thread, stop
    create expansion run (searching) ->
    Deepline people search with the persona filter, max EXPANSION_MAX_PEOPLE ->
    drop the original person and anyone already in leads ->
    light enrichment (email only, no phone) -> Claude fit score ->
    insert as suggested (parent_lead_id, fit_reason) ->
    post one expansion card sorted by fit; run posted (or empty if nobody found)
- add_suggested(lead_id)    status received -> enrichment.enrich(with_phone=True)
- skip_suggested(lead_id)   status skipped -> grey out on the card
- Suggested people are never enrolled in sequences automatically.

Phase: 5 · Tests: tests/integration/test_expansion.py
"""
