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

import math
import sys
import os

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
        xml = minidom.parse(filename)
        self.points = []
        for trk in xml.getElementsByTagName('trk')[0:1]:
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
        if len(self.points) < 2:
            print('error: GPX track contains too few data points:',
                  len(self.points), file=sys.stderr)
            sys.exit(1)
        reduce(self.reducefunction, self.points)

    def reducefunction(self, p1, p2):
        p2.dist = self.great_circle_distance(p1, p2)
        p2.total = p1.total + p2.dist
        return p2

    # see https://en.wikipedia.org/wiki/Great-circle_distance
    # for calculating the distance between two geographical coordinates
    def great_circle_distance(self, p1, p2):
        sdlat = math.sin((p1.lat - p2.lat) * math.pi / 180.0) / 2.0
        sdlon = math.sin((p1.lon - p2.lon) * math.pi / 180.0) / 2.0
        central_angle = 2.0 * math.asin(math.sqrt(sdlat * sdlat
                                                  + math.cos(p1.lat * math.pi / 180.0)
                                                  * math.cos(p2.lat * math.pi / 180.0)
                                                  * sdlon * sdlon))
        return central_angle * EARTH_RADIUS

    def points(self):
        return self.points

class ProfilePoint:
    def __init__(self, dist=None, ele=None):
        self.dist = dist
        self.ele = ele

class ProfileGenerator:
    def __init__(self, stepsize, profile=[], target=0.0, prev=None):
        self.stepsize = stepsize
        self.profile = profile
        self.prev = prev
        self.target = target

    def transform(self, s, x):
        while x.total > s.target:
            if x.total != s.prev.total:
                section = (s.target - s.prev.total) / (x.total - s.prev.total)
                climb = section * (x.ele - s.prev.ele)
                ele = s.prev.ele + climb
            else:
                ele = (x.ele - s.prev.ele) / 2 + s.prev.ele
            s.profile.append(ProfilePoint(s.stepsize, ele))
            s.target += s.stepsize
        s.prev = x
        return s

    def calculate_profile(self, points):
        reduce(self.transform, points, self)
        return self.profile

def build_epp(profile, stepsize, title, descr):
    maxheight = reduce(lambda x,y : x if x.ele > y.ele else y, profile).ele
    if maxheight < 500:
        graphmax = 500
    elif maxheight < 1000:
        graphmax = 1000
    elif maxheight < 2000:
        graphmax = 2000
    else:
        graphmax = 4000
    header = dict(title=title,
                  description=descr,
                  type='DIST_HEIGHT',
                  third='NONE',
                  length=len(profile),
                  graphmin=0,
                  graphmax=graphmax,
                  stepsize=stepsize,
                  blr=dict(run=1, lyps=1, bike=1),
                  startheight=0,
                  maxwatt=0,
                  maxpulse=0,
                  maxspeed=0)
    data = map(lambda x : dict(val1=int(x.dist), val2=x.ele, val3=0), profile)
    eppinfo = dict(version='VERSION_7',
                   header=header,
                   data=data)
    eppdata = epp.epp_file.build(eppinfo)
    return eppdata

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        if (len(sys.argv) > 2):
            stepsize = float(sys.argv[2])
        else:
            stepsize = 200.0

        points = GpxReader(sys.argv[1]).points
        if len(points) < 2:
            print("error: too few data points in GPX file:", len(points), file=sys.stderr)
            sys.exit(1)

        profile = ProfileGenerator(stepsize).calculate_profile(points)
        if len(profile) > 3000:
            print("error: Number of steps exceeds limit of 3000:", len(profile), file=sys.stderr)
            print("       Please try to use a higher stepsize than", stepsize, file=sys.stderr)
            sys.exit(1)
        if len(profile) < 2:
            print("error: too few data points after conversion:", len(profile), file=sys.stderr)
            sys.exit(1)

        title = str(os.path.basename(sys.argv[1]))
        descr = "file=" + str(os.path.basename(sys.argv[1])) + ", " + \
                "stepsize=" + str(stepsize)
        eppdata = build_epp(profile, stepsize, title, descr)
        print(eppdata)
    else:
        print("usage: gpx2epp <file> [stepsize]")
        sys.exit(1);
