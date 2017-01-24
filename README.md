[![Build Status](https://travis-ci.org/ra1fh/eppconvert.svg?branch=master)](https://travis-ci.org/ra1fh/eppconvert)

# eppconvert

Tools to parse and convert Daum Ergo Bike EPP files. This contains a
mostly complete specification of the epp/eup file format, using
python-construct.

## Requirements

  * [python](https://www.python.org) (version 2.7, 3.3, 3.4, 3.5, or 3.6)
  * [python-construct](https://pypi.python.org/pypi/construct) (version 2.8)
  * [docopt](https://pypi.python.org/pypi/docopt) (version 0.6.2)
  * Tested operating systems: Linux, OS X, OpenBSD

## Installation

    sudo python ./setup.py install

This will install `gpx2epp` and `eppread` including all dependencies
into `/usr/local/bin` or similar.

## Usage

### gpx2epp

Convert GPX to Daum EPP height profile.

    Usage:
        gpx2epp [-i FILE] [-o FILE] [-s STEPSIZE]

    Options:
        -h, --help               Show this.
            --version            Show version.
        -i, --input FILE         Input GPX file (default: stdin).
        -o, --output FILE        Output EPP file (default: stdout).
        -s, --stepsize STEPSIZE  Stepsize in meters.

gpx2epp reads the gpx file and writes an EPP version 7 height profile
to stdout. Example usage:

	gpx2epp --input track.gpx --stepsize 200 > track.epp

The optional stepsize parameter determines the stepsize in meters the
epp file uses. The ergo bike can cope with arbitrary stepsizes, but
only files with a stepsize of 200 can be modified in the bike UI
editor.

Only the first track of the GPX file is converted, including all track
segments.

### eppread

    Read and print Daum Ergo Bike EPP/EUP files.

    Usage:
        eppread [-i FILE] [-o FILE] [-l LIMIT]

    Options:
        -h, --help               Show this.
            --version            Show version.
        -i, --input FILE         Input EPP/EUP file (default: stdin).
        -o, --output FILE        Output text file (default: stdout).
        -l, --limit LIMIT        Limit of data points to print.

Eppread reads an epp file and prints a textual representation to
stdout. Can be useful for debugging. Example usage:

	eppread --input track.epp --limit 5

The optional second parameter limits the number of data points that
are printed.
