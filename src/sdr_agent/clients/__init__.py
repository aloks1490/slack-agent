"""Clients: one thin wrapper per external API.

Rules: retries and timeouts live here; no business decisions. Services depend on
these, and tests replace them with fakes (tests/conftest.py).
"""
