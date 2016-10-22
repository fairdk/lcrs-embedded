#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='lcrs-embedded',
    version='1.0dev',
    description=(
        "The embedded component of LCRS - Software for computer refurbishment "
        "workshops: Wipe disks, test hardware, store results in database."
    ),
    long_description=readme + '\n\n' + history,
    author="Benjamin Bach",
    author_email='benjamin@fairdanmark.dk',
    url='https://github.com/fairdk/lcrs-embedded',
    packages=[
        'lcrs_embedded',
    ],
    package_dir={'lcrs_embedded':
                 'lcrs_embedded'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='lcrs_embedded',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
