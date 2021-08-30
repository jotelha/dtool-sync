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


import difflib
import dtoolcore


from dtool_cli.cli import (
    CONFIG_PATH,
)

# from dtool_info.utils import sizeof_fmt, date_fmt


def _make_marker(d):
    """Mark everything for comparison."""
    if isinstance(d, list):
        return [_make_marker(e) for e in d]
    elif isinstance(d, dict):
        return {k: _make_marker(v) for k, v in d.items()}
    else:
        return True


def _compare(source, target, marker):
    """Compare source and target partially, as marked by marker."""
    logger = logging.getLogger(__name__)
    if isinstance(marker, dict):
        for k, v in marker.items():
            if k not in source:
                logger.error("{} not in source '{}'.".format(k, source))
                return False
            if k not in target:
                logger.error("{} not in target '{}'.".format(k, source))
                return False

            logger.debug("Descending into sub-tree '{}' of '{}'.".format(
                source[k], source))
            # descend
            if not _compare(source[k], target[k], v):
                return False  # one failed comparison suffices

    elif isinstance(marker, list):  # source, target and marker must have same length
        logger.debug("Branching into element wise sub-trees of '{}'.".format(
            source))
        for s, t, m in zip(source, target, marker):
            if not _compare(s, t, m):
                return False  # one failed comparison suffices
    else:  # arrived at leaf, comparison desired?
        if marker is not False:  # yes
            logger.debug("Comparing '{}' == '{}' -> {}.".format(
                source, target, source == target))
            return source == target

    # comparison either not desired or successfull for all elements
    return True


def _compare_nested(source, target, marker=None):
    """Compare source and target partially, as marked by marker. If marker is None, then compare everything."""
    if not marker:
        marker = _make_marker(source)
    return _compare(source, target, marker)


def _forward_compare(source, target, marker=None):
    """One-way-compare two dicts of nested dict and categorize into 'equal', 'differing' and 'missing'."""
    missing = dict()
    differing = dict()
    equal = dict()

    for k, sd in source.items():
        if k in target:
            td = target[k]
            is_equal = _compare_nested(sd, td, marker)
            if is_equal:
                equal[k] = (sd, td)
            else:
                differing[k] = (sd, td)
        else:
            missing[k] = sd

    return equal, differing, missing


def _ds_list_to_dict(l):
    """Convert list of dataset metadata entries to dict with UUIDs as keys."""
    return {e['uuid']: e for e in l}


def _direct_list(base_uri, config_path=CONFIG_PATH):
    """Directly list all datasets at base_uri via suitable storage broker."""
    base_uri = dtoolcore.utils.sanitise_uri(base_uri)
    storage_broker = dtoolcore._get_storage_broker(base_uri, config_path)
    info = []

    for uri in storage_broker.list_dataset_uris(base_uri, config_path):
        admin_metadata = dtoolcore._admin_metadata_from_uri(uri, config_path)
        info.append(admin_metadata)

    by_name = sorted(info, key=lambda d: d['name'])
    return by_name


def _format_nested(l):
    """Print a nested structure, i.e list or dict."""
    return json.dumps(l, indent=4)


def _format_dataset_list(l, verbose=True):
    """Print a list of dataset metadata entries."""
    if not verbose:
        l = [e[0]['uuid'] if isinstance(e, tuple) else e['uuid'] for e in l]
    return _format_nested(l)


def _get_info(storage_broker):
    info = []

    for uri in storage_broker.list_dataset_uris(base_uri, CONFIG_PATH):
        admin_metadata = dtoolcore._admin_metadata_from_uri(uri, CONFIG_PATH)
        name = admin_metadata["name"]
        if admin_metadata["type"] == "protodataset":
            fg = "red"
            name = "*" + name
        i = dict(
            name=name,
            uuid=admin_metadata["uuid"],
            creator=admin_metadata["creator_username"],
            uri=uri,
            fg=fg)
        if "frozen_at" in admin_metadata:
            i["date"] = date_fmt(admin_metadata["frozen_at"])
        info.append(i)

    return info


# def _list_datasets(base_uri):
#    base_uri = dtoolcore.utils.sanitise_uri(base_uri)
#    storage_broker = dtoolcore._get_storage_broker(base_uri, CONFIG_PATH)
#    return _get_info(storage_broker)


@click.command()
@click.argument("lhs_base_uri")
@click.argument("rhs_base_uri")
def udiff(lhs_base_uri, rhs_base_uri):
    """Print UUID diff list between left hand side base URI and right hand side base URI."""
    lhs_info = _direct_list(lhs_base_uri)
    rhs_info = _direct_list(rhs_base_uri)

    lhs_str = _format_dataset_list(lhs_info)
    rhs_str = _format_dataset_list(rhs_info)

    diff = difflib.ndiff(
        lhs_str.splitlines(keepends=True),
        rhs_str.splitlines(keepends=True))

    for line in diff:
        click.secho(line)


