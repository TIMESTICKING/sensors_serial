# -*- coding: utf-8 -*-
# @Time    : 2021/11/16 0:42
# @Author  : Jiabao Li
# @FileName: Radar.py
# @Software: PyCharm

from drivers.Serial import *
from drivers.Crc import *
import struct
from time import sleep

def BA(txt):
    return bytearray().fromhex(txt)

class MyRadar:


    def __init__(self, port, h=b'\x55', t=b'\xaa', addr='00', buadRate=115000, timeout=2):
        self.port = port
        self.addr = addr
        self.serial = MySerial(port, h, t, buadRate, timeout)

        self.frame = bytearray().fromhex(f'55{addr}03')
        self.measure = bytes(BA('550044'))


    def reset(self):
        f = bytes(self.frame + BA('05 13 01 3B 8F'))
        self.serial.sendData(f)

    def grab(self):
        self.serial.sendData(self.measure)

    def _send(self, suffix):
        self.serial.sendData(bytes(
            self.frame + suffix
        ))

    def crc_cal(self, by, usebyte=True):
        res = radarcrc_fun(by)
        res = int('{:016b}'.format(res)[::-1], 2)

        return struct.pack('>H', res) if usebyte else res


    def linmindu(self, magnitude=1):
        '''
        :param magnitude: 等级0(1、 2、3、4)
        '''
        assert magnitude in list(range(1, 5)), 'magnitude should be 1 2 3 4'
        a = [BA('05 02 00 88 86'), BA('05 02 01 0B 85'), BA('05 02 02 09 05'),
             BA('05 02 03 8A 06'), BA('05 02 04 08 45')]

        self._send(a[magnitude])

    def julisudufenbiannengli(self, magnitude=1):
        '''
        :param magnitude: 分辨率低中高（0、1、2）
        '''
        assert magnitude in list(range(3)), 'magnitude should be 0 1 2'
        a = [BA('06 04 01 01 81 98'), BA('06 04 01 02 83 18'), BA('06 04 01 04 82 58')]

        self._send(a[magnitude])

    def beijingzhixiuzheng(self, magnitude=1):
        '''
        :param magnitude:   0:设备重新获取背景值，获取当前情况下的背景值。
                        1:勾选在测量值中移除背景值， 设备会在测量结果中移除背景值。
                        2:取消设备在测量结果中移除背景值。
        '''
        assert magnitude in list(range(3)), 'magnitude should be 0 1 2'
        a = [BA('05 05 01 4B 89'), BA('05 05 02 49 09'), BA('05 05 03 CA 0A')]

        self._send(a[magnitude])

    def mubiaoshuliang(self, number=2):
        pass


if __name__ == '__main__':
    l = MyRadar('com1')
    print(l.crc_cal(BA('06 04 01 01')))





