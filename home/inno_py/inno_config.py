#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform

#################################### json配置 ###################################
gInnoJsonIndent = 2

#################################### cgi配置 ####################################
gInnoVersionPath = '/build_log'
gInnoPassWordPath = '/home/www/conf/password'
gInnoResolvPath = '/etc/resolv.conf'
gInnoInterfacePath ='/etc/network/interfaces'
gInnoTypePath   = '/tmp/type'
gInnoHWVerPath  = '/tmp/hwver'
gInnoRunShPath  = '/tmp/run.sh'
gInnoAutoSchLockPath = '/tmp/autosch_lock'
gInnoMinerConfPath = '/home/www/conf/miner.conf'
gInnoDnaDevicePath = '/dev/dna'
gInnoDnaFilePath = '/innocfg/dna'
gInnoAnalysLogPath = '/tmp/log/analys%d.log'
gInnoVolLogPath = '/tmp/log/volAnalys%d.log'
gInnoLogoPath = '/home/www/static/logo/logo.png'
gInnoUserLogoPath = '/home/www/conf/logo.png.user'
gInnoInnoLogoPath = '/home/www/static/images/logo.png.inno'
gInnoDmLogoPath = '/home/www/static/images/logo.png.dm'
gInnoBlankLogoPath = '/home/www/static/images/blank-logo.png'
gInnoSysLogPath = '/innocfg/log/miner.log'
gInnoDefVidPath = '/home/www/conf/defaultVID'
gInnoNewDefVidPath = '/home/www/conf/defVID'
gInnoDefPllPath = '/home/www/conf/defPLL'
gInnoDhcpPidPath = '/var/run/udhcpc.eth0.pid'
gInnoLogoFileSize = 512 * 1024     # 512K

##################################### network ####################################
gInnoGetDhcpCmd = "cat %s | grep ^iface | sed -n '$p' | awk '{print $4}'" % (gInnoInterfacePath)
gInnoGetIpCmd   = "ifconfig | grep inet | sed -n '1p' | awk '{print $2}' | awk -F ':' '{print $2}'"
gInnoGetNetmask = "ifconfig |grep inet| sed -n '1p'|awk '{print $4}'|awk -F ':' '{print $2}'"
gInnoGetGateway = "route -n | grep eth0 | grep UG | awk '{print $2}'"

gInnoIpaddrDef  = '192.168.1.254'
gInnoNetmaskDef = '255.255.255.0'
gInnoGatewayDef = '192.168.1.1'
gInnoDnsDef     = ['8.8.8.8', '114.114.114.114']

##################################### 正则表达式 ####################################
gInnoRexWebPwd   = r'^[a-zA-Z0-9 ~!@#$%^&*\_=+;:,.?<>\-]{8}$'
gInnoRexPoolUrl  = r'^[a-zA-Z0-9~!@#$%&*_=+;:,.?\-\'\[\]()/]+$'
gInnoRexPoolUser = r'^[a-zA-Z0-9 ~!@#$%^&*_=+;:,.<>?\-]+$'
gInnoRexPoolPwd  = r'^\"?[a-zA-Z0-9 ~!@#$%^&*_=+;:,.<>?\-]+\"?$'
gInnoRexIpAddr   = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
gInnoRexFreq     = r'^[0-9]{1,4}$'
gInnoRexVid      = r'^[0-9]{1,3}$'

##################################### json键 ####################################
gInnoCallBackKey    = 'callback'
gInnoLogoFileKey    = 'logofile'
gInnoBlankLogoKey   = 'nologo'

gInnoResultKey      = 'result'
gInnoResultValTrue  = 'true'
gInnoResultValFalse = 'false'
gInnoErrMsgKey      = 'errmsg'

gInnoPassWordKey    = 'password'
gInnoNewPassWdKey   = 'newpwd'
gInnoOldPassWdKey   = 'oldpwd'

gInnoTypeKey    = 'type'
gInnoFreqKey    = 'Frequency'
gInnoVolKey     = 'Voltage'
gInnoDhcpKey    = 'dhcp'
gInnoIpAddrKey  = 'ipaddress'
gInnoNetmaskKey = 'netmask'
gInnoGatawayKey = 'gateway'
gInnoDnsKey     = 'dns'
gInnoPoolKey    = 'Pool'
gInnoUserKey    = 'UserName'
gInnoPwdKey     = 'Password'
gInnoPoolNumKey = 'PoolNum'
gInnoPool1Key   = 'Pool1'
gInnoPool2Key   = 'Pool2'
gInnoPool3Key   = 'Pool3'
gInnoUser1Key   = 'UserName1'
gInnoUser2Key   = 'UserName2'
gInnoUser3Key   = 'UserName3'
gInnoPwd1Key    = 'Password1'
gInnoPwd2Key    = 'Password2'
gInnoPwd3Key    = 'Password3'
gInnoFanModeKey = 'fanmode'
gInnoFanSpdKey  = 'fanspeed'
gInnoVidModeKey = 'vidmode'
gInnoHeatTimeKey = 'heattime'

################################### xgminer配置 #################################
gInnoMinerApiIp        = '127.0.0.1'
gInnoMinerApiPort      = 4028
gInnoMinerApiBufSize   = 4096
gInnoMinerApiCmd       = 'command'
gInnoMinerApiParam     = 'parameter'
gInnoMinerApiGetDevs   = 'devs'
gInnoMinerApiGetPools  = 'pools'
gInnoMinerApiSetFanMod = 'fanmode'
gInnoMinerApiSetFanSpd = 'fanspd'
gInnoMinerApiPwDown    = 'powerdown'
gInnoMinerApiTest      = {"command" : "devs"}

################################### gpio配置 #################################
gInnoGPIOCmdExport  = '/sys/class/gpio/export'
gInnoGPIOCmdDir     = '/sys/class/gpio/gpio%d/direction'
gInnoGPIOCmdValue   = '/sys/class/gpio/gpio%d/value'
gInnoChainNum       = 8
gInnoGPIOPwOnBase   = 872       # 872,873,874,875,876,877,878,879
gInnoGPIOLedPwBase  = 881       # 881,882,883,884,885,886,887,888
gInnoGPIOLedGreen   = 869
gInnoGPIOLedRed     = 870
gInnoGPIOKey        = 895
gInnoGPIOBeep       = 867

################################### run.sh模板 ##################################
gInnoRunshTemple    = """#!/bin/sh
killall innominer_%s
killall innominer_%s
killall innominer_%s
sleep 5

"""

gInnoTestTime     = 600
gInnoInitCmdStr   = 'innominer_%s -o %s -u %s -p \"%s\" --A1Pll1 %s --A1Pll2 %s --A1Pll3 %s --A1Pll4 %s --A1Pll5 %s --A1Pll6 %s --A1Pll7 %s --A1Pll8 %s --A1Vol1 %s --A1Vol2 %s --A1Vol3 %s --A1Vol4 %s --A1Vol5 %s --A1Vol6 %s --A1Vol7 %s --A1Vol8 %s --A1Fanmode %s --A1Fanspd %s %s --api-listen --api-network --api-allow W:0/0 --syslog > /dev/null 2>&1 &'
gInnoCmdExtraDef  = ''
gInnoCmdHeatTime  = '--A1Heattime %s'
gInnoPoolNumMax   = 3
gInnoVidMode      = '1'
gInnoFanMode      = '1'
gInnoFanSpeed     = '1'
gInnoBtcName      = 'T1'
gInnoBtcPool      = 'stratum+tcp://dbg.stratum.slushpool.com:3335'
gInnoBtcPoolTest  = 'stratum+tcp://btc-sz.s.innpool.com:1800'
gInnoBtcUser      = 'inno.btc'
gInnoBtcPwd       = 'x'
gInnoBtcPwdTest   = 'fixed=1024'
gInnoBtcFreq      = 1260
gInnoBtcVid       = 10
gInnoBtcVidList   = [11, 10, 9, 8, 7] 
gInnoBtcPllList   = [1332, 1260]
gInnoInitBtcCmd   = gInnoInitCmdStr % (gInnoBtcName, gInnoBtcPool, gInnoBtcUser, gInnoBtcPwd, gInnoBtcFreq, gInnoBtcFreq, gInnoBtcFreq, gInnoBtcFreq, gInnoBtcFreq, gInnoBtcFreq, gInnoBtcFreq, gInnoBtcFreq, gInnoBtcVid, gInnoBtcVid, gInnoBtcVid, gInnoBtcVid, gInnoBtcVid, gInnoBtcVid, gInnoBtcVid, gInnoBtcVid, gInnoFanMode, gInnoFanSpeed, gInnoCmdExtraDef)
gInnoLtcName      = 'T2'
gInnoLtcPool      = 'stratum+tcp://ltc.s.innomining.com:1900'
gInnoLtcUser      = 'inno.ltc'
gInnoLtcPwd       = 'x'
gInnoLtcPwdTest   = 'fixed=2048'
gInnoLtcFreq      = 1100
gInnoLtcVid       = 20
gInnoLtcVidList   = [21, 20, 19]
gInnoLtcPllList   = [1100]
gInnoInitLtcCmd   = gInnoInitCmdStr % (gInnoLtcName, gInnoLtcPool, gInnoLtcUser, gInnoLtcPwd, gInnoLtcFreq, gInnoLtcFreq, gInnoLtcFreq, gInnoLtcFreq, gInnoLtcFreq, gInnoLtcFreq, gInnoLtcFreq, gInnoLtcFreq, gInnoLtcVid, gInnoLtcVid, gInnoLtcVid, gInnoLtcVid, gInnoLtcVid, gInnoLtcVid, gInnoLtcVid, gInnoLtcVid, gInnoFanMode, gInnoFanSpeed, gInnoCmdExtraDef)
gInnoDashName     = 'T3'
gInnoDashPool     = 'stratum+tcp://dash.s.innomining.com:2000'
gInnoDashUser     = 'inno.dash'
gInnoDashPwd      = 'x'
gInnoDashPwdTest  = 'fixed=8'
gInnoDashFreq     = 1100
gInnoDashVid      = 12
gInnoDashVidList  = [14, 13, 12]
gInnoDashPllList  = [1100]
gInnoInitDashCmd  = gInnoInitCmdStr % (gInnoDashName, gInnoDashPool, gInnoDashUser, gInnoDashPwd, gInnoDashFreq, gInnoDashFreq, gInnoDashFreq, gInnoDashFreq, gInnoDashFreq, gInnoDashFreq, gInnoDashFreq, gInnoDashFreq, gInnoDashVid, gInnoDashVid, gInnoDashVid, gInnoDashVid, gInnoDashVid, gInnoDashVid, gInnoDashVid, gInnoDashVid, gInnoFanMode, gInnoFanSpeed, gInnoCmdExtraDef)
gInnoXmrName      = 'T4'
gInnoXmrPool      = 'pool1'
gInnoXmrPoolTest  = 'stratum+tcp://a8.s.innomining.com:19333'
gInnoXmrUser      = 'kgdu.0001'
gInnoXmrPwd       = 'x'
gInnoXmrPwdTest   = 'fixed=65535'
gInnoXmrFreq      = 1100
gInnoXmrVid       = 175
gInnoXmrVidList   = [175]
gInnoXmrPllList   = [950, 1000, 1050]
gInnoInitXmrCmd   = gInnoInitCmdStr % (gInnoXmrName, gInnoXmrPool, gInnoXmrUser, gInnoXmrPwd, gInnoXmrFreq, gInnoXmrFreq, gInnoXmrFreq, gInnoXmrFreq, gInnoXmrFreq, gInnoXmrFreq, gInnoXmrFreq, gInnoXmrFreq, gInnoXmrVid, gInnoXmrVid, gInnoXmrVid, gInnoXmrVid, gInnoXmrVid, gInnoXmrVid, gInnoXmrVid, gInnoXmrVid, gInnoFanMode, gInnoFanSpeed, gInnoCmdExtraDef)
gInnoCmd1Pool     = gInnoInitCmdStr
gInnoCmd2Pool     = 'innominer_%s -o %s -u %s -p \"%s\" -o %s -u %s -p \"%s\" --A1Pll1 %s --A1Pll2 %s --A1Pll3 %s --A1Pll4 %s --A1Pll5 %s --A1Pll6 %s --A1Pll7 %s --A1Pll8 %s --A1Vol1 %s --A1Vol2 %s --A1Vol3 %s --A1Vol4 %s --A1Vol5 %s --A1Vol6 %s --A1Vol7 %s --A1Vol8 %s --A1Fanmode %s --A1Fanspd %s %s --api-listen --api-network --api-allow W:0/0 --syslog >/dev/null 2>&1 &'
gInnoCmd3Pool     = 'innominer_%s -o %s -u %s -p \"%s\" -o %s -u %s -p \"%s\" -o %s -u %s -p \"%s\" --A1Pll1 %s --A1Pll2 %s --A1Pll3 %s --A1Pll4 %s --A1Pll5 %s --A1Pll6 %s --A1Pll7 %s --A1Pll8 %s --A1Vol1 %s --A1Vol2 %s --A1Vol3 %s --A1Vol4 %s --A1Vol5 %s --A1Vol6 %s --A1Vol7 %s --A1Vol8 %s --A1Fanmode %s --A1Fanspd %s %s --api-listen --api-network --api-allow W:0/0 --syslog >/dev/null 2>&1 &'

gInnoMinerType = ['T1', 'T2', 'T3', 'T4']
gInnoVidDef = {
        'T1' : 10,
        'T2' : 25,
        'T3' : 12,
        'T4' : 175
    }
gInnoVidList = {
        'T1' : [11, 10, 9, 8],
        'T2' : [26, 25, 24],
        'T3' : [14, 13, 12],
        'T4' : [175]
    }
