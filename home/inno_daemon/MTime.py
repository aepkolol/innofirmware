#!/usr/bin/env python3
#coding = UTF-8

import time

class MGetTime():
    starttime = None

    def SetTime(self):
        MGetTime.starttime =time.time()
        return MGetTime.starttime
    
    def GetTime(self):
        return MGetTime.starttime

if __name__ == '__main__':
    MGetTime.SetTime()
    Time = MGetTime.GetTime()
    print("Time:%s" %Time)
