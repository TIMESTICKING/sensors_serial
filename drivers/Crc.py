# -*- coding: utf-8 -*-
# @Time    : 2021/10/30 13:45
# @Author  : Jiabao Li
# @FileName: Crc.py
# @Software: PyCharm

import crcmod.predefined
import crcmod

lasercrc_fun = crcmod.mkCrcFun(0x131, initCrc=0, rev=False)

# crc = mycrc(bytes().fromhex('01 00 00 00 00 '))
# print(hex(crc))














