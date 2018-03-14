#!/bin/python3
# -*- coding: utf-8 -*-

import sys

from inno_config import *
from inno_upgrade import *

# 升级数据包组成: 
#         名称                  输入路径             是否加密
gInnoUpgrPkgTable = (
        ['upgrade.cmd',        'upgrade.cmd',        True],
        ['BOOT.bin.G9',        'g9/BOOT.bin',        False],
        ['devicetree.dtb.G9',  'g9/devicetree.dtb',  False],
        ['uImage.G9',          'g9/uImage',          False],
        ['rootfs.jffs2',       'rootfs.jffs2',       False],
        ['BOOT.bin.G19',       'g19/BOOT.bin',       False],
        ['devicetree.dtb.G19', 'g19/devicetree.dtb', False],
        ['uImage.G19',         'g19/uImage',         False])

if __name__ == '__main__':
    # 根据lock参数决定是否生成升级锁定版本
    isLock = 0
    if len(sys.argv) > 1 and sys.argv[1] == 'lock':
        isLock = 1
        gInnoUpgrPkgTable[4][1] += '.lock'  # 打包时使用rootfs.jffs2.lock
    #print(gInnoUpgrPkgTable)

    MakeUpgrFile(gInnoUpgrScriptFile, gInnoUpgrPkgTable, isLock)

    print('build done.')

