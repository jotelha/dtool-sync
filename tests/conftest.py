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
 0b5f7c56-5f7e-43de-9b16-bd6f7ac7da12
+33a30c8d-60c2-44ac-8ade-abe99a7e2f92
 5cb6d8bb-255b-4ca5-a445-c1f8121c5333
-9d14c3e3-2c87-4bff-9e17-3c51f5f535a0
 cc6519a9-7862-4b47-91d2-105d4ae64512"""