import os
import sys
sys.path.append(".")

from src.Database import Database
import numpy as np
import cv2

class Obstacle:
    def __init__(self, db, ARC_ANGLE=110, OBSTACLE_OFFSET=85, ACTUAL_RADIUS=300, gpu=True):
        self.gpu_on = gpu
        self.ARC_ANGLE = ARC_ANGLE
        self.OBSTACLE_OFFSET = OBSTACLE_OFFSET
        self.ACTUAL_RADIUS = ACTUAL_RADIUS
        self.db = db

        if self.gpu_on:
            import pycuda.autoinit
            from pycuda.compiler import SourceModule
            mod = SourceModule(r"""
                            #include <stdio.h>
                            #include <math.h>
                            #define PI 3.14159265
                            __global__ void detect(int data[][2], int* rad, int* range, unsigned char *frame, int *pcol) {
                                    for(int r = 0; r < rad[0]; r++) {
                                        const int thetaIdx = threadIdx.x;
                                        const int theta = thetaIdx + range[0];
                                        int x = rad[0] + int(r * cos(theta * PI/180)) - 1;
                                        int y = rad[0] - int(r * sin(theta * PI/180)) - 1;
                                        if (data[thetaIdx][0] == 0) data[thetaIdx][1] = r;
                                        if (*(frame + y * *pcol + x) != 0) data[thetaIdx][0] = 1;
                                    }
                            }
                            """)

            self.cuda_detect_function = mod.get_function("detect")
            print("PLANNER: pycuda alloc end")

    def update(self):
        angle = self.ARC_ANGLE
        ACT_RAD = np.int32(self.ACTUAL_RADIUS)  # 실제 라이다 화면의 세로 길이 (즉 부채살의 실제 반경)
        AUX_RANGE = np.int32((180 - angle) / 2)  # 좌우대칭 부채살의 사잇각이 angle, AUX_RANGE 는 +x축 기준 첫 부채살의 각도

        lidar_raw_data =  self.db.lidar.data
        current_frame = np.zeros((ACT_RAD, ACT_RAD * 2), np.uint8)  # 그림 그릴 도화지 생성

        points = np.full((361, 2), -1000, np.int)  # 점 찍을 좌표들을 담을 어레이 (x, y), 멀리 -1000 으로 채워둠.

        for theta in range(0, 361):
            r = lidar_raw_data[theta] / 10  # 차에서 장애물까지의 거리, 단위는 cm

            if 2 <= r:  # 라이다 바로 앞 1cm 의 노이즈는 무시

                # r-theta 를 x-y 로 바꿔서 (실제에서의 위치, 단위는 cm)
                x = r * np.cos(np.radians(0.5 * theta))
                y = r * np.sin(np.radians(0.5 * theta))

                # 좌표 변환, 화면에서 보이는 좌표(왼쪽 위가 (0, 0))에 맞춰서 집어넣는다
                points[theta][0] = round(x) + ACT_RAD
                points[theta][1] = ACT_RAD - round(y)

        for point in points:  # 장애물들에 대하여
            cv2.circle(current_frame, tuple(point), self.OBSTACLE_OFFSET, 255, -1)  # 캔버스에 점 찍기

        # 부채살의 결과가 저장되는 변수
        data = np.zeros((angle + 1, 2), np.int)

        target = None

        if current_frame is not None:
            # 부채살 호출
            if self.gpu_on:
                import pycuda.driver as drv
                self.cuda_detect_function(drv.InOut(data), drv.In(ACT_RAD), drv.In(AUX_RANGE), drv.In(current_frame), drv.In(np.int32(ACT_RAD * 2)), block=(angle + 1, 1, 1))

                # 부채살이 호출되고 나면 data에 부채살 결과가 들어있음
                # (data[theta][0]: theta에서 뭔가에 부딪혔는가?(0 or 1), data[theta][1]: theta에서 뻗어나간 길이)
                data_transposed = np.transpose(data)
            else:
                for theta in range(angle + 1):
                    for r in range(ACT_RAD):
                        x = ACT_RAD + int(r * np.cos((theta + AUX_RANGE) * np.pi/180)) - 1
                        y = ACT_RAD - int(r * np.sin((theta + AUX_RANGE)* np.pi/180)) - 1
                        if data[theta][0] == 0:
                            data[theta][1] = r
                        
                        if current_frame[y][x] != 0:
                            data[theta][0] = 1
                data_transposed = np.transpose(data)

            # 장애물에 부딫힌 곳까지 하얀 선 그리기
            for i in range(0, angle + 1):
                x = ACT_RAD + int(data_transposed[1][i] * np.cos(np.radians(i + AUX_RANGE))) - 1
                y = ACT_RAD - int(data_transposed[1][i] * np.sin(np.radians(i + AUX_RANGE))) - 1
                cv2.line(current_frame, (ACT_RAD, ACT_RAD), (x, y), 255)

            # 진행할 방향을 빨간색으로 표시하기 위해 흑백에서 BGR 로 변환
            color = cv2.cvtColor(current_frame, cv2.COLOR_GRAY2BGR)

            # count 는 장애물이 부딪힌 방향의 갯수를 의미
            count = np.sum(data_transposed[0])

            if count <= angle - 1:
                relative_position = np.argwhere(data_transposed[0] == 0) - 90 + AUX_RANGE
                minimum_distance = int(min(abs(relative_position)))

                for i in range(0, len(relative_position)):
                    if abs(relative_position[i]) == minimum_distance:
                        target = int(90 + relative_position[i])

            else:
                target = int(np.argmax(data_transposed[1]) + AUX_RANGE)

            # 차량 바로 앞이 완전히 막혀버렸을 때: 좌로 최대조향할지, 우로 최대조향할지 결정
            # 좌, 우로 부채살 1개씩 뻗어서 먼저 뚫리는 곳으로 최대 조향함
            if np.sum(data_transposed[1]) == 0:
                r = 0
                found = False
                while not found:
                    for theta in (AUX_RANGE, 180 - AUX_RANGE):
                        x = ACT_RAD + int(r * np.cos(np.radians(theta))) - 1
                        y = ACT_RAD - int(r * np.sin(np.radians(theta))) - 1

                        if current_frame[y][x] == 0:
                            found = True
                            target = -theta
                            break
                    r += 1

            if target >= 0:
                x_target = ACT_RAD + int(data_transposed[1][int(target) - AUX_RANGE] * np.cos(np.radians(int(target))))
                y_target = ACT_RAD - int(data_transposed[1][int(target) - AUX_RANGE] * np.sin(np.radians(int(target))))
                cv2.line(color, (ACT_RAD, ACT_RAD), (x_target, y_target), (0, 0, 255), 2)
                max_dist = data_transposed[1][target - AUX_RANGE]
            else:
                x_target = ACT_RAD + int(100 * np.cos(np.radians(int(-target)))) - 1
                y_target = ACT_RAD - int(100 * np.sin(np.radians(int(-target)))) - 1
                cv2.line(color, (ACT_RAD, ACT_RAD), (x_target, y_target), (0, 0, 255), 2)
                target *= -1
                max_dist = r

            # For display and debugging
            max_dist_fordisplay = max_dist
            target_angle_fordisplay = (90 - target)
            str_1 = "max_dist: "+ str(max_dist_fordisplay)
            str_2 = "target_angle: "+ str(target_angle_fordisplay)

            # Display data on the monitor (green color)
            cv2.putText(color, str_1, (int(0.1 * ACT_RAD), int(0.8 * ACT_RAD)), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            cv2.putText(color, str_2, (int(0.1 * ACT_RAD), int(0.9 * ACT_RAD)), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

            return max_dist, target, color


if __name__ == "__main__":
    def make_sample_lidar_data():
        sample_data = 5000 * np.ones((361))
        random = np.random.randint(3, 10, 8)
        for i in range(361):
            if i < 45:
                sample_data[i] *= random[0] / 10
            elif i < 90:
                sample_data[i] *= random[1] / 10
            elif i < 135:
                sample_data[i] *= random[2] / 10
            elif i < 180:
                sample_data[i] *= random[3] / 10
            elif i < 225:
                sample_data[i] *= random[4] / 10
            elif i < 270:
                sample_data[i] *= random[5] / 10
            elif i < 315:
                sample_data[i] *= random[6] / 10
            else:
                sample_data[i] *= random[7] / 10
        
            if sample_data[i] < 0:
                sample_data[i] = 0

        return sample_data

    class Test:
        class LiDAR():
            data = None

        lidar = LiDAR()
    
    test = Test()
    test.lidar.data = make_sample_lidar_data()
    o = Obstacle(db=test, gpu=False)

    while True:
        b, a, image = o.update()
        print(b, a)
        cv2.imshow("123", image)
        cv2.waitKey(1)
