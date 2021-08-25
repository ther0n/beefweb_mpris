from setuptools import setup, find_packages

setup(
    name="beefweb_mpris",
    version="1.0.0",
    author="Theron Tjapkes",
    description="Adds MPRIS support to foobar2000 through beefweb",
    url="https://github.com/ther0n/beefweb_mpris",
    packages=["beefweb_mpris"],
    entry_points='''
    [console_scripts]
    beefweb_mpris=beefweb_mpris.main:main
    ''',
    install_requires=[
        'mpris_server',
        'pyfoobeef',
        'pyyaml',
        'pygobject'
    ]
)
