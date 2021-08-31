"""dtool_sync module."""

import click
import difflib

from . import _direct_list, _format_dataset_list
from .compare import compare_dataset_lists

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
    """Print textual diff between left hand side base URI and right hand side base URI UUID lists."""
    lhs_info = _direct_list(lhs_base_uri, raw=False)
    rhs_info = _direct_list(rhs_base_uri, raw=False)

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

@sync.command()
@click.option("-t", "--terse", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@click.option("-j", "--json", is_flag=True)
@click.option("-r", "--raw", is_flag=True)
@click.argument("source_base_uri")
@click.argument("target_base_uri")
def compare(source_base_uri, target_base_uri,
            marker={'uuid': True, 'name': True, 'frozen_at': True}, # key 'created_at' apparently introduced in later dtool versions
            verbose=True, terse=False, json=True, raw=False,
            print_equal=True,
            print_differing=True,
            print_missing=True):
    """Print diff report between left hand side base URI and right hand side."""
    source_info = _direct_list(source_base_uri, raw=raw)
    target_info = _direct_list(target_base_uri, raw=raw)

    equal, differing, missing = compare_dataset_lists(source_info, target_info, marker)

    if len(equal) > 0 and print_equal:
        if not terse:
            print("")
            print("Datasets equal on source and target:")
            print("")
        click.secho(
            _format_dataset_list(equal, quiet=terse, verbose=verbose, json=json, ls_output=True))

    if len(differing) > 0 and print_differing:
        if not terse:
            print("")
            print("Datasets differing between source and target:")
            print("")
        click.secho(
            _format_dataset_list(differing, quiet=terse, verbose=verbose, json=json, ls_output=True))

    if len(missing) > 0 and print_missing:
        if not terse:
            print("")
            print("Datasets misssing on target:")
            print("")
        click.secho(
            _format_dataset_list(missing, quiet=terse, verbose=verbose, json=json, ls_output=True))


@sync.command()
@click.option("-t", "--terse", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@click.option("-j", "--json", is_flag=True)
@click.option("-r", "--raw", is_flag=True)
@click.argument("source_base_uri")
@click.argument("target_base_uri")
def missing(source_base_uri, target_base_uri,
            marker={'uuid': True, 'name': True, 'frozen_at': True}, # key 'created_at' apparently introduced in later dtool versions
            verbose=True, terse=False, json=True, raw=False):
    """Report datasets present at source but missing at target."""
    source_info = _direct_list(source_base_uri, raw=raw)
    target_info = _direct_list(target_base_uri, raw=raw)

    _, _, missing = compare_dataset_lists(source_info, target_info, marker)

    if len(missing) > 0:
        click.secho(
            _format_dataset_list(missing, quiet=terse, verbose=verbose, json=json))


@sync.command()
@click.option("-t", "--terse", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@click.option("-j", "--json", is_flag=True)
@click.option("-r", "--raw", is_flag=True)
@click.argument("source_base_uri")
@click.argument("target_base_uri")
def equal(source_base_uri, target_base_uri,
            marker={'uuid': True, 'name': True, 'frozen_at': True}, # key 'created_at' apparently introduced in later dtool versions
            verbose=True, terse=False, json=True, raw=False):
    """Report datasets that equal each other at source and at target."""
    source_info = _direct_list(source_base_uri, raw=raw)
    target_info = _direct_list(target_base_uri, raw=raw)

    equal, _, _ = compare_dataset_lists(source_info, target_info, marker)

    if len(equal) > 0:
        click.secho(
            _format_dataset_list(equal, quiet=terse, verbose=verbose, json=json))


@sync.command()
@click.option("-t", "--terse", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@click.option("-j", "--json", is_flag=True)
@click.option("-r", "--raw", is_flag=True)
@click.argument("source_base_uri")
@click.argument("target_base_uri")
def differing(source_base_uri, target_base_uri,
            marker={'uuid': True, 'name': True, 'frozen_at': True}, # key 'created_at' apparently introduced in later dtool versions
            verbose=True, terse=False, json=True, raw=False):
    """Report datasets present but differing at source and target."""
    source_info = _direct_list(source_base_uri, raw=raw)
    target_info = _direct_list(target_base_uri, raw=raw)

    _, differing, _ = compare_dataset_lists(source_info, target_info, marker)

    if len(differing) > 0:
        click.secho(
            _format_dataset_list(differing, quiet=terse, verbose=verbose, json=json))