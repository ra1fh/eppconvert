.. image:: https://github.com/ra1fh/eppconvert/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/ra1fh/eppconvert/actions/workflows/ci.yml

eppconvert
==========

Tools to parse and convert Daum Ergo Bike EPP files. This contains a
mostly complete specification of the EPP/EUP file format, using
python-construct.

Requirements
------------

* `python <https://www.python.org>`_ (version 3.6, 3.7, 3.8, 3.9)

* `python-construct <https://pypi.python.org/pypi/construct>`_ (version 2.8.10)

* `docopt <https://pypi.python.org/pypi/docopt>`_ (version 0.6.2)

* Tested operating systems: Linux, OS X, OpenBSD, Windows


Installation
------------

The installation can be done with pip/pypi or from source.  In both
cases the scripts `gpx2epp` and `eppread` will be made available as
command line tools.

Linux/MacOS/BSD
'''''''''''''''

To install with pip from pypi:

::

    python -m pip install eppconvert

Alternatively install from source:

::

    python ./setup.py install --user


Afterwards, gpx2eep and eppread will be installed in ``~/.local/bin``,
which you may want to add to your PATH environment variable.

Windows
'''''''

- Install Python 3.9 from https://www.python.org. Enable checkbox "Add Python to PATH" in the installer.
- In CMD shell (Windows key + R, cmd <RETURN>), run: ``python -m pip install eppconvert``
- Afterwards, gpx2epp and eppread are available in CMD shell

Usage
-----

gpx2epp
'''''''

Convert GPX to Daum EPP elevation profile. Writes a version 7 EPP file.

::

    Usage:
        gpx2epp [-i FILE] [-o FILE] [-s STEPSIZE]

    Options:
        -h, --help               Show this.
            --version            Show version.
        -i, --input FILE         Input GPX file (default: stdin).
        -o, --output FILE        Output EPP file (default: stdout).
        -s, --stepsize STEPSIZE  Stepsize in meters (default: 200).


Here is an example that reads a GPX file and writes an EPP file to
stdout with a stepsize of 200 meters between data points:

::

    gpx2epp --input track.gpx --stepsize 200 --output track.epp


Only the first track of the GPX file is converted, including all track
segments. Please note that arbitrary stepsize values can be used and
do usually work, but only files with a stepsize of 200 meters can be
modified with the control console editor.

To use the EPP file with the Daum bike, copy the EPP file to the Daum
SD card, directory ``/DAUM/PROGRAM``. The track can be selected via
"Menü -> Trainieren -> Standard-Programme -> Höhenprofil -> eigene
Programme"

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

