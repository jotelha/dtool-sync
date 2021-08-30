"""Test the dtool-cli package."""

from click.testing import CliRunner


def test_version_is_string():
    import dtool_cli
    assert isinstance(dtool_cli.__version__, str)


def test_dtool():
    from dtool_cli.cli import dtool
    runner = CliRunner()
    result = runner.invoke(dtool)
    assert result.exit_code == 0
