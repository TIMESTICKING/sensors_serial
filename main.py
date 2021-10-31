# -*- coding: utf-8 -*-
# @Time    : 2021/10/30 22:37
# @Author  : Jiabao Li
# @FileName: main.py
# @Software: PyCharm

from Laser import *



if __name__ == '__main__':
    mylaser = MyLaserLowSpeed('COM13')
    mylaser.first_start()   # 初次启动（包含了初始化）

    '''
    读取`key`和`value`的原始数据
    '''
    try:
        '''
        ·异常捕获·，也可不要
        '''
        i = 0  # 计数
        for k, v in mylaser.reader():
            i += 1
            print(k, v)

            if i == 50:
                # 只测50次
                mylaser.stop()
                break
    except Exception as e:
        print(traceback.format_exc())
        raise
    except:
        mylaser.stop()  # 停止激光设备





    '''
    读取`测量状态`和`距离`数据
    '''
    mylaser.start()
    try:
        '''
        ·异常捕获·，也可不要
        '''
        i = 0   # 计数
        for sta, dis in mylaser.get_distance():
            i += 1
            print(f'状态号：{sta}', f'距离：{dis}mm')

            if i == 500:
                # 只测500次
                mylaser.stop()
                break
    except Exception as e:
        print(traceback.format_exc())
        raise
    except:
        mylaser.stop()  # 停止激光设备


    mylaser.close_port()    # 关闭串口


















