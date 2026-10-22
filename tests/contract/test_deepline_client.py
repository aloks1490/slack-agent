"""Contract tests for clients/deepline.py: replay recorded Deepline responses
(tests/fixtures/deepline/) through the real client code with respx.

Planned cases:
- each recorded response maps to the right model; missing fields -> None, not a crash
- "12,345"-style numbers parsed; Play polling handles running -> completed / failed
"""
