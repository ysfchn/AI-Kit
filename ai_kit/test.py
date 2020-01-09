"""Test app.py model."""
from .app import cleanaia
from .app import repairaia


def test_repairaia():
    """Test fun repairaia."""
    assert repairaia(aia_path='../devrim.aia')


def test_cleanaia():
    """Test fun cleanaia."""
    assert cleanaia(aia_path='../devrim.aia')
