import os
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="beefweb_mpris",
    version="1.0.3",
    author="Theron Tjapkes",
    description="Adds MPRIS support to foobar2000 through beefweb",
    url="https://github.com/ther0n/beefweb_mpris",
    packages=["beefweb_mpris"],
    entry_points='''
    [console_scripts]
    beefweb_mpris=beefweb_mpris.main:main
    ''',
    install_requires=required
)
