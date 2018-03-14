#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cgi
import json

from inno_config import *
from inno_lib import *

if __name__ == '__main__': 
    form = cgi.FieldStorage()
    InnoDebugCgiPrint('cgi.log', form)
    InnoDebugCgiInData('debug.log', form)

    obj = {'result' : 'true'}
    InnoPrintJson(obj)

