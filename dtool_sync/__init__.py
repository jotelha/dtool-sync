"""dtool_sync module."""

try:
    from importlib.metadata import version, PackageNotFoundError
except ModuleNotFoundError:
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
   pass


import json as JSON

import click
import dtoolcore

from dtool_info.utils import sizeof_fmt, date_fmt

from dtool_cli.cli import (
    CONFIG_PATH,
)


def _direct_list(base_uri, config_path=CONFIG_PATH, raw=True):
    """Directly list all datasets at base_uri via suitable storage broker.

    Parameters
    ----------
    base_uri: str
    config_path: str
    raw: bool, default: True
        if set, just yield admin metadata as returned by dtoolcore._admin_metadata_from_uri
        otherwise, reformat list entries as done by dtool_info.dataset._list_datasets
    """
    base_uri = dtoolcore.utils.sanitise_uri(base_uri)
    storage_broker = dtoolcore._get_storage_broker(base_uri, config_path)
    info = []

    for uri in storage_broker.list_dataset_uris(base_uri, config_path):
        admin_metadata = dtoolcore._admin_metadata_from_uri(uri, config_path)

        if raw:
            i = admin_metadata
            i['uri'] = uri
        else:
            name = admin_metadata["name"]
            if admin_metadata["type"] == "protodataset":
                name = "*" + name
            i = dict(
                name=name,
                uuid=admin_metadata["uuid"],
                creator_username=admin_metadata["creator_username"],
                uri=uri)
            if "frozen_at" in admin_metadata:
                i["frozen_at"] = date_fmt(admin_metadata["frozen_at"])
        info.append(i)

    # depending on the underlying storage, it is possible to have the same dataset with equivalent UUID
    # exist multiple times under differing names.
    by_uuid_and_name = sorted(info, key=lambda d: (d['uuid'], d['name']))
    return by_uuid_and_name


def _field_exists(e, field):
    return field in e[0] if isinstance(e, tuple) else field in e

def _extract_field(e, field):
    return e[0][field] if isinstance(e, tuple) else e[field]


def _json_format_dataset_list(dataset_list, quiet=False, verbose=False):
    """Formats list of dataset for pretty JSON output, returns list with modified entries."""
    if quiet:
        dataset_list = [_extract_field(element, 'uuid') for element in dataset_list]
    elif verbose:
        pass
    else:
        d = [{
            "name": _extract_field(element, 'name'),
            "uuid": _extract_field(element, 'uuid'),
            "creator_username": _extract_field(element, 'creator_username'),
        } for element in dataset_list]
        for el, ed in zip(dataset_list, d):
            if _field_exists(el, "frozen_at"):
                ed["frozen_at"] = str(_extract_field(el, 'frozen_at'))
        dataset_list = d
    return dataset_list


def _json_format_dataset_enumerable(dataset_enumerable, quiet=False, verbose=False):
    if isinstance(dataset_enumerable, dict):
        out_enumerable = {key: _json_format_dataset_list(value, quiet=quiet, verbose=verbose) for key, value in dataset_enumerable.items()}
    else:
        out_enumerable = _json_format_dataset_list(dataset_enumerable, quiet=quiet, verbose=verbose)
    return out_enumerable


def _txt_format_dataset_list(dataset_list, quiet=False, verbose=False, ls_output=False):
    """Format a list of dataset metadata entries as text."""
    out_string = ''
    if ls_output:  # output as formatted by 'dtool ls', not very meaningful for diffs
        for i in dataset_list:
            if quiet:
                out_string += _extract_field(i, "uri") + '\n'
                continue
            out_string += _extract_field(i, "name") + '\n'
            out_string += "  " + _extract_field(i, "uri") + '\n'
            if verbose:
                out_string += "  " + _extract_field(i, "creator_username")
                if _field_exists(i, "frozen_at"):
                    out_string += "  " + str(_extract_field(i, "frozen_at"))
                out_string += "  " + _extract_field(i, 'uuid') + '\n'
    else:  # ls-like output, but emphasizing uuids, excluding uris
        for i in dataset_list:
            if quiet:
                out_string += _extract_field(i, 'uuid') + '\n'
                continue
            out_string += _extract_field(i, "uuid") + '\n'
            out_string += "  " + _extract_field(i, "uri") + '\n'
            if verbose:
                out_string += "  " + _extract_field(i, "creator_username")
                if _field_exists(i, "frozen_at"):
                    out_string += "  " + str(_extract_field(i, 'frozen_at'))
                out_string += "  " + _extract_field(i, "name") + '\n'
    return out_string.rstrip()


def _txt_format_dataset_enumerable(dataset_enumerable, quiet=False, verbose=False, ls_output=True):
    key_label_pairs = {
        "equal": "Datasets equal on source and target:",
        "changed": "Datasets changed from source to target:",
        "missing": "Datasets missing on target:",
    }
    key_color_pairs = {
        "equal": "green",
        "changed": "yellow",
        "missing": "red"
    }
    if isinstance(dataset_enumerable, dict):
        out_string = ''
        for key, value in dataset_enumerable.items():
            if key not in key_label_pairs:
                raise ValueError(f"{key} not allowed.")
            if not quiet:
                out_string += click.style(key_label_pairs[key], bold=True) + '\n'
            out_string += click.style(
                _txt_format_dataset_list(value, quiet=quiet, verbose=verbose, ls_output=ls_output),
                fg=key_color_pairs[key]) + '\n'
    else:
        out_string = _txt_format_dataset_list(dataset_enumerable, quiet=quiet, verbose=verbose, ls_output=ls_output)

    return out_string.rstrip()


def _format_dataset_enumerable(dataset_enumerable, quiet=False, verbose=False, json=False, ls_output=False):
    if json:
        return JSON.dumps(
            _json_format_dataset_enumerable(dataset_enumerable, quiet=quiet, verbose=verbose),
            indent=4)
    else:
        return _txt_format_dataset_enumerable(dataset_enumerable, quiet=quiet, verbose=verbose, ls_output=ls_output)
