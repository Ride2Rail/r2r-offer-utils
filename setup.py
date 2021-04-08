#!/usr/bin/env python3
"""# Ride2Rail offer categorizer utils
"""

from setuptools import setup, find_packages

setup(
    name='r2r_offer_utils',
    version='0.1',
    author='Ride2Rail Project',
    author_email='',
    license='MIT',
    description='Utilities for building services in the Ride2Rail project.',
    long_description=__doc__,
    url='https://github.com/Ride2Rail/r2r-offer-utils',
    packages=find_packages(),
    entry_points={},
    options={
        'build_scripts': {
            'executable': 'python3',
        },
    },
    install_requires=[],
    py_modules=[],
    zip_safe=False
)
