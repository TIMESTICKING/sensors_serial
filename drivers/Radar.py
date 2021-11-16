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


    def __init__(self, port, h=b'\x55', t=b'\xaa', length=12, addr='00', buadRate=115000, timeout=7):
        self.port = port
        self.addr = addr
        self.object_number = 1
        self.serial = MySerial(port, h, t, length, buadRate, timeout)

        self.frame = bytearray().fromhex(f'55{addr}03')
        self.measure = bytes(BA(f'55{addr}44'))


    def config(self, object_num=1, enable_bg_correct=True):
        self.cancel_debugging()
        sleep(0.2)
        self.linmindu(1)
        sleep(0.2)
        self.julisudufenbiannengli(1)
        sleep(0.2)
        self.mubiaoshuliang(object_num)
        if enable_bg_correct:
            self.beijingzhixiuzheng(0)
            sleep(2)
            self.beijingzhixiuzheng(1)
        sleep(0.3)
        self.clear_port()
        print('设置完毕！')


    def reset(self):
        f = bytes(self.frame + BA('05 13 01 3B 8F'))
        self.serial.sendData(f)

    def snapshot(self):
        alldis = []
        self.serial.sendData(self.measure)
        for res in self.serial.readData():
            try:
                foo = res[1:-1] # addr pos mag dis ver crc_sum
                allres = struct.unpack('<BHHHHB', foo)
                # print(allres)
                addr, pos, mag, dis, ver, crc = allres

                if sum(foo[:-1]) & 0xff == crc:
                    # crc checked
                    alldis.append(dis)

                if len(alldis) == self.object_number:
                    # 到达设置的目标数
                    break
            except:
                print(traceback.format_exc())
                return []

        return alldis


    def _send(self, suffix):
        self.serial.sendData(bytes(
            self.frame + suffix
        ))

    def _crc_cal(self, by, usebyte=True):
        res = radarcrc_fun(by)
        res = int('{:016b}'.format(res)[::-1], 2)

        return struct.pack('>H', res) if usebyte else res

    def clear_port(self):
        self.serial.clear_buf()

    def linmindu(self, magnitude=1):
        '''
        :param magnitude: 等级0(1、 2、3、4)
        '''
        assert magnitude <= 4 and magnitude >= 0, 'magnitude should be 1 2 3 4'
        a = [BA('05 02 00 88 86'), BA('05 02 01 0B 85'), BA('05 02 02 09 05'),
             BA('05 02 03 8A 06'), BA('05 02 04 08 45')]

        print('正在设置灵敏度等级：', magnitude)
        self._send(a[magnitude])

    def julisudufenbiannengli(self, magnitude=1):
        '''
        :param magnitude: 分辨率低中高（0、1、2）
        '''
        assert magnitude in list(range(3)), 'magnitude should be 0 1 2'
        a = [BA('06 04 01 01 81 98'), BA('06 04 01 02 83 18'), BA('06 04 01 04 82 58')]

        print('正在设置分辨率等级：', magnitude)
        self._send(a[magnitude])

    def beijingzhixiuzheng(self, magnitude=1):
        '''
        :param magnitude:   0:设备重新获取背景值，获取当前情况下的背景值。
                        1:勾选在测量值中移除背景值， 设备会在测量结果中移除背景值。
                        2:取消设备在测量结果中移除背景值。
        '''
        assert magnitude in list(range(3)), 'magnitude should be 0 1 2'
        a = [BA('05 05 01 4B 89'), BA('05 05 02 49 09'), BA('05 05 03 CA 0A')]
        mess = ['获取当前情况下的背景值', '设备会在测量结果中移除背景值', '取消设备在测量结果中移除背景值']

        print('正在设置: ', mess[magnitude])
        self._send(a[magnitude])

    def mubiaoshuliang(self, number=1):
        '''
        :param number: 最大支持输出 32 个目标数，如果当前目标点数少于配置数量，则补零输出。
        '''
        assert number <= 32 and number >= 0, 'number should be in [1, 32]'

        self.object_number = number
        a = BA('05 07 00 00 00')
        a[2:3] = struct.pack('B', number)
        a[3:5] = self._crc_cal(a[0:3])

        print('正在设置目标数量：', number)
        self._send(a)

    def shebeidizhi_setting(self, newaddr):
        '''
        :param newaddr: 新的设备地址 [0, 255]
        '''
        assert newaddr <= 255 and newaddr >= 0, 'number should be in [0, 255]'

        a = BA('05 15 00 00 00')
        a[2:3] = struct.pack('B', newaddr)
        a[3:5] = self._crc_cal(a[0:3])

        self._send(a)

    def cancel_debugging(self):
        print('设置关闭调试模式')
        self._send(BA('05 08 00 E8 83'))


    def is_addr_valid(self):
        # todo
        pass


if __name__ == '__main__':
    l = MyRadar('com13', addr='00')
    l.config(2, True)
    # l.shebeidizhi_setting(0)

    # l.snapshot()
    # l.snapshot()
    # l.snapshot()


    t = time.time()
    for i in range(100):
        print(l.snapshot())
        lt = t
        t = time.time()
        print(t - lt)




