#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'docopt',
    'colorlog'
]

test_requirements = [
    'pytest',
    'requests',
    'coverage',
]


setup(
    name='lcrs-embedded',
    version="1.0dev",
    description=(
        "The embedded component of LCRS - Software for computer refurbishment "
        "workshops: Wipe disks, test hardware, store results in database."
    ),
    long_description=readme,
    author="Benjamin Bach",
    author_email='benjamin@fairdanmark.dk',
    url='https://github.com/fairdk/lcrs-embedded',
    packages=[
        'lcrs_embedded',
    ],
    package_dir={'lcrs_embedded': 'lcrs_embedded'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='computer reuse, recycling, logistics',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'lcrs-embedded = lcrs_embedded.cli:main'
        ]
    },
)
