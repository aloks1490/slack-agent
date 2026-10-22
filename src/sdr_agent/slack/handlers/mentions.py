"""Handles @icp-bot mentions.

Planned:
- on_app_mention(event, say, client)
    call services.intake.handle_mention, then reply in the thread:
      Invalid  -> "That doesn't look like a LinkedIn profile link"
      Existing -> lead card with "Already in the pipeline · owner · status · original thread"
      Created  -> "Enriching…" and submit services.enrichment.enrich as a background job

Phase: 0 (pong) -> 1
"""
