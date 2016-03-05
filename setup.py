#!/usr/bin/env python

from pontoon.meta import (__version__, __description__, __author__,
                          __author_email__, __url__)
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'pontoon',
    'pontoon.cmd',
    'pontoon.lib'
]

requires = open("requirements/base.txt").read().split()

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
    entry_points={
        "console_scripts": [
            "pontoon = pontoon.cmd.pontoon:main",
            "pontoon-configure = pontoon.cmd.pontoon_configure:main",
            "pontoon-droplet = pontoon.cmd.pontoon_droplet:main",
            "pontoon-event = pontoon.cmd.pontoon_event:main",
            "pontoon-image = pontoon.cmd.pontoon_image:main",
            "pontoon-region = pontoon.cmd.pontoon_region:main",
            "pontoon-size = pontoon.cmd.pontoon_size:main",
            "pontoon-snapshot = pontoon.cmd.pontoon_snapshot:main",
            "pontoon-sshkey = pontoon.cmd.pontoon_sshkey:main"
        ]
    },
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ),
)
