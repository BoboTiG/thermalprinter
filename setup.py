#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup

from thermalprinter import __version__


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3',
    'Topic :: Printing',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Hardware :: Hardware Drivers'
]
config = {
    'name': 'thermalprinter',
    'version': __version__,
    'author': 'Tiger-222',
    'author_email': 'contact@tiger-222.fr',
    'maintainer': 'Tiger-222',
    'maintainer_email': 'contact@tiger-222.fr',
    'url': 'https://github.com/BoboTiG/thermalprinter',
    'description': 'Driver for the DP-EH600 thermal printer (AdaFruit).',
    'long_description': open('README.rst').read(),
    'classifiers': classifiers,
    'platforms': ['Linux'],
    'license': 'MIT',
    'install_requires': ['pyserial >= 3.0'],
    'packages': ['thermalprinter'],
}

setup(**config)
