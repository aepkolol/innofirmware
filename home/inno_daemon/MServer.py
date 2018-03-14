#!/usr/bin/env python3
#coding = UTF-8

import os,socket
import threading
import sys,time,json
import ftplib,subprocess

from MConfig  import *
from MTime    import *
from MParser  import *

from inno_config import *
from inno_lib import *

GetBufSize  = 4096
Getip = {'command':'GetIP','param':''}
processFile = "/tmp/program_lock"

threadLock = threading.Lock()

KeyPressFlag = True

def NetStatus(mIP):
    fp = subprocess.Popen('ping -c 3 %s' %mIP, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out = fp.stdout.read()
    NetStatusStr = str(out)
    if 'time=' not in NetStatusStr:
        return 1
    else:
        return 0
        
def NetFlag():
    mLocalflag1 = NetStatus('8.8.8.8')
    mLocalflag2 = NetStatus('114.114.114.114')
    if mLocalflag1 == 1 and mLocalflag2 == 1:
        return 1
    else:
        return 0

def cgStatusFunction():
    GetHwType = InnoGetHWVer()
    NetCount = 0
    while True:
        time.sleep(60)
        NetConnectFlag = NetFlag()
        if NetConnectFlag == 1:
            NetCount += 1
            if NetCount >= 3:
                NetCount = 0
                InnoSetGPIOValue(1,gInnoGPIOLedRed)
                if GetHwType == 'G9':
                    InnoSetGPIOValue(1,gInnoGPIOBeep)
                    time.sleep(0.5)
                    InnoSetGPIOValue(0,gInnoGPIOBeep)
        else:
            InnoSetGPIOValue(0,gInnoGPIOLedRed)
            if GetHwType == 'G9':
                InnoSetGPIOValue(0,gInnoGPIOBeep)
            #avoid the innominer shut down by unknown reason
            os.system("ps -ef | grep innominer_T* | grep -v grep >%s" %processFile)
            if not(os.path.getsize(processFile)):
                #InnoPrintSysLog("MServer", "net is up,start miner...")
                os.system("/home/inno_tools/start_miner.py")
    
def NetModeStatusFunction():
    global KeyPressFlag
    while True:
        time.sleep(0.5)
        if KeyPressFlag == True:
            if InnoGetDhcp() == 'dhcp':
                while KeyPressFlag:
                    InnoSetGPIOValue(1,gInnoGPIOLedGreen)
                    time.sleep(0.5)
                    InnoSetGPIOValue(0,gInnoGPIOLedGreen)
                    time.sleep(0.5)
                    if InnoGetDhcp() == 'dhcp':
                        continue
                    else:
                        break
            else:
                InnoSetGPIOValue(1,gInnoGPIOLedGreen)

def KeyIPStatusFunction():
    count = 0
    global KeyPressFlag
    while True:
        gpiopath = gInnoGPIOCmdValue % gInnoGPIOKey
        fd_RESET = open(gpiopath, "r+")
        buf_reset = fd_RESET.read(3)
        value_reset = int(buf_reset)
        fd_RESET.close()
        while value_reset == 0:
            count += 1
            KeyPressFlag = False
            InnoSetGPIOValue(0,gInnoGPIOLedGreen)
            fd = open(gpiopath, "r+")
            buf = fd.read(3)
            fd.close()
            value_reset = int(buf)
            time.sleep(0.5)
            #if count >= 7:
                #break
        if (count < 4) and (count >= 1):
            #InnoPrintSysLog("MServer", "IP Send start.")
            #MinerIP = MDataParser(Getip)
            IPData = "MinerIP"
            mUdpBroadcastSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            mUdpBroadcastSock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
            mUdpBroadcastSock.sendto(json.dumps(IPData).encode(),('<broadcast>',gPcPort))
            mUdpBroadcastSock.close()
            InnoSetGPIOValue(1,gInnoGPIOLedGreen)
            time.sleep(1)
            InnoSetGPIOValue(0,gInnoGPIOLedGreen)
            time.sleep(3)
        if (count < 15) and (count >= 4):
            InnoPrintSysLog("MServer", "Reset miner conf")
            nCount = 0
            while nCount < 10:
                nCount += 1
                InnoSetGPIOValue(1,gInnoGPIOLedGreen)
                time.sleep(0.5)
                InnoSetGPIOValue(0,gInnoGPIOLedGreen)
                time.sleep(0.5)
            time.sleep(3)
            InnoRevert()
        if count >= 15:
            if InnoGetDhcp() == 'dhcp':
                InnoPrintSysLog("MServer.py", "%s" % str(gInnoDnsDef))
                InnoSetStaticIp(gInnoIpaddrDef,gInnoNetmaskDef,gInnoGatewayDef,gInnoDnsDef)
                InnoSetGPIOValue(1,gInnoGPIOLedGreen)
                time.sleep(10)
                InnoSetGPIOValue(0,gInnoGPIOLedGreen)
            else:
                InnoSetDhcp()
                nCount = 0
                while nCount < 5:
                    nCount += 1
                    InnoSetGPIOValue(1,gInnoGPIOLedGreen)
                    time.sleep(0.5)
                    InnoSetGPIOValue(0,gInnoGPIOLedGreen)
                    time.sleep(0.5)
            InnoNetReset()
            time.sleep(3)
        count = 0
        KeyPressFlag = True

class MudpServer():
    def __init__(self,ServerIP,ServerPort):
        self.count = 0
        self.serverip = ServerIP
        self.serverport = ServerPort
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((ServerIP, ServerPort))

        while True:
            print("Waiting for connect.......")
            GetMessage,addr = self.server_socket.recvfrom(GetBufSize)
            GetMessage1 = GetMessage.decode()
            python_Data = json.loads(GetMessage1)
            ParserData = MDataParser(python_Data)
            SendData = ParserData.ParserData()
            print("[MServer]:%s" %SendData)
            json_Data = json.dumps(SendData)
            self.server_socket.sendto(json_Data.encode(), addr)

        self.server_socket.close()

if __name__ == '__main__':
    #rst = InnoGetCmdRst('ps | grep -rn MServer | grep -v grep | awk \'{print $2}\'')
    #if rst != None and len(rst.split('\n')) > 1:
    #    print('Another MServer is running')
    #    exit()

    gTime = MGetTime()
    rtime = gTime.SetTime()

    # GPIO配置
    InnoExportGPIO(gInnoGPIOLedGreen)
    InnoExportGPIO(gInnoGPIOLedRed)
    InnoExportGPIO(gInnoGPIOKey)
    InnoSetGPIODirOut(gInnoGPIOLedGreen)
    InnoSetGPIODirOut(gInnoGPIOLedRed)
    InnoSetGPIODirIn(gInnoGPIOKey)
    for chain in range(0, gInnoChainNum):
        InnoExportGPIO(gInnoGPIOPwOnBase + chain)   # 每条链的电源控制
        InnoExportGPIO(gInnoGPIOLedPwBase + chain)  # 每条链的电源指示灯控制
        InnoSetGPIODirOut(gInnoGPIOPwOnBase + chain)
        InnoSetGPIODirOut(gInnoGPIOLedPwBase + chain)

    HwType = InnoGetHWVer()
    if HwType == 'G9':
        InnoExportGPIO(gInnoGPIOBeep)
        InnoSetGPIODirOut(gInnoGPIOBeep)

    #InnoPrintSysLog("MServer","MServer.py is running:%s:%s" % (HwType , rtime))

    CgStatus_thread = threading.Thread(target=cgStatusFunction)
    KeyIPStatus_thread = threading.Thread(target=KeyIPStatusFunction)
    NetModeStatus_thread = threading.Thread(target=NetModeStatusFunction)
    CgStatus_thread.start()
    KeyIPStatus_thread.start()
    NetModeStatus_thread.start()
    udp_server = MudpServer(ServerIP,ServerPort)
    time.sleep(0.1)
    CgStatus_thread.join()
    KeyIPStatus_thread.join()
    NetModeStatus_thread.join()
