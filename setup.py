# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from lesspy import __version__

setup(
    name = 'lesspy',
    version = __version__,
    description = """
    Helps compile collections of LESS files into CSS files

    * Given a source directory, recursively finds LESS (.less/lss) files
    * Saves resulting CSS files to ``destination_path``, using the same
      directory structure as the source.
    """,
    author = 'Ryan Petrello',
    author_email = 'ryan (at) ryanpetrello.com',
    install_requires = [],
    test_suite='lesspy.tests.suite',
    zip_safe = False,
    packages = find_packages(exclude=['ez_setup'])
)
