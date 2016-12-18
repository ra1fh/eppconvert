#!/usr/bin/env python

"""
parse daum ergo bike epp/eup files
"""

from construct import *
import time, datetime, sys

eppversion = Enum(Int32ul,
                  VERSION_1=1,
                  VERSION_2=2,
                  VERSION_3=3,
                  VERSION_4=4,
                  VERSION_5=5,
                  VERSION_6=6,
                  VERSION_7=7,
)

epptype = Enum(Int32ul,
               TIME_WATT = 0x01,
               TIME_PULSE = 0x02,
               TIME_SPEED = 0x04,
               TIME_RPM = 0x08,
               DIST_HEIGHT = 0x10,
               DIST_CLIMB = 0x20,
               TIME_FORCE = 0x40,
               STEP_PULSE_WATT = 0x80,
               TIME_SPEED_CLIMB = 0x100
)

eppblr = BitStruct(
             Padding(5),
    "run"  / Flag,
    "lyps" / Flag,
    "bike" / Flag,
             Padding(24),
    )

epp = Struct(
    "signature"  / Const(b"EW2_EUP "),
    "version"    / eppversion,
    "header"     / Switch(this.version, {
        "VERSION_5" : Struct(
            "field1"     / Int32ul,
            "field2"     / Int32ul,
            "title"      / Padded(0x40,  CString()),
            "description"/ Padded(0x100, CString()),
            "type"       / epptype,
            "length"     / Int32ul,
            "field4"     / Int32ul,
            "raster"     / Int32ul,
            "field6"     / Int32ul,
            "field7"     / Int16ul,
            "field8"     / Int16ul,
            "field11"    / Int32ul,
            # "blr"    = 7
        ),
        "VERSION_6" : Struct(
            "field1"     / Int32ul,
            "field2"     / Int32ul,
            "title"      / Padded(0x40,  CString()),
            "description"/ Padded(0x100, CString()),
            "type"       / epptype,
            "length"     / Int32ul,
            "field4"     / Int32ul,
            "field5"     / Int32ul,
            "raster"     / Int32ul,
            "blr"        / eppblr,
            "field6"     / Int32ul,
            "field7"     / Int32ul,
            "field8"     / Int32ul,
            "field11"    / Int32ul
        ),
        "VERSION_7" : Struct(
            "field1"     / Int32ul,
            "field2"     / Int32ul,
            "title"      / Padded(0x40,  CString()),
            "description"/ Padded(0x100, CString()),
            "type"       / epptype, # 0x148
            "field3"     / Int32ul, # 0x14C
            "field4"     / Int32ul, # 0x150
            "field5"     / Int32ul, # 0x154
            "length"     / Int32ul, # 0x158
            "raster"     / Int32ul, # 0x15C
            "blr"        / eppblr,  # 0x160
            "field6"     / Int32ul, # 0x164
            "field7"     / Int16ul, # 0x168
            "field8"     / Int16ul, # 0x16A
            "field9"     / Int32ul, # 0x16C
            "field10"    / Int32ul, # 0x170
            "field11"    / Int32ul, # 0x174
            "pos"        / Tell,
        ),
    }),
    "data" / Switch(this.version, {
        "VERSION_7" : Array(this.header.length,
            Struct(
                "val1"  / Int32ul,
                "val2"  / Float32l,
                "val3"  / Int32ul,  
            ),
        ),
        "VERSION_6" : Array(this.header.length,
            Struct(
                "val1"   / Int32ul,
                "val2"   / Float32l,
            ),
        ),
    }),
)

if __name__ == "__main__":
    p = epp.parse_stream(open(sys.argv[1], "rb"))
    print(p.signature)
    print(p.version)
    print(p.header)
    for v in p.data[0:4]:
        print(v)

    #p = packet.parse_stream(open("steigung15.epp", "rb"))
    #print(p)
