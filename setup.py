#!/usr/bin/env python
#
# Copyright (c) 2017 Ralf Horstmann <ralf@ackstorm.de>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import io
import os
import sys
import codecs

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = ""
    for line in f:
        if not 'travis-ci.org' in line:
            long_description += line

sys.path.insert(0, here + '/eppconvert')
from eppconvert.release import __version__

setup(
    name='eppconvert',
    version=__version__,

    description='Parse and convert Daum Ergo Bike EPP files',
    long_description=long_description,

    url='https://github.com/ra1fh/eppconvert',

    author='Ralf Horstmann',
    author_email='ralf@ackstorm.de',

    license='ISC',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages(exclude=['test']),

    install_requires=['construct>=2.8', 'docopt>=0.6.2'],

    entry_points={
        'console_scripts': [
            'eppread=eppconvert.eppread:main',
            'gpx2epp=eppconvert.gpx2epp:main',
        ],
    },
)
