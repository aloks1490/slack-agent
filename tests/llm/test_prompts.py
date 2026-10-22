"""AI output checks. Marked `llm`: skipped by default, cost tokens.
Run on purpose with:  uv run pytest -m llm

Planned cases:
- research: exactly 3 talking points, only facts present in the input,
  "data missing" for the near-empty payload
- fit score: 1-5, reason <= 120 chars, intern/recruiter <= 2
- LinkedIn draft: <= 300 chars, no emojis, no "I hope this finds you well",
  has a next step, one-word notes stay generic
"""
