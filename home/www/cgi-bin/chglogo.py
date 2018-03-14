#!/bin/python3
# -*- coding: utf-8 -*-

import sys
import cgi
import time

from inno_config import *
from inno_lib import *

def GetLogoFile():
    form = cgi.FieldStorage()
    nologo = form.getvalue(gInnoBlankLogoKey)

    if nologo == '1':       # 使用空白logo
        InnoPrintSysLog('chglogo', 'using blank logo')
        # 设置空白logo
        cmd = 'cp -avf %s %s' % (gInnoBlankLogoPath, gInnoLogoPath)
        InnoGetCmdRst(cmd)
        # 将用户设置的logo保存到配置分区
        cmd = 'cp -avf %s %s' % (gInnoLogoPath, gInnoUserLogoPath)
        InnoGetCmdRst(cmd)
        return gInnoResultValTrue
    else:                   # 使用上传的logo文件
        fileitem = form[gInnoLogoFileKey]
        if fileitem.filename:
            fileData = fileitem.file.read()
            # 校验尺寸
            fileLen = sys.getsizeof(fileData)
            InnoPrintSysLog('chglogo', 'logo file size: ' + str(fileLen))
            if fileLen > gInnoLogoFileSize:
                InnoPrintJsonHeader()
                obj = {gInnoResultKey : gInnoResultValFalse}
                InnoPrintJson(obj)
                sys.exit(0)
            # 写入文件
            fd = open(gInnoLogoPath, 'wb')
            fd.write(fileData)
            fd.close()
            # 修改权限
            cmd = 'chmod -x ' + gInnoLogoPath
            InnoGetCmdRst(cmd)
            # 将用户设置的logo保存到配置分区
            cmd = 'cp -avf %s %s' % (gInnoLogoPath, gInnoUserLogoPath)
            InnoGetCmdRst(cmd)
            return gInnoResultValTrue
        else:
            return gInnoResultValFalse

if __name__ == '__main__':
    result = None
    try:
        InnoPrintSysLog('chglogo', 'change logo')
        result = GetLogoFile()
    except:
        InnoPrintSysException('chglogo', 'Exception Logged')
        result = gInnoResultValFalse

    InnoPrintJsonHeader()
    obj = {gInnoResultKey : result}
    InnoPrintJson(obj)
