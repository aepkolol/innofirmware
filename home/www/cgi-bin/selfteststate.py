#!/bin/python3
# -*- coding: utf-8 -*-

import os

from inno_config import *
from inno_lib import *

if __name__ == '__main__':
    result = gInnoResultValFalse
    if os.path.exists(gInnoAutoSchLockPath):
        result = gInnoResultValTrue

    obj = { gInnoResultKey : result }
    InnoPrintJsonHeader()
    InnoPrintJson(obj)

