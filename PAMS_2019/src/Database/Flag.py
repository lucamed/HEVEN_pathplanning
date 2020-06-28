import sys
import os
sys.path.append(os.path.dirname(__file__))

class Flag:
    def __init__(self):
        self.system_stop = False
        self.platform_stop = False
        self.gps_stop = False
        self.imu_stop = False
        self.lidar_stop = False
        self.cam_stop = False
        self.yolo_stop = False
