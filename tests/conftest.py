"""Test fixtures."""

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


# Pytest does not add the working directory to the path so we do it here.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, "..")
sys.path.insert(0, _ROOT)

_DATA = os.path.join(_HERE, "data")

SAMPLE_DATASETS_DIR = os.path.join(_DATA, "datasets")


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

    return  lhs_uri_fixture


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

    return  rhs_uri_fixture


@pytest.fixture
def lhs_rhs_diff_q_output(request):
    return """@@ -1,4 +1,4 @@
 065d9fe0-9e41-4add-8a55-577dbcfe2149
-534792bd-d102-4efc-bc11-6af743959704
+7cc9d271-54c8-4685-99bf-70d872da0cc6
 9ee101a4-7d1a-45c0-8955-da779398a5ed
 c2249963-6459-4901-8263-85610a7a2ac9
"""