import logging


def compare_nested(A, B):
    """Compare nested dicts and lists."""
    if isinstance(A, list) and isinstance(B, list):
        for a, b in zip(A, B):
            if not compare_nested(a, b):
                return False
        return True

    if isinstance(A, dict) and isinstance(B, dict):
        if set(A.keys()) == set(B.keys()):
            for k in A.keys():
                if not compare_nested(A[k], B[k]):
                    return False
            return True
        else:
            return False
    return A == B


def comparison_marker_from_obj(obj):
    """Mark all nested objects for comparison."""
    if isinstance(obj, list):
        marker = []
        for elem in obj:
            marker.append(comparison_marker_from_obj(elem))
    elif isinstance(obj, dict):
        marker = {}
        for k, v in obj.items():
            marker[k] = comparison_marker_from_obj(v)
    else:
        marker = True
    return marker


def compare_marked_nested(A, B, marker):
    """Compare source and target partially, as marked by marker."""
    logger = logging.getLogger(__name__)
    if isinstance(marker, dict):
        for k, v in marker.items():
            if k not in A:
                logger.error("{} not in A '{}'.".format(k, A))
                return False
            if k not in B:
                logger.error("{} not in B '{}'.".format(k, A))
                return False

            logger.debug("Descending into sub-tree '{}' of '{}'.".format(
                A[k], A))
            # descend
            if not compare_marked_nested(A[k], B[k], v):
                return False  # one failed comparison suffices
    # A, B and marker must have same length:
    elif isinstance(marker, list):
        if len(A) != len(B) or len(marker) != len(B):
            logger.debug("A, B, and marker don't have equal length at "
                         "'{}', '{}', '{}'.".format(A, B, marker))
            return False
        logger.debug("Branching into element wise sub-trees of '{}'.".format(
            A))
        for s, t, m in zip(A, B, marker):
            if not compare_marked_nested(s, t, m):
                return False  # one failed comparison suffices
    else:  # arrived at leaf, comparison desired?
        if marker:  # yes
            logger.debug("Comparing '{}' == '{}' -> {}.".format(
                A, B, A == B))
            return A == B

    # comparison either not desired or successful for all elements
    return True
