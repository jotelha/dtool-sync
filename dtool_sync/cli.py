"""dtool_sync module."""

import click
import logging

from dtool_create.dataset import _copy as copy_dataset

from . import (
    _list,
    _format_dataset_enumerable,
    _parse_file_size,
    _parse_query,
    _clean_cache
)

from .compare import compare_dataset_lists


logger = logging.getLogger(__name__)

# TODO: use 'dtool diff' functionality to properly compare frozen datasets
# TODO: make comparison marker a cli option
DEFAULT_COMPARISON_MARKER = {'uuid': True, 'name': True, 'frozen_at': True, 'type': True}
# key 'created_at' only introduced in later dtool versions, thus not included in comparison


@click.command()
@click.option("-n", "--dry-run", is_flag=True, help="Only print datasets that will be transferred.")
@click.option("-j", "--json", is_flag=True, default=False, help="Print metadata of compared datasets as JSON")
@click.option("-q", "--quiet", is_flag=True, default=False, help="Print less.")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Print more.")
@click.option("--changed-only", is_flag=True, default=False,
              help="Sync only datasets present bu differing at both base URIs.")
@click.option("--missing-only", is_flag=True, default=False,
              help="Sync only datasets missing at right hand side base URI.")
@click.option('--lhs-query', default="none", type=click.UNPROCESSED, callback=_parse_query,
              help="""If lhs source is a lookup server, filter listed datasets by query.""")
@click.option('--rhs-query', default="none", type=click.UNPROCESSED, callback=_parse_query,
              help="""If rhs source is a lookup server, filter listed datasets by query.""")
@click.option("--ignore-errors", is_flag=True,
              help="In case of an error, continue with copying next dataset instead of stopping with an error.")
@click.option('--max-cache-size', default="none", type=click.UNPROCESSED, callback=_parse_file_size,
              help="""All synced datasets are cached locally. 
                      Specify maximum cache size here (i.e. --max-cache-size 5GB) 
                      to delete older cache entries when limit exceeded. Specify 
                      0 (zero) to empty cache after each copied dataset. Per
                      default, never empty cache.""")
@click.argument("source_base_uri")
@click.argument("target_base_uri")
@click.argument("tertiary_base_uri", required=False)
def sync(source_base_uri, target_base_uri, lhs_query, rhs_query,
         dry_run, ignore_errors, json, quiet, verbose,
         changed_only, missing_only,
         max_cache_size, tertiary_base_uri=None, marker=DEFAULT_COMPARISON_MARKER):
    """One-way comparison and synchronization from 'SOURCE_BASE_URI' to 'TARGET_BASE_URI'.
       If 'TERTIARY_BASE_URI' specified, will compare with 'TARGET_BASE_URI', but actually
       copy to 'TERTIARY_BASE_URI'."""
    source_info = _list(source_base_uri, query=lhs_query)
    target_info = _list(target_base_uri, query=rhs_query)

    equal, changed, missing = compare_dataset_lists(source_info, target_info, marker)
    out_dict = {
        "equal": equal,
        "changed": changed,
        "missing": missing,
    }

    if not quiet or json:
        click.echo(
            _format_dataset_enumerable(out_dict, quiet=quiet, verbose=verbose,
                                       json=json, ls_output=True)
        )

    if tertiary_base_uri is not None:
        target_base_uri = tertiary_base_uri

    if not missing_only:
        if not quiet:
            click.secho(
                "Resume sync of changed datasets, assuming their transfer might have been interrupted earlier.")

        for src_ds, dst_ds in changed:
            if dry_run:
                if not quiet:
                    click.secho(f"Dry run, would copy {src_ds['uri']} to {target_base_uri} now.")
            else:
                try:
                    copy_dataset(resume=True, quiet=quiet, dataset_uri=src_ds["uri"],
                                 dest_base_uri=target_base_uri)
                except Exception as exc:
                    if not ignore_errors:
                        raise
                    else:
                        logger.exception(exc)

                if max_cache_size is not None:
                    _clean_cache(max_cache_size)

    if not changed_only:
        if not quiet:
            click.secho("Copy missing datasets.")

        for src_ds in missing:
            if dry_run:
                if not quiet:
                    click.secho(f"Dry run, would copy {src_ds['uri']} to {target_base_uri} now.")
            else:
                try:
                    copy_dataset(resume=False, quiet=quiet, dataset_uri=src_ds["uri"],
                                 dest_base_uri=target_base_uri)
                except OSError as exc:
                    raise # might have run out of storage
                except Exception as exc:
                    try:
                        copy_dataset(resume=True, quiet=quiet, dataset_uri=src_ds["uri"],
                                     dest_base_uri=target_base_uri)
                    except OSError as exc:
                        raise  # might have run out of storage
                    except Exception as exc:
                        if not ignore_errors:
                            raise
                        else:
                            logger.exception(exc)

                if max_cache_size is not None:
                    _clean_cache(max_cache_size)
