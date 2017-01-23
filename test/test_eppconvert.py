
import os
import codecs
import pytest
import filecmp
import difflib
import hexdump

from eppconvert import gpx2epp
from eppconvert import eppread

@pytest.fixture(scope="module", params = [ 'koeterberg', 'codepage', 'singlepoint', 'overflow'])
def testfile(request):
    testfile = request.param
    yield testfile

def test_eppread(testfile):
    basename = 'test' + os.sep + testfile
    result = eppread.main(['-i', basename + '.epp', '-o', basename + '.test.txt'])
    assert(result == 0)
    a = codecs.open(basename + '.test.txt', encoding='utf-8').readlines()
    b = codecs.open(basename + '.txt', encoding='utf-8').readlines()
    print(''.join(difflib.unified_diff(a,b, basename + '.test.txt', basename + '.txt')))
    assert(filecmp.cmp(basename + '.txt', basename + '.test.txt'))

def test_gpx2epp(testfile):
    basename = 'test' + os.sep + testfile
    result = gpx2epp.main(['-i', basename + '.gpx', '-o', basename + '.test.epp'])
    assert(result == 0)
    with open(basename + '.test.epp', 'rb') as infile:
        hd = hexdump.hexdump(infile.read(), result='return')
        with open(basename + '.test.hex', 'w') as outfile:
            outfile.write(hd + '\n')
    a = open(basename + '.test.hex', 'r').readlines()
    b = open(basename + '.hex', 'r').readlines()
    print(''.join(difflib.unified_diff(a,b, basename + '.test.hex', basename + '.hex')))
    assert(filecmp.cmp(basename + '.hex', basename + '.test.hex'))
