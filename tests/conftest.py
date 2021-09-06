"""Test fixtures."""

import json
import os
import shutil
import sys
import tempfile

import pytest

import dtoolcore
from dtoolcore.utils import (
    IS_WINDOWS,
    windows_to_unix_path,
)

from . import comparison_marker_from_obj

# Pytest does not add the working directory to the path so we do it here.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, "..")
sys.path.insert(0, _ROOT)

_DATA = os.path.join(_HERE, "data")

SAMPLE_DATASETS_DIR = os.path.join(_DATA, "datasets")
EXPECTED_OUTPUT_DIR = os.path.join(_DATA, "expected_output")


def dir_to_uri(d):
    if IS_WINDOWS:
        return "file://" + windows_to_unix_path(d)
    return "file://" + d


@pytest.fixture
def lhs_uri_fixture(request):
    d = tempfile.mkdtemp()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)

    return dir_to_uri(d)


@pytest.fixture
def rhs_uri_fixture(request):
    d = tempfile.mkdtemp()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)

    return dir_to_uri(d)


@pytest.fixture
def lhs_repository_fixture(lhs_uri_fixture):
    for file in os.listdir(SAMPLE_DATASETS_DIR):
        src = os.path.join(SAMPLE_DATASETS_DIR, file)
        if os.path.isdir(src):
            if file == 'he':
                continue
            src = dir_to_uri(src)
            dest = lhs_uri_fixture
            dtoolcore.copy(src, dest)

    return lhs_uri_fixture


@pytest.fixture
def rhs_repository_fixture(rhs_uri_fixture):
    for file in os.listdir(SAMPLE_DATASETS_DIR):
        src = os.path.join(SAMPLE_DATASETS_DIR, file)
        if os.path.isdir(src):
            if file == 'people':
                continue
            src = dir_to_uri(src)
            dest = rhs_uri_fixture
            dtoolcore.copy(src, dest)

    return rhs_uri_fixture


@pytest.fixture
def comparable_repositories_fixture(request):
    lhs_src_tree = os.path.join(_DATA, "comparable", "lhs")
    rhs_src_tree = os.path.join(_DATA, "comparable", "rhs")

    d = tempfile.mkdtemp()
    lhs_dest_tree = os.path.join(d, 'lhs')
    rhs_dest_tree = os.path.join(d, 'rhs')
    lhs_uri = dir_to_uri(shutil.copytree(lhs_src_tree, lhs_dest_tree))
    rhs_uri = dir_to_uri(shutil.copytree(rhs_src_tree, rhs_dest_tree))

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)

    return lhs_uri, rhs_uri


# expected outputs
@pytest.fixture
def expected_output_diff_q(request):
    with open(os.path.join(EXPECTED_OUTPUT_DIR, 'test_dtool_compare_diff_q.out'), 'r') as f:
        return f.read()


@pytest.fixture
def expected_output_compare_all_j(request):
    with open(os.path.join(EXPECTED_OUTPUT_DIR,'test_dtool_compare_all_j.out'), 'r') as f:
        return f.read()


@pytest.fixture
def expected_output_compare_all_qj(request):
    with open(os.path.join(EXPECTED_OUTPUT_DIR,'test_dtool_compare_all_qj.out'), 'r') as f:
        return f.read()


@pytest.fixture
def expected_output_compare_all_jr(request):
    with open(os.path.join(EXPECTED_OUTPUT_DIR,'test_dtool_compare_all_jr.out'), 'r') as f:
        return f.read()


@pytest.fixture
def expected_output_compare_all_qu(request):
    with open(os.path.join(EXPECTED_OUTPUT_DIR,'test_dtool_compare_all_qu.out'), 'r') as f:
        return f.read()


@pytest.fixture
def expected_output_post_sync_all_compare_all_jr(request):
    with open(os.path.join(EXPECTED_OUTPUT_DIR,'test_dtool_post_sync_all_comparison.out'), 'r') as f:
        return f.read()


# @pytest.fixture
# def comparison_marker_post_sync_all(request):
#     with open(os.path.join(EXPECTED_OUTPUT_DIR,'test_dtool_post_sync_all_comparison.out'), 'r') as f:
#         sample_data = json.load(f)
#     marker = comparison_marker_from_obj(sample_data)
#     return marker



