#!/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import cgi
import json
import time
import struct
import binascii
import logging
import logging.handlers

# 升级数据包组成: 
#         名称                  输入路径             是否加密
gInnoUpgrPkgTable = (
        ['patch.sh',            'patch.sh',          True],
        ['patch.data',          'patch.data',        True])

gInnoJsonIndent     = 2

gInnoChainNum       = 8
gInnoGPIOPwOnBase   = 872       # 872,873,874,875,876,877,878,879
gInnoGPIOLedPwBase  = 881       # 881,882,883,884,885,886,887,888

gInnoMtdCharDev     = '/dev/mtd'
gInnoUpgrDir        = '/tmp/'
gInnoUpgrDataFile   = 'upgrade.data'
gInnoShowFifoFile   = 'show_fifo'
gInnoTypePath       = '/tmp/type'
gInnoHWVerPath      = '/tmp/hwver'
gInnoUpgrLogDir     = '/innocfg/log/'
gInnoUpgrLogFile    = 'upgrade.log'
gInnoNandLogFile    = 'nand.log'
gInnoUpgrPackFmt    = '<I'
gInnoUpgrEncryptKey = 99

gInnoXmrName        = 'T4'

# upgrade logger
gInnoUpgrLogger     = None
# max bytes of single log file
gInnoUpgrLogMax     = 20 * 1024
# log backup count
gInnoUpgrLogBakCnt  = 2

# 硬件版本
gInnoHWVerList      = ['G9', 'G19']
# 避免修改这个变量，路径中的文件在升级是可能会被清空
gInnoUserCfgPath    = ('/innocfg/etc/', '/innocfg/www/conf/miner.conf')

# 分区表
gInnoNandPartitionTable = {
        'BOOT.bin.a'        : '0',
        'BOOT.bin.b'        : '0',
        'env'               : '1',    # 不升级
        'devicetree.dtb.a'  : '2',
        'devicetree.dtb.b'  : '2',
        'uImage.a'          : '3',
        'uImage.b'          : '3',
        'rootfs.jffs2.a'    : '4',
        'cfg'               : '5',    # 不升级
        'rootfs.jffs2.b'    : '6' }

'''
来自inno_lib.py的工具函数
'''
def InnoGetCmdRst(cmd):
    cmdFile = os.popen(cmd)
    rst = cmdFile.read()
    rst = rst.strip('\n')
    cmdFile.close()
    return rst

def InnoGetType():
    fd = open(gInnoTypePath,'r')
    typeStr = fd.readline().strip()
    fd.close()
    return typeStr

def InnoGetHWVer():
    fd = open(gInnoHWVerPath, 'r')
    verStr = fd.readline().strip()
    fd.close()
    return verStr

def InnoGetRootfsFlag():
    rst = InnoGetCmdRst('fw_printenv rootfs_flag')
    flags = rst.split('=')
    print(flags)
    # 只能升级非当前运行的rootfs分区
    if 'a' == flags[1]:
        return 'b'
    else:
        return 'a'

def InnoSetRootfsFlag(flag):
    cmd = 'fw_setenv rootfs_flag ' + flag
    rst = InnoGetCmdRst(cmd)

def InnoSetGPIOValue(value, pin):
    cmd = ('echo %d > /sys/class/gpio/gpio%s/value' %(value,pin))
    #print(cmd)
    os.system(cmd)

# 对每条链的电源控制
# chainId: 链编号 - 1,2,3,4,5,6,7,8; *** -1表示操作所有链 ***
# pwon: 1 - 上电; 0 - 断电
def InnoChainPwCtrl(chainId, pwon):
    ledoff = 0
    if pwon == 0:
        ledoff = 1
    else:
        ledoff = 0

    if chainId > 0 and chanId <= gInnoChainNum:
        InnoSetGPIOValue(pwon, gInnoGPIOPwOnBase + chainId - 1)
        InnoSetGPIOValue(ledoff, gInnoGPIOLedPwBase + chainId - 1)
    elif chainId == -1:
        for offset in range(0, gInnoChainNum):
            InnoSetGPIOValue(pwon, gInnoGPIOPwOnBase + offset)
            InnoSetGPIOValue(ledoff, gInnoGPIOLedPwBase + offset)

def InnoReboot():
    cmd = 'sync'
    InnoGetCmdRst(cmd)

    # 所有链断电，LED全灭
    InnoChainPwCtrl(-1, 0)

    time.sleep(5)
    cmd = 'reboot'
    result = InnoGetCmdRst(cmd)

def InnoMinerApiSet(command, parameter):
    # 打开socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (gInnoMinerApiIp, gInnoMinerApiPort)
    s.connect(addr)
    # 发送命令
    cmd = {gInnoMinerApiCmd : str(command)}
    if None != parameter:
        cmd[gInnoMinerApiParam] = str(parameter)
    #InnoPrintSysLog('apiset', str(cmd))
    jsonStr = json.dumps(cmd, indent = gInnoJsonIndent)
    sendBuf = jsonStr.encode()
    s.send(sendBuf)

'''
升级相关函数
'''
def InitUpgrLog():
    # 创建一个logger
    global gInnoUpgrLogger
    gInnoUpgrLogger = logging.getLogger('Upgrade Log')
    gInnoUpgrLogger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    fh = logging.handlers.RotatingFileHandler(gInnoUpgrLogDir + gInnoUpgrLogFile, \
            maxBytes = gInnoUpgrLogMax, backupCount = gInnoUpgrLogBakCnt)
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
#    ch = logging.StreamHandler()
#    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    fmt = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
    fh.setFormatter(fmt)
#    ch.setFormatter(fmt)

    # 给logger添加handler
    gInnoUpgrLogger.addHandler(fh)
#    gInnoUpgrLogger.addHandler(ch)

def PrintUpgrLog(percent, text):
    if None == gInnoUpgrLogger:
        InitUpgrLog()

    gInnoUpgrLogger.info('<' + str(percent) + '%> ' + str(text))   # write log

def PrintUpgrException(text):
    gInnoUpgrLogger.exception(str(text))

def WritePercentToShowFile(percent, text):
    obj = {'percent' : str(percent), 'text': str(text)}
    jsonStr = json.dumps(obj, indent = gInnoJsonIndent) + '\n'

    data = open(gInnoUpgrDir + gInnoShowFifoFile, 'w')
    data.write(jsonStr)
    data.close()
    # 记录日志
    PrintUpgrLog(percent, text)

# 文本解密
# text: 待解密的文本 (bytes/string)
def TextDecrypt(text):
    decryptText = bytearray(text)
    for i in range(0, len(decryptText)):
        decryptText[i] = (decryptText[i] + 256 - gInnoUpgrEncryptKey) & 0xff
    return decryptText

# 解析upgrade.data，生成每个部分单独的文件
def ParseUpgrPkgs():
    # 读取头部信息
    fdIn = open(gInnoUpgrDir + gInnoUpgrDataFile, 'rb')
    isRetainCfg = struct.unpack(gInnoUpgrPackFmt, fdIn.read(4))[0]
    pkgNum = struct.unpack(gInnoUpgrPackFmt, fdIn.read(4))[0]
    length = struct.unpack(gInnoUpgrPackFmt, fdIn.read(4))[0]

    # 校验package个数
    if len(gInnoUpgrPkgTable) != pkgNum:
        WritePercentToShowFile(100, 'ERROR: package number not match (%d : %d).' 
            % (pkgNum, len(gInnoUpgrPkgTable)))
        #print('ERROR: package number not match (%d : %d).' 
        #    % (pkgNum, len(gInnoUpgrPkgTable)))
        exit()                          # package个数不匹配

    # 读取package table
    base = fdIn.tell()                  # 记录基准位置
    for pkgIdx in range(0, pkgNum):
        offset = struct.unpack(gInnoUpgrPackFmt, fdIn.read(4))[0]
        length = struct.unpack(gInnoUpgrPackFmt, fdIn.read(4))[0]
        name = struct.unpack('24s', fdIn.read(24))[0].strip(b'\x00')
        isEncrypt = gInnoUpgrPkgTable[pkgIdx][2]
        if isEncrypt:
            name = TextDecrypt(name)    # 文本解密
        name = name.decode(encoding='UTF-8', errors='strict')
        gInnoUpgrPkgTable[pkgIdx].append(offset)
        gInnoUpgrPkgTable[pkgIdx].append(length)
        gInnoUpgrPkgTable[pkgIdx].append(name)
        # 校验pkgName
        if gInnoUpgrPkgTable[pkgIdx][0] != name:
            WritePercentToShowFile(100, 'ERROR: package name not match (%s : %s).' 
                % (name, gInnoUpgrPkgTable[pkgIdx][0]))
            #print('ERROR: package name not match (%s : %s).' 
            #    % (name, gInnoUpgrPkgTable[pkgIdx][0]))
            exit()                      # package名称不匹配
            
    # 逐个读取package
    for pkgIdx in range(0, pkgNum):
        # 读取package数据部分
        isEncrypt = gInnoUpgrPkgTable[pkgIdx][2]
        fdIn.seek(base + gInnoUpgrPkgTable[pkgIdx][3])
        pkgData = fdIn.read(gInnoUpgrPkgTable[pkgIdx][4])
        if isEncrypt:
            pkgData = TextDecrypt(pkgData)    # 文本解密
        # 每个package分别写入对应的文件
        filepath = gInnoUpgrDir + gInnoUpgrPkgTable[pkgIdx][5]
        fdOut = open(filepath, 'wb')
        fdOut.write(pkgData)
        fdOut.close()

    fdIn.close()

    return isRetainCfg

# 升级单个package
# part: 示例：BOOT.bin/uImage/rootfs.jffs2
# hwVer: 'G9' or 'G19'
# abFlag: 'a' or 'b'
def UpgradePart(part, hwVer, abFlag):
    filepath = gInnoUpgrDir + part + '.' + hwVer
    if not os.path.exists(filepath):
        filepath = gInnoUpgrDir + part  # 针对G9/G19通用部分的逻辑（rootfs）
    if not os.path.exists(filepath):
        WritePercentToShowFile(100, 'ERROR: %s not exists.' % filepath)
        #print('ERROR: %s not exists.' % filepath)
        exit()                          # 文件不存在，升级失败

    mtd = gInnoMtdCharDev + gInnoNandPartitionTable[part + '.' + abFlag]   # A/B面

    # 创建临时文件记录cmd输出
    fd = open(gInnoUpgrLogDir + gInnoNandLogFile, 'a')
    # 擦除nand分区
    cmd = 'flash_eraseall %s' % mtd
    rst = InnoGetCmdRst(cmd)
    fd.write('\n' + cmd + '\n')
    fd.write(rst)
    # 写入数据
    cmd = 'nandwrite -p %s %s' % (mtd, filepath)
    rst = InnoGetCmdRst(cmd)
    fd.write('\n' + cmd + '\n')
    fd.write(rst)

    time.sleep(1)
    fd.close()

    return True

def DoUpgrade():
    # Step1: 解析升级包
    WritePercentToShowFile(25, 'parsing upgrade packages...')
    isRetainCfg = ParseUpgrPkgs()
    WritePercentToShowFile(30, 'parsing upgrade packages... done.')

    # Step2: 运行升级shell脚本
    shellPath = gInnoUpgrDir + gInnoUpgrPkgTable[0][0]
    cmd = 'chmod 777 ' + shellPath
    PrintUpgrLog(35, 'run shell: ' + cmd)
    InnoGetCmdRst(cmd)
    PrintUpgrLog(40, 'run shell: ' + shellPath)
    InnoGetCmdRst(shellPath)
    WritePercentToShowFile(70, 'update file... done.')

    # step4: 删除innocfg路径下除dna和passwd外的所有文件
    if isRetainCfg != 1:
        for path in gInnoUserCfgPath:
            InnoGetCmdRst('rm -rf ' + path)
        WritePercentToShowFile(90, 'clearing user conf... done.')
    else:
        WritePercentToShowFile(90, 'restoring user conf... done.')

    WritePercentToShowFile(100, 'upgrade done, waiting for reboot...')
    time.sleep(2)

    # Step7: 重启
    InnoReboot()

if __name__ == '__main__':
    try:
        DoUpgrade()
    except:
        PrintUpgrException('Exception Logged')
