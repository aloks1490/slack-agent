"""Phase 0 spike: find out what Deepline actually returns before building on it.

Plan:
1. Read DEEPLINE_API_KEY from .env.
2. For each tool we plan to use, fetch its input contract (free):
   GET /api/v2/integrations/{toolId}/get
3. Run each tool on 3-5 real LinkedIn profiles:
   person from LinkedIn URL, company enrichment, email waterfall Play
   (prebuilt/person-linkedin-to-email), a phone tool, people search on the company domain.
4. Save every raw response to tests/fixtures/deepline/<tool>__<slug>.json
5. Print a summary: which fields came back (title, followers, connections, email,
   phone...), time taken, and cost per call.
6. Fill in docs/deepline-findings.md with the results and the decisions.

Run with:  uv run python scripts/deepline_spike.py
"""
