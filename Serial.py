# -*- coding: utf-8 -*-
# @Time    : 2021/10/29 22:22
# @Author  : Jiabao Li
# @FileName: Serial.py
# @Software: PyCharm

import serial
import serial.tools.list_ports
import threading
import time


class MySerial:

    def __init__(self, port, h=b'\x55', t=b'\xaa', buandRate=115000):
        self.t = t
        self.h = h

        self.port = serial.Serial(port, buandRate)
        if not self.port.isOpen():
            self.port.open()
        # self.start_listen()

    def portOpen(self):
        if not self.port.isOpen():
            self.port.open()

    def portClose(self):
        self.port.close()

    def sendData(self, data):
        number = self.port.write(data)
        return number

    def readData(self):
        while True:
            try:
                data = self.port.read_until(self.t + self.h)
                yield data
                # print(data)
            except:
                print('throw a exception. quiting...')
                self.portClose()
                print('quited')
                return

    def clear_buf(self):
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()

    # def start_listen(self):
    #     threading.Thread(target=self.readData).start()


if __name__ == '__main__':
    S = MySerial('COM1')
    for res in S.readData():
        print(res)

