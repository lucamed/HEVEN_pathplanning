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
sys.path.append(os.path.dirname(__file__))

import time
import numpy as np
from YOLO import get_traffic_buffer
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
        
    def __main(self):
        if(self.num == 1):
            while not self.flag.system_stop:
                idx = self.db.now_idx
                
                if(idx>=211 and idx<=260): #1
                    self.__static_obstacle()
                if(idx>=581 and idx<=660): #2
                    self.__dynamic_obstacle()
                if((idx>=487 and idx<=580) or (idx>=704 and idx<=779)): #6
                    self.__signal_straight()
                if((idx>=411 and idx<=486) or (idx>=780 and idx<=870)): #7
                    self.__static_obstacle()
                else:
                    self.__path_tracking()
                    
        if(self.num == 2):
            while not self.flag.system_stop:
                print(0)
                
        ############### MISSON ###############

    ## 0. 직선 주행(기본 주행)
    def __path_tracking(self):
        self.make_path=False
        self.packet = [0, None, None, None, None]
        #True일 경우 빨강
        self.packet[4] = self.lane.get_floor_color(self.db.main_cam.data)
        self.db.mission_packet = self.packet

    ## 1. 정적 장애물 미션
    def __static_obstacle(self):
        '''
        if(self.make_path==False):
            self.packet = [1, None, None, None, None]
            #경로 생성하기, path_planning에 미션넘버와 db 파라미터 파싱
            path_planning = Planning(1,self.db)
            goal = (400,700,np.pi/2)#temp
            path_planning.make_path(goal, left = True, right = True, lidar = True)
            #path_plannin에서 path 가져오기
            self.packet[1] = path_planning.path
            self.db.mission_packet = self.packet
            self.make_path = True
        else:
            return
        '''
        self.packet = [1, None, None, None, None]
        
    ## 2. 동적 장애물 미션
    def __dynamic_obstacle(self):
        self.make_path=False
        self.packet = [2, None, None, None, None]
        self.packet[2] = self.distance()
        self.packet[4] = self.lane.get_floor_color(self.db.main_cam.data)
        self.db.mission_packet = self.packet
        
    ## 3. 비신호 직진 미션
    def __non_signal_straight(self):
        self.make_path=False
        self.packet = [3, None, None, None, None]
        self.db.mission_packet = self.packet

    ## 4. 비신호 좌회전 미션
    def __non_signal_left(self):
        self.make_path=False
        self.packet = [4, None, None, None, None]
        self.db.mission_packet = self.packet

    ## 5. 비신호 우회전 미션
    def __non_signal_right(self):
        self.make_path=False
        self.packet = [5, None, None, None, None]
        self.db.mission_packet = self.packet

    ## 6. 신호 좌회전 미션
    def __signal_left(self):
        self.make_path=False
        self.db.mission_packet[3]=1
        self.packet[0] = 6
        self.stop = False
        self.db.mission_packet[3] = 1
        while not self.stop: #정지선을 인식할 때 까지 전진
            temp_img = make_binary(self.db.main_cam.data)
            self.packet[2] = self.lane.get_stop_line(temp_img)
            
        light = self.get_light()
        if(light != 'arrow'): # 좌회전신호 판단 >> 주행 가능: 1, 멈춤: 0
            self.db.mission_packet[3] = 0
            while light != 'arrow':
                light = self.get_light()
                
        self.db.mission_packet[3]=1

    ## 7. 신호 직진 미션
    def __signal_straight(self):
        self.make_path=False
        self.db.mission_packet[3]=1
        self.packet[0] = 7
        self.stop = False
        self.db.mission_packet[3] = 1
        while not self.stop: #정지선을 인식할 때 까지 전진
            temp_img = make_binary(self.db.main_cam.data)
            self.stop = self.lane.get_stop_line(temp_img)
        
        light = self.get_light()
        if(light != 'green'): # 적색 신호 판단 >> 주행 가능: 1, 멈춤: 0
            self.db.mission_packet[3] = 0
            while light != 'green':
                light = self.get_light()
                
        self.db.mission_packet[3]=1

    ## 8. 주차 미션
    def __parking(self):
        if(self.make_path==False):
            temp_img = self.db.main_cam.data
            path_planning = Planning(0,self.db)
            self.packet[0]=8
            re1, re2, goal = parking(temp_img)
            if(goal == 0):
                self.packet[1] = None
            else:
                path_planning.make_path(goal, left = False, right = False, lidar = False)
                #self.packet[1] = path_planning.path
                self.packet[1] = goal
                self.make_path = True
        self.db.mission_packet = self.packet
        
    #####################################
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
    
    #신호등 색 반환
    def get_light(self):
        buffer = get_traffic_buffer()
        if(len(buffer)==0):
            return None
        buffer_0 = buffer[0]
        for i in buffer:
            if(i != buffer_0):
                return None
        return buffer_0

    def start(self):
        print("Starting Path_plan thread...")
        self.__path_thread.start()
        time.sleep(1)
        print("Path_plan thread start!")

    def join(self):
        print("Terminating Path_plan thread...")
        self.__path_thread.join()
        time.sleep(0.1)
        print("Path_plan termination complete!")
