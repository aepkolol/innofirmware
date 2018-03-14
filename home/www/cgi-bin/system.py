#!/bin/python3
# -*- coding: utf-8 -*-

import json

from inno_config import *
from inno_lib import *

if __name__ == '__main__':
    InnoPrintJsonHeader()

    cmd = 'uptime'
    statusStr = InnoGetCmdRst(cmd)

    cmd = 'free'
    infoStr = InnoGetCmdRst(cmd)
    infoList = infoStr.split('\n')
    memList = infoList[1].split(' ')
    cacheList = infoList[2].split(' ')

    memUsed = int(memList[14])
    memFree = int(memList[19])
    cacheUsed = int(cacheList[7])
    cacheFree = int(cacheList[-1])

    #print(infoList)
    #print()
    #print(memList)
    #print(cacheList)
    obj = {
            'status':   statusStr,
            'memUsed':  memUsed,
            'memFree':  memFree,
            'memTotal': memUsed + memFree,

            'cacheUsed':cacheUsed,
            'cacheFree':cacheFree,
            'cacheTotal':cacheUsed + cacheFree
            }

    InnoPrintJson(obj)

