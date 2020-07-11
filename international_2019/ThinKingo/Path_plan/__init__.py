'''
#################### PATH PLAN TEAM ####################

## ABOUT
- 각 미션 별로 제어팀에게 경로 정보가 담긴 packet을 넘겨줌

#https://github.com/x2ever/HEVEN-AutonomousCar-2019/wiki/Required-Values-for-Control-Algorithms
#제어팀 wiki 참조 

# +---+-------- packet[5] ----------+
# | 0 | mission number              |
# +---+-----------------------------+ 
# | 1 | coordinates of the targets  |
# +---+-----------------------------+
# | 2 | (depends on mission)        |
# +---+-----------------------------+
# | 3 | (depends on mission)        |
# +---+-----------------------------+
# | 4 | is school zone?             |
# +---+-----------------------------+


## INPUT & OUTPUT
- input: pathplan.py에서 표지판에 따른 YOLO 값 >> mission = Mission(1), mission.getpath()
- output: 각 미션 별 packet

'''

import threading
import sys
import os
import cv2
sys.path.append(os.path.dirname(__file__))

import time
import numpy as np
from _yolo.threading_yolo import YOLO
from Lane_Detection import Lane_Detection
from Planning import Planning
from util import make_binary
from Parking import parking

class Path_plan:
    def __init__(self, db, num):
        self.num = num
        self.db = db
        self.flag = db.flag
        self.lane = Lane_Detection()
        self.packet = [0, None, None, None, None]
        self.__path_thread = threading.Thread(target=self.__main)
        #path가 이미 만들어져 있다면 True 아니면 Fasle
        self.make_path = False
        #정지신호
        self.stop = False
        self.yolo = YOLO(db=db)
        self.idx = 0
        
    def __main(self):
        #본선     
        if(self.num == 2):
            while not self.flag.system_stop:   
                if(self.idx>=655 and self.idx<=765): #1
                    self.__static_obstacle()
                elif((self.idx>=407 and self.idx<=430) or (self.idx>=986 and self.idx<=1025)
                    or (self.idx>=1145 and  self.idx<=1170)): #6
                    self.__signal_straight()
                elif((self.idx>=496 and self.idx<=530) or (self.idx>=766 and self.idx<=805) or 
                   (self.idx>=1490 and self.idx<=1530) or (self.idx>=1721 and self.idx<=1770) or
                   (self.idx>=1830 and self.idx<=1875)): #7
                    self.__static_obstacle()
                elif(self.idx >= 86 and self.idx<=120):#8
                    self.__parking()
                else:
                    self.__path_tracking()
                
        ############### MISSON ###############

    ## 0. 직선 주행(기본 주행)
    def __path_tracking(self):
        self.packet = [0, None, None, None, None]
        #True일 경우 빨강
        #self.packet[4] = self.lane.get_floor_color(self.db.sub_cam.data)
        #print('now default')

    ## 1. 정적 장애물 미션
    def __static_obstacle(self):
        self.packet = [1, None, None, None, None]
        
    ## 2. 동적 장애물 미션
    def __dynamic_obstacle(self):
        self.packet = [2, None, None, None, None]
        self.packet[2] = self.distance()
        self.packet[4] = self.lane.get_floor_color(self.db.sub_cam.data)
        
    ## 3. 비신호 직진 미션
    def __non_signal_straight(self):
        self.make_path = False
        self.packet = [3, None, None, None, None]

    ## 4. 비신호 좌회전 미션
    def __non_signal_left(self):
        self.make_path=False
        self.packet = [4, None, None, None, None]

    ## 5. 비신호 우회전 미션
    def __non_signal_right(self):
        self.make_path=False
        self.packet = [5, None, None, None, None]

    ## 6. 신호 좌회전 미션
    def __signal_left(self):
        self.packet[0] = 6
        self.packet[2] = False
        self.packet[3] = True

        while self.packet[2] != True: #정지선을 인식할 때 까지 전진
            time.sleep(0.01)
            temp_img = make_binary(self.db.sub_cam.data, (800, 600))
            self.packet[2] = self.lane.get_stop_line(temp_img)
            #print(self.packet[2])
           
        cv2.destroyAllWindows() 
        light = self.yolo.check_lights()
        if(light == 'red'): # 좌회전신호 판단 >> 주행 가능: 1, 멈춤: 0
            self.packet[3] = False
            while light == 'red':
                light = self.yolo.check_lights()
                time.sleep(0.01)
                
        self.packet[3]=True

    ## 7. 신호 직진 미션
    def __signal_straight(self):
        self.packet[0] = 7
        self.packet[2] = False
        self.packet[3] = True

        while self.packet[2] != True:  #정지선을 인식할 때 까지 전진
            time.sleep(0.01)
            temp_img = make_binary(self.db.sub_cam.data, (800, 600))
            self.packet[2] = self.lane.get_stop_line(temp_img)

        cv2.destroyAllWindows()
        light = self.yolo.check_lights()
        if(light != 'green'): # 적색 신호 판단 >> 주행 가능: 1, 멈춤: 0
            self.packet[3] = False
            while light != 'green':
                light = self.yolo.check_lights()
                time.sleep(0.01)
                
        self.packet[3]=True

    ## 8. 주차 미션
    def __parking(self):
        self.packet[0] = 8
        self.packet[1] = None

        if(self.make_path == False):
            if self.idx >= 86 and self.idx<=92 :
                if parking(self.db.sub_cam.data,[0,0,0,0,0]) == 1:
                    cv2.destroyAllWindows()
                    self.packet[1] = 1
                    self.make_path = True

            elif self.idx >= 93 and self.idx<=98 :
                if parking(self.db.sub_cam.data,[0,0,0,0,0]) == 1:
                    cv2.destroyAllWindows()
                    self.packet[1] = 2
                    self.make_path = True

            elif self.idx >= 99 and self.idx<=103 :
                if parking(self.db.sub_cam.data,[0,0,0,0,0]) == 1:
                    cv2.destroyAllWindows()
                    self.packet[1] = 3
                    self.make_path = True

            elif self.idx >= 104 and self.idx<=110 :
                if parking(self.db.sub_cam.data,[0,0,0,0,0]) == 1:
                    cv2.destroyAllWindows()
                    self.packet[1] = 4
                    self.make_path = True

            elif self.idx >= 111 and self.idx<=115 :
                if parking(self.db.sub_cam.data,[0,0,0,0,0]) == 1:
                    cv2.destroyAllWindows()
                    self.packet[1] = 5
                    self.make_path = True

            elif self.idx >= 116 and self.idx<=120 :
                if parking(self.db.sub_cam.data,[0,0,0,0,0]) == 1:
                    cv2.destroyAllWindows()
                    self.packet[1] = 6
                    self.make_path = True
        
    #####################################
    def set_mission_idx(self, idx):
        self.idx = idx
    
    def get_mission_packet(self):
        return self.packet
    
    def distance(self):
        lidar_raw_data = self.db.lidar.data
        minimum_distance = lidar_raw_data[180] / 10
        min_theta = 180
        car_width = 120  # cm

        for theta in range(90, 270):
            if (minimum_distance > lidar_raw_data[theta] / 10) and \
                ((lidar_raw_data[theta] / 10) * abs(np.cos(theta * np.pi / 360)) < (
                    car_width / 2)):  # 2 Conditions

                minimum_distance = lidar_raw_data[theta] / 10

                min_theta = theta

        distance = minimum_distance * np.sin(min_theta * np.pi / 360)
        return distance
    

    def start(self):
        print("Starting Path_plan thread...")
        self.__path_thread.start()
        time.sleep(1)
        print("Path_plan thread start!")
        self.yolo.start()

    def join(self):
        print("Terminating Path_plan thread...")
        self.__path_thread.join()
        time.sleep(0.1)
        print("Path_plan termination complete!")
        self.yolo.join()
