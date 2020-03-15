import cv2
import random
import os

os.mkdir('C:\\workspace\\heven_week2\\data2')

image = cv2.imread("sign.jpg")
sign = image[300:430, 250:380]
road = cv2.imread("road.jpg")

road_H = road.shape[0]
road_W = road.shape[1]

for i in range(100):
    i+=1
    result = road.copy()

    sign_H = sign.shape[0]
    sign_W = sign.shape[1]

    x = random.randrange(0, road_W-sign_W)
    y = random.randrange(0, road_H-sign_H)

    result[y:y+sign_H, x:x+sign_W] = sign

    cv2.imwrite(os.path.join('C:\\workspace\\heven_week2\\data2', 'road_0'+str(i)+'.jpg'), result)




