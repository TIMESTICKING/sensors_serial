# -*- coding: utf-8 -*-
# @Time    : 2021/10/30 23:44
# @Author  : Jiabao Li
# @FileName: stable_test.py
# @Software: PyCharm


from drivers.Laser import *



if __name__ == '__main__':
    mylaser = MyLaserLowSpeed('COM13')
    mylaser.first_start()   # 初次启动（包含了初始化）

    for sta, dis in mylaser.get_distance():
        print(f'状态号：{sta}', f'距离：{dis}mm')











