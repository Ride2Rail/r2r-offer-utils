#!/usr/bin/env python3
"""compressed_stream
   -----------------
   A simple python module to handle streams of compressed files.

"""

from setuptools import setup, find_packages

setup(
    name='r2r_offer_utils',
    version='0.0.2',
    author='',
    author_email='',
    license='MIT',
    description='',
    long_description=__doc__,
    url='https://github.com/CristianCantoro/compressed_stream',
    packages=find_packages(),
    entry_points={},
    options={
        'build_scripts': {
            'executable': 'python3',
        },
    },
    install_requires=[],
    zip_safe=False,
)
