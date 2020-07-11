import sys
import os
sys.path.append(os.path.dirname(__file__))

from CAM import CAM
from Flag import Flag
from GPS import GPS
from LiDAR import LiDAR
from Platform import Platform

import threading
import time

CAM0_PARMS = {"SOCKET_TYPE": 'JPG',
        "WIDTH": 640, # image width
        "HEIGHT": 480, # image height
        "FOV": 90, # Field of view
        "localIP": "127.0.0.1",
        "localPort": 1232,
        "Block_SIZE": int(65000),
        "X": 0.5, # meter
        "Y": 0,
        "Z": 1,
        "YAW": 0, # deg
        "PITCH": -10,
        "ROLL": 0}

CAM1_PARMS = {"SOCKET_TYPE": 'JPG',
        "WIDTH": 640, # image width
        "HEIGHT": 480, # image height
        "FOV": 90, # Field of view
        "localIP": "127.0.0.1",
        "localPort": 1234,
        "Block_SIZE": int(65000),
        "X": 0.5, # meter
        "Y": 0,
        "Z": 1.5,
        "YAW": 0, # deg
        "PITCH": -10,
        "ROLL": 0}
class Database:
    def __init__(self, gps=True, platform=True, cam=True, lidar=True):
        self.run_gps = gps
        self.run_platform = platform
        self.run_cam = cam
        self.run_lidar = lidar
        print("\nIntializing Database")
        print("──────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        self.flag = Flag()
        if gps:
            self.gps = GPS('COM2', 19200, flag=self.flag)
            self.__gps_thread = threading.Thread(target=self.gps.main)

        if platform:
            self.platform  = Platform('COM6', 115200, flag=self.flag)
            self.__platform_thread = threading.Thread(target=self.platform.main)

        if cam:
            self.main_cam = CAM(0, 'Main', flag=self.flag, params_cam=CAM0_PARMS)
            self.sub_cam = CAM(1, 'Sub', flag=self.flag, params_cam=CAM1_PARMS)
            self.__main_cam_thread = threading.Thread(target=self.main_cam.main)
            self.__sub_cam_thread = threading.Thread(target=self.sub_cam.main)

        if lidar:
            self.lidar = LiDAR('127.0.0.1', 7248, flag=self.flag)
            self.__lidar_thread = threading.Thread(target=self.lidar.main)

        print("──────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        print("Database is ready to run!")

    def start(self):
        print("\nStart to run Database...")
        print("──────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        if self.run_gps:
            self.__gps_thread.start()
            time.sleep(0.1)
        if self.run_platform:
            self.__platform_thread.start()
            time.sleep(0.1)
        if self.run_cam:
            self.__main_cam_thread.start()
            time.sleep(0.1)
            self.__sub_cam_thread.start()
            time.sleep(0.1)
        if self.run_lidar:
            self.__lidar_thread.start()
        time.sleep(1)
        print("──────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        print("Database is running!\n")
    
    def join(self):
        print("\nTerminating Database...")
        print("──────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        if self.run_gps:
            self.__gps_thread.join()
            time.sleep(0.1)
        if self.run_platform:
            self.__platform_thread.join()
            time.sleep(0.1)
        if self.run_cam:
            self.__main_cam_thread.join()
            time.sleep(0.1)
            self.__sub_cam_thread.join()
            time.sleep(0.1)
        if self.run_lidar:
            self.__lidar_thread.join()
        print("──────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        print("Database termination complete!")


