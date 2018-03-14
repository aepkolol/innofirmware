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
    cmd = 'cat ' + '/build_log'
    infoStr = InnoGetCmdRst(cmd)
    infoList = infoStr.split('\n')

    hwver = InnoGetHWVer()
    ethaddr = InnoGetEmac()
    upgrlock = InnoGetLockDev()

    obj = {
            'hwver'     : hwver,
            'ethaddr'   : ethaddr,
            'build_date': GetVersionNum(infoList, 2),
            'platform_v': GetVersionNum(infoList, 4) + '.' + str(upgrlock), # 末尾显示设备是否矿场托管版本
            'plat_g19_v': GetVersionNum(infoList, 6),
            'uboot_v'   : GetVersionNum(infoList, 8),
            'kernel_v'  : GetVersionNum(infoList, 10),
            'busybox_v' : GetVersionNum(infoList, 12),
            'memtester_v':GetVersionNum(infoList, 14),
            'curl_v'    : GetVersionNum(infoList, 16),
            'openssl_v' : GetVersionNum(infoList, 18),
            'sgminer_v' : GetVersionNum(infoList, 20),
            'cpuminer_v': GetVersionNum(infoList, 22),
            'cgminer_v' : GetVersionNum(infoList, 24),
            'cgminer4a8_v':GetVersionNum(infoList, 26),
            'cpython_v' : GetVersionNum(infoList, 28),
            'rootfs_v'  : GetVersionNum(infoList, 30)
        }

    InnoPrintJsonHeader()
    InnoPrintJson(obj)

