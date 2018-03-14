#!/bin/python3
# -*- coding: utf-8 -*-

from inno_config import *
from inno_lib import *

def InnoSetNetwork(ipCfg):
    dhcp    = ipCfg[gInnoDhcpKey]
    ipaddr  = ipCfg[gInnoIpAddrKey]
    netmask = ipCfg[gInnoNetmaskKey]
    gateway = ipCfg[gInnoGatawayKey]
    dns     = ipCfg[gInnoDnsKey]

    if dhcp == 'dhcp':                              # dhcp
        # write /etc/network/interfaces
        InnoSetDhcp()
        # 查询ip & netmask & gateway以便提交给web
        #ipCfg[gInnoIpAddrKey] = InnoGetCmdRst(gInnoGetIpCmd)
        #ipCfg[gInnoNetmaskKey] = InnoGetCmdRst(gInnoGetNetmask)
        #ipCfg[gInnoGatawayKey] = InnoGetCmdRst(gInnoGetGateway)
        #ipCfg[gInnoDnsKey] = InnoGetDns()
        return True
    elif ipaddr and netmask and gateway and dns:    # static
        # 正则校验
        isArgsValid =  InnoRexMatch(gInnoRexIpAddr,  ipaddr)
        isArgsValid &= InnoRexMatch(gInnoRexIpAddr,  netmask)
        isArgsValid &= InnoRexMatch(gInnoRexIpAddr,  gateway)
        for d in dns: 
            isArgsValid &= InnoRexMatch(gInnoRexIpAddr,  d)
        if not isArgsValid:
            InnoPrintSysLog('submit_net', 'ERROR: invalid ipaddr or netmask or gateway or dns')
            return False
        InnoPrintSysLog("cgi.submit_net", "%s" % str(dns))
        # 修改网络配置
        InnoSetStaticIp(ipaddr, netmask, gateway, dns)
        return True
    else:
        InnoPrintSysLog('submit_net', 'ERROR: not enough information to change ip')
        return False

def InnoGetCgiNetwork():
    typeStr = InnoGetType()

    InnoGetCgi()
    dhcp    = InnoParseCgi(gInnoDhcpKey)
    ipaddr  = InnoParseCgi(gInnoIpAddrKey)
    netmask = InnoParseCgi(gInnoNetmaskKey)
    gateway = InnoParseCgi(gInnoGatawayKey)
    dns     = InnoParseCgi('dns[]')
    #dns     = InnoParseCgi(gInnoDnsKey)

    networkCfg = {  gInnoTypeKey:     typeStr,
                    gInnoDhcpKey:     dhcp,
                    gInnoIpAddrKey:   ipaddr,
                    gInnoNetmaskKey:  netmask,
                    gInnoGatawayKey:  gateway,
                    gInnoDnsKey:      dns}

    return networkCfg

if __name__ == '__main__':

    networkCfg = InnoGetCgiNetwork()

    # 修改配置
    result = InnoSetNetwork(networkCfg)

    if result:
        # log
        #cfgStr = json.dumps(networkCfg)
        InnoPrintSysLog('submit_net', 'network cfg changed to ' + str(networkCfg))
        # 向WEB反馈结果
        InnoPrintJsonHeader()
        InnoPrintJson(networkCfg)
        # 重启网络
        InnoNetReset()

