import logging

import json
import math

import dtoolcore
from dtool_cli.cli import CONFIG_PATH


def _make_marker(d):
    """Mark everything for comparison."""
    if isinstance(d, list):
        return [_make_marker(e) for e in d]
    elif isinstance(d, dict):
        return {k: _make_marker(v) for k, v in d.items()}
    else:
        return True


def _equal(source, target):
    """Treats slightly differing floats as equal."""

    # type-dependent treatment:
    # the lookup server yields floats with lower accuracy then the direct storage broker,
    # i.e. comparison will fail at '1646312878.401044' == '1646312878.401'
    if isinstance(source, float) and isinstance(target, float):
        return math.isclose(source, target, rel_tol=1e-9, abs_tol=0.0)
    else:
        return source == target


def _compare(source, target, marker):
    """Compare source and target partially, as marked by marker."""
    logger = logging.getLogger(__name__)
    if isinstance(marker, dict):
        for k, v in marker.items():
            if k not in source:
                logger.info("{} not in source '{}'.".format(k, source))
                return False
            if k not in target:
                logger.info("{} not in target '{}'.".format(k, source))
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
                source, target, _equal(source, target)))
            return _equal(source, target)

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
    StorageBroker = dtoolcore._get_storage_broker(base_uri, config_path)
    info = []

    for uri in StorageBroker.list_dataset_uris(base_uri, config_path):
        admin_metadata = dtoolcore._admin_metadata_from_uri(uri, config_path)
        info.append(admin_metadata)

    by_name = sorted(info, key=lambda d: d['name'])
    return by_name


def compare_dataset_lists(source, target, marker=None):
    """One-way compare source and target dataset metadata lists by fields set True within marker."""
    s = _ds_list_to_dict(source)
    t = _ds_list_to_dict(target)
    equal, differing, missing = _forward_compare(s, t, marker)
    return list(equal.values()), list(differing.values()), list(missing.values())
