#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cgi
import json
import time
import socket
import re
import urllib
import logging
import logging.handlers

from inno_config import *

# global value for cgi
gForm = None

# system logger
gInnoSysLogger = None
# max bytes of single log file
gInnoSysLogMax = 200 * 1024     # 200KB per log file
# log backup count
gInnoSysLogBakCnt = 4           # 4 backups (totaly 5 log files)

def InnoInitSysLog(logname, logpath):
    # 创建一个logger,可以考虑如何将它封装
    global gInnoSysLogger
    gInnoSysLogger = logging.getLogger(logname)
    gInnoSysLogger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件，设置gbk编码防止exception行有中文注释时报错
    fh = logging.handlers.RotatingFileHandler(logpath, \
            maxBytes = gInnoSysLogMax, backupCount = gInnoSysLogBakCnt, encoding = 'gbk')
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
#    ch = logging.StreamHandler()
#    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    fmt = logging.Formatter('%(asctime)s: <%(levelname)s> %(message)s')
    fh.setFormatter(fmt)
#    ch.setFormatter(fmt)

    # 给logger添加handler
    gInnoSysLogger.addHandler(fh)
#    gInnoSysLogger.addHandler(ch)

def InnoPrintSysLog(module, text):
    if gInnoSysLogger == None:
        InnoInitSysLog('Miner Log', gInnoSysLogPath)

    gInnoSysLogger.info(str(module) + ' - ' + str(text))   # write log

def InnoPrintSysException(module, text):
    if gInnoSysLogger == None:
        InnoInitSysLog('Miner Log', gInnoSysLogPath)

    gInnoSysLogger.exception(str(module) + ' - ' + str(text))

def InnoDebugCgiInData(log_path, form):
    fd = open(log_path, 'w')
    for k in form:
        val = form.getvalue(k)
        s = str(k) + ':' + str(val) + '\n'
        fd.write(s)
    fd.close()

def InnoDebugCgiPrint(log_path, data):
    fd = open(log_path, 'w')
    dataStr = str(data) + '\n'
    fd.write(dataStr)
    fd.close()

def InnoPrintJsonHeader():
    print("Content-type: application/json")
    print()

def InnoPrintJson(d):
    jsonStr = json.dumps(d, indent = gInnoJsonIndent)
    print(jsonStr)

def InnoReadPassWord():
    fd = open(gInnoPassWordPath, 'r')
    password = fd.readline()
    fd.close()
    #
    password = password.strip('\n')

    return password

def InnoWritePassWord(pwd):
    if None != pwd and '' != pwd:   # 校验空密码
        fd = open(gInnoPassWordPath, 'w')
        fd.write(pwd)
        fd.close()
        InnoPrintSysLog('inno_lib', 'change password to %s' % pwd)
        return True
    else:
        InnoPrintSysLog('inno_lib', 'ERROR: attempt to set NULL password')
        return False

def InnoReadMinerCfg():
    fd = open(gInnoMinerConfPath, 'r')
    minerCfg = fd.read()
    fd.close()
    return json.loads(minerCfg)

def InnoWriteMinerCfg(minerCfg):
    jsonStr = json.dumps(minerCfg, indent = gInnoJsonIndent)
    fd = open(gInnoMinerConfPath, 'w')
    fd.write(jsonStr)
    fd.close()

def InnoGetType():
    fd = open(gInnoTypePath,'r')
    typeStr = fd.readline().strip()
    fd.close()
    return typeStr

def InnoGetHWVer():
    fd = open(gInnoHWVerPath,'r')
    typeStr = fd.readline().strip()
    fd.close()
    return typeStr

def InnoGetLockDev():
    rst = InnoGetCmdRst('fw_printenv upgr_lock 2> /dev/null')
    if rst == None or rst == '':
        return 0
    vals = rst.split('=')
    if vals == None or len(vals) < 2:
        return 0
    elif vals[1] != '1':
        return 0
    else:
        return 1

def InnoGetCmdRst(cmd):
    """
    cmd
    """
    cmd_file = os.popen(cmd)
    rst = cmd_file.read()
    rst = rst.strip('\n')
    cmd_file.close()
    return rst

def InnoExportGPIO(pin):
    cmd = 'echo -n %s > %s' % (pin, gInnoGPIOCmdExport)
    #print(cmd)
    os.system(cmd)

def InnoSetGPIODirOut(pin):
    gpiopath = gInnoGPIOCmdDir % pin
    cmd = 'echo out > %s' % gpiopath
    #print(cmd)
    os.system(cmd)

def InnoSetGPIODirIn(pin):
    gpiopath = gInnoGPIOCmdDir % pin
    cmd = 'echo in > %s' % gpiopath
    #print(cmd)
    os.system(cmd)

def InnoSetGPIOValue(value, pin):
    gpiopath = gInnoGPIOCmdValue % pin
    cmd = 'echo %d > %s' % (value, gpiopath)
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
    # log
    InnoPrintSysLog('inno_lib', 'rebooting...')
    cmd = 'sync'
    InnoGetCmdRst(cmd)

    # 所有链断电，LED全灭
    InnoChainPwCtrl(-1, 0)

    time.sleep(3)
    cmd = 'reboot'
    result = InnoGetCmdRst(cmd)
    
    time.sleep(5)
    InnoPrintSysLog('inno_lib', 'ERROR: rebooting failed')

def InnoRevert():
    # 删除用户配置
    cmd = 'rm -rf /innocfg/www/conf/miner.conf'
    InnoGetCmdRst(cmd)
    #cmd = 'rm -rf /innocfg/etc'
    #InnoGetCmdRst(cmd)

    # 恢复DHCP
    InnoSetDhcp()

    # 同步
    InnoGetCmdRst('sync')
    InnoGetCmdRst('sync')
    InnoGetCmdRst('sync')

    # 重启
    InnoReboot()

def InnoRunSh():
    cmd = 'chmod 777 ' + gInnoRunShPath
    rst = InnoGetCmdRst(cmd)
    #InnoDebugCgiPrint('/tmp/r1.log', rst)
    cmd = gInnoRunShPath + ' &'
    #InnoDebugCgiPrint('/tmp/r2.log', cmd)
    rst = InnoGetCmdRst(cmd)
    #InnoDebugCgiPrint('/tmp/r3.log', rst)

def InnoWriteRunSh(typeStr):
    # 获取miner config默认值
    vidmode = gInnoVidMode
    fanmode = gInnoFanMode
    fanspeed = gInnoFanSpeed
    pool1 = None
    user1 = None
    password1 = None
    pool2 = None
    user2 = None
    password2 = None
    pool3 = None
    user3 = None
    password3 = None
    freq = None
    vol = None
    if gInnoBtcName == typeStr:
        pool1 = gInnoBtcPool
        user1 = gInnoBtcUser
        password1 = gInnoBtcPwd
        freq = gInnoBtcFreq
        vol = gInnoBtcVid
    elif gInnoLtcName == typeStr:
        pool1 = gInnoLtcPool
        user1 = gInnoLtcUser
        password1 = gInnoLtcPwd
        freq = gInnoLtcFreq
        vol = gInnoLtcVid
    elif gInnoDashName == typeStr:
        pool1 = gInnoDashPool
        user1 = gInnoDashUser
        password1 = gInnoDashPwd
        freq = gInnoDashFreq
        vol = gInnoDashVid
    elif gInnoXmrName == typeStr:
        pool1 = gInnoXmrPool
        user1 = gInnoXmrUser
        password1 = gInnoXmrPwd
        freq = gInnoXmrFreq
        vol = gInnoXmrVid
    else:
        InnoPrintSysLog('inno_lib',  ("ERROR: invalid miner type:%s" % typeStr))
        return

    minerCfgDef = {gInnoPool1Key:   pool1,   gInnoUser1Key:   user1,   gInnoPwd1Key:    password1,
                   gInnoPool2Key:   pool2,   gInnoUser2Key:   user2,   gInnoPwd2Key:    password2,
                   gInnoPool3Key:   pool3,   gInnoUser3Key:   user3,   gInnoPwd3Key:    password3,
                   gInnoFreqKey:    freq,    gInnoVolKey:     vol,     gInnoPoolNumKey: '1',
                   gInnoVidModeKey: vidmode, gInnoFanModeKey: fanmode, gInnoFanSpdKey:  fanspeed}
                   
    # 首次运行
    if not os.path.exists(gInnoMinerConfPath):
        # 使用默认值自动生成miner.conf 
        minerCfg = minerCfgDef
        InnoWriteMinerCfg(minerCfg)

    # 空白logo临时版本
    #cmd = 'cp -avf %s %s' % (gInnoBlankLogoPath, gInnoUserLogoPath)
    #InnoGetCmdRst(cmd)

    # 首次运行，生成web logo
    if not os.path.exists(gInnoLogoPath):
        if os.path.exists(gInnoUserLogoPath):   # 如果用户设置了logo则使用用户logo
            InnoPrintSysLog('inno_lib',  'restore user logo')
            cmd = 'cp -avf %s %s' % (gInnoUserLogoPath, gInnoLogoPath)
        else:                                   # 用户未设置过logo
            InnoPrintSysLog('inno_lib',  'create default logo for %s' % typeStr)
            cmd = None
            if gInnoBtcName == typeStr:         # T1使用DragonMint Logo
                cmd = 'cp -avf %s %s' % (gInnoDmLogoPath, gInnoLogoPath)
            elif gInnoXmrName == typeStr:       # T4使用Blank Logo
                cmd = 'cp -avf %s %s' % (gInnoBlankLogoPath, gInnoLogoPath)
            else:                               # 其他默认使用Inno Logo
                cmd = 'cp -avf %s %s' % (gInnoInnoLogoPath, gInnoLogoPath)
        rst = InnoGetCmdRst(cmd)

    # 读取miner.conf
    minerCfg = InnoReadMinerCfg()
    # 如果缺少字段，从默认值minerCfgDef里添加，适用版本更新添加字段的情形
    isModified = 0
    for i in minerCfgDef.keys():
        if not i in minerCfg:
            minerCfg[i] = minerCfgDef[i]
            isModified = 1
    # 兼容旧版本fanmode/fanspeed或vidmode为null的情况
    if minerCfg[gInnoFanModeKey] == None:
        minerCfg[gInnoFanModeKey] = gInnoFanMode
        isModified = 1
    if minerCfg[gInnoFanSpdKey] == None:
        minerCfg[gInnoFanSpdKey] = gInnoFanSpeed
        isModified = 1
    if minerCfg[gInnoVidModeKey] == None:
        minerCfg[gInnoVidModeKey] = gInnoVidMode
        isModified = 1
    # 兼容旧版本fanmode和vidmode值为'auto'/'manual'的情况
    if minerCfg[gInnoFanModeKey] == 'auto':
        minerCfg[gInnoFanModeKey] = '1'
        isModified = 1
    elif minerCfg[gInnoFanModeKey] == 'manual':
        minerCfg[gInnoFanModeKey] = '0'
        isModified = 1
    if minerCfg[gInnoVidModeKey] == 'auto':
        minerCfg[gInnoVidModeKey] = '1'
        isModified = 1
    elif minerCfg[gInnoVidModeKey] == 'manual':
        minerCfg[gInnoVidModeKey] = '0'
        isModified = 1
    if isModified == 1:
        InnoWriteMinerCfg(minerCfg)

    extraCmd = gInnoCmdExtraDef                                         # 默认的extra cmd参数
    if gInnoXmrName == typeStr and gInnoHeatTimeKey in minerCfg.keys(): # T4 且配置文件中有heattime项
        extraCmd = gInnoCmdHeatTime % minerCfg[gInnoHeatTimeKey]

    # 处理自动vid
    pllList = { str(i) : str(minerCfg[gInnoFreqKey]) for i in range(0, gInnoChainNum) }     # 手动vid模式或defPLL文件不存在时，使用miner.conf中的值
    vidList = { str(i) : str(minerCfg[gInnoVolKey]) for i in range(0, gInnoChainNum) }      # 手动vid模式或defVID和defaultVID文件均不存在时，使用miner.conf中的值
    if minerCfg[gInnoVidModeKey] == '1':
        if os.path.exists(gInnoDefPllPath):     # 从defPLL文件读取8条链默认pll
            fd = open(gInnoDefPllPath, 'r')
            pllStr = fd.read()
            fd.close()
            pllList = json.loads(pllStr)
        if os.path.exists(gInnoNewDefVidPath):  # 从defVID文件读取8条链默认vid
            fd = open(gInnoNewDefVidPath, 'r')
            vidStr = fd.read()
            fd.close()
            vidList = json.loads(vidStr)
    # 校验VID值
    for i in range(0, gInnoChainNum):
        chainId = str(i)
        if chainId not in pllList.keys() or not InnoRexMatch(gInnoRexFreq, pllList[chainId]):
            pllList[chainId] = minerCfg[gInnoFreqKey]
        if chainId not in vidList.keys() or not InnoRexMatch(gInnoRexVid, vidList[chainId]):
            vidList[chainId] = minerCfg[gInnoVolKey]

    # 生成cmd
    cmd = 'pool nums error.'
    if '1' == minerCfg[gInnoPoolNumKey]:
        password1 = InnoDequotes(minerCfg[gInnoPwd1Key])
        cmd = gInnoCmd1Pool % (typeStr, minerCfg[gInnoPool1Key], minerCfg[gInnoUser1Key], password1,
                pllList['0'], pllList['1'], pllList['2'], pllList['3'], pllList['4'], pllList['5'], pllList['6'], pllList['7'],
                vidList['0'], vidList['1'], vidList['2'], vidList['3'], vidList['4'], vidList['5'], vidList['6'], vidList['7'],
                minerCfg[gInnoFanModeKey], minerCfg[gInnoFanSpdKey], extraCmd);
    elif '2' == minerCfg[gInnoPoolNumKey]:
        password1 = InnoDequotes(minerCfg[gInnoPwd1Key])
        password2 = InnoDequotes(minerCfg[gInnoPwd2Key])
        cmd = gInnoCmd2Pool % (typeStr, minerCfg[gInnoPool1Key], minerCfg[gInnoUser1Key], password1,
                minerCfg[gInnoPool2Key], minerCfg[gInnoUser2Key], password2,
                pllList['0'], pllList['1'], pllList['2'], pllList['3'], pllList['4'], pllList['5'], pllList['6'], pllList['7'],
                vidList['0'], vidList['1'], vidList['2'], vidList['3'], vidList['4'], vidList['5'], vidList['6'], vidList['7'],
                minerCfg[gInnoFanModeKey], minerCfg[gInnoFanSpdKey], extraCmd);
    elif '3' == minerCfg[gInnoPoolNumKey]:
        password1 = InnoDequotes(minerCfg[gInnoPwd1Key])
        password2 = InnoDequotes(minerCfg[gInnoPwd2Key])
        password3 = InnoDequotes(minerCfg[gInnoPwd3Key])
        cmd = gInnoCmd3Pool % (typeStr, minerCfg[gInnoPool1Key], minerCfg[gInnoUser1Key], password1,
                minerCfg[gInnoPool2Key], minerCfg[gInnoUser2Key], password2,
                minerCfg[gInnoPool3Key], minerCfg[gInnoUser3Key], password3,
                pllList['0'], pllList['1'], pllList['2'], pllList['3'], pllList['4'], pllList['5'], pllList['6'], pllList['7'],
                vidList['0'], vidList['1'], vidList['2'], vidList['3'], vidList['4'], vidList['5'], vidList['6'], vidList['7'],
                minerCfg[gInnoFanModeKey], minerCfg[gInnoFanSpdKey], extraCmd);
    else:
        InnoPrintSysLog('inno_lib', 'ERROR: too many pools: %s' % minerCfg[gInnoPoolNumKey])
        return

    # run.sh
    fd = open(gInnoRunShPath, 'w')
    fd.write(gInnoRunshTemple % (typeStr, typeStr, typeStr))
    fd.write(cmd)
    fd.write('\n')
    fd.close()

def InnoGetCgi():
    global gForm
    gForm = cgi.FieldStorage()
    #InnoDebugCgiPrint('/tmp/gForm.log', gForm)

def InnoNeedUnquote(k):
    if gInnoPool1Key == k:
        return True
    if gInnoPool2Key == k:
        return True
    if gInnoPool3Key == k:
        return True

    if gInnoUser1Key == k:
        return True
    if gInnoUser2Key == k:
        return True
    if gInnoUser3Key == k:
        return True

    if gInnoPwd1Key == k:
        return True
    if gInnoPwd2Key == k:
        return True
    if gInnoPwd3Key == k:
        return True

    return False

def InnoParseCgi(k):
    #InnoDebugCgiPrint(str(k) + '.log', k)
    val = gForm.getvalue(k)
    #InnoDebugCgiPrint(str(k) + '_v.log', val)
    if not val:
        return val
    if InnoNeedUnquote(k):
        val = urllib.parse.unquote(val)
    return val

# 从/dev/dna获取设备DNA码
def InnoGetDnaDev():
    fd = open(gInnoDnaDevicePath, 'rb')
    dna = fd.read(8)
    fd.close()
    return dna

# 从/innocfg/dna文件获取DNA码
def InnoGetDnaNand():
    fd = open(gInnoDnaFilePath, 'rb')
    dna = fd.read(8)
    fd.close()
    return dna

# 保存DNA码到文件
def InnoSetDnaNand(dna):
    fd = open(gInnoDnaFilePath, 'wb')
    fd.write(dna)
    fd.close()

# 校验dna是否匹配
def InnoDevice():
    dna = None

    try:
        # 如果读到dna码长度不是8，重新读取，最多5次
        timeout = 5
        while (dna == None or len(dna) != 8) and timeout != 0:
            dna = InnoGetDnaDev()
            timeout -= 1
        if timeout == 0:
            InnoPrintSysLog('inno_lib', 'ERROR: failed to read DNA from FPGA')
            return False
    except:
        InnoPrintSysException('inno_lib', 'Exception logged')
        return False

    if not os.path.exists(gInnoDnaFilePath):
        # 首次上电，生成dna文件/innocfg/dna
        InnoSetDnaNand(dna)
        return True
    else:
        # 读取dna文件
        dnaInFile = InnoGetDnaNand()
        # 处理dna文件为空或dna不满8字节的问题，后期稳定后可以删掉这段代码
        if len(dnaInFile) < 8:
            InnoSetDnaNand(dna)
            InnoPrintSysLog('inno_lib', 'reload DNA from FPGA')
            return True
        # 校验DNA
        if dnaInFile == dna:
            return True
        else:
            return False

# 正则匹配
def InnoRexMatch(rex, text):
    return (None != text) and (None != re.match(rex,  str(text)))

# 去双引号
def InnoDequotes(str):
    isQuoteStart = (str[0] == '\"')
    isQuoteEnd   = (str[len(str) - 1] == '\"')
    if isQuoteStart and isQuoteEnd:
        return str[1 : len(str) - 1]
    else:
        return str

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

    return True
 
def InnoMinerApiGet(command):
    # 打开socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (gInnoMinerApiIp, gInnoMinerApiPort)
    s.connect(addr)
    # 发送命令
    cmd = {gInnoMinerApiCmd : str(command)}
    #InnoPrintSysLog('apiget', str(cmd))
    jsonStr = json.dumps(cmd, indent = gInnoJsonIndent)
    sendBuf = jsonStr.encode()
    s.send(sendBuf)
    # 接收数据
    buf = s.recv(gInnoMinerApiBufSize)
    done = False
    while not done:
        more = s.recv(gInnoMinerApiBufSize)
        if not more:
            done = True
        else:
            buf = buf + more

    buf = buf.decode()
    buf = buf.replace('\x00','')

    s.close()

    if buf:
        return json.loads(buf)  # 返回字典
    else:
        return None

# 返回MAC地址
def InnoGetEmac():
    cmd = 'fw_printenv ethaddr'
    ethaddr = InnoGetCmdRst(cmd)
    ethaddr = ethaddr.split('=')
    ethaddr = ethaddr[1]
    return ethaddr

# 返回'dhcp'或'static'
def InnoGetDhcp():
    return InnoGetCmdRst(gInnoGetDhcpCmd)

# 返回ip地址
def InnoGetIpaddr():
    return InnoGetCmdRst(gInnoGetIpCmd)

# 返回子网掩码
def InnoGetNetmask():
    return InnoGetCmdRst(gInnoGetNetmask)

# 返回网关
def InnoGetGateway():
    return InnoGetCmdRst(gInnoGetGateway)

# 返回DNS列表
def InnoGetDns():
    dns = []
    fd = open(gInnoResolvPath,'r')
    for line in fd:
        dnsStr = line.split(' ')[1]
        dnsStr = dnsStr.strip('\n')
        dns.append(dnsStr)
    fd.close()
    return dns

# 设置为DHCP
def InnoSetDhcp():
    fd = open(gInnoInterfacePath,'w')
    fd.write("auto eth0\n")
    fd.write("iface eth0 inet dhcp\n")
    fd.close()

# 设置静态IP
def InnoSetStaticIp(ipaddr, netmask, gateway, dns):
    # 修改/etc/network/interfaces
    fd = open(gInnoInterfacePath,'w')
    fd.write("auto eth0\n")
    fd.write("iface eth0 inet static\n")
    fd.write("address %s\n" % ipaddr )
    fd.write("netmask %s\n" % netmask)
    fd.write("gateway %s\n" % gateway)
    fd.close()
    # 修改/etc/resolv.conf
    fd = open(gInnoResolvPath, 'w')
    for d in dns: 
        fd.write("nameserver %s\n" % str(d))
    fd.close()

def InnoNetReset():
    cmd = 'ifdown -f eth0'
    rst = InnoGetCmdRst(cmd)

    # kill udhcpc进程
    time.sleep(1)
    if os.path.exists(gInnoDhcpPidPath):
        pid = InnoGetCmdRst('cat ' + gInnoDhcpPidPath)
        InnoGetCmdRst('kill ' + pid)
        InnoGetCmdRst('rm -rf ' + gInnoDhcpPidPath)

    time.sleep(1)
    cmd = 'ifup eth0'
    rst = InnoGetCmdRst(cmd)

if __name__ == '__main__':
    obj = {'result' : 'true'}
    InnoPrintJson(obj)

    """
    dns = InnoGetDns()
    print(dns)

    ifconfigStr = InnoGetCmdRst('ifconfig')
    print(ifconfigStr)

    InnoNetReset()
    """


