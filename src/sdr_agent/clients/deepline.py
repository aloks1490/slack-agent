"""Deepline client: person/company enrichment, email waterfall, phone, people search.

API (REST, no Python SDK):
  base URL      https://code.deepline.com
  auth          Authorization: Bearer <DEEPLINE_API_KEY>
  tool schema   GET  /api/v2/integrations/{toolId}/get        (free, no execution)
  run a tool    POST /api/v2/integrations/{toolId}/execute    body {"payload": {...}}
  run a Play    POST /api/v2/plays/run          body {"name": "prebuilt/...", "input": {...}}
  Play result   GET  /api/v2/runs/{url-encoded run id}        poll until completed/failed/cancelled

Planned:
- get_tool_schema(tool_id) -> dict
- execute_tool(tool_id, payload) -> dict
- run_play(name, input, timeout_s) -> dict        starts, then polls with backoff
- enrich_person(linkedin_url) -> PersonData
- enrich_company(domain_or_url) -> CompanyData
- find_work_email(linkedin_url) -> EmailResult    e.g. Play "prebuilt/person-linkedin-to-email"
- find_phone(person) -> PhoneResult
- search_people(company_domain, persona, limit) -> list[PersonSummary]

Open questions for the Phase 0 spike (scripts/deepline_spike.py):
exact tool IDs, follower/connection counts, phone coverage, cost per call, rate limits.

Phase: 0 (spike) -> 2
"""
