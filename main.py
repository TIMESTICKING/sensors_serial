# -*- coding: utf-8 -*-
# @Time    : 2021/10/30 22:37
# @Author  : Jiabao Li
# @FileName: main.py
# @Software: PyCharm

from drivers.Laser import *
from drivers.Sonic import *
from drivers.Radar import *
from drivers.Serial import *

if __name__ == '__main__':
    '''
    毫米波雷达
    读取距离
    '''
    finder = find_port_radarlike(MyRadar, ['00','01','05'])   # 自动寻找串口，并提供可能的addr列表
    if finder is None:
        print('didnt find any port and address match the device')
        exit(1)
    print('find port and addr:', finder)
    R = MyRadar(port=finder[0], addr=finder[1])
    R.start(object_num=3, enable_bg_correct=True)   # 目标检测数量2，启动背景获取&纠正
    for _ in range(200):
        print('2 objects distance:', R.snapshot())

    exit(1)
    #
    # '''
    # 超声波
    # 读取`测量状态`和`距离`数据
    # '''
    # S = MySonic(find_port(MySonic))
    # for d in S.get_distance():
    #     print('distance:', d, 'mm')

    '''
    激光主动问询
    '''
    mylaser = MyLaserLowSpeed('COM13')
    # mylaser = MyLaserLowSpeed(find_port(MyLaser_base))
    mylaser.first_start(measure_mode=1)   # 初次启动（包含了初始化）
    res = mylaser.snapshot(times=3)   # 要测3次 res = [(vs1, dis1), (vs2, dis2) ...]
    print(res)


    '''
    激光2钟示例
    '''
    mylaser = MyLaserLowSpeed('COM13')
    # mylaser = MyLaserLowSpeed(find_port(MyLaser_base))
    mylaser.first_start()   # 初次启动（包含了初始化）

    '''
        激光
        读取`key`和`value`的原始数据
    '''
    print('='*20, 'focus on the raw datas')
    try:
        '''
        ·异常捕获·，也可不要. It is save to do so.
        '''
        i = 0  # 计数
        for k, v in mylaser.reader():
            i += 1
            print(k, v)

            if i == 10:
                # 只测10次
                mylaser.stop()
                break
    except Exception as e:
        print(traceback.format_exc())
        raise
    except:
        mylaser.stop()  # 停止激光设备





    '''
        激光
        读取`测量状态`和`距离`数据
    '''
    print('='*20, 'focus on the distance datas')
    mylaser.start()
    try:
        '''
        ·异常捕获·，也可不要.It is save to do so.
        '''
        i = 0   # 计数
        for sta, dis in mylaser.get_distance():
            i += 1
            print(f'status：{sta}', f'distance：{dis}mm')

            if i == 2000:
                # 只测50次
                mylaser.stop()
                break
    except Exception as e:
        print(traceback.format_exc())
        raise
    except:
        mylaser.stop()  # 停止激光设备


    mylaser.close_port()    # 关闭串口
















