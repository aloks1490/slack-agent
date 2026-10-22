"""Smoke test: the package imports. Keeps CI green until the real tests exist."""

import sdr_agent


def test_package_imports():
    assert sdr_agent.__doc__
