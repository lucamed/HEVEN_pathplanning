import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(__file__))

from SimulatorDatabase import Database

from Database_Status_Screen import DatabaseScreen
from GPS_Screen import GPSScreen
from Main_CAM_Screen import MainCAMScreen
from Sub_CAM_Screen import SubCAMScreen
from LiDAR_Cluster_Screen import LiDARClusterScreen
from Platform_Status_Screen import PlatformStatusScreen
from LiDAR_Target_Point_Screen import LiDARTargetPointScreen

class Monitor:
    def __init__(self, db: Database):
        self.db = db
        self.Database = DatabaseScreen(db = self.db)
        self.GPS = GPSScreen(db = self.db)
        self.MainCAM = MainCAMScreen(db = self.db)
        self.SubCAM = SubCAMScreen(db = self.db)
        self.LiDAR_C = LiDARClusterScreen(db = self.db)
        self.Platform = PlatformStatusScreen(db = self.db)
        self.LiDAR_TP = LiDARTargetPointScreen(db = self.db)
        '''
                                      1728
        ┌─────────────────────┬────────────────────┬─────────────────────┐
        │  DB & Sensor Status │                    │                     │
        │      576 x 306      │   MAIN CAM (YOLO)  │                     │
        ├─────────────────────┤     576 x 324      │                     │
        │                     ├────────────────────┤   Platform Status   │
        │                     │                    │      576 x 648      │
        │                     │   SUB CAM  (LANE)  │                     │ 972
        │     GPS Monitor     │     576 x 324      │                     │
        │      576 x 576      ├────────────────────┼─────────────────────┤
        │                     │                    │                     │
        │                     │   LiDAR (Cluster)  │ LiDAR (Target Point)│
        │                     │     576 x 324      │     576 x 324       │
        └─────────────────────┴────────────────────┴─────────────────────┘
        '''
        self.__img = np.zeros((972, 1728, 3), np.uint8)

    def update(self):
        # Left Screen
        self.__img[   0: 306,    0: 576, :] = self.Database.render()
        self.__img[ 306: 972,    0: 576, :] = self.GPS.render()

        # Middle Screen
        self.__img[   0: 324,  576:1152, :] = self.MainCAM.render()
        self.__img[ 324: 648,  576:1152, :] = self.SubCAM.render()
        self.__img[ 648: 972,  576:1152, :] = self.LiDAR_C.render()

        # Right Screen
        self.__img[   0: 648, 1152:1728, :] = self.Platform.render()
        self.__img[ 648: 972, 1152:1728, :] = self.LiDAR_TP.render()

    @property
    def img(self):
        # self.update()
        return self.__img