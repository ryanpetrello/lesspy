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

    * Given a source directory, recursively finds LESS (.less/lss/.css) files
    * Saves compiled CSS files to a destination path, using the same directory
      structure as the source.
    """,
    long_description     = None,
    classifiers          = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Internet :: WWW/HTTP :: Browsers'
    ],
    keywords            = 'less lesscss css compile',
    url                 = 'http://github.com/ryanpetrello/lesspy',
    author              = 'Ryan Petrello',
    author_email        = 'ryan (at) ryanpetrello.com',
    license             = 'MIT',
    install_requires    = [],
    test_suite          = 'lesspy.tests.suite',
    zip_safe            = False,
    packages            = find_packages(exclude=['ez_setup'])
)
