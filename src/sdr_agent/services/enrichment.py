"""Enrichment pipeline (runs as a background job, ~1-3 minutes).

Planned:
- enrich(lead_id, with_phone=True)
    status enriching ->
    Deepline: person -> company -> email waterfall (+ validation) ->
    phone (only if senior enough and with_phone) ->
    Claude: research summary + talking points + ICP fit ->
    save to Supabase, status enriched ->
    crm_sync.sync(lead_id) (Phase 3) ->
    post the lead card in the thread
  A failed lookup records what is missing and carries on; only a crash marks the lead error.

Phase: 2 · Tests: tests/integration/test_enrichment.py
"""
