#!/bin/python3
# -*- coding: utf-8 -*-

import time

from inno_config import *
from inno_lib import *

gLastError = 'Success'

class CPool:
    mPoolNum = 0
    
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        CPool.mPoolNum += 1

def InnoGetCgiMinerCfg():
    InnoGetCgi()

    result = {}
    result[gInnoFreqKey]     = InnoParseCgi(gInnoFreqKey)
    result[gInnoVidModeKey]  = InnoParseCgi(gInnoVidModeKey)
    result[gInnoVolKey]      = InnoParseCgi(gInnoVolKey)
    result[gInnoFanModeKey]  = InnoParseCgi(gInnoFanModeKey)
    result[gInnoFanSpdKey]   = InnoParseCgi(gInnoFanSpdKey)
    result[gInnoHeatTimeKey] = InnoParseCgi(gInnoHeatTimeKey)

    pool1     = InnoParseCgi(gInnoPoolKey + '1')
    user1     = InnoParseCgi(gInnoUserKey + '1')
    password1 = InnoParseCgi(gInnoPwdKey + '1')
    if None != pool1:
        result[gInnoPoolKey] = [CPool(pool1, user1, password1),]
        pool2     = InnoParseCgi(gInnoPoolKey + '2')
        user2     = InnoParseCgi(gInnoUserKey + '2')
        password2 = InnoParseCgi(gInnoPwdKey + '2')
        if None != pool2:
            result[gInnoPoolKey].append(CPool(pool2, user2, password2))
        pool3     = InnoParseCgi(gInnoPoolKey + '3')
        user3     = InnoParseCgi(gInnoUserKey + '3')
        password3 = InnoParseCgi(gInnoPwdKey + '3')
        if None != pool3:
            result[gInnoPoolKey].append(CPool(pool3, user3, password3))

    return result

# 设置矿池信息
# 将newCfg更新到oldCfg
def InnoSetPoolConf(oldCfg, newCfg):
    global gLastError

    poolCfg = newCfg[gInnoPoolKey]

    # 正则匹配
    isArgsValid = True
    for pool in poolCfg:
        if not InnoRexMatch(gInnoRexPoolUrl,  pool.url):
            isArgsValid = False
            gLastError = 'Invalid argument: %s' % (pool.url)
            break
        if not InnoRexMatch(gInnoRexPoolUser, pool.user):
            isArgsValid = False
            gLastError = 'Invalid argument: %s' % (pool.user)
            break
        if not InnoRexMatch(gInnoRexPoolPwd,  pool.password):
            isArgsValid = False
            gLastError = 'Invalid password format'
            break
        isQuoteStart = (pool.password[0] == '\"')
        isQuoteEnd   = (pool.password[len(pool.password) - 1] == '\"')
        if isQuoteStart != isQuoteEnd:
            isArgsValid = False
            gLastError = 'Invalid password format'
            break

    if isArgsValid:
        # 将newCfg中的值更新到oldCfg
        oldCfg[gInnoPoolNumKey] = str(CPool.mPoolNum)
        for i in range(0, gInnoPoolNumMax):
            urlKey  = gInnoPoolKey + str(i + 1)
            userKey = gInnoUserKey + str(i + 1)
            pwdKey  = gInnoPwdKey + str(i + 1)
            if i < CPool.mPoolNum:  # 该矿池有效
                pool = poolCfg[i]
                oldCfg[urlKey]  = pool.url
                oldCfg[userKey] = pool.user
                oldCfg[pwdKey]  = pool.password
            else:                   # 删除该矿池
                oldCfg[urlKey]  = None
                oldCfg[userKey] = None
                oldCfg[pwdKey]  = None
        return True
    else:
        return False

# 设置频率电压风扇信息
# 将newCfg更新到oldCfg，然后拷贝到newCfg返回
def InnoSetMinerConf(oldCfg, newCfg):
    # 将newCfg所有非空值设置到oldCfg
    for (key, val) in newCfg.items():
        if None != val:
            oldCfg[key] = val

    # 自动vid处理
    #if oldCfg[gInnoVidModeKey] == '1':      # 自动vid模式下从gInnoDefVidPath读取vid值
    #    if os.path.exists(gInnoDefVidPath):
    #        fdVid = open(gInnoDefVidPath, 'r')
    #        vol = fdVid.read()
    #        vol = vol.strip('\n')
    #        fdVid.close()
    #        oldCfg[gInnoVolKey] = vol
    #    else:   # 如果defaultVID文件不存在，则不改变vid值
    #        InnoPrintSysLog('pool', 'ERROR: %s is not exist' % gInnoDefVidPath)

    return True

if __name__ == '__main__':
    global gLastError

    try:
        minerCfg = InnoReadMinerCfg()
        newCfg = InnoGetCgiMinerCfg()

        isSucc = True
        # 如果传了矿池信息，设置矿池
        if gInnoPoolKey in newCfg.keys():
            isSucc = InnoSetPoolConf(minerCfg, newCfg)
            del newCfg[gInnoPoolKey]

        # 设置设备配置
        if isSucc:
            isSucc = InnoSetMinerConf(minerCfg, newCfg)

        result = None
        if isSucc:
            # 写配置文件
            InnoWriteMinerCfg(minerCfg)
            # log
            cfgStr = json.dumps(minerCfg)
            InnoPrintSysLog('pool', 'miner cfg changed to ' + cfgStr)
            # 生成run.sh
            typeStr = InnoGetType()
            InnoWriteRunSh(typeStr)
            # miner重启(这里只负责关掉，由MServer.py负责启动)
            rst = False
            try:
                rst = InnoMinerApiSet(gInnoMinerApiPwDown, '3')     # 3秒后退出
                time.sleep(5)                                       # 延时5s，防止miner还没退出页面就已跳转
            except ConnectionError:
                rst = False
            if not rst:
                gLastError = 'Success. Please reboot manually to apply the new settings.'
            result = gInnoResultValTrue
        else:
            result = gInnoResultValFalse
        obj = {gInnoResultKey : result, gInnoErrMsgKey : gLastError}
        InnoPrintJsonHeader()
        InnoPrintJson(obj)
    except:
        InnoPrintSysException('pool', 'Exception logged')

