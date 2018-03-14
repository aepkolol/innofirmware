#!/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('../inno_py/')

from inno_config import *
from inno_upgrade import *

# 升级数据包组成: 
#         名称                  输入路径             是否加密
gInnoUpgrPkgTable = (
        ['patch.sh',            'patch.sh',          True],
        ['patch.data',          'patch.data',        True])

gInnoPatchFile = 'patch.py'

if __name__ == '__main__':
    # 根据lock参数决定是否生成升级锁定版本
    isLock = 1      # 默认生成lock版本, 避免矿场无法升级
    filapath = None
    if len(sys.argv) > 2 and sys.argv[1] == 'unlock':
        isLock = 0
        filepath = gInnoUpgrFile
    else:
        isLock = 1
        filepath = gInnoUpgrLFile

    MakeUpgrFile(gInnoPatchFile, gInnoUpgrPkgTable, isLock)
    
    InnoGetCmdRst('chmod 777 ' + filepath)

    print('patch build done.')
