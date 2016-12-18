#!/usr/bin/env python

"""
parse daum ergo bike epp/eup files
"""

from construct import *
import time, datetime, sys

epp_version = Enum(Int32ul,
    VERSION_1 = 1,
    VERSION_2 = 2,
    VERSION_3 = 3,
    VERSION_4 = 4,
    VERSION_5 = 5,
    VERSION_6 = 6,
    VERSION_7 = 7,
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

# Intepretation of the third data column, probably not used for
# TIME_SPEED_CLIMB. Other values will trigger a DPPEdit bug, that
# case is not well handled.
epp_third = Enum(Int32ul,
    NONE  = 0x00,
    WATT  = 0x01,
    PULSE = 0x02,
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
    "version"    / epp_version,
    "header"     / Switch(this.version, {
        "VERSION_1" : Struct(
                           Padding(8),
            "title"      / Padded(0x32,  CString()),
            "description"/ Padded(0x100, CString()),
                           Padding(2),
            "length"     / Int32ul,
            "type"       / epp_type16,
            "raster"     / Int16ul,
                           Padding(4),   # according to jErgoPlanet data starts
                                         # at 0x15c, so add some padding 
        ),
        "VERSION_2" : Struct(
                           Padding(8),
            "title"      / Padded(0x32,  CString()),
            "description"/ Padded(0x100, CString()),
            "length"     / Int32ul,
            "type"       / epp_type16,
            "raster"     / Int16ul,
            "maxwatt"    / Int16ul,
            "maxpulse"   / Int16ul,
            "unknown1"   / Int32ul,
        ),
        "VERSION_3" : Struct(
                           Padding(8),
            "title"      / Padded(0x32,  CString()),
            "description"/ Padded(0x100, CString()),
            "graphmin"   / Int32sl,
            "graphmax"   / Int32sl,
            "length"     / Int32ul,
            "type"       / epp_type16,
            "raster"     / Int16ul,
            "maxwatt"    / Int16ul,
            "maxpulse"   / Int16ul,
            "unknown1"   / Int32ul,
                           Padding(4),
            # "blr"    = 7
        ),
        "VERSION_4" : Struct(
                           Padding(8),
            "title"      / Padded(0x40,  CString()),
            "description"/ Padded(0x100, CString()),
            "type"       / epp_type32,
            "length"     / Int32ul,
            "graphmin"   / Int32sl,
            "graphmax"   / Int32sl,
            "raster"     / Int32ul,
            "unknown1"   / Int32ul,
            "maxwatt"    / Int16ul,
            "maxpulse"   / Int16ul,
                           Padding(4),
            # "blr"    = 7
        ),
        "VERSION_5" : Struct(
                           Padding(8),
            "title"      / Padded(0x40,  CString()),
            "description"/ Padded(0x100, CString()),
            "type"       / epp_type32,
            "length"     / Int32ul,
            "graphmin"   / Int32sl,
            "graphmax"   / Int32sl,
            "raster"     / Int32ul,
            "unknown1"   / Int32ul,
            "maxwatt"    / Int16ul,
            "maxpulse"   / Int16ul,
                           Padding(4),
            # "blr"    = 7
        ),
        "VERSION_6" : Struct(
                           Padding(8),
            "title"      / Padded(0x40,  CString()),
            "description"/ Padded(0x100, CString()),
            "type"       / epp_type32,
            "length"     / Int32ul,
            "graphmin"   / Int32sl,
            "graphmax"   / Int32sl,
            "raster"     / Int32ul,
            "blr"        / epp_blr,
            "unknown1"   / Int32ul,
            "maxwatt"    / Int16ul,
            "maxpulse"   / Int16ul,
                           Padding(8),
        ),
        "VERSION_7" : Struct(
                           Padding(8),
            "title"      / Padded(0x40,  CString()),
            "description"/ Padded(0x100, CString()),
            "type"       / epp_type32, # 0x148
            "third"      / epp_third,  # 0x14C
            "graphmin"   / Int32sl,   # 0x150
            "graphmax"   / Int32sl,   # 0x154
            "length"     / Int32ul,   # 0x158
            "raster"     / Int32ul,   # 0x15C
            "blr"        / epp_blr,    # 0x160
            "unkown1"    / Int32ul,   # 0x164
            "maxwatt"    / Int16ul,   # 0x168
            "maxpulse"   / Int16ul,   # 0x16A
            "maxspeed"   / Float32l,  # 0x16C
                           Padding(8),
        ),
    }),
    "data" / Switch(this.version, {
        "VERSION_1" : Array(this.header.length,
            Struct(
                "val1"   / Int32ul,
            ),
        ),
        "VERSION_2" : Array(this.header.length,
            Struct(
                "val1"   / Int32ul,
            ),
        ),
        "VERSION_3" : Array(this.header.length,
            Struct(
                "val1"   / Int32ul,
            ),
        ),
        "VERSION_4" : Array(this.header.length,
            Struct(
                "val1"   / Int32ul,
                           Int32ul,
                "val2"   / Float64l,
            ),
        ),
        "VERSION_5" : Array(this.header.length,
            Struct(
                "val1"   / Int32ul,
                "val2"   / Float32l,
            ),
        ),
        "VERSION_6" : Array(this.header.length,
            Struct(
                "val1"   / Int32ul,
                "val2"   / Float32l,
            ),
        ),
        "VERSION_7" : Array(this.header.length,
            Struct(
                "val1"  / Int32ul,
                "val2"  / Float32l,
                "val3"  / Float32l,  
            ),
        ),
    }),
)

if __name__ == "__main__":
    p = epp_file.parse_stream(open(sys.argv[1], "rb"))
    print(p.signature)
    print(p.version)
    print(p.header)
    for v in p.data[0:5]:
        print(v)
