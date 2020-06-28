from image_function import parking_transform, combine, detect, lane_detect, transform2, get_stop_line, get_parking_line, ret_shift_const, brt_corr
import cv2
import numpy as np


class Parking:
    def __init__(self, db):
        self.db = db
        
    #주차선이 검출되었는지를 리턴한다.
    def check_park_line(self):
        parking_cam = self.db.sub_cam.data        
        img_parking = parking_transform(parking_cam) # 주차캠 원근변환
        img_hsv = cv2.cvtColor(img_parking, cv2.COLOR_BGR2HSV) # BGR 채널을 HSV 채널로 변환
        h, s, v = cv2.split(img_hsv) # hsv채널 중 v채널만을 분리
        brt_mean = np.mean(v) # v채널의 평균 값을 이용하여 밝기 측정
        print(brt_mean)
        img_parking = brt_corr(brt_mean, img_parking) # 밝기 보정 함수를 이용하여 이미지 밝기 평활화
        img_parking_bin = detect(img_parking) # 평활화한 이미지를 이진화

        # 영상 회전 변환

        return get_parking_line(img_parking_bin) # 주차선 검출 함수의 리턴 값을 리턴


if __name__ == "__main__":
    test_video = "parking_right3.avi"
    cap1 = cv2.VideoCapture(test_video)

    while True:
        ret1, img1 = cap1.read()
        cv2.imshow("Original", img1)
        
        img_parking = parking_transform(img1)
        cv2.imshow("transform", img_parking)
        img_parking_bin = detect(img_parking, list = ['w'])

        print("parking line", get_parking_line(img_parking_bin))
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
