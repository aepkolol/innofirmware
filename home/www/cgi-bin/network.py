#!/bin/python3
# -*- coding: utf-8 -*-

from inno_config import *
from inno_lib import *

if __name__ == '__main__':
    dhcpStr    = InnoGetDhcp()
    addressStr = InnoGetIpaddr()
    netmaskStr = InnoGetNetmask()
    gatewayStr = InnoGetGateway()
    dns        = InnoGetDns()

    obj = {
            gInnoDhcpKey:   dhcpStr,
            gInnoIpAddrKey: addressStr,
            gInnoNetmaskKey:netmaskStr,
            gInnoGatawayKey:gatewayStr,
            gInnoDnsKey:    dns 
          }
    
    InnoPrintJsonHeader()
    InnoPrintJson(obj)

