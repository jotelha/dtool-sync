from setuptools import setup
from setuptools_scm import get_version
version = get_version(root='.', relative_to=__file__)

def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


url = "https://github.com/IMTEK-Simulation/dtool-sync"
readme = open('README.rst').read()

setup(
    name="dtool-sync",
    packages=["dtool_sync"],
    version=version,
    description="One-way synchronization utility fo data management command line tool dtool.",
    long_description=readme,
    include_package_data=True,
    author="Johanns L. Hörmann",
    author_email="johannes.hoermann@imtek.uni-freiburg.de",
    use_scm_version={"local_scheme": local_scheme},
    url=url,
    setup_requires=['setuptools_scm'],
    install_requires=[
        "click",
        "dtoolcore",
        "dtool-cli",
        "humanfirendly",
    ],
    entry_points={
        'dtool.cli': ['sync=dtool_sync.cli:sync', 'compare=dtool_sync.cli:compare'],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
