"""Unit tests for __version__.py."""

import newport_tlb6700  # noqa


def test_package_version():
    """Ensure the package version is defined and not set to the initial
    placeholder."""
    assert hasattr(newport_tlb6700, "__version__")
    assert newport_tlb6700.__version__ != "0.0.0"
