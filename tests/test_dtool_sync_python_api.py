"""Test the dtool-sync package."""

from click.testing import CliRunner

def test_version_is_string():
    import dtool_sync
    assert isinstance(dtool_sync.__version__, str)

