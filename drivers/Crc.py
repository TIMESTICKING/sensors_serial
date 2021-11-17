# -*- coding: utf-8 -*-
# @Time    : 2021/10/30 13:45
# @Author  : Jiabao Li
# @FileName: Crc.py
# @Software: PyCharm

import crcmod.predefined as cpr
import crcmod
import struct

lasercrc_fun = crcmod.mkCrcFun(0x131, initCrc=0, rev=False)

radarcrc_fun = crcmod.mkCrcFun(0x18005, initCrc=0, rev=True)

# crc = mycrc(bytes().fromhex('01 00 00 00 00 '))
# print(hex(crc))

if __name__ == '__main__':
    b = bytes(bytearray().fromhex('06 04 01 02'))

    print(b)

    res = radarcrc_fun(b)
    print(res)
    # print(struct.pack('BB', (res>>8) & 0xff, res & 0xff).hex())
    # print(struct.pack('>H', res).hex())

    print(int('{:016b}'.format(res)[::-1], 2))
    print(struct.pack('>H', int('{:016b}'.format(res)[::-1], 2)))











