#!/usr/bin/python
# encoding: UTF-8
"""
# Author: yjiong
# Created Time : 2018-12-18 09:20:42

# File Name: base.py
# Description:

"""
import utime
import sys
import os
import machine
sys.path.append('..')
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


'''
基本用法 from machine import UART
u1 = UART(1, 9600)
u1.writechar(65)
u1.write('123')
u1.readchar()
u1.readall()
u1.readline()
u1.read(10)
u1.readinto(buf)
u1.any()
初始化
uart.init(baudrate, bits=8, parity=None, stop=1,
  timeout=1000, flow=None, timeout_char=0, read_buf_len=64)
baudrate:波特率
bits:数据位,7/8/9
parity:校验,None, 0 (even) or 1 (odd)
stop:停止位,1/2
flow:流控,可以是 None, UART.RTS, UART.CTS or UART.RTS | UART.CTS
timeout:读取打一个字节超时时间(ms)
timeout_char:两个字节之间超时时间
read_buf_len:读缓存长度
uart.deinit():关闭串口
uart.any():返回缓冲区数据个数,大于0代表有数据
uart.writechar(char):写入一个字节
uart.read([nbytes]):读取最多nbytes个字节。如果数据位是9bit,那么一个数据占用两个字节,并且nbytes必须是偶数
uart.readall():读取所有数据
uart.readchar():读取一个字节
uart.readinto(buf[, nbytes])
buf:数据缓冲区
nbytes:最大读取数量
uart.readline():读取一行
uart.write(buf):写入缓冲区。在9bits模式下,两个字节算一个数据
uart.sendbreak():往总线上发送停止状态,拉低总线13bit时间
串口对应GPIO
UART(4) is on XA: (TX, RX) = (X1, X2) = (PA0, PA1)
UART(1) is on XB: (TX, RX) = (X9, X10) = (PB6, PB7)
UART(6) is on YA: (TX, RX) = (Y1, Y2) = (PC6, PC7)
UART(3) is on YB: (TX, RX) = (Y9, Y10) = (PB10, PB11)
UART(2) is on: (TX, RX) = (X3, X4) = (PA2, PA3)
'''


class DynApp(object):
    devtypes = {}
    serstat = {}
    for pt in [1, 2]:
        serstat[pt] = 0

    @staticmethod
    def registerdev(app, devname):
        def call(cls):
            thiscls = cls()
            app.devtypes[devname] = thiscls
            return cls
        return call

    def load_drive(self, path='/device'):
        for pyfl in os.listdir(path):
            try:
                tstr = pyfl.split('.')
                if len(tstr) > 1 and tstr[1] == r'py':
                    if tstr[0] != 'base':
                        exec("from " + path[1:] + '.' + tstr[0] + " import *")
            except Exception:
                print("import drive error")
                #  print sys.exc_info()[1]


class DevObj(object):
    def read_dev_value(self, addr, port=2):
        ser = 0
        try:
            count = 0
            if port not in DynApp.serstat:
                DynApp.serstat[port] = 0
            while DynApp.serstat[port] != 0:
                utime.sleep_ms(200)
                count += 1
                if count > 25:
                    raise 'timeout'
                    return "open serial timeout"
            ser = machine.UART(
                    port,
                    baudrate=self.baudrate
                    )
            ser.init(
                    baudrate=self.baudrate,
                    bits=self.bytesize,
                    parity=self.parity,
                    stop=self.stopbits,
                    timeout=self.timeout
                    )
            if ser == 0:
                raise "open serial failed"
            DynApp.serstat[port] = 1
            value = self.read_device(addr, ser)
            if value is None or len(value) == 0:
                raise Exception("value is empty")
        except Exception as e:
            value = {'_status': 'offline', 'error': e}
            utime.sleep_ms(200)
        except DevError as e:
            value.update({'error': e.value})
            utime.sleep_ms(200)
        #  ser.deinit()
        DynApp.serstat[port] = 0
        return value

# user define method
    def read_device(self, addr, ser):
        value = {'example_value': 8888}
        return value
# user define method

    def write_dev_value(self, addr, port, var_name, var_value):
        ser = 0
        ret = 'unknow error'
        try:
            count = 0
            while DynApp.serstat[port] != 0:
                utime.sleep_ms(200)
                count += 1
                if count > 25:
                    raise 'timeout'
                    return "open serial timeout"
            ser = machine.UART(
                    port,
                    baudrate=self.baudrate
                    )
            ser.init(
                    self.baudrate,
                    self.bytesize,
                    self.parity,
                    self.stopbits,
                    self.timeout
                    )
            if ser == 0:
                raise "open serial failed"
            else:
                DynApp.serstat[port] = 2
                func = getattr(self, var_name, None)
                if func:
                    ret = func(ser, addr, var_value)
                else:
                    raise 'wrong data:%s' % var_name
        except Exception as e:
            ret = e.message
        if ser != 0 and ser.isOpen():
            ser.deinit()
        DynApp.serstat[port] = 0
        return ret

# user define method
    def write_dev_cmd(self, ser, addr, cmd_value):
        ret = 0
        return ret
# user define method


class DevError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
