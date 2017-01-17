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

import sys
import eppformat as epp

def main():
    if (sys.version_info < (3,0)):
        reload(sys)
        sys.setdefaultencoding('utf-8')
    if (len(sys.argv) > 1):
        p = epp.epp_file.parse_stream(open(sys.argv[1], "rb"))
        print("signature =", p.signature.decode('ascii'))
        print("version =", p.version)
        print(p.header)
        if (len(sys.argv) > 2):
            limit=int(sys.argv[2])
        else:
            limit=None
        for v in p.data[:limit]:
            print(v)
    else:
        print("usage: eppread <file> [limit]")
        sys.exit(1);

if __name__ == "__main__":
    main()
