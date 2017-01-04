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

class Point:
    lat = None
    lon = None
    ele = None
    dist = None
    total = None
    def __init__(self, lat=None, lon=None, ele=None, dist=None, total=None):
        self.lat = lat
        self.lon = lon
        self.ele = ele
        self.dist = dist
        self.total = total

class Profile:
    dist = None
    ele = None
    def __init__(self, dist=None, ele=None):
        self.dist = dist
        self.ele = ele

# see https://en.wikipedia.org/wiki/Great-circle_distance
# for calculating the distance between two geographical coordinates
def great_circle_distance(p1, p2):
    sdlat = math.sin((p1.lat - p2.lat) * math.pi / 180.0) / 2.0
    sdlon = math.sin((p1.lon - p2.lon) * math.pi / 180.0) / 2.0
    central_angle = 2.0 * math.asin(math.sqrt(sdlat * sdlat
                                              + math.cos(p1.lat * math.pi / 180.0)
                                              * math.cos(p2.lat * math.pi / 180.0)
                                              * sdlon * sdlon))
    return central_angle * EARTH_RADIUS

def read_gpx(filename):
    xml = minidom.parse(filename)
    pts = []
    for trk in xml.getElementsByTagName('trk')[0:1]:
        trkpts = trk.getElementsByTagName('trkpt')
        prev = None
        for trkpt in trkpts:
            ele = trkpt.getElementsByTagName('ele')
            if not ele or len(ele) < 1 or ele[0].firstChild == None:
                print('error: GPX track point has no elevation data (#',
                      len(pts), ')', file=sys.stderr, sep='')
                sys.exit(1)

            try:
                ele = float(ele[0].firstChild.nodeValue)
            except ValueError:
                print('error: GPX track point contains invalid elevation data (#',
                      len(pts), '): ', ele[0].firstChild.nodeValue,
                      file=sys.stderr, sep='')
                sys.exit(1)

            try:
                lat = float(trkpt.getAttribute('lat'))
            except ValueError:
                print('error: GPX track point contains invalid latitude data (#',
                      len(pts), '): ', trkpt.getAttribute('lat'), file=sys.stderr, sep='')
                sys.exit(1)

            try:
                lon = float(trkpt.getAttribute('lon'))
            except ValueError:
                print('error: GPX track point contains invalid longitude data (#',
                      len(pts), '): ', trkpt.getAttribute('lon'), file=sys.stderr, sep='')
                sys.exit(1)

            p = Point(lat, lon, ele, 0.0, 0.0)
            if prev:
                p.dist = great_circle_distance(prev, p)
                p.total = prev.total + p.dist
            pts.append(p)
            prev = p
    return pts

class State:
    profile = None
    prev = None
    target = None
    stepsize = None
    def __init__(self, stepsize, profile=[], target=0.0, prev=None):
        self.stepsize = stepsize
        self.profile = profile
        self.prev = prev
        self.target = target

def transform(s, x):
    while x.total > s.target:
        if x.total != s.prev.total:
            section = (s.target - s.prev.total) / (x.total - s.prev.total)
            climb = section * (x.ele - s.prev.ele)
            ele = s.prev.ele + climb
        else:
            ele = (x.ele - s.prev.ele) / 2 + s.prev.ele
        s.profile.append(Profile(s.stepsize, ele))
        s.target += s.stepsize
    s.prev = x
    return s

def calculate_profile(points, stepsize):
    state = State(stepsize=stepsize)
    reduce(transform, points, state)
    return state.profile

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

        points = read_gpx(sys.argv[1])
        if len(points) < 2:
            print("error: too few data points in GPX file:", len(points), file=sys.stderr)
            sys.exit(1)

        profile = calculate_profile(points, stepsize)
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
