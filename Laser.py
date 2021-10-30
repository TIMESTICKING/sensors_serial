# -*- coding: utf-8 -*-
# @Time    : 2021/10/30 0:11
# @Author  : Jiabao Li
# @FileName: Laser.py
# @Software: PyCharm

from Serial import *

class MyLaser:
    frame = bytearray().fromhex('55000000000000aa')

    keys = {
        'ginfo': b'\x01'
        , 'sfreq': b'\x03'
        , 'sdataformat': b'\x04'
        , 'smeasure': b'\x0d'
        , 'start': b'\x05'
        , 'stop': b'\x06'
        , 'save': b'\x08'
        , 'gnumber': b'\x0a'
        , 'saddr': b'\x11'
        , 'sbaud': b'\x12'
    }

    @classmethod
    def make_frame(cls, key, value=0):
        frame = cls.frame.copy()
        frame[1:2] = cls.keys[key]

        print(frame)





if __name__ == '__main__':
    MyLaser.make_frame('saddr')















