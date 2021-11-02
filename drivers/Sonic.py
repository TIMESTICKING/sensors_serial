# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 20:51
# @Author  : Jiabao Li
# @FileName: Sonic.py
# @Software: PyCharm

from drivers.Serial import *
import struct
from time import sleep


class MySonic:

    def __init__(self, port, addr=b'\xff', h=b'\xff', buadRate=9600, timeout=2):
        self.addr = addr
        self.port = port
        self.serial = MySerial_headerOnly(4, port, h, None, buadRate, timeout)


    def send_addr(self):
        self.serial.sendData(self.addr)


    def reader(self, only_1_frame=False):
        try:
            for res in self.serial.readData():
                h = res[0]
                d_h = res[1]
                d_l = res[2]
                sumv = res[3]

                if (h + d_h + d_l) & 0xff == sumv:
                    # print('yeah')
                    yield h, d_h, d_l
                else:
                    if only_1_frame:
                        yield 0, 0, 0
                    continue
        except:
            print(traceback.format_exc())
            return

    def get_distance(self):
        try:
            for _, h, l in self.reader():
                yield h * 256 + l
        except:
            print(traceback.format_exc())
            return

    def close_port(self):
        self.serial.portClose()

    def clear_port(self):
        self.serial.clear_buf()

    def port_verify(self):
        self.send_addr()
        h, dh, dl = self.reader(True).__next__()
        if h == 0xff:
            print('sonic device find port', self.port)
            return self.port
        return False



if __name__ == '__main__':
    print(find_port(MySonic))
    # S = MySonic(find_port(MySonic))
    # for d in S.get_distance():
    #     print('distance:', d, 'mm')









