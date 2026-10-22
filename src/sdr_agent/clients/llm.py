"""Claude client (official SDK: anthropic) for the three AI tasks.

Setup:
- model from settings.claude_model (default "claude-opus-5-5"), effort "low"
- structured outputs: client.messages.parse(..., output_format=<Pydantic model>)
  -> response.parsed_output is a validated object
- server-side refusal fallback enabled (fallbacks="default")
- prompts are plain text files in src/sdr_agent/prompts/

Planned:
- research(enrichment) -> Research          summary, talking points, icp_fit
- fit_score(person, persona, original_lead) -> FitScore
- draft_message(lead, call_notes, goal, sdr_name, previous_draft=None) -> LinkedInDraft
    previous_draft is passed on "Regenerate" so the new draft differs

Phase: 2 (research), 5 (fit score), 6 (drafts)
"""
