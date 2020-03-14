import cv2
import random
import os

os.makedirs('C:\\Users\\신동한\\Downloads\\Autonomous-Car-Simulator-master\\heven2020\\data')

image = cv2.imread("sign.jpg")
sign = image[80:190, 20:130]
cv2.imshow("sign",sign)
cv2.waitKey(0)

for i in range(100):
    road = cv2.imread("road.jpg")
    road_H = road.shape[0]
    road_W = road.shape[1]
    a = random.randrange(0, road_H-110)
    b = random.randrange(0, road_W-110)
    road_copy = road.copy()
    road_copy[a:a+110,b:b+110] = sign
    cv2.imwrite('road00{}.jpg'.format(i))



