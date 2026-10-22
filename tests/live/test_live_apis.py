"""Live tests against real APIs. Marked `live`: skipped by default, cost credits.
Run on purpose with:  uv run pytest -m live

Planned cases:
- one known public test profile through each Deepline tool -> result shape
- HubSpot: create then delete a test contact
- HeyReach / Instantly: TEST campaigns only, never real ones
"""
