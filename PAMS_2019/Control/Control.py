import time
import numpy as np

import sys
import os

from .Lane_tracking import lane_tracking

import cv2

sys.path.append(os.path.dirname(__file__))

# 주차 매크로를 위한 시간
TIME_1 = 2.5   # TIME_1 초 동안 조금 앞으로 가기
TIME_2 = 4.5   # TIME_2 초 동안 옆으로 움직이기
TIME_3 = 5   # TIME_3 초 동안 정지
TIME_4 = 6   # TIME_4 초 동안 옆으로 빠져나오기

class Control:
    def __init__(self, db, path):
        self.db = db
        self.path = path
        self.flag = db.flag

        # Flag
        self.uturn_mission_start_time = 0
        self.uturn_1_left_obstacle_detected = False
        self.uturn_2_left_obstacle_gone = False
        
        # Flag
        self.traffic_light_start_time = 0

        # Flag
        self.default_start_time = 0
        self.default_end = False

        # Flag
        self.target_mission_start_time = 0
        self.target_first_stop = False
        self.target_start = False
        self.target_second_stop = False
        self.target_second_stop_time = 0
        self.target_mission_end = False

        # Flag
        self.parking_macro_start_time = 0
        self.parking_mission_end = False
        
        # Flag
        self.crosswalk_stop_count_start = False
        self.crosswalk_mission_end = False
        self.crosswalk_count = 0

    def main(self, speed = 90, brake = 0, portion_offset = 0):
        # Receive datas from DB
        self.path.line.set_info()

        lane_current_angle = self.db.degree
        car_current_position = self.db.position
        car_current_position -= portion_offset

        # Lane tracking test
        target_angle = lane_tracking(lane_current_angle, car_current_position)  # in degree

        # Final speed
        final_speed = speed

        # Final gear
        final_gear = 0x00

        # Final brake
        final_brake = brake

        # Send datas to platform
        final_angle = target_angle * 71

        # Constraint
        
        if final_angle >= 2000:
            final_angle = 2000
            
        elif final_angle <= -2000:
            final_angle = -2000

        self.db.platform.send_data.steer = final_angle
        self.db.platform.send_data.speed = final_speed
        self.db.platform.send_data.gear = final_gear
        self.db.platform.send_data.brake = final_brake

    def traffic_light(self):

        self.db.platform.send_data.speed = 0
        self.db.platform.send_data.steer = 0
        self.db.platform.send_data.gear = 0x00
        self.db.platform.send_data.brake = 60

    def narrow(self, max_distance, target_angle):

        target_angle = (90 - target_angle)*(71) # Serial 통신 단위
        
        if max_distance <= 200:
            speed = 40
        else:
            speed = 40
            
        # Constraint
        if target_angle >= 2000:
            target_angle = 2000
        elif target_angle <= -2000:
            target_angle = -2000
        
        self.db.platform.send_data.speed = speed
        self.db.platform.send_data.steer = target_angle
        self.db.platform.send_data.gear = 0x00
        self.db.platform.send_data.brake = 0

    def uturn_macro(self):
        # Flag
        elapsed_time = time.time() - self.uturn_mission_start_time

        if elapsed_time < 7:
            pass

        else:
            if self.uturn_1_left_obstacle_detected is False and self.left_wall_distance() <= 180:
                self.uturn_1_left_obstacle_detected = True
                cv2.destroyAllWindows()

            elif self.uturn_1_left_obstacle_detected is True and self.left_wall_distance() >= 300:
                self.uturn_2_left_obstacle_gone = True

            else:
                pass

        # Algorithm
        if self.uturn_1_left_obstacle_detected is False:
            # 0번 상황 (협로에서 빠져나온 직후)

            self.main(speed = 70, portion_offset = 0.3) # 차량 정렬

        else:
            if self.uturn_2_left_obstacle_gone is False:
                # 1번 상황 (왼쪽 벽이 사라지기 전까지)
                self.db.platform.send_data.speed = 50
                self.db.platform.send_data.steer = 0
                self.db.platform.send_data.gear = 0x00
                self.db.platform.send_data.brake = 0
                
            else:
                # 2번 상황 (유턴 매크로 시작)
                self.db.platform.send_data.speed = 50
                self.db.platform.send_data.steer = -2000
                self.db.platform.send_data.gear = 0x00
                self.db.platform.send_data.brake = 0

        print(self.uturn_1_left_obstacle_detected, self.uturn_2_left_obstacle_gone, self.db.lidar.data[90] / 10)
        
    def left_wall_distance(self):

        lidar_raw_data = self.db.lidar.data
        minimum_distance = lidar_raw_data[300] / 10 # cm
        min_theta = 300 # 차량 좌측으로부터 30도 (360 - 30*2 = 300)

        for theta in range(300, 360):
            if (minimum_distance > lidar_raw_data[theta] / 10): # 0도 ~ 30도 에서, 최솟값보다 더 작은 거리가 있다면

                minimum_distance = lidar_raw_data[theta] / 10   # 최솟값 갱신

                min_theta = theta   # 각도 갱신

        min_theta = (360-min_theta)/2   # 0도~30도 사이의 값으로 Mapping

        distance = minimum_distance * np.cos(min_theta * np.pi / 180)   # return (cm)

        return distance

    def target_car(self):
        # Flag
        elapsed_time = time.time() - self.target_mission_start_time

        if elapsed_time < 3:
            pass

        else:
            if self.target_first_stop is False and self.distance() < 300:
                self.target_first_stop = True
            
            elif self.target_first_stop is True and self.distance() > 450:
                self.target_start = True
            
            elif self.target_start is True and self.target_second_stop is False and self.distance() < 300:
                self.target_second_stop = True
                self.target_second_stop_time = time.time()

            else:
                pass

        # Algorithm

        if time.time() - self.target_mission_start_time < 1:
            self.db.platform.send_data.speed = 0
            self.db.platform.send_data.brake = 20
            self.db.platform.send_data.steer = -2000
            self.db.platform.send_data.gear = 0x00

        else:
            if self.target_first_stop is False:
                # 0번 상황 (타겟차 미션에 들어간 직후)
                print(f"distance: ", self.distance())
                self.main(speed=50, brake=0, portion_offset=-0.2) # 차량 정렬하며 움직임
            
            else:
                if self.target_start is False:
                    # 1번 상황 (차량이 멈춰있다는 것을 판단한 이후)
                    
                    self.main(speed=0, brake=60, portion_offset=-0.2)
                
                else:
                    if self.target_second_stop is False:
                    # 2번 상황 (차량이 다시 출발했다는 것을 확인)
                    
                        if self.distance() > 400:   # 차량이 너무 멀면, 빠르게
                            self.main(speed=80)

                        elif 300 < self.distance() <= 400:  # 차량이 어느 정도 가까워지면, 멈출 준비
                            self.main(speed=0, brake=40)
                        
                        else:
                            self.main(speed=0, brake=60)

                    else:
                        # 3번 상황 (차량이 두 번째로 멈췄다는 것을 판단)

                        elapsed_time = time.time() - self.target_second_stop_time
                        print(elapsed_time)
                        if elapsed_time < 4:
                            self.db.platform.send_data.speed = 0
                            self.db.platform.send_data.steer = 0
                            self.db.platform.send_data.gear = 0x00
                            self.db.platform.send_data.brake = 80

                        elif 4 <= elapsed_time < 7.5:
                            self.db.platform.send_data.speed = 90
                            self.db.platform.send_data.steer = -2000
                            self.db.platform.send_data.gear = 0x00
                            self.db.platform.send_data.brake = 0

                        elif 7.5 <= elapsed_time < 9:
                            self.db.platform.send_data.speed = 90
                            self.db.platform.send_data.steer = 0
                            self.db.platform.send_data.gear = 0x00
                            self.db.platform.send_data.brake = 0

                        elif 9 <= elapsed_time < 11:
                            self.db.platform.send_data.speed = 90
                            self.db.platform.send_data.steer = 1500
                            self.db.platform.send_data.gear = 0x00
                            self.db.platform.send_data.brake = 0

                        else:
                        
                            self.target_mission_end = True

        print(f"1st_stop : {self.target_first_stop}, start : {self.target_start}, 2nd_stop : {self.target_second_stop}, end : {self.target_mission_end}")

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

    def parking_macro(self):

        elapsed_time = time.time() - self.parking_macro_start_time

        print(elapsed_time)
        # 주차 매크로의 시작 부분 - 주차선이 인식된 직후부터 parameter 조정 필요.

        if elapsed_time < TIME_1:    # 조금 앞으로 가기
            self.db.platform.send_data.speed = 30
            self.db.platform.send_data.steer = 0
            self.db.platform.send_data.gear = 0x00
            self.db.platform.send_data.brake = 0
        
        elif TIME_1 <= elapsed_time < TIME_1 + TIME_2:    # 옆으로 움직여 주차
            self.db.platform.send_data.speed = 40
            self.db.platform.send_data.steer = 1500
            self.db.platform.send_data.gear = 0x00
            self.db.platform.send_data.brake = 0

        elif TIME_1 + TIME_2 <= elapsed_time < TIME_1 + TIME_2 + TIME_3:   # 정지
            self.db.platform.send_data.speed = 0
            self.db.platform.send_data.steer = 0
            self.db.platform.send_data.gear = 0x00
            self.db.platform.send_data.brake = 60
        
        elif TIME_1 + TIME_2 + TIME_3 <= elapsed_time < TIME_1 + TIME_2 + TIME_3 + TIME_4:   # 뒤로 나오기
            self.db.platform.send_data.speed = 90
            self.db.platform.send_data.steer = 1400
            self.db.platform.send_data.gear = 0x02
            self.db.platform.send_data.brake = 0

        else:    # 주차 미션 탈출
            self.db.platform.send_data.speed = 0
            self.db.platform.send_data.steer = 0
            self.db.platform.send_data.gear = 0x00
            self.db.platform.send_data.brake = 30

            self.parking_mission_end = True

    def crosswalk(self, if_stop_line = False):
        # Flag
        if self.right_sign_distance() < 220 and self.crosswalk_stop_count_start is False:
            self.crosswalk_stop_count_start = True
            self.crosswalk_count = time.time()

        else:
            pass

        if self.crosswalk_stop_count_start is False:
            # 0번 상황 (멈추기 전)
            self.main(speed=60)
            print(self.right_sign_distance())
        else:
            # 1번 상황 (멈추기를 시작한 후)
            elapsed_time = time.time() - self.crosswalk_count
            print(elapsed_time)
            if elapsed_time < 6:
                self.db.platform.send_data.speed = 0
                self.db.platform.send_data.steer = 0
                self.db.platform.send_data.gear = 0x00
                self.db.platform.send_data.brake = 70

            elif 6 <= elapsed_time < 15:
                self.db.platform.send_data.speed = 70
                self.db.platform.send_data.steer = 0
                self.db.platform.send_data.gear = 0x00
                self.db.platform.send_data.brake = 0    

            else:
                self.db.platform.send_data.speed = 0
                self.db.platform.send_data.steer = 0
                self.db.platform.send_data.gear = 0x00
                self.db.platform.send_data.brake = 60    

        '''if if_stop_line is False:
            self.main(speed = 70)
        
        else:
            cv2.destroyAllWindows()
            print("정지선 인식")

            crosswalk_stop_time = time.time()                          # 시간 카운팅

            while True:
                elapsed_time = time.time() - crosswalk_stop_time       # 경과 시간

                print(elapsed_time)

                if elapsed_time < 7:                                        # 5초간 정지
                    
                    self.db.platform.send_data.speed = 0
                    self.db.platform.send_data.steer = 0
                    self.db.platform.send_data.gear = 0x00
                    self.db.platform.send_data.brake = 80
                
                elif 7 <= elapsed_time < 17:                                                       # 출발
                    self.db.platform.send_data.speed = 100
                    self.db.platform.send_data.steer = 0
                    self.db.platform.send_data.gear = 0x00
                    self.db.platform.send_data.brake = 0

                else:
                    self.crosswalk_mission_end = True
                    break

                time.sleep(0.1)'''

    def right_sign_distance(self):

        lidar_raw_data = self.db.lidar.data
        minimum_distance = lidar_raw_data[70] / 10 # cm
        min_theta = 70 # 차량 좌측으로부터 35도

        for theta in range(70, 110):
            if (minimum_distance > lidar_raw_data[theta] / 10): # 0도 ~ 30도 에서, 최솟값보다 더 작은 거리가 있다면

                minimum_distance = lidar_raw_data[theta] / 10   # 최솟값 갱신

                min_theta = theta   # 각도 갱신

        min_theta = (min_theta)/2   # 0도~30도 사이의 값으로 Mapping

        distance = minimum_distance * np.sin(min_theta * np.pi / 180)   # return (cm)

        return distance