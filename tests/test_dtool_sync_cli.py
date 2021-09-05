"""Test the dtool-sync package."""

from click.testing import CliRunner


def test_version_is_string():
    import dtool_sync
    assert isinstance(dtool_sync.__version__, str)


def test_dtool_diff_q(lhs_repository_fixture, rhs_repository_fixture, lhs_rhs_diff_q_output):
    from dtool_sync.cli import diff
    runner = CliRunner()
    result = runner.invoke(diff, ['-q', lhs_repository_fixture, rhs_repository_fixture])
    assert result.exit_code == 0
    assert '\n'.join(result.stdout.splitlines()[2:]) == lhs_rhs_diff_q_output


def test_dtool_compare_all_tj(lhs_repository_fixture, rhs_repository_fixture):
    from dtool_sync.cli import compare_all
    runner = CliRunner()
    result = runner.invoke(compare_all, [lhs_repository_fixture, rhs_repository_fixture])
    assert result.exit_code == 0
    # assert '\n'.join(result.stdout.splitlines()[2:]) == lhs_rhs_diff_q_output
    print(result.stdout)
