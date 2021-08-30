"""Test the dtool-sync package."""

from click.testing import CliRunner

def test_version_is_string():
    import dtool_sync
    assert isinstance(dtool_sync.__version__, str)


def test_dtool_diff(lhs_repository_fixture, rhs_repository_fixture):
    from dtool_sync import diff
    runner = CliRunner()
    result = runner.invoke(diff, [lhs_repository_fixture, rhs_repository_fixture])
    # assert result.exit_code == 0
