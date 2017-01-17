[![Build Status](https://travis-ci.org/ra1fh/eppconvert.svg?branch=master)](https://travis-ci.org/ra1fh/eppconvert)

# eppconvert

Tools to parse and convert Daum Ergo Bike EPP files. This contains a
mostly complete specification of the epp/eup file format, using
python-construct.

## Requirements

  * [python](https://www.python.org) 2.7, 3.5, or 3.6

  * [python-construct](https://pypi.python.org/pypi/construct) 2.8

    The distribution-provided version of python-construct will likely
    be too old, so install the latest version with: `pip install
    construct`

## gpx2epp

gpx2epp reads the gpx file and writes epp version 7 file to
stdout. Example usage:

	./eppconvert/gpx2epp.py track.gpx 200 > track.epp

The optional second parameter determines the stepsize in meters the
epp file uses. The ergo bike can cope with arbitrary stepsizes, but
only files with a stepsize of 200 can be modified in the bike UI
editor.

Only the first track of the GPX is converted, including all track
segments.

## eppread

eppread reads an epp file and prints a textual representation to
stdout. Can be useful for debugging. Example usage:

	./eppconvert/eppread.py track.epp 5

The optional second parameter limits the number of data points that
are printed.
