#!/usr/bin/env python

from pontoon.meta import (__version__, __description__, __author__,
                          __author_email__, __url__)
from glob import glob
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'pontoon',
]

requires = ["docopt >= 0.6.0",
            "PyYAML",
            "requests"]

scripts = glob('scripts/pontoon*')

setup(
    name='pontoon',
    version=__version__,
    description=__description__,
    long_description=open('docs/README.rst').read(),
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'pontoon': 'pontoon'},
    scripts=scripts,
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ),
)
