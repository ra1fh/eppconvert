#!/usr/bin/env python

"""
convert gpx into epp dist/height profile
"""

from __future__ import print_function
from xml.dom import minidom

import math
import sys

import eppread as epp

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
            p = Point(float(trkpt.getAttribute('lat')),
                      float(trkpt.getAttribute('lon')),
                      float(trkpt.getElementsByTagName('ele')[0].firstChild.nodeValue),
                      0.0, 0.0)
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
    raster = None
    def __init__(self, raster, profile=[], target=0.0, prev=None):
        self.raster = raster
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
        s.profile.append(Profile(s.raster, ele))
        s.target += s.raster
    s.prev = x
    return s

def calculate_profile(points, raster):
    state = State(raster=raster)
    reduce(transform, points, state)
    return state.profile

def build_epp(profile, raster):
    header = dict(title='test',
                  description='test',
                  type='DIST_HEIGHT',
                  third='NONE',
                  length=len(profile),
                  graphmin=0,
                  graphmax=500,
                  raster=raster,
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
            raster = float(sys.argv[2])
        else:
            raster = 500.0
        points = read_gpx(sys.argv[1])
        profile = calculate_profile(points, raster)
        eppdata = build_epp(profile, raster)
        print(eppdata)
    else:
        print("usage: gpx2epp <file>")
        sys.exit(1);
