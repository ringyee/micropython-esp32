#!/usr/bin/python
# coding=utf8
"""
# Author: yjiong
# Created Time : 2018-12-24 13:36:16

# File Name: main.py
# Description:

"""

import ujson
from device.base import DynApp

TestDevice = DynApp()
addr = '3300027014'

try:
    print(ujson.dumps(TestDevice.devtypes['DTL645_07'].read_dev_value(addr)))
except Exception as e:
    print(e)
