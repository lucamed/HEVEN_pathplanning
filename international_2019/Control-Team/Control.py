import time
import numpy as np

import threading
import sys
import os

sys.path.append(os.path.dirname(__file__))

# For Test
# =====================================================================================================================
# 아래 값들을 바꿔서 실험해볼 수 있습니다.
CAR_SPEED = 70  # 차량의 기본 주행 속력 (km/h * 10)
KP = 0.1  # P gain
KD = 0.3  # D gain
DISTANCE_SQUARE = 0  # 타겟 점 선택 반경 (meter) 의 * 제곱 *
# =====================================================================================================================


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

        self.curr_target_list = []  # target list 를 저장해야 함.

        # --------------------------------------------------------------------

        # For parking mission
        self.parking_count = 0
        self.prev_position = [0, 0]
        self.prev_imu = 0
        self.car_angle = 0
        self.p_curr = [0, 0]

    def __main(self):

        # =============================================================================================================
        # 카메라 차선 검출이 안될 시, 예선 UTM 경로로 테스트하기 위해
        # 예선 UTM 경로 파싱

        # f = open("C:/Users/HEVEN/Desktop/K-City 예선전 경로 파일(UTM)_ver2.txt", 'r')
        f = open("C:/Users/HEVEN/Desktop/gps_t.txt", 'r')

        total_track = []
        lines = f.readlines()

        for line in lines:
            temp = line.split('\t')
            temp2 = [0, 0]
            temp2[0] = float(temp[0])
            temp2[1] = float(temp[1])

            total_track.append(temp2)

        index = 0

        # UTM 경로를 사용하지 않을거라면, 현재 파티션 부분을 주석처리
        # =============================================================================================================

        '''# Initial target list

        self.curr_target_list = self.db.new_list'''

        # Set initial condition
        # -------------------------------------------------------------------------------------------------------------
        self.car_angle = self.set_initial_angle()
        # -------------------------------------------------------------------------------------------------------------
        prevtime = time.time()
        # 자율주행 알고리즘 시작
        while not self.flag.system_stop:
            curr_time = time.time()
            dt = curr_time - prevtime
            # For point tracking test
            mission_num = 0

            # packet from Path Planning
            packet = [mission_num, None, None, None, None]

            # 현재 차체 좌표 (meter 단위)

            gps_curr = [self.db.gps.data[1]*1099.5849, self.db.gps.data[3]*887.4]
            
            if gps_curr[0] - self.prev_position[0] > 0.001 or gps_curr[1] - self.prev_position[1] > 0.001:
                self.p_curr = gps_curr.copy()
                self.prev_position[0] = gps_curr[0]
                self.prev_position[1] = gps_curr[1]
            else:
                self.p_curr[0] += np.cos(self.car_angle * np.pi / 180) * self.db.platform.recv_data.speed / 3.6 * dt
                self.p_curr[1] += np.sin(self.car_angle * np.pi / 180) * self.db.platform.recv_data.speed / 3.6 * dt
            
            # print(f"dt: {dt}")
            # print(f"angle: {self.car_angle} , {self.prev_imu}")
            # print(f"manual_speed: {self.db.platform.recv_data.speed}")

            # 현재 차체 방향 (from IMU), 로컬 각도 변환 필요함
            yaw = self.db.imu.data[2]
            dif = yaw - self.prev_imu
            self.prev_imu = yaw
            while dif < 0:
                dif += 360
            self.car_angle += dif
            while self.car_angle < 0:
                self.car_angle += 360
            while self.car_angle > 360:
                self.car_angle -= 360

            '''# 타겟 점 선택, 다음 리스트 요청 알고리즘

            if index == SOME_NUMBER:     # 일정 인덱스가 되면
                # 새로운 리스트와 이전에 저장되어 있던 리스트를 합치기
                for point in self.db.new_list:
                    self.curr_target_list.append(point)

            elif index == LIST_SIZE:     # 마지막 index 에 도달하면
                # 이전 target list 는 제거하고
                self.curr_target_list = self.curr_target_list[LIST_SIZE:2*LIST_SIZE]
                
                # 다시 0번 인덱스부터 시작
                index = 0

            else:
                pass

            target_list = self.curr_target_list

            # target_list 준비 완료

            # target_list 가 준비 되었다면, 타겟 점 선택 알고리즘

            if ((p_curr[0]-target_list[index+1][0]) ** 2 + (p_curr[1]-target_list[index+1][1]) ** 2) < DISTANCE_SQUARE:
                index += 1

            else:
                pass
            
            p_targ = target_list[index]
            
            # 타겟 점 선택 완료'''

            p_curr = gps_curr
            car_angle = self.car_angle

            # Test 1 # print(p_curr)
            # Test 2 # print(car_angle)
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

            # 제어 알고리즘에 필요한 데이터 수신 완료
            # ---------------------------------------------------------------------------------------------------------
            # 조향각 제어

            # path tracking
            curr_angle_error = self.__find_angle_error(car_angle, p_curr, p_targ)  # 현재 각도 오차를 구합니다.
            # Test 3 # print(curr_angle_error)

            # 기어 설정, 만약 주차 미션의 경우 뒤로 갈 때 각도 오차를 다시 구함
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
            # 주차 미션일 경우, 따로 조향각과 속력 및 브레이크 제어

            if mission_num is 8:
                speed = CAR_SPEED
                target_speed, steer_angle, final_brake = self.__parking_mission(packet, speed, steer_angle)

            # 그 외에는, 미션별 속력 및 브레이크 제어

            else:
                speed = CAR_SPEED  # 기본 주행 속력
                target_speed, final_brake = self.__do_mission(packet, speed)  # 목표 속력과 브레이크를 제어합니다.

            # 속력 최종 결정
            # ---------------------------------------------------------------------------------------------------------
            # 값 조정 (시리얼 패킷으로 보낼 값들 조정)

            # 조향각에 71을 곱합니다. (serial 통신을 위해)
            steer_angle_to_packet = steer_angle * 71

            # 만약 조향각이 2000/71도 보다 크거나, -2000/71도 보다 작다면, 값을 조정하면서 목표 속력을 줄입니다.
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

            # ==========================통신 완료=======================================================================
            # 보내준 이후, 현재 각도 오차를 이전 각도 오차로 저장.
            self.prev_angle_error = curr_angle_error
            self.save_datas(p_targ, curr_angle_error)

            # 측정 시간을 prev_time 에 저장

            self.prev_time = curr_time
            time.sleep(0.01)

    # Set imu initial angle, should be called at start only
    # ---------------------------------------------------------------------------------------------
    def set_initial_angle(self):
        prevangle = 0
        prevx = self.db.gps.data[1]*1099.5849
        prevy = self.db.gps.data[3]*887.4
        
        while True:
            currx = self.db.gps.data[1]*1099.5849
            curry = self.db.gps.data[3]*887.4 
            if np.abs(prevx - currx) > 0.01 or np.abs(prevy - curry) > 0.01:
                angle = np.arctan2(curry - prevy, currx - prevx) * 180 / np.pi
                prevx = currx
                prevy = curry
                print(f"curr angle: {angle}, prev angle: {prevangle}")
                if np.abs(prevangle - angle) < 1:
                    return angle
                prevangle = angle
            time.sleep(0.1)

    def save_datas(self, target, angle_error):
        self.db.control_data.curr_pos = self.p_curr.copy()
        self.db.control_data.target = target.copy()
        self.db.control_data.curr_angle = self.car_angle
        self.db.control_data.angle_error = angle_error
    # ---------------------------------------------------------------------------------------------

    def __find_angle_error(self, car_angle, position_curr, position_targ):  # 현재 차체의 각도, 현재 차의 위치, 선택한 타겟점의 위치

        targetdir_x = position_targ[0] - position_curr[0]  # 타겟 방향의 벡터 = 타겟 위치 - 현재 위치
        targetdir_y = position_targ[1] - position_curr[1]

        target_angle = np.arctan2(targetdir_y, targetdir_x) * 180 / np.pi
        # 각도 오차로 변환
        angle_error = target_angle - car_angle          # target_angle 에서 car_angle 을 빼서 각도 오차를 구함
        if angle_error >= 180:
            angle_error -= 360                          # 각도 오차의 절댓값이 180보다 커지면 보정
        if angle_error <= -180:
            angle_error += 360
        # -180도 ~ 180도 사이의 angle_error 를 얻게 됨.

        print(f"car_angle {car_angle}, target_angle {target_angle}")
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
            target_speed -= 30

        elif mode_num is 2:       # 동적 장애물
            target_speed -= 30

            if packet[4] is True:
                target_speed -= 50

            # 동적 장애물 까지의 거리
            distance_obstacle = packet[2]

            if distance_obstacle < 500:
                brake = 15

            elif distance_obstacle < 300:
                brake = 30

            elif distance_obstacle < 150:
                brake = 60

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

            if packet[3] is not None:  # 좌회전 신호가 보인다면
                if packet[3] is True:  # 좌회전 신호가 켜져있다면, 주행 계속
                    pass

                else:  # 좌회전 신호가 아니라면, 정지선 앞에 멈춰야 함
                    distance_stop = packet[2]  # 정지선까지의 거리

                    if distance_stop < 500:
                        brake = 15

                    elif distance_stop < 300:
                        brake = 30

                    elif distance_stop < 150:
                        brake = 60

            else:  # 좌회전 신호가 안보인다면, 그냥 주행 계속
                pass

        elif mode_num is 7:
            target_speed -= 30

            if packet[3] is not None:  # 적색 신호가 보인다면
                if packet[3] is True:  # 적색 신호가 켜져있다면, 정지선 앞에 멈춰야 함
                    distance_stop = packet[2]  # 정지선까지의 거리

                    if distance_stop < 500:
                        brake = 15

                    elif distance_stop < 300:
                        brake = 30

                    elif distance_stop < 150:
                        brake = 60

                else:  # 적색 신호가 아니라면, 주행 계속
                    pass

            else:  # 적색 신호가 안보인다면, 그냥 주행 계속
                pass

        return target_speed, brake

    def __parking_mission(self, packet, speed, steer):
        parking_track = packet[2]
        index = packet[3]

        final_speed = speed
        final_steer_angle = steer
        final_brake = 0

        if self.parking_count == 30000:
            pass

        elif index == len(parking_track) - 1:
            final_steer_angle = 0
            final_brake = 30

            self.parking_count += 1

        else:
            pass

        return final_speed, final_steer_angle, final_brake
    # -------------------------------------------------------------------------------------------------
    # threading

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
