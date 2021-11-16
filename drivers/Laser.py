# -*- coding: utf-8 -*-
# @Time    : 2021/10/30 0:11
# @Author  : Jiabao Li
# @FileName: Laser.py
# @Software: PyCharm

from drivers.Serial import *
from drivers.Crc import *
import struct
from time import sleep


class MyLaser_base:
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

    def __init__(self, port, h=b'\x55', t=b'\xaa', buadRate=115000, timeout=2):
        self.port = port
        self.serial = MySerial(port, h, t, buadRate, timeout)

    def keyval_decoder(self, kv):
        return kv[:1], kv[1:]

    def reader(self, only_1_frame=False):
        try:
            for res in self.serial.readData():
                foo = res[1:-1]
                keyval = foo[:-1]
                crc = foo[-1]

                crc_veri = self._crc_cal(keyval, False) == crc
                # crc_veri = True

                if crc_veri:
                    yield self.keyval_decoder(keyval)
                else:
                    if only_1_frame:
                        yield 0, 0
                    continue
        except Exception as e:
            print(traceback.format_exc())
            raise
        except:
            self.stop()
            return

    def make_frame(self, key, value=0):
        frame = self.frame.copy()
        frame[1:2] = key

        if isinstance(value, bytes):
            frame[2:6] = bytearray(value)
        else:
            frame[2:6] = bytearray(struct.pack('>L', value))

        frame[6:7] = self._crc_cal(bytes(frame[1:6]))

        # print(frame.hex())
        return bytes(frame)

    def _crc_cal(self, by, usebyte=True):
        res = lasercrc_fun(by)
        return struct.pack('B', res) if usebyte else res

    def get_info(self):
        self.serial.sendData(self.make_frame(self.GINFO))


    def get_addr(self):
        self.serial.sendData(self.make_frame(self.SADDR))

        k, v = self.reader().__next__()
        if k == b'\x11':
            return int.from_bytes(v, byteorder='big', signed=False)
        else:
            return False


    def set_addr(self, addr):
        assert addr in list(range(1, 256)), 'addr must be in [1, 255]'

        print('setting addr')
        self.serial.sendData(self.make_frame(self.SADDR, addr))
        print('getting addr')
        a = self.get_addr()
        print('the current addr is ', a)
        if a == addr:
            print('setting success!')
        else:
            print('setting fail!')



    def first_start(self, freq=30):
        if freq >= 40:
            warnings.warn('超过40Hz将会有延迟，这是本Serial类的readData()效率不高导致的，可自行修改')
        delay = 0.3
        self.stop()
        sleep(delay)
        self.get_info()
        sleep(delay)
        self.serial.sendData(self.make_frame(self.SDATAFORMAT, 1))
        sleep(delay)
        self.serial.sendData(self.make_frame(self.SMEASURE))
        sleep(delay)
        self.serial.sendData(self.make_frame(self.SFREQ, freq))
        sleep(delay)
        self.start()

    def stop(self):
        self.serial.sendData(self.make_frame(self.STOP))
        sleep(0.1)

    def close_port(self):
        self.serial.portClose()

    def start(self):
        self.serial.sendData(self.make_frame(self.START))

    def clear_port(self):
        self.serial.clear_buf()

    def port_verify(self):
        self.get_info()
        k, v = self.reader(True).__next__()
        if k == b'\x01':
            print('laser device find port', self.port)
            return self.port
        return False




class MyLaserLowSpeed(MyLaser_base):

    def get_distance(self, warns=True):
        errs = ['none', '信号过弱', '信号过强', '超出量程', '系统错误']
        try:
            for k, v in self.reader():
                vs = struct.unpack('>B', v[:1])[0]
                if k == b'\x07':
                    distance = int.from_bytes(v[1:4], 'big', signed=False)
                    if vs is not 0 and warns:
                        print(errs[vs])
                    yield vs, distance
        except Exception as e:
            print(traceback.format_exc())
            raise
        except:
            self.stop()
            return


if __name__ == '__main__':
    # print(find_port(MyLaser_base))
    # print(MySerial.list_ports())
    # dev = MyLaser_base('COM1', timeout=1)
    # dev.get_info()
    # print(dev.make_frame(dev.SADDR, 254).hex())
    print(int.from_bytes(b'\x00\xfe', byteorder='big', signed=False))









