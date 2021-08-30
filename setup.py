from setuptools import setup

url = "https://github.com/IMTEK-Simulation/dtool-sync"
version = "0.0.1"
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
    url=url,
    install_requires=[
        "dtool-cli",
    ],
    entry_points={
        'dtool.cli': ['sync=dtool_sync:sync'],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
