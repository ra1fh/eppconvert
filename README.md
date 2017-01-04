# eppconvert

Tools to parse and convert Daum Ergo Bike EPP files. This contains a
mostly complete specification of the epp/eup file format, using
python-construct.

## Requirements

 * python-2.7 or python-3.4
 * (python-construct 2.8)[https://pypi.python.org/pypi/construct]

## gpx2epp

Reads gpx file and writes epp version 7 file to stdout. Example usage:

	gpx2epp.py track.gpx 200 > track.epp

The optional second parameter determines the stepsize the hight
profile uses in meters. The ergo bike can cope with arbitrary
stepsizes, but only files with a stepsize of 200 can be modified in
the bike UI editor.

Only the first track of the GPX is converted, including all track
segments.

## eppread

Reads an epp file and prints a textual representation to
stdout. Usefule for debugging. Example usage:

	eppread.py track.epp 5

The optional second parameter limits the number of data points that
are printed.
