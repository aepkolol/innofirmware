#!/bin/python3
# -*- coding: utf-8 -*-

from inno_config import *
from inno_lib import *

if __name__ == '__main__':
    try:
        InnoGetCgi()
        oldPwd = InnoParseCgi(gInnoOldPassWdKey).strip('\n')
        newPwd = InnoParseCgi(gInnoNewPassWdKey).strip('\n')

        pwdInFile = InnoReadPassWord().strip('\n')
        
        # 校验
        isOldPwdValid = (oldPwd == pwdInFile)
        isNewPwdValid = InnoRexMatch(gInnoRexWebPwd,  newPwd)

        if isOldPwdValid and isNewPwdValid:
            if InnoWritePassWord(newPwd):
                InnoPrintSysLog('pwdrst', 'change password to %s' % newPwd)
                result = gInnoResultValTrue
            else:
                InnoPrintSysLog('pwdrst', 'failed to set password: %s' % newPwd)
                result = gInnoResultValFalse
        else:
            InnoPrintSysLog('pwdrst', 'invalid new password: %s' % newPwd)
            result = gInnoResultValFalse

        InnoPrintJsonHeader()
        obj = {gInnoResultKey : result}
        InnoPrintJson(obj)
    except:
        InnoPrintSysException('pwdrst', 'Exception Logged')
