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

from __future__ import absolute_import, print_function

import difflib
import filecmp
import hexdump
import io
import os
import pytest
import sys

from eppconvert import gpx2epp
from eppconvert import eppread

TESTCASES = [ 'koeterberg', 'codepage', 'singlepoint', 'overflow']

@pytest.fixture(scope="module", params = TESTCASES)
def testfile(request):
    ''' return a list of test data files in the test/ directory '''
    testfile = request.param
    yield testfile

def test_gpx2epp(testfile):
    ''' test conversion from gpx to epp '''
    basename = 'test' + os.sep + testfile
    iname = basename + '.gpx'
    oname = basename + '.test.epp'
    result = gpx2epp.main(['-i', iname, '-o', oname, '-s', '200'])
    assert(result == 0)
    # generate diff of hexdumps that will be shown in case of failure
    with open(basename + '.test.epp', 'rb') as infile:
        hd = hexdump.hexdump(infile.read(), result='return')
        with open(basename + '.test.hex', 'w') as outfile:
            outfile.write(hd + '\n')
    a = open(basename + '.test.hex', 'r').readlines()
    b = open(basename + '.hex', 'r').readlines()
    print(''.join(difflib.unified_diff(a,b, basename + '.test.hex', basename + '.hex')))
    assert(filecmp.cmp(basename + '.epp', basename + '.test.epp'))

def test_gpx2epp_stdout(testfile, capfd):
    ''' test conversion from epp to plain text on stdout'''
    basename = 'test' + os.sep + testfile
    iname = basename + '.gpx'
    result = gpx2epp.main(['-i', iname])
    assert(result == 0)
    b = io.open(basename + '.epp', 'rb').read()
    out, err = capfd.readouterr()
    # Comparing binary strings captured from stdout
    # is quite tricky to do in a way that works with both
    # python 2 and 3. So do at least minimal test that works
    # reliably
    assert(out.startswith('EW2_EUP'))

def test_eppread(testfile):
    ''' test conversion from epp to plain text '''
    basename = 'test' + os.sep + testfile
    iname = basename + '.epp'
    oname = basename + '.test.txt'
    result = eppread.main(['-i', iname, '-o', oname])
    assert(result == 0)
    # generate diff that will be shown in case of failure
    a = io.open(basename + '.test.txt', encoding='utf-8').readlines()
    b = io.open(basename + '.txt', encoding='utf-8').readlines()
    print(''.join(difflib.unified_diff(a,b, basename + '.test.txt', basename + '.txt')))
    assert(filecmp.cmp(basename + '.txt', basename + '.test.txt'))

def test_eppread_stdout(testfile, capfd):
    ''' test conversion from epp to plain text on stdout'''
    basename = 'test' + os.sep + testfile
    iname = basename + '.epp'
    result = eppread.main(['-i', iname])
    assert(result == 0)
    out, err = capfd.readouterr()
    b = io.open(basename + '.txt', encoding='utf-8').read()
    assert(out == b)

if __name__ == "__main__":
    ''' setup data for test cases '''
    print("Generating known good data for test cases.")
    for testfile in TESTCASES:
        basename = 'test' + os.sep + testfile
        iname = basename + '.gpx'
        oname = basename + '.epp'
        result = gpx2epp.main(['-i', iname, '-o', oname, '-s', '200'])
        if result != 0:
            print("error: conversion from {0} to {1} failed.".format(iname, oname))
            sys.exit(1)
        iname = basename + '.epp'
        oname = basename + '.txt'
        result = eppread.main(['-i', iname, '-o', oname])
        if result != 0:
            print("error: conversion from {0} to {1} failed.".format(iname, oname))
            sys.exit(1)
        print('{0}: OK'.format(basename))
