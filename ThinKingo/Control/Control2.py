import time
import numpy as np

import threading
import sys
import os

sys.path.append(os.path.dirname(__file__))

# For Test
# =====================================================================================================================
# 아래 값들을 바꿔서 실험해볼 수 있습니다.
CAR_SPEED = 150  # 차량의 기본 주행 속력 (km/h * 10)
KP = 0.5  # P gain
KD = 3  # D gain
DISTANCE_SQUARE = 9 # 타겟 점 선택 반경 (meter) 의 제곱
K_ADJUST = 0.4
# =====================================================================================================================


class Control2:
    def __init__(self, db):
        # class parameter

        self.db = db
        self.flag = db.flag
        self.__control_thread = threading.Thread(target=self.__main)
        #라인 변경중 여부
        self.line_flag = False
        #지나친 인덱스 갯수
        self.passing_idx = 0

        # --------------------------------------------------------------------

        # 제어 알고리즘에 값을 넘겨주기 위한 packet
        # https://github.com/x2ever/HEVEN-AutonomousCar-2019/wiki/Required-Values-for-Control-Algorithms 참고

        # --------------------------------------------------------------------

        # PID control
        # PD 제어 기반
        # P 제어는 각도 오차에 비례하는 값을, D 제어는 현재 오차 각도와 이전 오차 각도의 차이값을 이용합니다.

        self.prev_angle_error = 0  # PD 제어를 위해 이전 각도 오차 저장이 필요.
        self.prev_final_steer_angle = 0

        # --------------------------------------------------------------------

        # For parking mission
        self.parking_count = 0

        # For static obstacle mission
        self.index_for_obs = 0

    def __main(self):
        # =============================================================================================================
        # 경로 선택

        # track for test
        total_track = self.db.path.gps_path_test_for_Control

        # 본선 track
        #total_track = self.db.path.gps_2_track
        
        # 본선전에서는 1번-2번-1번 트랙
        obstacle_track = self.db.path.static_obs_2_1.copy()

        parking_track = None

        index = 0
        index_for_parking = 0
        
        # UTM 경로를 사용하지 않을거라면, 현재 파티션 부분을 주석처리
        # =============================================================================================================

        # 자율주행 알고리즘 시작
        while not self.flag.system_stop:
            mission_num = 8

            packet = [mission_num, None, None, None, None]
            #packet = self.db.mission_packet.copy()
            # mission_num = packet[0]
            '''# *********************************************
            # 기본주행과 주차 index
            packet[0] = 8
            mission_num = 0
            packet[1] = 3
            # *********************************************'''

            # 미션 탈출
            # =============================================================
            if mission_num is 8:
                # 주차 이후 다시 돌아왔다면, 미션 번호를 다시 0번으로
                if self.parking_count == 70000 and index_for_parking == 0:
                    mission_num = 0

            elif mission_num is 1:
                obstacle_size = len(self.db.path.static_obs_2_1) - 1
                # 마지막 인덱스에 도달했다면, 미션 번호를 다시 0번으로
                if self.index_for_obs == obstacle_size:
                    mission_num = 0
            # =============================================================          

            # 현재 차체 좌표 (meter 단위)

            gps_data = self.db.gps.data
            minute_lad = gps_data[1] % 100
            degree_lad = (gps_data[1] - minute_lad)/100
            latitude = degree_lad + minute_lad/60

            minute_lon = gps_data[3] % 100
            degree_lon = (gps_data[3] - minute_lon)/100
            longitude = degree_lon + minute_lon/60
            
            p_curr = [latitude* 110000, longitude * 88800]

            # 현재 차체 방향 (정북 0도)

            car_angle = self.db.imu.data[2] + 180

            # 현재 차체 데이터 호출 완료
            #print(gps_data, car_angle)
            # =======================================================================================================
            # 미션별 트랙 선택 알고리즘

            if mission_num is 8:  # 주차 미션의 경우
                if packet[1] is not None:  # 주차 트랙이 주어질 경우
                    parking_track = packet[1].copy()  # 주차 트랙 사용
                else:  # 주차 트랙이 주어지지 않을 경우
                    pass  # pass, total_track 사용

            elif mission_num is 1:
                obstacle_track = self.__static_obstacle(self.db.path.static_obs_2_1, self.db.path.static_obs_2_2, obstacle_track)
            
            #print(parking_track)

            # ======================================================================================================
            
            # 트랙에서 타겟 점 선택 알고리즘

            # 기본적으로 로컬 경로에서 index 넘어가는 것은 계속함
            distance = (p_curr[0] - total_track[index][0]) ** 2 + (p_curr[1] - total_track[index][1]) ** 2
            distance_detect = DISTANCE_SQUARE

            if distance < distance_detect:
                index += 1

            else:
                pass

            # ------------------------------------------------------------------------------------------------------
            
            # 미션별 index 넘어가기

            # 주차 미션
            if mission_num is 8:
                if parking_track is not None:  # parking_track 이 있다면
                    distance_park = (p_curr[0] - parking_track[index_for_parking][0]) ** 2 + (p_curr[1] - parking_track[index_for_parking][1]) ** 2
                    distance_detect = 3

                    if self.parking_count < 70000:  # 주차 정차 이전
                        if index_for_parking == len(parking_track) - 1:
                            pass
                        else:
                            if distance_park < distance_detect:
                                index_for_parking += 1
                            else:
                                pass

                    else:  # 주차 정차 이후
                        if index_for_parking == 0:
                            pass
                        else:
                            if (p_curr[0] - parking_track[index_for_parking-1][0]) ** 2 + (p_curr[1] - parking_track[index_for_parking-1][1]) ** 2 < distance_detect:
                                index_for_parking -= 1
                            else:
                                pass

                else:  # parking_track 이 없다면 원래 미션처럼
                    pass

            # 정적 장애물 미션
            elif mission_num is 1:

                distance_obs = (p_curr[0] - obstacle_track[self.index_for_obs][0]) ** 2 + (p_curr[1] - obstacle_track[self.index_for_obs][1]) ** 2
                distance_detect = 4

                if distance_obs < distance_detect :
                    self.index_for_obs += 1
                    if self.line_flag is True:
                        self.passing_idx += 1

                else:
                    pass

            # 그 외의 미션은 상관 없음          
            else:
                pass
            
            # index 선택 완료

            # =======================================================================================================

            # 타겟 점 선택
            p_targ = total_track[index]

            # 미션 별 트랙이 있을 경우, 각 트랙의 index 선택
            if mission_num is 8:
                if parking_track is not None:  # parking_track 이 있으면
                    p_targ = parking_track[index_for_parking]  # 타겟 점은 parking_track 에서 선택
                    packet[2] = len(parking_track) - 1  # 주차 알고리즘을 위한 데이터 저장
                    packet[3] = index_for_parking
                else:
                    pass
            
            elif mission_num is 1:
                if(self.passing_idx <= 5 and self.line_flag == True):
                    pass
                else:
                    self.line_flag = False
                    self.passing_idx = 0
                p_targ = obstacle_track[self.index_for_obs]  # 타겟 점은 obstacle_track 에서 선택

            else:  # 그 외의 미션에서는 상관 없음
                pass

            # 타겟 점 선택 완료

            # *********************************************************************************************************
            # 제어 알고리즘에 필요한 데이터 수신 완료
            # *********************************************************************************************************
            
            # 조향각 제어

            # path tracking
            curr_angle_error = self.__find_angle_error(car_angle, p_curr, p_targ, index)  # 현재 각도 오차를 구합니다.

            # 기어 설정, 만약 주차 미션의 경우 뒤로 갈 때 각도 오차를 다시 구함
            final_gear = 0x00

            if mission_num is 8:
                if self.parking_count == 70000:
                    if 180 >= curr_angle_error >= 90:
                        curr_angle_error = 180 - curr_angle_error
                        final_gear = 0x02

                    elif -90 >= curr_angle_error >= -180:
                        curr_angle_error = - (180 + curr_angle_error)
                        final_gear = 0x02

                    else:
                        final_gear = 0x02

                else:
                    final_gear = 0x00

            # PID control 으로 조향각 (degree) 을 구합니다.
            steer_angle = self.__calculate_pid(curr_angle_error, self.prev_angle_error, mission_num)

            # 조향각 결정
            # ---------------------------------------------------------------------------------------------------------
            # 주차 미션일 경우, 따로 조향각과 속력 및 브레이크 제어

            if mission_num is 8:
                speed = 50
                target_speed, steer_angle, final_brake = self.__parking_mission(packet, speed, steer_angle)

            # 그 외에는, 미션별 속력 및 브레이크 제어
            else:
                speed = CAR_SPEED
                target_speed, final_brake = self.__do_mission(packet, speed)

            # 속력 및 브레이크 최종 결정
            # ---------------------------------------------------------------------------------------------------------
            # 값 조정 (시리얼 패킷으로 보낼 값들 조정)

            # 조향각에 71을 곱합니다. (serial 통신을 위해)
            steer_angle_to_packet = steer_angle * 71

            # 만약 조향각이 2000/71도 보다 크거나, -2000/71도 보다 작다면, 값을 조정하면서 목표 속력을 줄입니다.
            final_steer_angle, final_speed = self.__constraint(steer_angle_to_packet, target_speed, mission_num)

            # 브레이크 값이 있다면, 속력을 0으로
            if final_brake > 0:
                final_speed = 0
            else:
                pass

            # 이전 조향각 feedback
            adjust = K_ADJUST
            final_steer_angle = adjust * self.prev_final_steer_angle + (1 - adjust) * final_steer_angle

            # 값 조정 완료
            # ---------------------------------------------------------------------------------------------------------
            # 통신부로 보내주기

            self.db.platform.send_data.speed = final_speed
            self.db.platform.send_data.steer = final_steer_angle
            self.db.platform.send_data.gear = final_gear
            self.db.platform.send_data.brake = final_brake

            print(f"final_steer_angle {final_steer_angle}, index {index}, index_for_parking {index_for_parking}, count {self.parking_count}")
            #print(f"final_brake {final_brake}, index {index}, distance_obs {distance_obs}")
            #print(f"self.line_flag{self.line_flag}, index_for_obs {self.index_for_obs}, obstacle {obstacle_track[0]}, distance {self.distance()}")
            # *********************************************************************************************************
            # 플랫폼으로 통신 완료
            # *********************************************************************************************************
            
            # 현재 각도 오차를 이전 각도 오차로 저장.
            self.prev_angle_error = curr_angle_error
            self.prev_final_steer_angle = final_steer_angle

            # Save current index
            self.db.now_idx = index
            
            # Save control data for monitoring
            self.db.control_data.p_curr = p_curr.copy()
            self.db.control_data.p_targ = p_targ.copy()
            self.db.control_data.ladlon = [latitude, longitude]
            self.db.control_data.car_angle = car_angle
            self.db.control_data.distance = distance
            self.db.control_data.final_speed = final_speed
            self.db.control_data.final_steer_angle = final_steer_angle
            self.db.control_data.final_gear = final_gear
            self.db.control_data.final_brake = final_brake
        
        print(f"현재 index는 {index}")

    def __find_angle_error(self, car_angle, position_curr, position_targ, index):  # 현재 차체의 각도, 현재 차의 위치, 선택한 타겟점의 위치
        targetdir_x = position_targ[1] - position_curr[1]  # 타겟 방향의 벡터 = 타겟 위치 - 현재 위치
        targetdir_y = position_targ[0] - position_curr[0]

        target_angle = np.arctan2(targetdir_y, targetdir_x) * 180 / np.pi

        # 각 변환
        target_angle = (450 - target_angle) % 360

        # 각도 오차 구하기
        angle_error = target_angle - car_angle          # target_angle 에서 car_angle 을 빼서 각도 오차를 구함
        while angle_error >= 180:
            angle_error -= 360                          # 각도 오차의 절댓값이 180보다 커지면 보정
        while angle_error <= -180:
            angle_error += 360
        # -180도 ~ 180도 사이의 angle_error 를 얻게 됨.

        #print(targetdir_x, targetdir_y, index)
        #print(f"car_angle {car_angle}, target_angle {target_angle}, angle_error {angle_error}, index {index}")
        return angle_error

    def __calculate_pid(self, current_angle_error, prev_angle_error, mission_num):
        if mission_num == 8 or mission_num == 1:
            k_p = 1.5
            k_d = 3
        else:
            k_p = KP
            k_d = KD

        angle_error = current_angle_error

        # p control
        proportional_term = k_p * angle_error

        # d control
        if prev_angle_error - angle_error >= 5 or prev_angle_error - angle_error <= - 5:
            derivative_term = 0  # 너무 차이가 크게 나는 값일 경우, 진동이 클것으로 판단되어 제외
        else:
            derivative_term = k_d * (angle_error - prev_angle_error)
        steer_angle = proportional_term + derivative_term

        return steer_angle

    def __constraint(self, steer_angle, speed, mission_num):  # 조향각이 너무 클 경우, 2000/71도로 조정하고 속력 감소
        if steer_angle >= 2000:
            steer_angle = 2000

        elif steer_angle <= -2000:
            steer_angle = -2000

        else:
            if mission_num == 8 or mission_num == 1:
                pass
            else:
                if steer_angle >= 400:
                    speed -= 50

                elif steer_angle <= -400:
                    speed -= 50

                else:
                    pass
            
        return steer_angle, speed

    def __do_mission(self, packet, target_speed):
        """:packet:
        packet 설명
        packet = [0, None, data1, data2, data3]
        [0] : 현재 모드 번호
        [1] : None
        [2] : data1
        [3] : data2
        [4] : data3

        :return:
        목표 속력과 브레이크 값을 return 합니다."""

        mode_num = packet[0]
        brake = 0

        if mode_num is 0 or None:
            if packet[4] is True:
                target_speed -= 50
            else:
                pass

        elif mode_num is 1:       # 정적 장애물
            target_speed -= 50

        elif mode_num is 2:       # 동적 장애물

            if packet[4] is True:
                target_speed -= 50

            # 동적 장애물 까지의 거리
            distance_from_obstacle = packet[2]

            if 500 <= distance_from_obstacle < 700:
                brake = 30

            elif 300 <= distance_from_obstacle < 500:
                brake = 50

            elif distance_from_obstacle < 300:
                brake = 70

        elif mode_num is 3:
            target_speed -= 30

        elif mode_num is 4:
            target_speed -= 30

        elif mode_num is 5:
            target_speed -= 30

        elif mode_num is 6:
            target_speed -= 30

            if packet[4] is True:
                target_speed -= 50

            if packet[3] is not None:  # 신호가 보인다면
                if packet[3] is True:  # 가도 되는 신호라면, 주행 계속
                    pass

                else:  # 가도 되는 신호가 아니라면, 정지선 앞에 멈춰야 함
                    if packet[2] is True:  # 멈춰야 하는 신호면
                        brake = 50

                    else:  # 아니면
                        pass

            else:  # 신호가 안보인다면, 그냥 주행 계속
                pass

        elif mode_num is 7:
            target_speed -= 30

            if packet[3] is not None:  # 신호가 보인다면
                if packet[3] is True:  # 가도 되는 신호라면, 주행 계속
                    pass

                else:  # 가도 되는 신호가 아니라면, 정지선 앞에 멈춰야 함
                    if packet[2] is True:  # 멈춰야 하는 신호면
                        brake = 50

                    else:  # 아니면
                        pass

            else:  # 신호가 안보인다면, 그냥 주행 계속
                pass

        return target_speed, brake

    def __parking_mission(self, packet, speed, steer):
        parking_track_length = packet[2]
        index = packet[3]

        final_speed = speed
        final_steer_angle = steer
        final_brake = 0

        if self.parking_count == 70000:
            pass

        elif index == parking_track_length:
            if self.parking_count < 30000:
                final_steer_angle = 0
                final_speed = 0
                final_brake = 70
            elif 30000 <= self.parking_count < 70000:
                final_steer_angle = 0
                final_speed = 0
                final_brake = 70

            self.parking_count += 1

        else:
            pass

        return final_speed, final_steer_angle, final_brake
    
    def __static_obstacle(self, obstacle1, obstacle2, obstacle):
        if self.distance()>350 :
            if obstacle == obstacle1 :
                return obstacle1
            elif obstacle == obstacle2 :
                return obstacle2

        elif self.line_flag == False :
            self.line_flag = True
            self.index_for_obs += 1
            # 트랙 바꾸기
            if obstacle == obstacle1 :
                return obstacle2
            elif obstacle == obstacle2 :
                return obstacle1

        else:
            if obstacle == obstacle1 :
                return obstacle1
            elif obstacle == obstacle2 :
                return obstacle2

    # -------------------------------------------------------------------------------------------------
    # threading
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
        print("Starting Control thread...")
        self.__control_thread.start()
        time.sleep(1)
        print("Control thread start!")

    def join(self):
        print("Terminating Control thread...")
        self.__control_thread.join()
        time.sleep(0.1)
        print("Control termination complete!")
