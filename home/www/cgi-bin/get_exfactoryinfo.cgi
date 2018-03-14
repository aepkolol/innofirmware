#!/bin/python3
# -*- coding: utf-8 -*-

import json

from inno_config import *
from inno_lib import *

def GetVersionNum(infoList, index):
    line = infoList[index]
    lineList = line.split(',')
    msg = lineList[0]

    return msg

if __name__ == '__main__':
    infoStr = InnoGetCmdRst('cat /build_log')
    infoList = infoStr.split('\n')

    dna = InnoGetCmdRst("xxd -p %s | sed 's/[ ]*$//g' 2> /dev/null" % gInnoDnaFilePath)
    minertype = InnoGetType()
    devtype = InnoGetCmdRst('cat /tmp/dev_type 2> /dev/null')
    hwver = InnoGetHWVer()
    ethaddr = InnoGetEmac()
    dhcp = InnoGetDhcp()
    upgrlock = InnoGetLockDev()

    obj = {
            "hwver"      : hwver,
            "fwver"      : GetVersionNum(infoList, 2),
            "dna"        : dna,
            "miner_type" : minertype,
            "device_type": devtype,
            "emac"       : ethaddr,
            "dhcp"       : dhcp,
            "managed"    : upgrlock
        }

    InnoPrintJsonHeader()
    InnoPrintJson(obj)

