import time
import sys
import os
import socket
import select
sys.path.append(os.path.dirname(__file__))

from Flag import Flag

import serial

class Platform:
    def __init__(self, port, baud, flag: Flag):
        self.__recv_data = SerialPacket()
        self.__send_data = SerialPacket()
        self.flag = flag
        self.__platform_initializing_success = False

        try:
            self.__serial = serial.Serial(port, baud, timeout=0)
            try:
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.__socket.bind(('127.0.0.1', 7700))
                self.__platform_initializing_success = True
            except Exception as e:
                print("[Platform Intializing \tFail] \tCheck your Socket: ", e)
            print("[Platform Intializing \tOk  ]")
        except serial.serialutil.SerialException as e:
            print("[Platform Intializing \tFail] \tCheck your COMPORT: ", e)

    def main(self):
        if self.__platform_initializing_success:
            time.sleep(1)
            print("Start Platform \t- Success\n")
            self.__run()
        else:
            print("Start Platform \t- Fail: \tPlatform doesn't initialize succeessfully. Therefore, Platform will not run.")
        print("\t\t\t\t-->\tTerminate Platform")
    
    def __run(self):
        while not self.flag.system_stop:
            if self.flag.platform_stop:
                time.sleep(0.1)
            else:
                self.__send()
                self.__read()

                '''
                https://github.com/HongBeenKim/pams-skku/blob/master/thinkingo/car_platform.py에 있는 코드인데 이해를 아직 못해서 주석으로 남겨둠
                이후에, 이해 후 수정이 필요함.
                
                if not self.data.debug_flag and self.data.read_packet.aorm == SerialPacket.AORM_MANUAL:
                    self.data.reset_to_default()
                '''
        time.sleep(0.1)
        print("Terminating Platform")
        self.__socket.close()
        self.__serial.close()
    
    def __read(self):
        try:
            bytes_data, addr = self.__socket.recvfrom(37)
            self.decode_from_bytes(bytes_data)

        except Exception as e:
            print("car_platform RECEIVE ERROR: ", e)

    def __send(self):
        # self.__send_data.alive = self.__recv_data.alive
        try:
            self.__serial.write(self.__send_data.write_bytes())
        except Exception as e:
            print("car_platform SEND ERROR: ", e)

    def decode_from_bytes(self, data):
        len_header_and_tail = 5
        len_info = 4 * 8
        len_total = len_header_and_tail + len_info

        assert len(data) == len_total, \
            '[ERROR] cannot parse this data. Data length must be equal to {}. Data length = {}, Data passed = {}'.format(\
        len_total, len(data), data)

        format_string = '<ccffffffffccc'
        data_unpacked = struct.unpack(format_string, data)

        assert data_unpacked[0] == b'M', \
            '[ERROR] Error in the header, it must be M, but the value is = {}'.format(data_unpacked[0])
        assert data_unpacked[1] == b'O', \
            '[ERROR] Error in the header, it must be O, but the value is = {}'.format(data_unpacked[1])
        assert data_unpacked[-3] == b'R', \
            '[ERROR] Error in the header, it must be R, but the value is = {}'.format(data_unpacked[2])
        assert data_unpacked[-2] == b'A', \
            '[ERROR] Error in the header, it must be A, but the value is = {}'.format(data_unpacked[-2])
        assert data_unpacked[-1] == b'I', \
            '[ERROR] Error in the header, it must be I, but the value is = {}'.format(data_unpacked[-1])

        self.__recv_data = list(data_unpacked)[2:10]
        print(self.__recv_data)
    
    @property
    def recv_data(self):
        return self.__recv_data

    @property
    def send_data(self):
        return self.__send_data

"""
통신 코드를 위한 시리얼 패킷 API
https://github.com/Jueun-Park/HEVEN_AutonomousCar_2018/blob/master/src/serial_packet.py
김진웅 (2018-05)
패킷 세부 형식(byte array)은 플랫폼 안내 책자 참조
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import numpy as np
import struct


class SerialPacket(object):
    START_BYTES = [0x53, 0x54, 0x58]
    END_BYTES = [0x0D, 0x0A]
    AORM_MANUAL = 0x00
    AORM_AUTO = 0x01
    AORM_DEFAULT = AORM_AUTO
    ESTOP_OFF = 0x00
    ESTOP_ON = 0x01
    ESTOP_DEFAULT = ESTOP_OFF
    GEAR_FORWARD = 0x00
    GEAR_NEUTRAL = 0x01
    GEAR_BACKWARD = 0x02
    GEAR_DEFAULT = GEAR_FORWARD
    SPEED_MIN = 0
    STEER_MAXLEFT = -2000
    STEER_STRAIGHT = 0
    STEER_MAXRIGHT = 2000
    BRAKE_NOBRAKE = 1
    BRAKE_FULLBRAKE = 33
    BRAKE_DEFAULT = BRAKE_NOBRAKE
    BRAKE_MAXBRAKE = 200

    def __init__(self, data=None, start_bytes=START_BYTES,
                 aorm=AORM_DEFAULT, estop=ESTOP_DEFAULT, gear=GEAR_DEFAULT,
                 speed=0, steer=0, brake=BRAKE_DEFAULT,
                 enc=0, alive=0,
                 end_bytes=END_BYTES):
        if data is not None: self.read_bytes(data); return
        self.start_bytes = start_bytes
        self.aorm = aorm
        self.estop = estop
        self.gear = gear
        self.speed = speed
        self.steer = steer
        self.brake = brake
        self.enc = enc
        self.alive = alive
        self.end_bytes = end_bytes

    def __setattr__(self, attr, v):
        if attr == 'start_bytes': super().__setattr__(attr, np.array(v, np.uint8)); return
        if attr == 'aorm': super().__setattr__(attr, np.uint8(v)); return
        if attr == 'estop': super().__setattr__(attr, np.uint8(v)); return
        if attr == 'gear': super().__setattr__(attr, np.uint8(v)); return
        if attr == 'speed': super().__setattr__(attr, np.uint16(v)); return
        if attr == 'steer': super().__setattr__(attr, np.int16(v)); return
        if attr == 'brake': super().__setattr__(attr, np.uint8(v)); return
        if attr == 'enc': super().__setattr__(attr, np.int32(v)); return
        if attr == 'alive': super().__setattr__(attr, np.uint8(v)); return
        if attr == 'end_bytes': super().__setattr__(attr, np.array(v, np.uint8)); return
        super().__setattr__(attr, v)

    def default(self):
        self.start_bytes = SerialPacket.START_BYTES
        self.aorm = SerialPacket.AORM_DEFAULT
        self.estop = SerialPacket.ESTOP_DEFAULT
        self.gear = SerialPacket.GEAR_DEFAULT
        self.speed = SerialPacket.SPEED_MIN
        self.steer = SerialPacket.STEER_STRAIGHT
        self.brake = SerialPacket.BRAKE_DEFAULT
        self.enc = 0
        self.alive = 0
        self.end_bytes = SerialPacket.END_BYTES

    def get_attr(self, mode=None):
        if mode is None:
            return self.gear, self.speed, self.steer, self.brake
        if mode == 'a':
            return self.aorm, self.estop, self.gear, self.speed, self.steer, self.brake, self.enc, self.alive
        if mode == 'ra':
            return self.start_bytes, self.aorm, self.estop, self.gear, self.speed, self.steer, self.brake, self.enc, self.alive, self.end_bytes
        return 'wrong mode'

    def read_bytes(self, b):
        if len(b) == 0:
            return
        try:
            u = struct.unpack('<3sBBBHhBiB2s', b)
            # print(u)
        except Exception as e:
            print('[SerialPacket| READ ERROR:', b, e)
            print('-Set to default value]')
            self.default()
            return
        print(u)
        self.start_bytes = bytearray(u[0])
        self.aorm = u[1]
        self.estop = u[2]
        self.gear = u[3]
        self.speed = u[4]
        self.steer = u[5]
        self.brake = u[6]
        self.enc = u[7]
        self.alive = u[8]
        self.end_bytes = bytearray(u[9])

    def write_bytes(self):
        try:
            b = struct.pack('!3sBBBHhBB2s', bytes(self.start_bytes), self.aorm, self.estop, self.gear, self.speed,
                            self.steer, self.brake, self.alive, bytes(self.end_bytes))
        except:
            print('[SerialPacket| WRITE ERROR]')
            print('-Set to default value]')
            self.default()
            b = struct.pack('!3sBBBHhBB2s', bytes(self.start_bytes), self.aorm, self.estop, self.gear, self.speed,
                            self.steer, self.brake, self.alive, bytes(self.end_bytes))
        return b

    def verify(self):
        if (self.start_bytes != SerialPacket.START_BYTES).any(): return False
        if (self.end_bytes != SerialPacket.END_BYTES).any(): return False
        return True


if __name__ == '__main__':
    a = SerialPacket(bytearray.fromhex("53545800 00000000 00000100 00000000 0D0A"))
    a.read_bytes(bytearray.fromhex("53545800 00000000 00000100 00000000 0D0A"))
    a.default()
    print(a.start_bytes, a.end_bytes)
    print(str(a.write_bytes()))