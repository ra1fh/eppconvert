[![Build Status](https://travis-ci.org/ra1fh/eppconvert.svg?branch=master)](https://travis-ci.org/ra1fh/eppconvert)

# eppconvert

Tools to parse and convert Daum Ergo Bike EPP files. This contains a
mostly complete specification of the epp/eup file format, using
python-construct.

## Requirements

  * [python](https://www.python.org) (version 2.7, 3.2, 3.3, 3.4, 3.5, or 3.6)

  * [python-construct](https://pypi.python.org/pypi/construct) (version 2.8)


## Installation

    sudo python ./setup.py install

This will install `gpx2epp` and `eppread` in `/usr/bin` or similar.

## Usage

### gpx2epp

gpx2epp reads the gpx file and writes epp version 7 file to
stdout. Example usage:

	gpx2epp --input track.gpx --stepsize 200 > track.epp

The optional stepsize parameter determines the stepsize in meters the
epp file uses. The ergo bike can cope with arbitrary stepsizes, but
only files with a stepsize of 200 can be modified in the bike UI
editor.

Only the first track of the GPX is converted, including all track
segments.

### eppread

eppread reads an epp file and prints a textual representation to
stdout. Can be useful for debugging. Example usage:

	eppread --input track.epp --limit 5

The optional second parameter limits the number of data points that
are printed.
