#!/bin/python3
# -*- coding: utf-8 -*-

from inno_config import *
from inno_lib import *

if __name__ == '__main__':
    typeStr = InnoGetType()
    typeNum = 15 + int(typeStr[1])

    obj = {gInnoTypeKey: typeNum}

    InnoPrintJsonHeader()
    InnoPrintJson(obj)

