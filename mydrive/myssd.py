#!/usr/bin/python
# coding=utf8
"""
# Author: yjiong
# Created Time : 2018-12-18 09:20:42

# File Name: myssd.py
# Description:

"""
import ssd1306
import time
import utime


class MYSSD(ssd1306.SSD1306_I2C):
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        super(MYSSD, self).__init__(
                width, height, i2c, addr=0x3c, external_vcc=False)
        self.verticaltext = ['date', 'time']
        try:
            import _thread
            _thread.start_new_thread(self.show())
        except:
            print('no module _thread')

    def myshow(self):
        while True:
            l = len(self.verticaltext)
            if self.verticaltext[0][:4] == 'date':
                self.verticaltext[0] = (
                        'date:{}-{:0>2}-{:0>2}'.format(utime.localtime()[0],
                                                       utime.localtime()[1],
                                                       utime.localtime()[2]))
                self.verticaltext[1] = (
                        "time:{:0>2}:{:0>2}:{:0>2}".format(
                            utime.localtime()[3] + 8,
                            utime.localtime()[4],
                            utime.localtime()[5]))
            pageh = l * 12 + 64
            if l <= 5:
                self.fill(0)
                for k in range(l):
                    self.text(self.verticaltext[k], 0, k*12)
                self.show()
                time.sleep_ms(100)
            else:
                for i in range(pageh):
                    self.fill(0)
                    for k in range(l):
                        self.text(self.verticaltext[k], 0, 64-i+k*12)
                    self.show()
                    time.sleep_ms(100)




