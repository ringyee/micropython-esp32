#!/usr/bin/python
# coding=utf8
"""
# Author: yjiong
# Created Time : 2018-12-14 14:27:57

# File Name: breath.py
# Description:

"""
import utime
import math
from machine import Pin, PWM


class Switch():
    """
    创建一个开关类
    """
    def __init__(self, pin, freq=1000):
        """
        初始化绑定一个引脚,设置默认的PWM频率为1000
        """
        self.pwm = PWM(pin, freq=freq)

    def change_duty(self, duty):
        """
        改变占空比
        """
        if 0 <= duty and duty <= 1023:
            self.pwm.duty(duty)
        else:
            print('警告：占空比只能为 [0-1023] ')

    def deinit(self):
        """
        销毁
        """
        self.pwm.deinit()

    def pulse(self, period, gears):
        # 呼吸灯核心代码
        # 借用sin正弦函数，将PWM范围控制在 23 - 1023范围内
        # self 开关对象
        # period 呼吸一次的周期 单位/毫秒
        # gears 呼吸过程中经历的亮度档位数
        for i in range(2 * gears):
            self.change_duty(int(math.sin(i / gears * math.pi) * 500) + 523)
            # 延时
            utime.sleep_ms(int(period / (2 * gears)))


'''
# 呼吸十次
#switch_led = Switch(Pin(2))
for i in range(100):
    pulse(switch_led, 2000, 100)

# 释放资源
switch_led.deinit()
'''
