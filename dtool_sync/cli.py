"""dtool_sync module."""

import click
import difflib

from . import _direct_list, _format_dataset_list


@click.group()
def sync():
    """synchronization utilities."""

@sync.command()
@click.option("-q", "--quiet", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@click.option("-j", "--json", is_flag=True)
@click.argument("lhs_base_uri")
@click.argument("rhs_base_uri")
def diff(quiet, verbose, json, lhs_base_uri, rhs_base_uri):
    """Print UUID diff list between left hand side base URI and right hand side base URI."""
    lhs_info = _direct_list(lhs_base_uri)
    rhs_info = _direct_list(rhs_base_uri)

    lhs_str = _format_dataset_list(lhs_info, quiet=quiet, verbose=verbose, json=json)
    rhs_str = _format_dataset_list(rhs_info, quiet=quiet, verbose=verbose, json=json)

    diff = difflib.unified_diff(
        lhs_str.splitlines(keepends=True),
        rhs_str.splitlines(keepends=True),
        fromfile=lhs_base_uri,
        tofile=rhs_base_uri)

    for i, line in enumerate(diff):
        c = "white"
        bold = False
        if i < 2:
            bold = True
        elif len(line) > 0 and line[0] == '+':
            c = "green"
        elif len(line) > 0 and line[0] == '-':
            c = "red"
        elif len(line) > 1 and line[0:2] == '@@':
            c = "bright_cyan"
        click.secho(line, nl=False, fg=c, bold=bold)
    click.secho('')
