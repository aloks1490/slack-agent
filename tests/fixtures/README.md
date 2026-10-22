# Test fixtures

Recorded API payloads used by contract and integration tests, so tests never call
real APIs. The Phase 0 spike (`scripts/deepline_spike.py`) saves real Deepline
responses into `deepline/`; Slack event and interaction payloads go in `slack/`.

Strip personal data you don't need before committing (keep shapes, not people).
