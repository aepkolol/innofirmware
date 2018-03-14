#!/bin/python3
# -*- coding: utf-8 -*-

import json

from inno_config import *
from inno_lib import *

if __name__ == '__main__':
    InnoPrintJsonHeader()

    obj = {gInnoResultKey : gInnoResultValTrue}
    InnoPrintJson(obj)

