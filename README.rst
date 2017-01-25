.. image:: https://travis-ci.org/ra1fh/eppconvert.svg?branch=master
    :target: https://travis-ci.org/ra1fh/eppconvert

eppconvert
==========

Tools to parse and convert Daum Ergo Bike EPP files. This contains a
mostly complete specification of the EPP/EUP file format, using
python-construct.

Requirements
------------

* `python <https://www.python.org>`_ (version 2.7, 3.3, 3.4, 3.5, or 3.6)

* `python-construct <https://pypi.python.org/pypi/construct>`_ (version 2.8)

* `docopt <https://pypi.python.org/pypi/docopt>`_ (version 0.6.2)

* Tested operating systems: Linux, OS X, OpenBSD, Windows


Installation
------------

The installation can be done with pip/pypi or from source.  In both
cases the scripts `gpx2epp` and `eppread` will be made available as
command line tools.

To install with pip from pypi:

::

    sudo python -m pip install eppconvert

Alternatively install from source:

::

    sudo python ./setup.py install

Usage
-----

gpx2epp
'''''''

Convert GPX to Daum EPP height profile. Writes a version 7 EPP file.

::

    Usage:
        gpx2epp [-i FILE] [-o FILE] [-s STEPSIZE]

    Options:
        -h, --help               Show this.
            --version            Show version.
        -i, --input FILE         Input GPX file (default: stdin).
        -o, --output FILE        Output EPP file (default: stdout).
        -s, --stepsize STEPSIZE  Stepsize in meters.


Here is an example that reads a GPX file and writes an EPP file to
stdout with a stepsize of 200 meters between data points:

::

    gpx2epp --input track.gpx --stepsize 200 > track.epp


Only the first track of the GPX file is converted, including all track
segments. Please note that arbitrary stepsize values can be used and
do usually work, but only files with a stepsize of 200 meters can be
modified with the control console editor.

eppread
'''''''

Read and print Daum Ergo Bike EPP/EUP files. Prints textual representation
to stdout.

::

    Usage:
        eppread [-i FILE] [-o FILE] [-l LIMIT]

    Options:
        -h, --help               Show this.
            --version            Show version.
        -i, --input FILE         Input EPP/EUP file (default: stdin).
        -o, --output FILE        Output text file (default: stdout).
        -l, --limit LIMIT        Limit of data points to print.

Example usage that reads an EPP file and prints the header and 5 data
points at most:

::

    eppread --input track.epp --limit 5

