"""Test the dtool-sync package."""

import json

from click.testing import CliRunner

from . import compare_nested, comparison_marker_from_obj, compare_marked_nested


def test_dtool_diff_q(lhs_repository_fixture, rhs_repository_fixture, expected_output_diff_q):
    from dtool_sync.cli import diff
    runner = CliRunner()
    result = runner.invoke(diff, ['-q', lhs_repository_fixture, rhs_repository_fixture])
    assert result.exit_code == 0
    assert '\n'.join(result.stdout.splitlines()[2:]) == '\n'.join(expected_output_diff_q.splitlines()[2:])


def test_dtool_compare_all_j(comparable_repositories_fixture, expected_output_compare_all_j):
    from dtool_sync.cli import compare_all
    lhs_uri, rhs_uri = comparable_repositories_fixture
    runner = CliRunner()
    result = runner.invoke(compare_all, ['-j', lhs_uri, rhs_uri])
    assert result.exit_code == 0
    out = json.loads(result.stdout)
    expected = json.loads(expected_output_compare_all_j)
    assert compare_nested(out, expected)


def test_dtool_compare_all_qj(comparable_repositories_fixture, expected_output_compare_all_qj):
    from dtool_sync.cli import compare_all
    lhs_uri, rhs_uri = comparable_repositories_fixture
    runner = CliRunner()
    result = runner.invoke(compare_all, ['-q', '-j', lhs_uri, rhs_uri])
    assert result.exit_code == 0
    out = json.loads(result.stdout)
    expected = json.loads(expected_output_compare_all_qj)
    assert compare_nested(out, expected)


def test_dtool_compare_all_jr(comparable_repositories_fixture, expected_output_compare_all_jr):
    from dtool_sync.cli import compare_all
    lhs_uri, rhs_uri = comparable_repositories_fixture
    runner = CliRunner()
    result = runner.invoke(compare_all, ['-j', '-r', lhs_uri, rhs_uri])
    assert result.exit_code == 0
    out = json.loads(result.stdout)
    expected = json.loads(expected_output_compare_all_jr)
    assert compare_nested(out, expected)


def test_dtool_compare_all_qu(comparable_repositories_fixture, expected_output_compare_all_qu):
    from dtool_sync.cli import compare_all
    lhs_uri, rhs_uri = comparable_repositories_fixture
    runner = CliRunner()
    result = runner.invoke(compare_all, ['-q', '-u', lhs_uri, rhs_uri])
    assert result.exit_code == 0
    assert result.stdout == expected_output_compare_all_qu


def test_dtool_sync_all(comparable_repositories_fixture, expected_output_compare_all_jr, expected_output_post_sync_all_compare_all_jr):
    from dtool_sync.cli import sync_all, compare_all
    lhs_uri, rhs_uri = comparable_repositories_fixture

    runner = CliRunner()

    # first, content of base URIs differs
    result = runner.invoke(compare_all, ['-j', '-r', lhs_uri, rhs_uri])
    assert result.exit_code == 0
    out = json.loads(result.stdout)
    expected = json.loads(expected_output_compare_all_jr)
    assert compare_nested(out, expected)

    # next, we sync
    result = runner.invoke(sync_all, [lhs_uri, rhs_uri])
    assert result.exit_code == 0

    # eventually, content must be equal
    result = runner.invoke(compare_all, ['-j', '-r', lhs_uri, rhs_uri])
    assert result.exit_code == 0
    out = json.loads(result.stdout)
    expected = json.loads(expected_output_post_sync_all_compare_all_jr)
    assert compare_nested(out, expected)


