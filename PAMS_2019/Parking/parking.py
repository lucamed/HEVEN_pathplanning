import cv2
import numpy as np
import math
# from Database.Database import Database

LiDAR_MIN = 5  # 주차장에 차가 없다고 판단할 라이다의 최소 거리
DIAGONAL_MIN = 250  # 사각형이라고 인식할 대각선의 최소 길이
DIAGONAL_MAX = 350  # 사각형이라고 인식할 대각선의 최대 길이
SCALE = 2  # 1 pixel에 해당하는 cm (축척)

def parking(cap):
    '''
    Mission: 차량이 있는 주차공간과 장애인 전용 주차구간을 피해 주차를 함
    <Flow Chart>
    Lidar의 135도 방향중 일정 거리 이내에 ┌ 물체가 포착됨(이미 주차되어있는 차량이 있는 경우) -> return 0
                                      └ 포착되지 않음 -> 주차용 카메라에서 사각형을 찾음 ┌ 사각형이 검출되지 않는 경우 -> return 0
                                                                                   └ 사각형이 검출되는 경우 ┌ 장애인 주차구역인 경우 -> return 0
                                                                                                         └ 장애인 주차구역이 아닌경우 -> target, map을 저장, return 1
    '''

    '''
    # ==================== lidar에 장애물이 검출되나 확인 ====================== #
    if lidar[135] < LiDAR_MIN:  # lidar data의 135도에 물체가 있을 경우 그냥 넘어감
        return 0, 0, 0
    # ================================================================== #
    '''

    try:
        cv2.waitKey(10)
        #BGR -> Grayscale
        cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        cv2.imshow('original', cap)

        # cap = cv2.resize(cap, dsize = (0, 0), fx = 0.5, fy = 0.5, interpolation=cv2.INTER_LINEAR)  # 가로세로 크기 조절
        # interpolation -> 영역 보간법
        cap = cv2.resize(cap, dsize=(640, 480), interpolation=cv2.INTER_AREA)
        height = cap.shape[0]
        width = cap.shape[1]

        # ============================ 사각형 찾기 ============================== #
        ## bird view로 바꿈

        source_points = np.array(
            [(0.433 * width, 0.177 * height), (0.155 * width, 0.348 * height),
             (0.848 * width, 0.413 * height), (0.745 * width, 0.198 * height)], np.float32)  # 왼쪽 위부터 반시계방향

        '''
        destination_points = np.array(
            [(0.445 * width, 0.084 * height), (0.445 * width, 0.484 * height),
             (0.645 * width, 0.484 * height), (0.645 * width, 0.084 * height)], np.float32)  # 왼쪽 위부터 반시계방향
        '''

        destination_points = np.array(
            [(0.425 * width, 0.260 * height), (0.425 * width, 0.8 * height),
             (0.665 * width, 0.8 * height), (0.665 * width, 0.260 * height)], np.float32)  # 왼쪽 위부터 반시계방향


        warp_matrix = cv2.getPerspectiveTransform(source_points, destination_points)
        birdview_img = cv2.warpPerspective(cap, warp_matrix, (width, height), flags=cv2.INTER_LINEAR)

        cv2.imshow('why', birdview_img)

        ## 차선만 뽑아냄(흑백으로 바꿈)
        _, threshold_img = cv2.threshold(birdview_img, 180, 255, cv2.THRESH_BINARY)

        ## FOR DEBUGGING ##
        # 디버깅시 차선의 흑백 구분이 제대로 되나 확인
        # cv2.imshow('threshold_img', threshold_img)
        # cv2.imshow('threshold_img', threshold_img)

        ## 사각형이 검출되지 않는 경우 -> 그냥 진행
        contours, _ = cv2.findContours(threshold_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        is_rectangle = 0  # 사각형이 있는 경우 1, 없는 경우 0
        rectangle_coordinate = [(0, 0), (0, 0), (0, 0), (0, 0)] # 사각형이 있는 경우 꼭지점의 네 좌표를 저장
        center = [(0, 0)]

        for cnt in contours:
            # approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            approx = cv2.approxPolyDP(cnt, 30, True)
            cv2.drawContours(birdview_img, [approx], 0, (0), 5)

            if len(approx) == 4:
                is_rectangle = 1
                ## 무게중심 구하기
                raw_center = cv2.moments(approx)
                center = (int(raw_center['m10'] / raw_center['m00']), int(raw_center['m01'] / raw_center['m00']))
                ## 좌표 찾아 집어넣기(rectangle_coordinate에 네개의 꼭짓점을 각각 집어넣음)
                rectangle_coordinate[0] = (approx.ravel()[0], approx.ravel()[1])
                rectangle_coordinate[1] = (approx.ravel()[2], approx.ravel()[3])
                rectangle_coordinate[2] = (approx.ravel()[4], approx.ravel()[5])
                rectangle_coordinate[3] = (approx.ravel()[6], approx.ravel()[7])
                break
        # ================================================================== #

        ## FOR DEBUGGING ##
        # 디버깅시 사각형 제대로 찾아지나 확인
        new_img = cv2.circle(threshold_img, rectangle_coordinate[0], 20, (255, 255, 255), -1)
        new_img = cv2.circle(threshold_img, rectangle_coordinate[1], 20, (255, 255, 255), -1)
        new_img = cv2.circle(threshold_img, rectangle_coordinate[2], 20, (255, 255, 255), -1)
        new_img = cv2.circle(threshold_img, rectangle_coordinate[3], 20, (255, 255, 255), -1)
        cv2.imshow("detect_rectangle", new_img)

        # ======================== 사각형이 없는경우 ========================== # >> 사각형이 없는 경우는 그냥 넘어감

        diagonal_half = math.sqrt((rectangle_coordinate[0][0] - center[0]) * (rectangle_coordinate[0][0] - center[0])
                      + ((rectangle_coordinate[0][1] - center[1]) * (rectangle_coordinate[0][1] - center[1])))

        if 2 * diagonal_half < DIAGONAL_MIN: is_rectangle = 0
        if 2 * diagonal_half > DIAGONAL_MAX: is_rectangle = 0
        if is_rectangle == 0: return 0, 0, 0
        # ================================================================== #

        # ======================== 사각형이 있는 경우 ========================= # >> 사각형이 있는 경우 장애인 주차구간인지 아닌지 판단
        ## 장애인 구역인지 판단
        count_white = 0
        handicap_radius = int(diagonal_half / 6)
        count_all = handicap_radius * handicap_radius * 4
        for i in range(center[0] - handicap_radius, center[0] + handicap_radius, 1):
            for j in range(center[1] - handicap_radius, center[1] + handicap_radius, 1):
                if threshold_img[j][i] == 255: count_white = count_white + 1

        ## 장애인 주차구간일때 >> 장애인 주차구간인 경우 그냥 넘어감

        if count_white / count_all > 0.1:  # 흰색 비율이 무게중심 주위 정사각형의 10% 이상 차지할때는 장애인표시 있는걸로 생각
            return 0, 0, 0

        ## 장애인 주차구간이 아닐때 >> target과 map을 저장
        else:  # 흰색 비율이 무게중심 주위 정사각형의 10% 미만일떄는 장애인표시 없는걸로 생각
            ## 주차공간의 사각형 중 차에서 가장 가까운 두 꼭짓점을 찾음
            close_find = 0
            far_find = 0
            close_point = [0, 1]
            far_point = [2, 3]
            for i in range(0, 4, 1):
                if rectangle_coordinate[i][1] > center[1]:
                    close_point[close_find] = i
                    close_find = close_find + 1
                else:
                    far_point[far_find] = i
                    far_find = far_find + 1
            if (rectangle_coordinate[close_point[0]][0] - rectangle_coordinate[close_point[1]][0]) \
                    * (rectangle_coordinate[far_point[0]][0] - rectangle_coordinate[far_point[1]][
                0]) < 0:  # close_point[0]과 far_point[0]이 center를 기준으로 대각선에 있지 않도록 조절
                temp = close_point[0]
                close_point[0] = close_point[1]
                close_point[1] = temp

            # print(rectangle_coordinate)
            # 모두 0으로 되어 있는 빈 Canvas(검정색)
            img = np.zeros((600, 800, 3), np.uint8)
            final_rectangle_coordinate = [(0,0), (0,0), (0,0), (0,0)]

            final_rectangle_coordinate[0] = (rectangle_coordinate[close_point[0]][0] + 80, rectangle_coordinate[close_point[0]][1] + 50)
            final_rectangle_coordinate[1] = (rectangle_coordinate[far_point[0]][0] + 80, rectangle_coordinate[far_point[0]][1] + 50)
            final_rectangle_coordinate[2] = (rectangle_coordinate[far_point[1]][0] + 80, rectangle_coordinate[far_point[1]][1] + 50)
            final_rectangle_coordinate[3] = (rectangle_coordinate[close_point[1]][0] + 80, rectangle_coordinate[close_point[1]][1] + 50)
            final_center = [center[0] + 80, center[1] + 50]


            final_map = cv2.line(img, final_rectangle_coordinate[0], final_rectangle_coordinate[1],
                               (255, 255, 255), 10)  # 선은 흰색을 따라 그림
            final_map = cv2.line(final_map, final_rectangle_coordinate[1], final_rectangle_coordinate[2],
                               (255, 255, 255), 10)  # 선은 흰색을 따라 그림
            final_map = cv2.line(final_map, final_rectangle_coordinate[2], final_rectangle_coordinate[3],
                               (255, 255, 255), 10)  # 선은 흰색을 따라 그림

            ## 넘겨줄때 얘는 꼭 주석처리해야함!!
            final_map = cv2.circle(final_map, (final_center[0], final_center[1]), 10, (255, 255, 255), -1)

            ## FOR DEBUGGING ##
            # map 출력 테스트
            cv2.imshow('final', final_map)

            ## 주차장 쪽의 기울기
            if rectangle_coordinate[far_point[0]][0] < rectangle_coordinate[far_point[1]][0]:
                gradient = (rectangle_coordinate[far_point[1]][1] - rectangle_coordinate[far_point[0]][1])/\
                           (rectangle_coordinate[far_point[1]][0] - rectangle_coordinate[far_point[0]][0])
            else:
                gradient = (rectangle_coordinate[far_point[0]][1] - rectangle_coordinate[far_point[1]][1]) /\
                           (rectangle_coordinate[far_point[0]][0] - rectangle_coordinate[far_point[1]][0])

            center_angle = 1.570796 + math.atan(gradient)  # 90도 라디안 값 + 플랫폼의 움직인 각도
            final_center[3] = center_angle

            ## 플랫폼 현재 위치 정하기
            platform_location = [400, 600, 2.356195]  # 차의 각도는 항상 135도(카메라가 45도 고정이기 떄문)

            '''
            1. 사각형(0-1, 1-2, 2-3 순서) 좌표
            2. 플랫폼 현재좌표 및 각도
            3. 목적지 좌표 및 각도
            순으로 반환
            '''
            return final_rectangle_coordinate, platform_location, final_center

        # ================================================================== #
    except:
        return 0, 0, 0


########### test ###########
# video = cv2.VideoCapture('./real_park1.mp4')
video = cv2.VideoCapture('./real_park1.mp4')
#video = cv2.VideoCapture('./video/pre_park.mp4')

# database = Database(0, 0, 1, 1, 0)
# database.start()
# lidar_array = database.lidar

while (video.isOpened()):
    _, cap = video.read()
    parking(cap)
