# -*- coding: utf-8 -*-
# @Time    : 2021/10/30 0:11
# @Author  : Jiabao Li
# @FileName: Laser.py
# @Software: PyCharm

from Serial import *

class MyLaser:
    frame = bytearray().fromhex('55000000000000aa')

    GINFO = b'\x01'
    SFREQ = b'\x03'
    SDATAFORMAT = b'\x04'
    SMEASURE = b'\x0d'
    START = b'\x05'
    STOP = b'\x06'
    SAVE = b'\x08'
    GNUMBER = b'\x0a'
    SADDR = b'\x11'
    SBAUD = b'\x12'

    @classmethod
    def make_frame(cls, key, value=0):
        frame = cls.frame.copy()
        frame[1:2] = key

        print(frame)





if __name__ == '__main__':
    MyLaser.make_frame(MyLaser.SADDR)












