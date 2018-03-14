#!/bin/python3
# -*- coding: utf-8 -*-

from inno_config import *
from inno_lib import *

import time

if __name__ == '__main__':
    typeStr = InnoGetType()
    if InnoDevice():
        # 生成run.sh
        InnoWriteRunSh(typeStr)
        # 运行miner主程序
        InnoRunSh()
    else:
        while True:
            print('the image is not from Innosilicon.')
            time.sleep(5)

