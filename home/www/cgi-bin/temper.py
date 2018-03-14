#!/bin/python3
# -*- coding: utf-8 -*-

from inno_config import *
from inno_lib import *

def ApiGetTempInfo():
    # 查询温度信息
    tempInfo = InnoMinerApiGet(gInnoMinerApiGetDevs)

    return tempInfo

if __name__ == '__main__':
    tempInfo = ApiGetTempInfo()

    InnoPrintJsonHeader()
    InnoPrintJson(tempInfo)
