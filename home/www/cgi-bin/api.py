#!/bin/python3
# -*- coding: utf-8 -*-

from inno_config import *
from inno_lib import *

gMinerApiKeyDevs  = 'DEVS'
gMinerApiKeyPools = 'POOLS'

def ApiGetDevInfo():
    # 查询设备信息
    devInfo = InnoMinerApiGet(gInnoMinerApiGetDevs)
    # 查询矿池信息
    poolInfo = InnoMinerApiGet(gInnoMinerApiGetPools)

    # 将矿池信息添加到设备信息
    if poolInfo:
        pools = poolInfo[gMinerApiKeyPools]
        devInfo[gMinerApiKeyPools] = pools

    return devInfo

if __name__ == '__main__':
    devInfo = ApiGetDevInfo()

    InnoPrintJsonHeader()
    InnoPrintJson(devInfo)

