#!/bin/python3
# -*- coding: utf-8 -*-

import json

from inno_config import *
from inno_lib import *

gInnoDevTypeKey   = 'dev_type'

def InnoSetEnv(key, value):
    InnoGetCmdRst('fw_setenv %s %s' % (key, value))

def InnoGetEnv(key):
    rst = InnoGetCmdRst('fw_printenv %s' % key)
    vals = rst.split('=')
    if len(vals) > 1:
        return vals[1].strip()
    else:
        return None

if __name__ == '__main__':
    InnoGetCgi()
    dev_type = InnoParseCgi(gInnoDevTypeKey)

    InnoSetEnv(gInnoDevTypeKey, dev_type)
    result = None
    if InnoGetEnv(gInnoDevTypeKey) == dev_type:
        result = gInnoResultValTrue
    else:
        result = gInnoResultValFalse

    InnoPrintJsonHeader()
    obj = {gInnoResultKey : result}
    InnoPrintJson(obj)

