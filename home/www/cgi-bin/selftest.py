#!/bin/python3
# -*- coding: utf-8 -*-

import time,os
import socket,json,sys
import datetime
from inno_config import *
from inno_lib import *

def Line_Split(socket):
    buf = socket.recv(gInnoMinerApiBufSize)
    done = False
    while not done:
        more = socket.recv(gInnoMinerApiBufSize)
        if not more:
            done = True
        else:
            buf = buf + more
    if buf:
        return buf

def getAccValue():
     chainInfo  = {}
     for index in range(0,cidNum):
         chainInfo[index] = 0

     respDict = InnoMinerApiGet(gInnoMinerApiGetDevs)
     if respDict == None:
         return chainInfo

     #get active chain info
     devInfo = respDict['DEVS']
     for chain in devInfo:
         chainInfo[chain['ASC']] = chain['Accepted']

     return chainInfo

if __name__ == '__main__':
    accList = {}
    vidList = []
    pllList = []
    innoName = None
    innoPool = None
    innoUser = None
    innoPwd  = None
    innoFreq = None
    cidNum = 8

    # TODO 如果lock已存在，杀掉之前的selftest进程
    #if os.path.exists(gInnoAutoSchLockPath):
    #    fd = open(gInnoAutoSchLockPath, 'r')
    #    pid = fd.read()
    #    fd.close()
    #    os.system("kill %s" % pid)
    #    os.system("rm -rf %s" % gInnoAutoSchLockPath)

    InnoPrintSysLog('selftest', 'start auto vid search')

    # 创建lock文件
    os.system("ps | grep selftest* | grep -v grep > %s" % gInnoAutoSchLockPath)

    addressStrList = InnoGetCmdRst(gInnoGetIpCmd).split('.')
    innoUser = 'inno.' + addressStrList[3]

    typeStr = InnoGetType()
    if gInnoBtcName == typeStr:
        vidList = list(gInnoBtcVidList)
        pllList = list(gInnoBtcPllList)
        innoName = gInnoBtcName
        innoPool = gInnoBtcPoolTest
        innoFreq = gInnoBtcFreq
        innoPwd  = gInnoBtcPwdTest
    elif gInnoLtcName == typeStr:
        vidList = list(gInnoLtcVidList)
        pllList = list(gInnoLtcPllList)
        innoName = gInnoLtcName
        innoPool = gInnoLtcPool
        innoFreq = gInnoLtcFreq
        innoPwd  = gInnoLtcPwdTest
    elif gInnoDashName == typeStr:
        vidList = list(gInnoDashVidList)
        pllList = list(gInnoDashPllList)
        innoName = gInnoDashName
        innoPool = gInnoDashPool
        innoFreq = gInnoDashFreq
        innoPwd  = gInnoDashPwdTest
    elif gInnoXmrName == typeStr:
        vidList = list(gInnoXmrVidList)
        pllList = list(gInnoXmrPllList)
        innoName = gInnoXmrName
        innoPool = gInnoXmrPool
        innoFreq = gInnoXmrFreq
        innoPwd  = gInnoXmrPwdTest
    else:
        InnoPrintSysLog('inno_lib',  ("ERROR: invalid miner type:%s" % typeStr))
        exit() 

    for idx in range(len(pllList)):
        for index in range(len(vidList)):
            os.system("killall innominer_%s" % innoName)
            os.system("killall innominer_%s" % innoName)
            os.system("killall innominer_%s" % innoName)
            os.system(gInnoInitCmdStr % (innoName, innoPool, innoUser, innoPwd, pllList[idx], pllList[idx], pllList[idx], pllList[idx], pllList[idx], pllList[idx], pllList[idx], pllList[idx], vidList[index], vidList[index], vidList[index], vidList[index], vidList[index], vidList[index], vidList[index], vidList[index], 1, 3, ''))
            time.sleep(gInnoTestTime)
            accList[(index + idx*len(vidList))] = getAccValue()

    vidDict = {}
    pllDict = {}
    for i in range(0,cidNum):
        maxVal = -1
        maxVid = -1
        maxPll = -1
        for j in range(0,len(accList)):
            print(accList[j])
            if accList[j][i] > maxVal:
                maxVal = accList[j][i]
                maxVid = int(j % len(vidList))
                maxPll = int(j / len(vidList))
                print("maxVal = %d, maxVid = %d, maxPll = %d" % (maxVal, maxVid, maxPll))

        vidDict[str(i)] = str(vidList[maxVid])
        pllDict[str(i)] = str(pllList[maxPll])
        print("cid = %d, bestVid = %d, bestPll = %d, maxVal = %d" % (i,vidList[maxVid],pllList[maxPll],maxVal))

    vidStr = json.dumps(vidDict)
    pllStr = json.dumps(pllDict)

    fd = open(gInnoNewDefVidPath, 'w')
    fd.write(vidStr)
    fd.close()

    fd = open(gInnoDefPllPath, 'w')
    fd.write(pllStr)
    fd.close()


    # miner.conf中vidmode设置为自动
    minerCfg = InnoReadMinerCfg()
    if '1' != minerCfg[gInnoVidModeKey]:
        minerCfg[gInnoVidModeKey] = '1'
        InnoWriteMinerCfg(minerCfg)
        InnoPrintSysLog('selftest', 'vidmode change to auto')

    # 启动miner进程
    os.system("/home/inno_tools/start_miner.py")

    # 删除lock文件
    os.system("rm -rf %s" % gInnoAutoSchLockPath)

    obj = { gInnoResultKey : gInnoResultValTrue }
    InnoPrintJsonHeader()
    InnoPrintJson(obj)

