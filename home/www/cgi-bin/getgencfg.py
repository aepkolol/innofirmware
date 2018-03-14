#!/bin/python3
# -*- coding: utf-8 -*-

from inno_config import *
from inno_lib import *
from pool import *
from submit_net import *

if __name__ == '__main__':
    fdCfg = open(gInnoMinerConfPath, 'r')
    minerCfgStr = fdCfg.read()
    fdCfg.close()
    minerCfg = json.loads(minerCfgStr)
    
    typeStr = InnoGetType()

    addressStr = InnoGetCmdRst(gInnoGetIpCmd)
    netmaskStr = InnoGetCmdRst(gInnoGetNetmask)
    gatewayStr = InnoGetCmdRst(gInnoGetGateway)
    dns = InnoGetDns()

    minerCfg[gInnoTypeKey] = typeStr
    minerCfg[gInnoIpAddrKey] = addressStr
    minerCfg[gInnoNetmaskKey] = netmaskStr
    minerCfg[gInnoGatawayKey] = gatewayStr
    minerCfg[gInnoDnsKey] = dns

    # 返回jsonp
    InnoGetCgi()
    callback = InnoParseCgi(gInnoCallBackKey)
    jsonStr = json.dumps(minerCfg, indent = gInnoJsonIndent)
    jsonpStr = callback + '(' + jsonStr + ')'

    InnoPrintJsonHeader()
    print(jsonpStr)
