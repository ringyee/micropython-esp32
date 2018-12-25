#!/usr/bin/python
# coding=utf8

"""
# Author: yjiong
# Created Time : 2018-12-14 14:27:57
# File Name: main.py
# Description:
"""

# from breath import Switch
import myssd
from machine import Pin
from machine import I2C
import network
import time
import ntptime
import utime


if __name__ == '__main__':
    # sled = Switch(Pin(2))
    ssid = 'things3'
    passwd = 'thingspower3'
    p = Pin(16, Pin.OUT)
    i2c = I2C(scl=Pin(0), sda=Pin(2), freq=100000)
    lcd = myssd.MYSSD(128, 64, i2c)
    lcd.fill(0)
    lcd.text('connect ......', 2, 8)
    lcd.show()
    wl = network.WLAN(network.STA_IF)
    wl.active(True)
    wl.connect(ssid, passwd)
    while not wl.isconnected():
        time.sleep(1)
    ntptime.settime()
    ver = []
    ver.append("SSID:   %s" % ssid)
    ver.append("ipaddr:")
    ver.append("%16s" % wl.ifconfig()[0])
    ver.append("netmask:")
    ver.append("%16s" % wl.ifconfig()[1])
    ver.append("gateway:")
    ver.append("%16s" % wl.ifconfig()[2])
    lcd.verticaltext = ver
    lcd.myshow()
