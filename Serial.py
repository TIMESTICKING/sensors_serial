# -*- coding: utf-8 -*-
# @Time    : 2021/10/29 22:22
# @Author  : Jiabao Li
# @FileName: Serial.py
# @Software: PyCharm
import warnings

import serial
import serial.tools.list_ports
import threading
import time
import traceback

class SM:
    findinghead=0
    findingtail=1

class MySerial:

    def __init__(self, port, h=b'\x55', t=b'\xaa', buandRate=115000):
        self.t = t
        self.h = h

        self.port = serial.Serial(port, buandRate, timeout=2)
        if not self.port.isOpen():
            self.port.open()
        # self.start_listen()

    def portOpen(self):
        if not self.port.isOpen():
            self.port.open()

    def portClose(self):
        self.port.close()

    def sendData(self, data):
        # if not self.port.isOpen():
        #     self.port.open()

        number = self.port.write(data)
        return number

    def readData(self):
        buf = b''
        sta = SM.findinghead
        while True:
            # try:
                data = self.port.read()
                if len(data) == 0:
                    warnings.warn('串口读取超时')
                    self.portClose()
                    break

                if sta == SM.findinghead:
                    if data == self.h:
                        buf += data
                        sta = SM.findingtail
                elif sta == SM.findingtail:
                    buf += data
                    if data == self.t:
                        yield buf
                        buf = b''
                        sta = SM.findinghead

            # except Exception as e:
            #     print('throw a exception')
            #     print(traceback.format_exc())
            #     # self.portClose()
            #     # print('quited')
            #     # return

    def clear_buf(self):
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()

    # def start_listen(self):
    #     threading.Thread(target=self.readData).start()


if __name__ == '__main__':
    S = MySerial('COM1')
    S.sendData(b'\x12\x34')
    for res in S.readData():
        print(res)

