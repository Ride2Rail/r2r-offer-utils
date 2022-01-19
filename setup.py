#!/usr/bin/env python3
"""Ride2Rail offer categorizer utils"""

from distutils.core import setup

packages = ['r2r_offer_utils']

package_data = {'': ['*']}

setup(
    name='r2r_offer_utils',
    version='0.2.3',
    description='Utilities for building services in the Ride2Rail project.',
    author='Ride2Rail Project',
    author_email='cristian.consonni@eurecat.org',
    url='https://github.com/Ride2Rail/r2r-offer-utils/',
    license='MIT',
    long_description=__doc__,
    packages=packages,
    package_data=package_data
)
