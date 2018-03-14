#!/bin/python3
# -*- coding: utf-8 -*-

import json

from inno_config import *
from inno_lib import *

if __name__ == '__main__':
    InnoGetCgi()
    pwd = InnoParseCgi(gInnoPassWordKey)

    pwdInFile = InnoReadPassWord()

    # 判断密码是否正确
    if pwdInFile == pwd:
        result = gInnoResultValTrue
    else:
        result = gInnoResultValFalse

    InnoPrintJsonHeader()
    obj = {gInnoResultKey : result}
    InnoPrintJson(obj)
