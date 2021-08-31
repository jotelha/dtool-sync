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


def _format_dataset_list(l, quiet=False, verbose=False, json=False, ls_output=False):
    """Format a list of dataset metadata entries as text."""
    if json:  # print as indented json
        if quiet:
            l = [_extract_field(e, 'uuid') for e in l]
        elif verbose:
            pass
        else:
            d = [{
                    "name": _extract_field(e, 'name'),
                    "uuid": _extract_field(e, 'uuid'),
                    "creator_username": _extract_field(e, 'creator_username'),
                } for e in l]
            for el, ed in zip(l, d):
                if _field_exists(el, "frozen_at"):
                    ed["frozen_at"] = str(_extract_field(el, 'frozen_at'))
            l = d
        s = JSON.dumps(l, indent=4)
    elif ls_output:  # output as formatted by 'dtool ls', not very meaningful for diffs
        s = ''
        for i in l:
            if quiet:
                s += _extract_field(i, "uri") + '\n'
                continue
            s += _extract_field(i, "name") + '\n'
            s += "  " + _extract_field(i, "uri") + '\n'
            if verbose:
                s += "  " + _extract_field(i, "creator_username")
                if _field_exists(i, "frozen_at"):
                    s += "  " + str(_extract_field(i, "frozen_at"))
                s += "  " + _extract_field(i, 'uuid') + '\n'
    else:  # ls-like output, but emphasizing uuids, excluding uris
        s = ''
        for i in l:
            if quiet:
                s += _extract_field(i, 'uuid') + '\n'
                continue
            s += _extract_field(i, "name") + '\n'
            s += "  " + _extract_field(i, "uuid") + '\n'
            if verbose:
                s += "  " + _extract_field(i, "creator_username")
                if _field_exists(i, "frozen_at"):
                    s += "  " + str(_extract_field(i, 'frozen_at'))
                s += '\n'
    return s