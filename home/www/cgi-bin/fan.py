#!/bin/python3
# -*- coding: utf-8 -*-

#import sys

from inno_config import *
from inno_lib import *

def ApiSetFanMode(fanmode):
    # 设置风扇速度
    InnoMinerApiSet(gInnoMinerApiSetFanMod, fanmode)
    InnoPrintSysLog('fan', 'fanmode set to %s' % fanmode)
    #print(result)
    return True

def ApiSetFanSpd(fanspeed):
    # 设置风扇速度
    InnoMinerApiSet(gInnoMinerApiSetFanSpd, fanspeed)
    InnoPrintSysLog('fan', 'fanspeed set to %s' % fanspeed)
    #print(result)
    return True

if __name__ == '__main__':
    rstStr = gInnoResultValFalse
    try:
        InnoGetCgi()
        fanmode  = InnoParseCgi(gInnoFanModeKey)
        fanspeed = InnoParseCgi(gInnoFanSpdKey)

        #fanmode = sys.argv[1]
        #fanspeed = sys.argv[2]

        result = True
        if fanmode:
            result = ApiSetFanMode(fanmode)

        if result and (fanmode == None or fanmode == '0') and fanspeed:
            result = ApiSetFanSpd(fanspeed)

        if result:
            # 修改miner.conf
            minerCfg = InnoReadMinerCfg()
            if fanmode:
                minerCfg[gInnoFanModeKey] = fanmode
            if fanspeed:
                minerCfg[gInnoFanSpdKey] = fanspeed
            InnoWriteMinerCfg(minerCfg)
            rstStr = gInnoResultValTrue
        else:
            rstStr = gInnoResultValFalse
    except:
        InnoPrintSysException('fan', 'Exception logged')

    InnoPrintJsonHeader()
    obj = {gInnoResultKey : rstStr}
    InnoPrintJson(obj)

