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

"""
convert gpx to epp dist/height profile
"""

from __future__ import print_function
from xml.dom import minidom

import functools
import math
import os
import sys

import eppformat as epp

EARTH_RADIUS = 6378137.0

class GpxPoint:
    def __init__(self, lat=None, lon=None, ele=None, dist=None, total=None):
        self.lat = lat
        self.lon = lon
        self.ele = ele
        self.dist = dist
        self.total = total

class GpxReader:
    def __init__(self, filename):
        self.name = None

        xml = minidom.parse(filename)
        self.points = []
        for trk in xml.getElementsByTagName('trk')[0:1]:
            name = trk.getElementsByTagName('name')
            if name and len(name) > 0 and name[0].firstChild != None:
                self.name = name[0].firstChild.nodeValue
            trkpts = trk.getElementsByTagName('trkpt')
            for trkpt in trkpts:
                ele = trkpt.getElementsByTagName('ele')
                if not ele or len(ele) < 1 or ele[0].firstChild == None:
                    print('error: GPX track point has no elevation data (#',
                          len(self.points), ')', file=sys.stderr, sep='')
                    sys.exit(1)

                try:
                    ele = float(ele[0].firstChild.nodeValue)
                except ValueError:
                    print('error: GPX track point contains invalid elevation data (#',
                          len(self.points), '): ', ele[0].firstChild.nodeValue,
                          file=sys.stderr, sep='')
                    sys.exit(1)

                try:
                    lat = float(trkpt.getAttribute('lat'))
                except ValueError:
                    print('error: GPX track point contains invalid latitude data (#',
                          len(self.points), '): ', trkpt.getAttribute('lat'), file=sys.stderr, sep='')
                    sys.exit(1)

                try:
                    lon = float(trkpt.getAttribute('lon'))
                except ValueError:
                    print('error: GPX track point contains invalid longitude data (#',
                          len(self.points), '): ', trkpt.getAttribute('lon'), file=sys.stderr, sep='')
                    sys.exit(1)

                p = GpxPoint(lat, lon, ele, 0.0, 0.0)
                self.points.append(p)
        if len(self.points) > 1:
            functools.reduce(self.reducefunction, self.points)

    def reducefunction(self, p1, p2):
        p2.dist = self.great_circle_distance(p1, p2)
        p2.total = p1.total + p2.dist
        return p2

    # see https://en.wikipedia.org/wiki/Great-circle_distance
    # for calculating the distance between two geographical coordinates
    def great_circle_distance(self, p1, p2):
        sdlat = math.sin((p1.lat - p2.lat) * math.pi / 180.0) / 2.0
        sdlon = math.sin((p1.lon - p2.lon) * math.pi / 180.0) / 2.0
        squared = math.cos(p1.lat * math.pi / 180.0) * \
                  math.cos(p2.lat * math.pi / 180.0) * \
                  sdlon**2 + sdlat**2
        central_angle = 2.0 * math.asin(math.sqrt(squared))
        return central_angle * EARTH_RADIUS

class ProfilePoint:
    def __init__(self, dist=None, ele=None):
        self.dist = dist
        self.ele = ele

class ProfileGenerator:
    def __init__(self, points, stepsize):
        self.stepsize = stepsize
        self.profile = []
        self.target = 0.0
        self.prev = None
        functools.reduce(self.transform, points)

    def transform(self, p1, p2):
        while p2.total > self.target:
            if p2.total != p1.total:
                section = (self.target - p1.total) / (p2.total - p1.total)
                climb = section * (p2.ele - p1.ele)
                ele = p1.ele + climb
            else:
                ele = (p2.ele - p1.ele) / 2 + p1.ele
            self.profile.append(ProfilePoint(self.stepsize, ele))
            self.target += self.stepsize
        return p2

class EppBuilder:
    def __init__(self, profile, stepsize, title, descr):
        header = dict(title=title,
                      description=descr,
                      type='DIST_HEIGHT',
                      third='NONE',
                      length=len(profile),
                      graphmin=0,
                      graphmax=self.graphmax(profile),
                      stepsize=stepsize,
                      blr=dict(run=1, lyps=1, bike=1),
                      startheight=0,
                      maxwatt=0,
                      maxpulse=0,
                      maxspeed=0)
        data = list(map(lambda x : dict(val1=int(x.dist), val2=x.ele, val3=0), profile))
        eppinfo = dict(version='VERSION_7',
                       header=header,
                       data=data)
        self.eppdata = epp.epp_file.build(eppinfo)

    def graphmax(self, profile):
        m = functools.reduce(self.max, profile).ele
        if m < 500:
            return 500
        elif m < 1000:
            return 1000
        elif m < 2000:
            return 2000
        else:
            return 4000

    def max(self, x, y):
        if x.ele > y.ele:
            return x
        else:
            return y

def main():
    if (len(sys.argv) > 1):
        if (len(sys.argv) > 2):
            stepsize = int(sys.argv[2])
        else:
            stepsize = 200

        gpx = GpxReader(sys.argv[1])
        points = gpx.points
        if len(points) < 1:
            print("error: no track points in GPX file.", file=sys.stderr)
            sys.exit(1)

        profile = ProfileGenerator(points, stepsize).profile
        if len(profile) > 3000:
            print("error: number of steps exceeds limit of 3000:", len(profile), file=sys.stderr)
            print("       Please try to use a higher stepsize than", stepsize, file=sys.stderr)
            sys.exit(1)
        if len(profile) < 1:
            print("error: no epp data points after conversion.", file=sys.stderr)
            sys.exit(1)

        if gpx.name:
            title = gpx.name
        else:
            title = str(os.path.basename(sys.argv[1]))
        descr = "file=" + str(os.path.basename(sys.argv[1])) + \
                ", stepsize=" + str(stepsize)
        title = title[0:49]
        descr = descr[0:255]
        eppdata = EppBuilder(profile, stepsize, title, descr).eppdata
        with os.fdopen(sys.stdout.fileno(), 'wb') as f:
            f.write(eppdata)
    else:
        print("usage: gpx2epp <file> [stepsize]")
        sys.exit(1);

if __name__ == "__main__":
    main()