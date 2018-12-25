#!/usr/bin/python
# coding=utf8
"""
# Author: yjiong
# Created Time : 2018-12-24 13:36:16

# File Name: main.py
# Description:

"""

from device.base import DynApp

TestDevice = DynApp()
TestDevice.load_drive()
addr = '3300027014'

try:
    print(TestDevice.devtypes['dtsd422'].read_dev_value(addr))
except Exception as e:
    print(e)
