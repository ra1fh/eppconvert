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
Daum Ergo Bike EPP/EUP format definition
"""

from __future__ import absolute_import, print_function

from construct import *

class FloatAdapter(Adapter):
    def _encode(self, obj, context):
        return obj
    def _decode(self, obj, context):
        return round(obj, 2)

epp_version = Enum(Int32ul,
    VERSION_1 = 1,
    VERSION_2 = 2,
    VERSION_3 = 3,
    VERSION_4 = 4,
    VERSION_5 = 5,
    VERSION_6 = 6,
    VERSION_7 = 7,
)

epp_type16 = Enum(Int16ul,
    TIME_WATT        = 0x01,
    TIME_PULSE       = 0x02,
    TIME_SPEED       = 0x04,
    TIME_RPM         = 0x08,
    DIST_HEIGHT      = 0x10,
    DIST_CLIMB       = 0x20,
    TIME_FORCE       = 0x40,
    STEP_PULSE       = 0x80,
)

epp_type32 = Enum(Int32ul,
    TIME_WATT        = 0x01,
    TIME_PULSE       = 0x02,
    TIME_SPEED       = 0x04,
    TIME_RPM         = 0x08,
    DIST_HEIGHT      = 0x10,
    DIST_CLIMB       = 0x20,
    TIME_FORCE       = 0x40,
    STEP_PULSE       = 0x80,
    TIME_SPEED_CLIMB = 0x100
)

epp_third = Enum(Int32ul,
    NONE  = 0x00,
    WATT  = 0x01,
    PULSE = 0x02,
    CLIMB = 0x20,
)

epp_blr = BitStruct(
             Padding(5),
    "run"  / Flag,
    "lyps" / Flag,
    "bike" / Flag,
             Padding(24),
)

epp_file = Struct(
    "signature"  / Const(b"EW2_EUP "),
    "version"    / epp_version, Embedded(Switch(this.version, {
        "VERSION_1" : Struct(
            "header" / Struct(
                               Padding(8),
                "title"      / Padded(0x32,  CString(encoding="cp1252")),
                "description"/ Padded(0x100, CString(encoding="cp1252")),
                               Padding(2),
                "length"     / Int32ul,
                "type"       / epp_type16,
                "stepsize"   / Int16ul,
                               Padding(4),
            ),
            "data" / Array(this.header.length, Struct(
                "val1"       / Int32ul,
            )),
        ),
        "VERSION_2" : Struct(
            "header" / Struct(
                               Padding(8),
                "title"      / Padded(0x32,  CString(encoding="cp1252")),
                "description"/ Padded(0x100, CString(encoding="cp1252")),
                "length"     / Int32ul,
                "type"       / epp_type16,
                "stepsize"   / Int16ul,
                "maxwatt"    / Int16ul,
                "maxpulse"   / Int16ul,
                "startheight"/ Int32ul,
            ),
            "data" / Array(this.header.length, Struct(
                "val1"       / Int32ul,
            )),
        ),
        "VERSION_3" : Struct(
            "header" / Struct(
                               Padding(8),
                "title"      / Padded(0x32,  CString(encoding="cp1252")),
                "description"/ Padded(0x100, CString(encoding="cp1252")),
                "graphmin"   / Int32sl,
                "graphmax"   / Int32sl,
                "length"     / Int32ul,
                "type"       / epp_type16,
                "stepsize"   / Int16ul,
                "maxwatt"    / Int16ul,
                "maxpulse"   / Int16ul,
                "startheight"/ Int32ul,
                               Padding(4),
            ),
            "data" / Array(this.header.length, Struct(
                "val1"       / Int32ul,
            )),
        ),
        "VERSION_4" : Struct(
            "header" / Struct(
                               Padding(8),
                "title"      / Padded(0x40,  CString(encoding="cp1252")),
                "description"/ Padded(0x100, CString(encoding="cp1252")),
                "type"       / epp_type32,
                "length"     / Int32ul,
                "graphmin"   / Int32sl,
                "graphmax"   / Int32sl,
                "stepsize"   / Int32ul,
                "startheight"/ Int32ul,
                "maxwatt"    / Int16ul,
                "maxpulse"   / Int16ul,
                               Padding(4),
            ),
            "data" / Array(this.header.length, Struct(
                "val1"       / Int32ul,
                               Int32ul,
                "val2"       / FloatAdapter(Float64l),
            )),
        ),
        "VERSION_5" : Struct(
            "header" / Struct(
                               Padding(8),
                "title"      / Padded(0x40,  CString(encoding="cp1252")),
                "description"/ Padded(0x100, CString(encoding="cp1252")),
                "type"       / epp_type32,
                "length"     / Int32ul,
                "graphmin"   / Int32sl,
                "graphmax"   / Int32sl,
                "stepsize"   / Int32ul,
                "startheight"/ Int32ul,
                "maxwatt"    / Int16ul,
                "maxpulse"   / Int16ul,
                               Padding(4),
            ),
            "data" / Array(this.header.length, Struct(
                "val1"       / Int32ul,
                "val2"       / FloatAdapter(Float32l),
            )),
        ),
        "VERSION_6" : Struct(
            "header" / Struct(
                               Padding(8),
                "title"      / Padded(0x40,  CString(encoding="cp1252")),
                "description"/ Padded(0x100, CString(encoding="cp1252")),
                "type"       / epp_type32,
                "length"     / Int32ul,
                "graphmin"   / Int32sl,
                "graphmax"   / Int32sl,
                "stepsize"   / Int32ul,
                "blr"        / epp_blr,
                "startheight"/ Int32ul,
                "maxwatt"    / Int16ul,
                "maxpulse"   / Int16ul,
                               Padding(8),
            ),
            "data" / Array(this.header.length, Struct(
                "val1"       / Int32ul,
                "val2"       / FloatAdapter(Float32l),
            )),
        ),
        "VERSION_7" : Struct(
            "header" / Struct(
                               Padding(8),
                "title"      / Padded(0x40,  CString(encoding="cp1252")),
                "description"/ Padded(0x100, CString(encoding="cp1252")),
                "type"       / epp_type32,
                "third"      / epp_third,
                "graphmin"   / Int32sl,
                "graphmax"   / Int32sl,
                "length"     / Int32ul,
                "stepsize"   / Int32ul,
                "blr"        / epp_blr,
                "startheight"/ Int32ul,
                "maxwatt"    / Int16ul,
                "maxpulse"   / Int16ul,
                "maxspeed"   / FloatAdapter(Float32l),
                               Padding(8),
            ),
            "data" / Array(this.header.length, Struct(
                "val1"       / Int32ul,
                "val2"       / FloatAdapter(Float32l),
                "val3"       / FloatAdapter(Float32l),
            )),
        ),
    })),
)

# DPPEdit creates the following combination of type/third.
# Some more combinations do work at least in DPPEdit.
#
# - "Cardio Puls": STEP_PULSE + WATT
# - "Distance(m)": DIST_HEIGHT + NONE
# - "Distance(%)": DIST_CLIMB + NONE, uses startheight field
# - "NM":          TIME_FORCE + NONE
# - "Pulse":       TIME_PULSE + NONE
# - "RPM":         TIME_RPM + NONE
# - "Speed":       TIME_SPEED + NONE
# - "Speed/Climb": TIME_SPEED_CLIMB + CLIMB
# - "Watt":        TIME_WATT + NONE
