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
parse daum ergo bike epp/eup files
"""

from __future__ import print_function

import os
import sys
import string
import argparse
import eppconvert.eppformat as epp

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def eppread(document, limit=None):
    output = StringIO()
    doc = epp.epp_file.parse(document)
    output.write("signature = {0}\n".format(doc.signature.decode('ascii')))
    output.write("version = {0}\n".format(doc.version))
    output.write(str(doc.header) + "\n")
    output.write("\n".join(map(str, doc.data[:limit])))
    output.write("\n")
    return output.getvalue()

def main(argv=None):
    if (sys.version_info < (3,0)):
        reload(sys)
        sys.setdefaultencoding('utf-8')

    if (argv == None):
        argv = sys.argv
        
    parser = argparse.ArgumentParser(prog='gpx2epp')
    parser.add_argument('-i', '--input',  help="input file (default: stdin)")
    parser.add_argument('-o', '--output', help="output file (default: stdout)")
    parser.add_argument('-l', '--limit',  help="limit number of data points to print", type=int)
    args = parser.parse_args(args=argv[1:])

    if args.input:
        with open(args.input, 'rb') as f:
            text = eppread(f.read(), args.limit)
    else:
        with sys.stdin as f:
            text = eppread(f.read(), args.limit)

    if args.output:
        with open(args.output, 'wb') as outfile:
            outfile.write(text.encode('utf-8'))
    else:
        sys.stdout.write(text.encode('utf-8'))
    return 0
    
if __name__ == "__main__":
    sys.exit(main())
