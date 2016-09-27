#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup
from thermalprinter import __version__


open('MANIFEST.in', 'w').write('include *.rst\n')


setup(
    name='thermalprinter',
    version=__version__,
    packages=['thermalprinter'],
    author='Tiger-222',
    license='zlib/libpng',
    author_email='contact@tiger-222.fr',
    description='Driver for the DP-EH600 thermal printer (AdaFruit).',
    long_description=open('README.rst').read(),
    include_package_data=True,
    install_requires=[
        'pyserial >= 3.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: zlib/libpng License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Printing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers'
    ],
    url='https://github.com/BoboTiG/thermalprinter'

)
