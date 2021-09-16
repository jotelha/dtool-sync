"""dtool_sync module."""

import click
import difflib
import logging

import humanfriendly

from dtool_create.dataset import _copy as copy_dataset

from . import (
    _direct_list,
    _format_dataset_enumerable,
    _parse_file_size,
    _clean_cache,
)
from .compare import compare_dataset_lists


logger = logging.getLogger(__name__)


@click.group()
def sync():
    """repository synchronization utilities."""


@click.group()
def compare():
    """repository comparison utilities."""


# textual compare

@compare.command()
@click.option("-q", "--quiet", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@click.option("-j", "--json", is_flag=True)
@click.argument("lhs_base_uri")
@click.argument("rhs_base_uri")
def diff(quiet, verbose, json, lhs_base_uri, rhs_base_uri):
    """Print textual diff between left hand side base URI and right hand side base URI UUID lists."""
    lhs_info = _direct_list(lhs_base_uri, raw=False)
    rhs_info = _direct_list(rhs_base_uri, raw=False)

    lhs_str = _format_dataset_enumerable(lhs_info, quiet=quiet, verbose=verbose, json=json)
    rhs_str = _format_dataset_enumerable(rhs_info, quiet=quiet, verbose=verbose, json=json)

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


# true compare

@compare.command(name="all")
@click.option("-j", "--json", is_flag=True, help="Print metadata of compared datasets as JSON")
@click.option("-q", "--quiet", is_flag=True, help="Print less.")
@click.option("-r", "--raw", is_flag=True, help="Compare and print raw metadata instead of reformatted values in the style of 'dtool ls' output.")
@click.option("-u", "--uuid", is_flag=True, help="Print UUIDs instead of names.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Print more metadata.")
@click.argument("source_base_uri")
@click.argument("target_base_uri")
def compare_all(source_base_uri, target_base_uri,
            json, quiet, raw, uuid, verbose,
            marker={'uuid': True, 'name': True, 'frozen_at': True}):  # key 'created_at' apparently introduced in later dtool versions:
    """Print diff report between source and target base URIs."""
    source_info = _direct_list(source_base_uri, raw=raw)
    target_info = _direct_list(target_base_uri, raw=raw)

    equal, changed, missing = compare_dataset_lists(source_info, target_info, marker)
    out_dict = {
        "equal": equal,
        "changed": changed,
        "missing": missing,
    }
    click.echo(
        _format_dataset_enumerable(out_dict, quiet=quiet, verbose=verbose, json=json, ls_output=not uuid)
    )


@compare.command(name="equal")
@click.option("-j", "--json", is_flag=True, help="Print metadata of compared datasets as JSON")
@click.option("-q", "--quiet", is_flag=True, help="Print less.")
@click.option("-r", "--raw", is_flag=True, help="Compare and print raw metadata instead of reformatted values in the style of 'dtool ls' output.")
@click.option("-u", "--uuid", is_flag=True, help="Print UUIDs instead of names.")
@click.option("-v", "--verbose", is_flag=True, help="Print more metadata.")
@click.argument("source_base_uri")
@click.argument("target_base_uri")
def compare_equal(source_base_uri, target_base_uri,
            json, quiet, raw, uuid, verbose,
            marker={'uuid': True, 'name': True, 'frozen_at': True}):  # key 'created_at' apparently introduced in later dtool versions:
    """Report datasets that equal each other at source and at target."""
    source_info = _direct_list(source_base_uri, raw=raw)
    target_info = _direct_list(target_base_uri, raw=raw)

    equal, _, _ = compare_dataset_lists(source_info, target_info, marker)
    click.echo(
        _format_dataset_enumerable(equal, quiet=quiet, verbose=verbose, json=json, ls_output=not uuid)
    )


@compare.command(name="changed")
@click.option("-j", "--json", is_flag=True, help="Print metadata of compared datasets as JSON")
@click.option("-q", "--quiet", is_flag=True, help="Print less.")
@click.option("-r", "--raw", is_flag=True, help="Compare and print raw metadata instead of reformatted values in the style of 'dtool ls' output.")
@click.option("-u", "--uuid", is_flag=True, help="Print UUIDs instead of names.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Print more metadata.")
@click.argument("source_base_uri")
@click.argument("target_base_uri")
def compare_missing(source_base_uri, target_base_uri,
            json, quiet, raw, uuid, verbose,
            marker={'uuid': True, 'name': True, 'frozen_at': True}):  # key 'created_at' apparently introduced in later dtool versions:
    """Report datasets present at source but missing at target."""
    source_info = _direct_list(source_base_uri, raw=raw)
    target_info = _direct_list(target_base_uri, raw=raw)

    _, changed, _ = compare_dataset_lists(source_info, target_info, marker)
    click.echo(
        _format_dataset_enumerable(changed, quiet=quiet, verbose=verbose, json=json, ls_output=not uuid)
    )


@compare.command(name="missing")
@click.option("-j", "--json", is_flag=True, help="Print metadata of compared datasets as JSON")
@click.option("-q", "--quiet", is_flag=True, help="Print less.")
@click.option("-r", "--raw", is_flag=True, help="Compare and print raw metadata instead of reformatted values in the style of 'dtool ls' output.")
@click.option("-u", "--uuid", is_flag=True, help="Print UUIDs instead of names.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Print more metadata.")
@click.argument("source_base_uri")
@click.argument("target_base_uri")
def compare_missing(source_base_uri, target_base_uri,
            json, quiet, raw, uuid, verbose,
            marker={'uuid': True, 'name': True, 'frozen_at': True}):  # key 'created_at' apparently introduced in later dtool versions:
    """Report datasets present at source but missing at target."""
    source_info = _direct_list(source_base_uri, raw=raw)
    target_info = _direct_list(target_base_uri, raw=raw)

    _, _, missing = compare_dataset_lists(source_info, target_info, marker)
    click.echo(
        _format_dataset_enumerable(missing, quiet=quiet, verbose=verbose, json=json, ls_output=not uuid)
    )


# sync

@sync.command(name="all")
@click.option("-n", "--dry-run", is_flag=True, help="Only print datasets that will be transferred.")
@click.option("-q", "--quiet", is_flag=True, help="Print less.")
@click.option("-u", "--uuid", is_flag=True, help="Print UUIDs instead of names.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Print more.")
@click.option("--ignore-errors", is_flag=True, help="In case of an error, continue with copying next dataset instead of stopping with an error.")
@click.option('--max-cache-size', default="none", type=click.UNPROCESSED, callback=_parse_file_size,
              help="""All synced datasets are cached locally. 
                      Specify maximum cache size here (i.e. --max-cache-size 5GB) 
                      to delete older cache entries when limit exceeded. Specify 
                      0 (zero) to empty cache after each copied dataset. Per
                      default, never empty cache.""")
@click.argument("source_base_uri")
@click.argument("target_base_uri")
def sync_all(source_base_uri, target_base_uri,
             dry_run, ignore_errors, quiet, uuid, verbose,
             max_cache_size,
             marker={'uuid': True, 'name': True, 'frozen_at': True}):  # key 'created_at' apparently introduced in later dtool versions:
    """Sync datasets from source to target base URIs."""
    source_info = _direct_list(source_base_uri, raw=True)
    target_info = _direct_list(target_base_uri, raw=True)

    equal, changed, missing = compare_dataset_lists(source_info, target_info, marker)
    out_dict = {
        "equal": equal,
        "changed": changed,
        "missing": missing,
    }

    if not quiet:
        click.echo(
            _format_dataset_enumerable(out_dict, quiet=quiet, verbose=verbose, json=False, ls_output=not uuid)
        )

        click.secho("Resume copying of changed datasets, presuming their transfer had been interrupted in an earlier attempt.")

    for src_ds, dst_ds in changed:
        try:
            copy_dataset(resume=True, quiet=quiet, dataset_uri=src_ds["uri"], dest_base_uri=target_base_uri)
        except Exception as exc:
            if not ignore_errors:
                raise
            else:
                logger.exception(exc)

    if not quiet:
        click.secho("Copy missing datasets.")

    for src_ds in missing:
        if dry_run:
            click.secho(f"Dry run, would copy {src_ds['uri']} to {target_base_uri} now.")
        else:
            try:
                copy_dataset(resume=False, quiet=quiet, dataset_uri=src_ds["uri"], dest_base_uri=target_base_uri)
            except OSError as exc:
                raise # might have run out of storage
            except Exception as exc:
                if not ignore_errors:
                    raise
                else:
                    logger.exception(exc)

            if max_cache_size is not None:
                _clean_cache(max_cache_size)
