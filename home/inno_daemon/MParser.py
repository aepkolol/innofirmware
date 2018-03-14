#!/usr/bin/env python3
#coding = UTF-8


import time
import sys
import socket
import os
import json
import uuid

#sys.path.append("..")
from MConfig  import *
from MTime import *

from inno_config import *
from inno_lib import *
class MDataParser():
    def __init__(self, ReceiveData):
        self.command = ReceiveData['command']
        self.param   = ReceiveData['param']

    def ParserData(self):
        if self.command == 'GetData':
            Data = self.GetMinerData()
            #InnoPrintSysLog("MParser", "GetData:%s" %Data)
            return Data
        elif self.command == 'SetData':
            self.SetMinerData()
        elif self.command == 'GetIP':
            return self.GetHostIP()
        elif self.command == 'GetTime':
            return self.GetSystemTime()

    def GetHostIP(self):
        cmd_GetStr = os.popen("ifconfig | grep 'inet'")
        TempStr = cmd_GetStr.readlines()
        GetStr = TempStr[0]
        hostIP = GetStr.split()
        hostNameTemp = hostIP[1]
        hostName = hostNameTemp[5:]
        return hostName

    def GetHostMac(self):
        node = uuid.getnode()
        GetData = uuid.UUID(int=node).hex[-12:]
        mac = GetData[0:2]+':'+GetData[2:4]+':'+GetData[4:6]+':'+GetData[6:8]+':'+GetData[8:10]+':'+GetData[10:12]
        return mac

    def GetMinerData(self):
        LocalIP  = self.GetHostIP()
        TempDNA = InnoGetDnaNand()
        LocalDNA  = '0x'
        for c in TempDNA:
            LocalDNA += '%x' %c
        LocalType= InnoGetType()
        LocalMac = self.GetHostMac()
        GetHostData = LocalType+'/'+LocalDNA+'/'+LocalIP+'/'+LocalMac
        return GetHostData
        
    def SetMinerData(self):
        print(self.param)
        RecvData = self.param.split('/')
        #InnoPrintSysLog("MParser", "SetData:%s" %RecvData)
        self.SetMinerIP(RecvData[0],RecvData[1],RecvData[2],RecvData[3],RecvData[4])
         
    def SetMinerIP(self,ipData,maskData,gatewayData,dns1,dns2):
        #print("SetIP......")
        #os.system("cp interfaces interfaces.bak")
        GetFd = open('/etc/network/interfaces','w+')
        SetData = 'auto eth0\n'
        GetFd.write(SetData)
        SetData = 'iface eth0 inet static\n'
        GetFd.write(SetData)
        SetData = ("address  %s\n" %ipData)
        GetFd.write(SetData)
        SetData = ("netmask  %s\n" %maskData)
        GetFd.write(SetData)
        SetData = ("gateway  %s\n" %gatewayData)
        GetFd.write(SetData)
        GetFd.close()
        InnoPrintSysLog("MParser.py", "%s,%s" % (dns1, dns2))
        dnsFd = open('/etc/resolv.conf','w+')
        dnsFd.write("nameserver %s\n" %dns1)
        dnsFd.write("nameserver %s\n" %dns2)
        dnsFd.close()
        InnoNetReset()
        StatusFlag = 'OK'
        return StatusFlag
             
    def GetSystemTime(self):
        print("Get Time......")
        gTime = MGetTime()
        Runtime = gTime.GetTime()
        Curtime = time.time()
        TotalTime = Curtime - Runtime
        print("Toatal:%d" %TotalTime)
        if(TotalTime > (3600-1)):
            mHour = TotalTime/3600
            mMinute = (TotalTime%3600)/60
            TotalTime = (TotalTime%3600)%60
            Rtime  = ("%d Hour,%d Min,%d Sec" %(mHour,mMinute,TotalTime))
        elif(TotalTime > 59):
            mMinute = TotalTime/60
            TotalTime = TotalTime%60
            Rtime  = ("%d Min, %d Sec" %(mMinute,TotalTime))
        else:
            Rtime  =  ("%d Sec" %TotalTime)
        
        return Rtime

    def linesplit(self,socket):
        buffer = socket.recv(4096)
        done = False
        while not done:
            more = socket.recv(4096)
            if not more:
                done = True
            else:
                buffer = buffer+more
        if buffer:
            return buffer

    def GetMinerSummary(self):
        print("Get Miner Summary Info......")
        api_ip = '127.0.0.1'
        api_port = 4028
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((api_ip,int(api_port)))
        s.send(json.dumps({"command":'summary'}).encode())
        response = self.linesplit(s)
        response = response.decode()
        response = response.replace('\x00','')
        response = json.loads(response)
        Data = response['SUMMARY']
        print("GetData:%s" %Data) 
        s.close()
        return response

if __name__ == '__main__':
    commandList = ['GetData','SetData','GetTime']
    for icommand in commandList:
        DataParser = MDataParser(icommand,"")
        DataParser.ParserData();
