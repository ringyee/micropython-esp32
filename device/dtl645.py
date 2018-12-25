#!/usr/bin/python
# encoding: UTF-8
"""
# Author: yjiong
# Created Time : 2018-12-24 13:20:42

# File Name: DTL645_07.py
# Description:

"""

from device.base import DevObj
from device.base import DynApp
from device.base import DevError

DI = {
      "TotalEnergy":   [0x00, 0x01, 0x00, 0x00],
      "Voltage":   [0x02, 0x01, 0xFF, 0x00],
      "Current":   [0x02, 0x02, 0xFF, 0x00],
      # "PowerFactor":   [0x02, 0x06, 0xFF, 0x00],
      "InstantActivePower":   [0x02, 0x03, 0xFF, 0x00],
        }


def h2bcd(hexv):
    if isinstance(hexv, list):
        retval = 0
        for h in hexv:
            if isinstance(h, int):
                retval *= 100
                retval += (h >> 4) * 10 + (h & 0xf)
            else:
                return 0
        return retval
    if isinstance(hexv, int):
        return (hexv >> 4) * 10 + hexv & 0xf
    return 0


def chsum(cl):
    chsum = 0
    for chsumi in cl:
        chsum = (chsum + chsumi) % 256
    return chsum


class DTL645_07(DevObj):
    def __init__(self):
        self.set_config()

    @classmethod
    def set_config(cls):
        cls.baudrate = 2400
        cls.bytesize = 8
        cls.parity = 0
        cls.stopbits = 1
        cls.timeout = 500

    def plus33(self, buf):
        rb = []
        for i in range(len(buf)):
            rb.append(0)
        for i in range(len(buf)):
            if buf[i] < 0xCD:
                rb[len(buf) - i - 1] = buf[i] + 0x33
            else:
                rb[len(buf) - i - 1] = buf[i] - 0xCD
        return rb

    def sub33(self, buf):
        rb = []
        for i in range(len(buf)):
            rb.append(0)
        for i in range(len(buf)):
            if buf[i] >= 0x33:
                rb[len(buf) - i - 1] = buf[i] - 0x33
            else:
                rb[len(buf) - i - 1] = buf[i] + 0xCD
        return rb

    def create_read_buf(self, amm_addr, di):
        amm_addr = '%012d' % int(amm_addr)
        buf = [0xFE]
        buf.append(0xFE)
        buf.append(0x68)
        buf.append(int(amm_addr[10:12]) // 10 * 16 + int(amm_addr[10:12]) % 10)
        buf.append(int(amm_addr[8:10]) // 10 * 16 + int(amm_addr[8:10]) % 10)
        buf.append(int(amm_addr[6:8]) // 10 * 16 + int(amm_addr[6:8]) % 10)
        buf.append(int(amm_addr[4:6]) // 10 * 16 + int(amm_addr[4:6]) % 10)
        buf.append(int(amm_addr[2:4]) // 10 * 16 + int(amm_addr[2:4]) % 10)
        buf.append(int(amm_addr[0:2]) // 10 * 16 + int(amm_addr[0:2]) % 10)
        buf.append(0x68)
        buf.append(0x11)
        buf.append(0x04)
        buf = buf + self.plus33(di)
        chsum = 0
        for chsumi in buf[2:]:
            chsum = (chsum + chsumi) % 256
        buf.append(chsum)
        buf.append(0x16)
        return buf

    def read_device(self, addr, ser):
        ret = {}
        for dik in DI:
            send_data = self.create_read_buf(addr, DI[dik])
            # print([hex(x) for x in send_data])
            sbytes = bytes()
            for i in [bytes([x]) for x in send_data]:
                sbytes = sbytes + i
            ser.write(sbytes)
            rece_data = []
            while True:
                va = ser.read(1)
                if va is None:
                    break
                intva = ord(va)
                rece_data.append(intva)
            # print([hex(x) for x in rece_data])
            index = rece_data.index(0x68)
            if len(rece_data) < 12 or \
                    rece_data[len(rece_data) - 1] != 0x16 or \
                    chsum(rece_data[index:(len(rece_data) - 2)]) != \
                    rece_data[len(rece_data) - 2] or \
                    rece_data[index + 8] != 0x91:
                raise DevError('wrong receive date')
            data = rece_data[index:(len(rece_data) - 2)]
            # print([hex(x) for x in data])
            ret.update(self.decode(dik, data[10:]))
        return ret

    def decode(self, dik, buf):
        ret = {}
        if dik == 'TotalEnergy':
            valb = self.sub33(buf)
            ret = {
                    'TotalEnergy': h2bcd(valb[0]) * 10000 +
                    h2bcd(valb[1]) * 100 +
                    h2bcd(valb[2]) +
                    h2bcd(valb[3]) / 100
                                    }
        if dik == 'Voltage':
            valb = self.sub33(buf)
            ret = {
                    'Va': int('%s' % h2bcd(valb[4:6])) / 10.0,
                    'Vb': int('%s' % h2bcd(valb[2:4])) / 10.0,
                    'Vc': int('%s' % h2bcd(valb[0:2])) / 10.0
                   }
        if dik == 'Current':
            valb = self.sub33(buf)
            ret = {
                    'Ia': int('%s' % h2bcd(valb[6:9])) / 1000.0,
                    'Ib': int('%s' % h2bcd(valb[3:6])) / 1000.0,
                    'Ic': int('%s' % h2bcd(valb[0:3])) / 1000.0
                   }
        if dik == 'InstantActivePower':
            valb = self.sub33(buf)
            ret = {
                    'TotalInstantActivePower':
                    int('%s' % h2bcd(valb[9:12])) / 1000.0,
                    'InstantActivePower_a':
                    int('%s' % h2bcd(valb[6:9])) / 1000.0,
                    'InstantActivePower_b':
                    int('%s' % h2bcd(valb[3:6])) / 1000.0,
                    'InstantActivePower_c':
                    int('%s' % h2bcd(valb[0:3])) / 1000.0
                   }
        return ret

    def write_init_data(self, ser, addr, var_value):  # 0x6A78
        ret = None
        return ret


DynApp.registerdev(DynApp, 'DTL645_07')(DTL645_07)

if __name__ == '__main__':
    mydev = DTL645_07()
    amm_addr = '3300027014'

    try:
        print(mydev.read_dev_value(amm_addr))
    except Exception as e:
        print(e)
# #    ser.close()
#     sh = logging.StreamHandler()
#     sh.setLevel(10)
#     _log.addHandler(sh)
