import cv2
import numpy as np
import math
# from Database.Database import Database

LiDAR_MIN = 3000  # 주차장에 차가 없다고 판단할 라이다의 최소 거리
DIAGONAL_MIN = 200  # 사각형이라고 인식할 대각선의 최소 길이
DIAGONAL_MAX = 300  # 사각형이라고 인식할 대각선의 최대 길이
SCALE = 2  # 1 pixel에 해당하는 cm (축척)

def parking(cap, lidar):
    '''
    Mission: 차량이 있는 주차공간과 장애인 전용 주차구간을 피해 주차를 함
    <Flow Chart>
    Lidar의 135도 방향중 일정 거리 이내에 ┌ 물체가 포착됨(이미 주차되어있는 차량이 있는 경우) -> return 0
                                      └ 포착되지 않음 -> 주차용 카메라에서 사각형을 찾음 ┌ 사각형이 검출되지 않는 경우 -> return 0
                                                                                   └ 사각형이 검출되는 경우 ┌ 장애인 주차구역인 경우 -> return 0
                                                                                                         └ 장애인 주차구역이 아닌경우 -> target, map을 저장, return 1
    '''



    # ==================== lidar에 장애물이 검출되나 확인 ====================== #
    is_obstacle = 0
    for i in range(5):
        if int(lidar[i]) < LiDAR_MIN: is_obstacle += 1
    if (is_obstacle >= 3):
        return 0
    # ================================================================== #


    try:
        cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('original', cap)

        # cap = cv2.resize(cap, dsize = (0, 0), fx = 0.5, fy = 0.5, interpolation=cv2.INTER_LINEAR)  # 가로세로 크기 조절
        cap = cv2.resize(cap, dsize=(640, 480), interpolation=cv2.INTER_AREA)
        height = cap.shape[0]
        width = cap.shape[1]

        # ============================ 사각형 찾기 ============================== #
        ## bird view로 바꿈

        '''
        source_points = np.array(
            [(0.429 * width, 0.175 * height), (0.233 * width, 0.282 * height),
             (0.590 * width, 0.315 * height), (0.620 * width, 0.182 * height)], np.float32)  # 왼쪽 위부터 반시계방향
        '''
        source_points = np.array(
            [(0.429 * width, 0.175 * height), (0.233 * width, 0.282 * height),
             (0.590 * width, 0.315 * height), (0.620 * width, 0.182 * height)], np.float32)  # 왼쪽 위부터 반시계방향

        destination_points = np.array(
            [(0.368 * width, 0.239 * height), (0.368 * width, 0.639 * height),
             (0.568 * width, 0.639 * height), (0.568 * width, 0.239 * height)], np.float32)  # 왼쪽 위부터 반시계방향


        warp_matrix = cv2.getPerspectiveTransform(source_points, destination_points)
        birdview_img = cv2.warpPerspective(cap, warp_matrix, (width, height), flags=cv2.INTER_LINEAR)

        cv2.imshow('why', birdview_img)

        ## 차선만 뽑아냄(흑백으로 바꿈)
        _, threshold_img = cv2.threshold(birdview_img, 60, 255, cv2.THRESH_BINARY)
        threshold_img = threshold_img[0:480, 170:470]

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
        cv2.imwrite('detect.jpg', new_img)

        # ======================== 사각형이 없는경우 ========================== # >> 사각형이 없는 경우는 그냥 넘어감

        diagonal_half = math.sqrt((rectangle_coordinate[0][0] - center[0]) * (rectangle_coordinate[0][0] - center[0])
                      + ((rectangle_coordinate[0][1] - center[1]) * (rectangle_coordinate[0][1] - center[1])))


        if 2 * diagonal_half < DIAGONAL_MIN: is_rectangle = 0
        if 2 * diagonal_half > DIAGONAL_MAX: is_rectangle = 0

        if is_rectangle == 0: return 0
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
            return 0
        ## 장애인 주차구간이 아닐때 >> target과 map을 저장
        else:  # 흰색 비율이 무게중심 주위 정사각형의 10% 미만일떄는 장애인표시 없는걸로 생각
            return 1
        # ================================================================== #
    except:
        return 0


########### test ###########
'''
#video = cv2.VideoCapture('./video/real_park1.mp4')
video = cv2.VideoCapture('./video/parking_0901.mp4')

# database = Database(0, 0, 1, 1, 0)
# database.start()
# lidar_array = database.lidar

while (video.isOpened()):
    _, cap = video.read()
    print(parking(cap, _))

img = cv2.imread('./video/temp3.png')
print(parking(img, [7000, 7000, 7000, 8000, 7000]))
'''
