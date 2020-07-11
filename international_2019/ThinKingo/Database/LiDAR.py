#-*- coding:utf-8 -*-
import socket
import time
import copy
import sys
import os
sys.path.append(os.path.dirname(__file__))

from Flag import Flag

class LiDAR:
    def __init__(self, host, port, buff, flag: Flag):
        self.__data = None
        self.flag = flag
        self.__lidar_initializing_success = False
        self.__buff = buff

        INIT_MESG = chr(2) + 'sEN LMDscandata 1' + chr(3)

        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((host, port))
            self.__socket.send(str.encode(INIT_MESG))
            self.__lidar_initializing_success = True
            print("[LiDAR Intializing \tOk  ]")
        except Exception as e:
            print("[LiDAR Intializing \tFail] \tError occurred while opening the socket:", e)

    def main(self):
        if self.__lidar_initializing_success:
            print("Start LiDAR\t- Success\n")
            time.sleep(1)
            self.__read_lidar()
        else:
            print("Start LiDAR\t- Fail:\t\tLiDAR doesn't initialize succeessfully. Therefore, LiDAR will not run.")
        print("\t\t\t\t-->\tTerminate LiDAR")

    def __read_lidar(self):
        while not self.flag.system_stop:
            if self.flag.lidar_stop:
                time.sleep(0.1)
            else:
                data = str(self.__socket.recv(self.__buff))
                if data.__contains__('sEA'):
                    pass
                else:
                    try:
                        data = data.split(' ')[116:477]
                        temp_data = [1000000] * 361
                        for i in range(0, 361):
                            r = int(data[i], 16)
                            if r > 3:
                                temp_data[i] = r
                        self.__data = copy.deepcopy(temp_data)
                    except Exception as e:
                        print("[LiDAR Running \tError] \t Error occured while parsing data from LiDAR:", e)
        
        time.sleep(0.1)
        print("Terminating LiDAR")
        self.__socket.send(str.encode(chr(2) + 'sEN LMDscandata 0' + chr(3)))
        self.__socket.close()


    @property
    def data(self):
        return copy.deepcopy(self.__data)