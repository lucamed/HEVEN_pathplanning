from Path.image_function import transform, combine, detect, lane_detect, transform2, get_stop_line, ret_shift_const, gamma_correction
import cv2

class Line:
    def __init__(self, db):
        self.db = db
    
    #차량의 조향각과 현재 차선을 기준으로 얼마나 치우쳐져 있는지를 db의 position과 degree에 값을 리턴한다.
    #degree는 0도 일 때 정면이며, -일경우로 왼쪽, +일 경우 오른쪽으로 치우쳐져 있음을 나타내고
    #position은 0.5일 때 중앙, 0.5보다 작을 경우 왼쪽, 클 경우 오른쪽으로 치우쳐져 있다.
    def set_info(self):
        left_cam = self.db.main_cam.data # db로부터 Camera law data를 받는다.
        right_cam = self.db.sub_cam.data
        img_left, img_right = transform(left_cam, right_cam) # image_function의 transform 함수로 원근변환한다.
        img_concat = combine(img_left, img_right) # 원근변환한 이미지를 붙인다.
        img_bin = detect(img_concat) # 붙인 이미지를 이진변환한다.
        position, degree, ret_img = lane_detect(img_bin) # 이진변환한 이미지로부터, 라인을 추출하고 position과 degree를 도출한다.
        img_ret = cv2.add(ret_img, img_bin) #img_ret은 추출한 라인과 degree, position을 함께 볼 수 있는 결과 이미지다.
        cv2.imshow("img_ret", img_ret)
        cv2.waitKey(1)

        self.db.position = position #db에 position과 degree를 넣는다. 이는 나중에 제어에서 사용하게 된다.
        self.db.degree = degree
    
    #정지선을 검출하고 정지신호를 보낸다.
    def check_stop_line(self):
        front_cam = self.db.parking_cam.data # db로부터 정면 Camera law data를 받는다.
        gamma_correction(front_cam, 2) # 감마보정을 이용하는데, 두번째 argument는 상황에 따라 조정해야 한다.
        img_front = transform2(front_cam) # 받은 이미지를 원근 변환한다.
        img_bin = detect(img_front) # 원근 변환한 이미지를 이진화한다.
        cv2.imshow("Crosswalk", img_bin)
        return get_stop_line(img_bin) # 이진화된 이미지를 get_stop_line를 이용해 정지선을 검출한다.
    
    #concat할 때 좌우 라인의 공간을 직접 측정하여 넣게 되는데, 이 값은 shift_const와 관계가 있다. 이를 리턴한다.
    def get_shift_const(self):
        return ret_shift_const
