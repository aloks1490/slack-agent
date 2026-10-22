"""Shared pytest fixtures.

Planned:
- Fake clients that record every call, so tests can assert what was sent where:
  FakeRepo (in-memory Supabase), FakeDeepline, FakeHubSpot, FakeHeyReach,
  FakeInstantly, FakeLLM, FakeSlack
- settings fixture with dummy values (no real keys needed for the fast suite)
- load_fixture(name) helper for recorded payloads in tests/fixtures/
- Live tests skip automatically when their env vars are missing
"""
