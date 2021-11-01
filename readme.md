# Intro

It is a serial communicator(controller, receiver...), communicate with sensor LP20 which is a laser ranger. 

Its datasheet is contained in this repo.

# dir Tree

```
sensors
 ├── CH341SER_LINUX
 │   ├── built-in.a
 │   ├── ch34x.c
 │   ├── ch34x.mod
 │   ├── ch34x.mod.c
 │   ├── ch34x.mod.o
 │   ├── ch34x.o
 │   ├── Makefile
 │   ├── Module.symvers
 │   ├── modules.order
 │   └── readme.txt
 ├── drivers
 │   ├── Crc.py
 │   ├── Laser.py
 │   ├── Serial.py
 │   └── __init__.py
 ├── linux.py
 ├── LPxx-DataSheet_V0.5.pdf
 ├── main.py
 ├── readme.md
 └── stable_test.py
```

# Usage

## code

shown in both below and main.py

```python
from drivers.Laser import *

if __name__ == '__main__':
    mylaser = MyLaserLowSpeed('COM13')
    mylaser.first_start()   # 初次启动（包含了初始化）

    '''
    读取`key`和`value`的原始数据
    '''
    print('='*20, 'focus on the raw datas')
    try:
        '''
        ·异常捕获·，也可不要. It is save to do so. Or just drop it.
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
    读取`测量状态`和`距离`数据
    '''
    print('='*20, 'focus on the distance datas')
    mylaser.start()
    try:
        '''
        ·异常捕获·，也可不要.It is save to do so. Or just drop it.
        '''
        i = 0   # 计数
        for sta, dis in mylaser.get_distance():
            i += 1
            print(f'status：{sta}', f'distance：{dis}mm')

            if i == 50:
                # 只测50次
                mylaser.stop()
                break
    except Exception as e:
        print(traceback.format_exc())
        raise
    except:
        mylaser.stop()  # 停止激光设备


    mylaser.close_port()    # 关闭串口
```



## output

```
==================== focus on the raw datas
b'\x01' b'\x0e\x02\x01\t'
b'\x01' b'\x01\x02\x00\x1e'
b'\x07' b'\x00\x00\x00\xe8'
b'\x07' b'\x00\x00\x00\xf1'
b'\x07' b'\x00\x00\x00\xf1'
b'\x07' b'\x00\x00\x00\xf1'
b'\x07' b'\x00\x00\x00\xe8'
b'\x07' b'\x00\x00\x00\xe8'
b'\x07' b'\x00\x00\x00\xf8'
b'\x07' b'\x00\x00\x00\xf8'
==================== focus on the distance datas
status：0 distance：190mm
status：0 distance：174mm
status：0 distance：162mm
status：0 distance：159mm
status：0 distance：160mm
status：0 distance：160mm
status：0 distance：175mm
status：0 distance：156mm
status：0 distance：153mm
status：0 distance：153mm
status：0 distance：155mm
```

