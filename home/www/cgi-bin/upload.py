#!/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import cgi
import json
import time
import struct
import binascii

from inno_config import *
from inno_lib import *
from inno_upgrade import *

gInnoShowFifoFile    = 'show_fifo'

# form key
gInnoUpgrFileKey      = 'upfile'
gInnoUpgrRetainCfgKey = 'keepsettings'

def WritePercentToShowFile(percent, text):
    obj = {'percent' : str(percent), 'text': str(text)}
    jsonStr = json.dumps(obj, indent = gInnoJsonIndent) + '\n'

    data = open(gInnoUpgrDir + gInnoShowFifoFile, 'w')
    data.write(jsonStr)
    data.close()
    # 记录日志
    PrintUpgrLog(percent, text)

def GetFile():
    form = cgi.FieldStorage()

    fileitem = form[gInnoUpgrFileKey]
    fileName = None

    isRetainCfg = form[gInnoUpgrRetainCfgKey].value     # 这里form[key]获取到的仍是一个FieldStorage对象，需要用.value获取值
    if isRetainCfg != '1':
        isRetainCfg = '0'
    InnoPrintSysLog('upload', gInnoUpgrRetainCfgKey + '=' + isRetainCfg)

    # 保存文件
    if fileitem.filename:
        fileName = gInnoUpgrDir + gInnoUpgrFile
        fileData = fileitem.file.read()
        # 校验尺寸
        fileLen = sys.getsizeof(fileData)
        InnoPrintSysLog('upload', 'upgrade file size: ' + str(fileLen))
        if fileLen > gInnoUpgrFileSize:
            InnoPrintJsonHeader()
            obj = {gInnoResultKey : gInnoResultValFalse}
            InnoPrintJson(obj)
            sys.exit(0)
        # 写入文件
        fd = open(fileName, 'wb')
        fd.write(fileData)
        fd.close()
        # 修改权限
        #cmd = 'chmod -x ' + fileName
        #InnoGetCmdRst(cmd)

    return isRetainCfg

def Upgrade(isRetainCfg):
    # 解析文件
    WritePercentToShowFile(15, 'parsing upgrade file...')
    rst = ParseUpgrFile(isRetainCfg)
    if not rst:
        WritePercentToShowFile(100, UpgrGetLastError())
        exit()
    WritePercentToShowFile(20, 'parsing upgrade file... done.')

    # 设置权限
    scriptPath = gInnoUpgrDir + gInnoUpgrScriptFile
    cmd = 'chmod 777 ' + scriptPath
    InnoGetCmdRst(cmd)

    # 磁盘同步
    cmd = 'sync'
    InnoGetCmdRst(cmd)

    # 运行upgrade script
    InnoPrintSysLog('upload', 'start running %s' % scriptPath)
    cmd = scriptPath
    InnoGetCmdRst(cmd)

if __name__ == '__main__':
    try:
        # log
        InnoPrintSysLog('upload', 'start upgrading')
        WritePercentToShowFile(1, 'start upgrading.')

        # 终止MServer和innominer_Tx
        #cmd = 'ps | grep -rn %s | grep -v grep | awk \'{print $2}\''
        #rst = InnoGetCmdRst(cmd % 'MServer.py')
        #InnoGetCmdRst('kill %s' % rst)
        #rst = InnoGetCmdRst(cmd % 'innominer_T')
        #InnoGetCmdRst('kill %s' % rst)
        # 所有链断电
        #InnoChainPwCtrl(-1, 0)

        # step1: 获取文件
        WritePercentToShowFile(2, 'transferring upgrade file...')
        isRetainCfg = GetFile()
        WritePercentToShowFile(10, 'transferring upgrade file... done.')

        # step2: 升级
        Upgrade(isRetainCfg)
    except:
        PrintUpgrException('Exception Logged')
