# -*- coding: utf-8 -*-
# @Time    : 2021/10/30 0:11
# @Author  : Jiabao Li
# @FileName: Laser.py
# @Software: PyCharm
import warnings

from Serial import *
from Crc import *
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

    def __init__(self, port, h=b'\x55', t=b'\xaa', buadRate=115000):
        self.serial = MySerial(port, h, t, buadRate)

    def keyval_decoder(self, kv):
        pass

    def reader(self):
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
                    continue
        except Exception as e:
            print(traceback.format_exc())
            raise
        except:
            self.stop()
            self.close_port()
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

    def first_start(self, freq=30):
        if freq >= 40:
            warnings.warn('超过40Hz将会有延迟，这是本Serial类的readData()效率不高导致的，可自行修改')
        delay = 0.3
        self.stop()
        sleep(delay)
        self.serial.sendData(self.make_frame(self.GINFO))
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

    def close_port(self):
        sleep(0.3)
        self.serial.portClose()

    def start(self):
        self.serial.sendData(self.make_frame(self.START))



class MyLaserLowSpeed(MyLaser_base):

    def keyval_decoder(self, kv):
        return kv[:1], kv[1:]

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
            self.close_port()
            return


if __name__ == '__main__':
    mylaser = MyLaserLowSpeed('COM13')
    mylaser.start()
    # mylaser.stop()
    i = 0
    for k, v in mylaser.reader():
        i += 1
        print(k.hex(), v.hex())

        if i == 600:
            mylaser.stop()
            break











