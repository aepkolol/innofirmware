#!/bin/python3
# -*- coding: utf-8 -*-

import sys
import struct
import binascii
import logging
import logging.handlers

from inno_config import *
from inno_lib import *

gInnoUpgrPackFmt    = '<I'
gInnoUpgrFile       = 'update.bin'
gInnoUpgrLFile      = 'update_lock.bin'
gInnoUpgrScriptFile = 'upgrade.py'
gInnoUpgrDataFile   = 'upgrade.data'
gInnoUpgrEncryptKey = 99

gInnoUpgrDir        = '/tmp/'
gInnoUpgrLogDir     = '/innocfg/log/'
gInnoUpgrLogFile    = 'upgrade.log'

gInnoUpgrFileSize   = 100 * 1024 * 1024     # 100M

# upgrade logger
gInnoUpgrLogger     = None
# max bytes of single log file
gInnoUpgrLogMax     = 20 * 1024
# log backup count
gInnoUpgrLogBakCnt  = 2

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

gUpgrLastErr = None

def InitUpgrLog():
    # 创建一个logger
    global gInnoUpgrLogger
    gInnoUpgrLogger = logging.getLogger('Upgrade Log')
    gInnoUpgrLogger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件，设置gbk编码防止exception行有中文注释时报错
    fh = logging.handlers.RotatingFileHandler(gInnoUpgrLogDir + gInnoUpgrLogFile, \
            maxBytes = gInnoUpgrLogMax, backupCount = gInnoUpgrLogBakCnt, encoding = 'gbk')
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

    gInnoUpgrLogger.info('<' + str(percent) + '%> ' + text) # write log

def PrintUpgrException(text):
    if None == gInnoUpgrLogger:
        InitUpgrLog()

    gInnoUpgrLogger.exception(text)

def UpgrGetLastError():
    return gUpgrLastErr

# 文本加密
# text: 待加密的文本 (bytes/string)
def TextEncrypt(text):
    encryptText = bytearray(text)
    for i in range(0, len(encryptText)):
        encryptText[i] = (encryptText[i] + gInnoUpgrEncryptKey) & 0xff
    return encryptText

# 文本解密
# text: 待解密的文本 (bytes/string)
def TextDecrypt(text):
    decryptText = bytearray(text)
    for i in range(0, len(decryptText)):
        decryptText[i] = (decryptText[i] + 256 - gInnoUpgrEncryptKey) & 0xff
    return decryptText

# 打包update.bin：MakeScriptSegment/MakeDataSegment/MakeUpgrFile
def MakeScriptSegment(scriptPath):
    # 生成script段，由以下部分组成
    # 1.segHeadLen: 4 Bytes (为1~5项长度之和)
    # 2.segNameLen: 4 Bytes
    # 3.segName:   segNameLen Bytes
    # 4.reserved:   16 Bytes
    # 5.segDataLen: 4 Bytes
    # 6.segData:    segDataLen Bytes
    # 读取script文件
    fd = open(scriptPath, 'rb')
    filedata = fd.read()
    fd.close()
    # 文本加密
    encryptData = TextEncrypt(filedata)
    # 初始化头部信息
    segName = gInnoUpgrScriptFile.encode(encoding='UTF-8', errors='strict') # utf-8编码
    segName = TextEncrypt(segName)                                          # 文本加密
    segNameLen = len(segName)
    segHeadLen = segNameLen + 28
    segResv0 = 0
    segResv1 = 0
    segResv2 = 0
    segResv3 = 0
    #encryptData = encryptData.encode(encoding='UTF-8', errors='strict')
    segDataLen = len(encryptData)
    # 打包
    segment = b''
    segment += struct.pack(gInnoUpgrPackFmt, segHeadLen)
    segment += struct.pack(gInnoUpgrPackFmt, segNameLen)
    segment += segName
    segment += struct.pack(gInnoUpgrPackFmt, segResv0)
    segment += struct.pack(gInnoUpgrPackFmt, segResv1)
    segment += struct.pack(gInnoUpgrPackFmt, segResv2)
    segment += struct.pack(gInnoUpgrPackFmt, segResv3)
    segment += struct.pack(gInnoUpgrPackFmt, segDataLen)
    segment += encryptData

    return segment

def MakeDataSegment(pkgTab):
    '''
    data段由segHead、pkgTab、segData三部分组成
    segHead由以下字段构成:
    1.segHeadLen: 4 Bytes (为1~5项长度之和)
    2.segNameLen: 4 Bytes
    3.segName：   segNameLen Bytes
    4.segPkgNum:  4 Bytes
    5.reserved:   12 Bytes
    6.segDataLen: 4 Bytes
    pkgTab包含若干个条目，每个条目对应一个package，定义如下：
    1.pkgOffset: 4 Bytes
    2.pkgLen:    4 Bytes
    3.pkgName：  24 Bytes
    紧随其后的segData中按照pkgTab中定义的偏移量和长度存放各package的数据
    '''

    # 生成data段package table和数据部分
    segPkgTab = b''
    segData = b''
    segPkgTabLen = 32 * len(pkgTab)
    offset = segPkgTabLen       # offset为pkgData相对于pkgTab起始位置的偏移量
    for pkg in pkgTab:
        # 读取文件内容
        fd = open(pkg[1], 'rb')
        filedata = fd.read()
        fd.close()
        # 文本加密
        pkgName = pkg[0].encode(encoding='UTF-8', errors='strict')
        isEncrypt = pkg[2]
        if isEncrypt:
            pkgName = TextEncrypt(pkgName)
            filedata = TextEncrypt(filedata)
        # 生成package table
        filelen = len(filedata)
        segPkgTab += struct.pack(gInnoUpgrPackFmt, offset)      # offset
        segPkgTab += struct.pack(gInnoUpgrPackFmt, filelen)     # length
        segPkgTab += struct.pack('24s', pkgName)                # name
        # 打包
        segData += filedata
        offset += filelen

    # 初始化头部信息
    segName = gInnoUpgrDataFile.encode(encoding='UTF-8', errors='strict')
    segNameLen = len(segName)
    segHeadLen = segNameLen + 28
    segPkgNum = len(pkgTab)
    segResv0 = 0
    segResv1 = 0
    segResv2 = 0
    segDataLen = segPkgTabLen + len(segData)
    # 打包
    segHead = b''
    segHead += struct.pack(gInnoUpgrPackFmt, segHeadLen)
    segHead += struct.pack(gInnoUpgrPackFmt, segNameLen)
    segHead += segName
    segHead += struct.pack(gInnoUpgrPackFmt, segPkgNum)
    segHead += struct.pack(gInnoUpgrPackFmt, segResv0)
    segHead += struct.pack(gInnoUpgrPackFmt, segResv1)
    segHead += struct.pack(gInnoUpgrPackFmt, segResv2)
    segHead += struct.pack(gInnoUpgrPackFmt, segDataLen)

    return segHead + segPkgTab + segData

def MakeUpgrFile(scriptPath, pkgTab, lock):
    # 设置矿场锁，防止升级public release
    filepath = None
    isLock = 0
    if lock:
        isLock = 1
        filepath = gInnoUpgrLFile
    else:
        isLock = 0
        filepath = gInnoUpgrFile

    # step1: 构造升级包数据部分
    upgrData = MakeScriptSegment(scriptPath) + MakeDataSegment(pkgTab)

    # step2: 构造包头，由以下部分组成
    # 1.headLen:  4 Bytes (为1~6项长度之和)
    # 2.crc32:    4 Bytes (数据部分crc校验值)
    # 3.nameLen:  4 Bytes
    # 4.name：    segNameLen Bytes
    # 5.isLock:   4 Bytes
    # 6.reserved: 12 Bytes
    # 7.dataLen:  4 Bytes
    crc32 = binascii.crc32(upgrData)
    name = gInnoUpgrFile.encode(encoding='UTF-8', errors='strict')
    nameLen = len(name)
    headLen = nameLen + 32
    dataLen = len(upgrData)
    resv0 = 0
    resv1 = 0
    resv2 = 0
    upgrHead = b''
    upgrHead += struct.pack(gInnoUpgrPackFmt, headLen)
    upgrHead += struct.pack(gInnoUpgrPackFmt, crc32)
    upgrHead += struct.pack(gInnoUpgrPackFmt, nameLen)
    upgrHead += name
    upgrHead += struct.pack(gInnoUpgrPackFmt, isLock)
    upgrHead += struct.pack(gInnoUpgrPackFmt, resv0)
    upgrHead += struct.pack(gInnoUpgrPackFmt, resv1)
    upgrHead += struct.pack(gInnoUpgrPackFmt, resv2)
    upgrHead += struct.pack(gInnoUpgrPackFmt, dataLen)

    # step3: 写入升级文件
    fd = open(filepath, 'wb')
    fd.write(upgrHead + upgrData)
    fd.close()

# 解析update.bin生成upgrade.py和upgrade.data, 然后运行upgrade.py解析upgrade.data
def ParseUpgrFile(isRetainCfg):
    global gUpgrLastErr

    # 读取升级文件内容
    fdUpgr = open(gInnoUpgrDir + gInnoUpgrFile, 'rb')
    headLen    = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    crc32Val   = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    nameLen    = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    name       = fdUpgr.read(nameLen).decode(encoding='UTF-8', errors='strict')
    isLock     = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    resv       = fdUpgr.read(12)
    dataLen    = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    position   = fdUpgr.tell()
    upgrData   = fdUpgr.read(dataLen)

    # CRC校验
    crc32Calc  = binascii.crc32(upgrData)
    del upgrData        # 删除变量释放内存空间
    if crc32Calc != crc32Val:
        gUpgrLastErr = 'ERROR: CRC32 not match.'
        return False

    # 矿场升级锁校验
    isDevLock = InnoGetLockDev()
    if isDevLock == 1 and isLock == 0:
        gUpgrLastErr = 'ERROR: invalid upgrade package.'
        return False

    # 解析script segment
    fdUpgr.seek(position)
    segHeadLen = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    segNameLen = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    segName    = fdUpgr.read(segNameLen)
    segName    = TextDecrypt(segName)                               # 文本解密
    segName    = segName.decode(encoding='UTF-8', errors='strict')  # utf-8解码
    segResv    = fdUpgr.read(16)
    segDataLen = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    segData    = fdUpgr.read(segDataLen)
    #segData    = segData.decode(encoding='UTF-8', errors='strict')
    # 校验文件名
    if segName != gInnoUpgrScriptFile:
        gUpgrLastErr = 'ERROR: script name not match.'
        return False
    # 文本解密
    decryptData = TextDecrypt(segData)
    del segData        # 删除变量释放内存空间

    # 保存upgrade script
    fdScript = open(gInnoUpgrDir + gInnoUpgrScriptFile, 'wb')
    fdScript.write(decryptData)
    fdScript.close()
    del decryptData    # 删除变量释放内存空间

    # 解析data segment
    segHeadLen = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    segNameLen = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    segName    = fdUpgr.read(segNameLen).decode(encoding='UTF-8', errors='strict')
    segPkgNum  = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    segResv    = fdUpgr.read(12)
    segDataLen = struct.unpack(gInnoUpgrPackFmt, fdUpgr.read(4))[0]
    # 校验文件名
    if segName != gInnoUpgrDataFile:
        gUpgrLastErr = 'ERROR: data segment name not match.'
        return False
    # 保存upgrade data
    filedata = b''
    filedata += struct.pack(gInnoUpgrPackFmt, int(isRetainCfg))
    filedata += struct.pack(gInnoUpgrPackFmt, segPkgNum)
    filedata += struct.pack(gInnoUpgrPackFmt, segDataLen)
    fdData = open(gInnoUpgrDir + gInnoUpgrDataFile, 'wb')
    fdData.write(filedata)
    fdData.write(fdUpgr.read(segDataLen))
    fdData.close()
    fdUpgr.close()

    # 删除update.bin，避免空间不足
    cmd = 'rm -f ' + gInnoUpgrDir + gInnoUpgrFile
    InnoGetCmdRst(cmd)

    return True

