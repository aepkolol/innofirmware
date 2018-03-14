#!/bin/python3
# -*- coding: utf-8 -*-

import os
import cgi
import time

from inno_config import *
from inno_lib import *

if __name__ == '__main__':
    result = None
    
    InnoPrintSysLog('resetlogo', 'change to default logo')

    # 获取设备type
    typeStr = InnoGetType()
    deflogopath = None
    if gInnoBtcName == typeStr:     # T1使用DragonMint logo
        deflogopath = gInnoDmLogoPath
    elif gInnoXmrName == typeStr:   # T4使用Blank logo
        deflogopath = gInnoBlankLogoPath
    else:                           # 其他使用Inno logo
        deflogopath = gInnoInnoLogoPath
    
    if os.path.exists(deflogopath):
        InnoGetCmdRst('rm ' + gInnoLogoPath)
        InnoGetCmdRst('cp -avf %s %s' % (deflogopath, gInnoLogoPath))
        # 清除配置分区保存的用户logo
        cmd = 'rm -rf %s' % gInnoUserLogoPath
        InnoGetCmdRst(cmd)
        result = gInnoResultValTrue
    else:
        result = gInnoResultValFalse

    InnoPrintJsonHeader()
    obj = {gInnoResultKey : result}
    InnoPrintJson(obj)
