import cv2
import numpy as np
import sys
import os
import time
import threading
sys.path.append(os.path.dirname(__file__))

from Database import Database

from Database_Status_Screen import DatabaseScreen
from GPS_Screen import GPSScreen
from Main_CAM_Screen import MainCAMScreen
from Sub_CAM_Screen import SubCAMScreen
from LiDAR_Cluster_Screen import LiDARClusterScreen
from Platform_Status_Screen import PlatformStatusScreen
from LiDAR_Target_Point_Screen import LiDARTargetPointScreen

class Monitor:
    def __init__(self, db: Database):
        time.sleep(0.1)
        print("\n[Monitor] Intializing Monitor", end='\r')
        self.db = db
        self.Database = DatabaseScreen(height=306, width=576, db = self.db)
        self.GPS = GPSScreen(height=576, width=576, db = self.db)
        self.MainCAM = MainCAMScreen(height=324, width=576, db = self.db)
        self.SubCAM = SubCAMScreen(height=324, width=576, db = self.db)
        self.LiDAR_C = LiDARClusterScreen(height=324, width=576, db = self.db)
        self.Platform = PlatformStatusScreen(height=648, width=576, db = self.db)
        self.LiDAR_TP = LiDARTargetPointScreen(height=324, width=576, db = self.db)

        self.__moniter_thread = threading.Thread(target=self.__main)

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
        print("[Monitor] Intializing Monitor - Done", end="\n")

    def update(self):
        # Left Screen
        #self.__img[   0: 306,    0: 576, :] = self.Database.render()
        #self.__img[ 306: 972,    0: 576, :] = self.GPS.render()

        # Middle Screen
        #self.__img[   0: 324,  576:1152, :] = self.MainCAM.render()
        #self.__img[ 324: 648,  576:1152, :] = self.SubCAM.render()
        self.__img[ 648: 972,  576:1152, :] = self.LiDAR_C.render()

        # Right Screen
        #self.__img[   0: 648, 1152:1728, :] = self.Platform.render()
        #self.__img[ 648: 972, 1152:1728, :] = self.LiDAR_TP.render()

    def __main(self):
        animation = 0 # 0~ 2999
        print("                                                      ", end="\r") # Cleenup
        while True:
            if self.db.flag.system_stop:
                break
            else:
                try:
                    animation += 1
                    animation %= 3
                    print("\r[Monitor] Running" + "." * (animation // 1 + 1) + " " * (2 - animation // 1), end="")
                    self.update()
                    cv2.imshow("Monitor", cv2.resize(self.__img, (1280, 720)))
                    if ord("q") == cv2.waitKey(1):
                        print("\r[Monitor] Running" + "." * (animation // 1 + 1) + " " * (2 - animation // 1) + " - Closed")
                        break
                    time.sleep(0.5)
                except Exception as e:
                    print(e)

    def start(self):
        print("[Monitor] Start")
        self.__moniter_thread.start()
    
    def join(self):
        time.sleep(0.5)
        print("\n[Monitor] Terminating Monitor", end="\r")
        self.__moniter_thread.join()
        print("[Monitor] Terminating Monitor - Done")

    @property
    def img(self):
        # self.update()
        return self.__img