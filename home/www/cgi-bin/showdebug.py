#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from inno_config import *
from inno_lib import *

if __name__ == '__main__': 
    text = ''
    # 读取defPLL
    pllList = 'None'
    if os.path.exists(gInnoDefPllPath):
        fd = open(gInnoDefPllPath, 'r')
        pllList = fd.read().strip()
        fd.close()
    text += ('+1: ' + pllList + '\n')
    # 读取defVID
    vidList = 'None'
    if os.path.exists(gInnoNewDefVidPath):
        fd = open(gInnoNewDefVidPath, 'r')
        vidList = fd.read().strip()
        fd.close()
    text += ('+2: ' + vidList + '\n')
    # 读取vol log文件
    for i in range(0, gInnoChainNum):
        filepath = gInnoVolLogPath % i
        if os.path.exists(filepath):
            fd = open(filepath, 'r')
            data = fd.read()
            fd.close()
            text += data
    # 读取log文件
    for i in range(0, gInnoChainNum):
        filepath = gInnoAnalysLogPath % i
        if os.path.exists(filepath):
            fd = open(filepath, 'r')
            data = fd.read()
            fd.close()
            text += data

    obj = {'result' : 'true', 'data' : text}
    InnoPrintJsonHeader()
    InnoPrintJson(obj)

