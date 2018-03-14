#!/bin/python3
# -*- coding: utf-8 -*-

import json

from inno_config import *
from inno_lib import *

if __name__ == '__main__':
    InnoGetCgi()
    callback = InnoParseCgi(gInnoCallBackKey)

    obj = {gInnoResultKey : gInnoResultValTrue}
    jsonStr = json.dumps(obj, indent = gInnoJsonIndent)
    jsonData = callback + '(' + jsonStr + ')'

    InnoPrintJsonHeader()
    print(jsonData)

