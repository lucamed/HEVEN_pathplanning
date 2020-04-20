import cv2
import random

def im_trim(img):
    x = 500//4; y = 500//6; w = 120;h = 120;
    img_trim = img[y:y + h,x:x + w]
    return img_trim

signs = cv2.imread("sign.jpg",cv2.IMREAD_COLOR)
road = cv2.imread("road.jpg",cv2.IMREAD_COLOR)
road_height, road_width,_=road.shape #1131,1696,3
sign_1=im_trim(signs)
sign_1_height, sign_1_width,_=sign_1.shape #120,120,3

for i in range(0,100):
    roads = road.copy()
    x = random.randint(0,road_width-sign_1_width)
    y = random.randint(0,road_height-sign_1_height)
    roads[y:y+sign_1_height, x:x+sign_1_width]=sign_1
    cv2.imwrite("road_00%d.jpg" %i,roads)

