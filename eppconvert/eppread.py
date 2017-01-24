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

'''Read and print Daum Ergo Bike EPP/EUP files.

Usage:
    eppread [-i FILE] [-o FILE] [-l LIMIT]

Options:
    -h, --help               Show this.
        --version            Show version.
    -i, --input FILE         Input EPP/EUP file (default: stdin).
    -o, --output FILE        Output text file (default: stdout).
    -l, --limit LIMIT        Limit of data points to print.

'''

from __future__ import absolute_import, print_function

import docopt
import io
import os
import string
import sys

from eppconvert import eppformat
from eppconvert.release import __version__

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def eppread(document, limit=None):
    output = StringIO()
    doc = eppformat.epp_file.parse(document)
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
        argv = sys.argv[1:]

    try:
        args = docopt.docopt(__doc__, argv=argv, version='eppread ' + __version__)

        limit = None
        if args['--limit']:
            limit = int(args['--limit'])

        if args['--input']:
            with io.open(args['--input'], 'rb') as f:
                text = eppread(f.read(), limit)
        else:
            with sys.stdin as f:
                text = eppread(f.read(), limit)

        if args['--output']:
            with io.open(args['--output'], 'wb') as outfile:
                outfile.write(text.encode('utf-8'))
        else:
            sys.stdout.write(text)

        return 0

    except KeyboardInterrupt:
        print(" Interrupted.", file=sys.stderr)

    except IOError as error:
        print("error: IOError {0}".format(error, file=sys.stderr))

    return 1

if __name__ == "__main__":
    sys.exit(main())
