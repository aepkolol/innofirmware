#!/bin/python3
# -*- coding: utf-8 -*-

from inno_config import *
from inno_lib import *
from pool import *
from submit_net import *

def InnoParseMinerCfg():
    pool1    = InnoParseCgi(gInnoPool1Key)
    user1    = InnoParseCgi(gInnoUser1Key)
    password1= InnoParseCgi(gInnoPwd1Key)

    pool2    = InnoParseCgi(gInnoPool2Key)
    user2    = InnoParseCgi(gInnoUser2Key)
    password2= InnoParseCgi(gInnoPwd2Key)

    pool3    = InnoParseCgi(gInnoPool3Key)
    user3    = InnoParseCgi(gInnoUser3Key)
    password3= InnoParseCgi(gInnoPwd3Key)

    poolNums = '1'

    if None != pool2:
        poolNums = '2'

    if None != pool3:
        poolNums = '3'

    #InnoDebugCgiPrint('p2.log', pool2)
    #InnoDebugCgiPrint('p3.log', pool3)
    freq = InnoParseCgi(gInnoFreqKey);
    vol  = InnoParseCgi(gInnoVolKey);

    vidmode  = gInnoVidMode
    fanmode  = gInnoFanMode
    fanspd   = gInnoFanSpeed

    minerCfg = {gInnoPool1Key:   pool1,   gInnoUser1Key:   user1,   gInnoPwd1Key:    password1,
                gInnoPool2Key:   pool2,   gInnoUser2Key:   user2,   gInnoPwd2Key:    password2,
                gInnoPool3Key:   pool3,   gInnoUser3Key:   user3,   gInnoPwd3Key:    password3,
                gInnoFreqKey:    freq,    gInnoVolKey:     vol,     gInnoPoolNumKey: poolNums,
                gInnoVidModeKey: vidmode, gInnoFanModeKey: fanmode, gInnoFanSpdKey:  fanspd}

    return minerCfg
    
def InnoParseNetCfg():
    typeStr = InnoGetType()
    dhcp    = 'static'
    ipaddr  = InnoParseCgi(gInnoIpAddrKey)
    netmask = InnoParseCgi(gInnoNetmaskKey)
    gateway = InnoParseCgi(gInnoGatawayKey)
    dns     = InnoParseCgi('dns[]')

    networkCfg = {  gInnoDhcpKey:     dhcp,
                    gInnoTypeKey:     typeStr,
                    gInnoIpAddrKey:   ipaddr,
                    gInnoNetmaskKey:  netmask,
                    gInnoGatawayKey:  gateway,
                    gInnoDnsKey:      dns}

    return networkCfg

if __name__ == '__main__':
    InnoGetCgi()
    
    # 修改网络配置
    networkCfg = InnoParseNetCfg()
    InnoSetNetwork(networkCfg)
    #InnoDebugCgiPrint('/home/networkCfg.log', networkCfg)

    # 修改miner conf
    minerCfg = InnoParseMinerCfg()
    InnoWriteMinerCfg(minerCfg)
    #InnoDebugCgiPrint('/home/minerCfg.log', minerCfg)

    # 合并
    minerCfg.update(networkCfg)
    #InnoDebugCgiPrint('/home/generalCfg.log', minerCfg)
    
    # 返回jsonp
#    callback = InnoParseCgi(gInnoCallBackKey)
#    jsonStr = json.dumps(minerCfg, indent = gInnoJsonIndent)
#    jsonpStr = callback + '(' + jsonStr + ')'
#    InnoDebugCgiPrint('/home/jsonp.log', jsonpStr)

#    InnoPrintJsonHeader()
#    print(jsonpStr)
    
    InnoReboot()

