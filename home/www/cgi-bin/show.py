#!/bin/python3
# -*- coding: utf-8 -*-

import time
import json
import os

from upload import gInnoUpgrDir, gInnoShowFifoFile
from inno_lib import *

def Show(showFileName):
    InnoGetCgi()
    callback = InnoParseCgi(gInnoCallBackKey)

    InnoPrintJsonHeader()

    jsonStr = None
    if not os.path.isfile(showFileName):
        obj = {'percent' : '0', 'text': 'update starting...'}
        jsonStr = json.dumps(obj, indent = gInnoJsonIndent)
    else:
        showFile = open(showFileName, 'r')
        jsonStr = showFile.read()
        showFile.close()

    # 跨域支持
    if None != callback:
        jsonStr = callback + '(' + jsonStr + ')'

    print(jsonStr)

if __name__ == '__main__':
    Show(gInnoUpgrDir + gInnoShowFifoFile)

