import time
import numpy as np

import threading
import sys
import os

sys.path.append(os.path.dirname(__file__))

# For Test
# 아래 값들을 바꿔서 실험해볼 수 있습니다.
CAR_SPEED = 150  # 차량의 기본 주행 속력 (km/h * 10)
KP = 0.5  # P gain
KD = 0.3  # D gain
DISTANCE_SQUARE = 4  # 타겟 점 선택 반경 (meter) 의 * 제곱 *


class Control:
    def __init__(self, db):
        # class parameter

        self.db = db
        self.flag = db.flag
        self.__control_thread = threading.Thread(target=self.__main)

        # --------------------------------------------------------------------

        # 제어 알고리즘에 값을 넘겨주기 위한 packet
        # https://github.com/x2ever/HEVEN-AutonomousCar-2019/wiki/Required-Values-for-Control-Algorithms 참고

        # --------------------------------------------------------------------

        # 직진, 좌회전, 우회전, 횡단보도 미션
        # 정지선까지의 거리

        # 정지선에 들어가기 전, 속력을 서서히 낮춰야 함
        # 정지선과 평행하게 정지하도록 제어

        # --------------------------------------------------------------------

        # 스쿨존 미션
        # 스쿨존 안에 있는지 여부

        # --------------------------------------------------------------------

        # 주차 미션

        # --------------------------------------------------------------------

        # PID control
        # PD 제어 기반
        # P 제어는 각도 오차에 비례하는 값을, D 제어는 현재 오차 각도와 이전 오차 각도의 차이값을 이용합니다.

        self.prev_angle_error = 0  # PD 제어를 위해 이전 각도 오차 저장이 필요.
        self.prev_time = time.time()  # D 제어를 위해 주행 시간 저장이 필요. (second)

        # --------------------------------------------------------------------

        # For simulation
        self.initial_time = time.time()

        # For parking mission
        self.parking_count = 0

        # For real gps
        self.saved_data=[]

    def __main(self):
        # 예선 UTM 경로 파싱

        f = open("C:/Users/HEVEN/Desktop/K-City 예선전 경로 파일(UTM)_ver2.txt", 'r')
    
        gps_data = open("C:/Users/HEVEN/Desktop/test/gps_data.txt", 'w')
        yaw_data = open("C:/Users/HEVEN/Desktop/test/yaw_data.txt", 'w')
        lidar_data = open("C:/Users/HEVEN/Desktop/test/lidar_data.txt", 'w')

        total_track = []
        lines = f.readlines()

        cnt = 0

        for line in lines:
            temp = line.split('\t')
            # 점 간격 2배로 증가
            if cnt % 2 == 1:
                cnt += 1
                continue
            else:
                temp2 = [0, 0]
                temp2[0] = float(temp[0]) - 302459.942000
                temp2[1] = float(temp[1]) - 4122635.537000
                
                total_track.append(temp2)
                cnt += 1

        index = 0
        # 자율주행 알고리즘 시작
        while not self.flag.system_stop:

            # For simulation
            # 경과 시간 측정
            curr_time = time.time()
            # elapsed_time = curr_time - self.initial_time

            # 현재 차체와 타겟 점 사이의 거리를 이용해서 타겟 점 선택하는 알고리즘
            # 주차 모드 만드느라고 좀 흩어놨음

            current_position = [self.db.platform.recv_data[0], self.db.platform.recv_data[1]]  # 현재 차체 좌표
            self.saved_data.append(current_position)

            # real gps delay
            if len(self.saved_data) == 7000:
                p_curr = current_position
                self.saved_data = [current_position]
            
            else:
                p_curr = self.saved_data[0]

            # =========================================================================================================
            # UTM 경로에서 타겟 점 선택
            # 다음 index 점이 반경 내로 들어오면, index 를 증가시킴

            if ((p_curr[0]-total_track[index+1][0]) ** 2 + (p_curr[1]-total_track[index+1][1]) ** 2) < DISTANCE_SQUARE:
                index += 1
            else:
                pass

            p_targ = total_track[index]

            # UTM 경로에서 타겟 점 선택 완료
            # UTM 경로를 사용하지 않을 거라면, 현재 파티션 부분을 주석처리 하고 target 선택하는 알고리즘을 이 파티션 위에 추가
            # =========================================================================================================

            # 타겟 점 선택 완료
            '''# ---------------------------------------------------------------------------------------------------------
            # Simulation : 기본 주행 + 동적 장애물 모드 변경을 위한 코드
            # only for simulation

            dynamic_obstacle_point = [130.54289, 1209.5395]
            distance_from_dop = (p_curr[0] - dynamic_obstacle_point[0]) ** 2 + (
                    p_curr[1] - dynamic_obstacle_point[1]) ** 2
            if distance_from_dop < 225:
                mission_num = 2
            else:
                mission_num = 0

            # ---------------------------------------------------------------------------------------------------------'''
            mission_num = 0
            packet = [mission_num, None, None, None, None]
            if mission_num is 8:
                packet[2] = total_track
                packet[3] = index

            car_angle = self.__transform(self.db.platform.recv_data[5])  # 현재 차체 방향, from imu sensor - yaw

            # 제어 알고리즘에 필요한 데이터들 저장 완료
            # =========================================================================================================
            # 조향각 제어

            # path tracking
            curr_angle_error = self.__find_angle_error(car_angle, p_curr, p_targ)  # 현재 각도 오차를 구합니다.

            # For parking, 뒤로 가는 경우 각도 오차를 다시 구하기
            final_gear = 0x00
            if mission_num is 8:
                if self.parking_count == 30000:
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
            steer_angle = self.__calculate_pid(curr_angle_error, self.prev_angle_error, curr_time, self.prev_time)

            # 조향각 결정
            # ---------------------------------------------------------------------------------------------------------
            # =========================================================================================================
            # 주차 미션, 중간에 바꿔야 됨

            if mission_num is 8:
                speed = CAR_SPEED
                target_speed, steer_angle, final_brake = self.__parking(packet, speed, steer_angle)

            # =========================================================================================================
            # 미션별 속력 제어
            else:
                speed = CAR_SPEED  # 기본 주행 속력
                target_speed, final_brake = self.__do_mission(packet, speed)  # 목표 속력을 제어합니다.

            # 속력 최종 결정
            # ---------------------------------------------------------------------------------------------------------
            # 값 조정 (시리얼 패킷으로 보낼 값들 조정)

            # 조향각에 71을 곱합니다. (serial 통신을 위해)
            steer_angle_to_packet = steer_angle * 71

            # 만약 조향각이 어느 정도 크다면, -2000 ~ 2000 사이의 값으로 제한하고 목표 속력을 줄입니다.
            final_steer_angle, final_speed = self.__constraint(steer_angle_to_packet, target_speed)

            # 브레이크 값이 있다면, 속력을 0으로
            if final_brake > 0:
                final_speed = 0

            # 값 조정 완료
            # ---------------------------------------------------------------------------------------------------------
            # 통신부로 보내주기

            self.db.platform.send_data.speed = final_speed
            self.db.platform.send_data.steer = final_steer_angle
            self.db.platform.send_data.gear = final_gear
            self.db.platform.send_data.brake = final_brake

            # data 출력
            # ***********************************************************************
            gps_data_write = str(current_position) + '\n'
            gps_data.write(gps_data_write)

            yaw_data_write = str(car_angle) + '\n'
            yaw_data.write(yaw_data_write)

            lidar_data_write = str(self.db.lidar.data) + '\n'
            lidar_data.write(lidar_data_write)
            # ***********************************************************************

            # ==========================통신 완료=====================================
            # 보내준 이후, 현재 각도 오차를 이전 각도 오차로 저장.

            self.prev_angle_error = curr_angle_error

            # 측정 시간을 prev_time 에 저장

            self.prev_time = curr_time

        gps_data.close()
        yaw_data.close()
        lidar_data.close()

    # For simulation
    # UTM 좌표계로의 변환

    def __transform(self, enu_angle):
        # East = 0 을 기준으로 하는 ENU angle 을 local angle 로 변환
        angle = 90 - enu_angle
        if 0 > angle >= -90:
            angle += 360
        else:
            pass

        return angle

    # =======================================================================

    def __find_angle_error(self, car_angle, position_curr, position_targ):  # 현재 차체의 각도, 현재 차체의 위치, 선택한 타겟점의 위치

        targetdir_x = position_targ[0] - position_curr[0]  # 타겟 방향의 벡터 = 타겟 위치 - 현재 위치
        targetdir_y = position_targ[1] - position_curr[1]
        target_angle = 0
        if targetdir_x == 0 and targetdir_y > 0:
            target_angle = 0
        elif targetdir_x == 0 and targetdir_y < 0:
            target_angle = 180
        elif targetdir_x > 0 and targetdir_y == 0:
            target_angle = 90
        elif targetdir_x < 0 and targetdir_y == 0:
            target_angle = 270
        else:
            if targetdir_x > 0:
                target_angle = (90 - (np.arctan(targetdir_y / targetdir_x) * 180 / np.pi))
            elif targetdir_x < 0:
                target_angle = (270 - (np.arctan(targetdir_y / targetdir_x) * 180 / np.pi))
        # 0도 ~ 360도 사이의 값을 얻게 됨. (North = 0도)
        # 각도 오차로 변환

        angle_error = target_angle - car_angle  # target_angle 에서 car_angle 을 빼서 각도 오차를 구함
        if angle_error >= 180:
            angle_error -= 360  # 각도 오차의 절댓값이 180보다 커지면 보정
        if angle_error <= -180:
            angle_error += 360
        # -180도 ~ 180도 사이의 angle_error 를 얻게 됨.

        return angle_error

    def __calculate_pid(self, current_angle_error, prev_angle_error, current_time, prev_time):
        k_p = KP
        k_d = KD
        dt = current_time - prev_time  # (현재 시간 - 이전 시간)

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

    def __constraint(self, steer_angle, speed):  # 조향각이 너무 클 경우, 2000/71도로 조정하고 속력 감소
        if steer_angle >= 2000:
            steer_angle = 2000

        elif steer_angle <= -2000:
            steer_angle = -2000

        else:
            if steer_angle >= 400:
                speed -= 30

            elif steer_angle <= -400:
                speed -= 30

            else:
                pass

        return int(steer_angle), int(speed)

    def __do_mission(self, packet, target_speed):
        '''
        :packet:
        packet 설명
        packet = [0, [0,0] , data1, data2, data3]
        [0] : 현재 모드 번호
        [1] : 선택한 타겟 점의 좌표
        [2] : data1
        [3] : data2
        [4] : data3

        :return:
        목표 속력과 브레이크 값을 return 합니다.
        '''

        mode_num = packet[0]
        brake = 0

        if mode_num is 0 or None:

            if packet[4] is True:
                target_speed -= 50

            pass

        elif mode_num is 1:  # 정적 장애물

            target_speed -= 30

            pass

        elif mode_num is 2:  # 동적 장애물

            target_speed -= 30

            if packet[4] is True:
                target_speed -= 50

            lidar_raw_data = self.db.lidar.data

            # only for simulation
            for i, data in enumerate(lidar_raw_data):

                if data == 0:
                    lidar_raw_data[i] = 50000

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
            # 동적 장애물 까지의 거리 구함.

            if distance < 500:

                brake = 15

            elif distance < 300:

                brake = 30

            elif distance < 150:

                brake = 60

            pass

        elif mode_num is 3:

            target_speed -= 30

            pass

        elif mode_num is 4:

            target_speed -= 30

            pass

        elif mode_num is 5:

            target_speed -= 30

            pass

        elif mode_num is 6:

            target_speed -= 30

            if packet[4] is True:
                target_speed -= 50

            if packet[3] is not None:  # 좌회전 신호가 보인다면

                if packet[3] is True:

                    pass  # 좌회전 신호가 켜져있다면, 주행 계속

                else:

                    distance_stop = packet[2]  # 정지선까지의 거리

                    if distance_stop < 500:

                        brake = 15

                    elif distance_stop < 300:

                        brake = 30

                    elif distance_stop < 150:

                        brake = 60  # 좌회전 신호가 아니라면, 정지선 앞에 멈춰야 함

            else:  # 좌회전 신호가 안보인다면, 그냥 주행 계속

                pass

        elif mode_num is 7:

            target_speed -= 30

            if packet[3] is not None:  # 적색 신호가 보인다면

                if packet[3] is True:

                    distance_stop = packet[2]  # 정지선까지의 거리

                    if distance_stop < 500:

                        brake = 15

                    elif distance_stop < 300:

                        brake = 30

                    elif distance_stop < 150:

                        brake = 60

                    pass  # 적색 신호가 켜져있다면, 정지선 앞에 멈춰야 함

                else:

                    pass  # 적색 신호가 아니라면, 주행 계속

            else:  # 적색 신호가 안보인다면, 그냥 주행 계속

                pass

        elif mode_num is 8:

            pass

        return target_speed, brake

    # -------------------------------------------------------------------------------------------------

    def __parking(self, packet, speed, steer):
        total_track = packet[2]
        index = packet[3]

        final_speed = speed
        final_steer_angle = steer
        final_brake = 0

        if self.parking_count == 30000:

            pass

        elif index == len(total_track) - 1:

            final_steer_angle = 0
            final_brake = 30

            self.parking_count += 1

        else:

            pass

        return final_speed, final_steer_angle, final_brake

    # -------------------------------------------------------------------------------------------------
    # For threading
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
