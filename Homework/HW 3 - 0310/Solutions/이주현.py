'''
1. Crop the road sign picture. (Any sign you want)
2. Paste the road sign picture on the random position of the road picture.
 * The road sign should not be cut off
3. Create 100 pictures and save the file as 'road_001.jpg', 'road_002.jpg', ..., 'road_100.jpg' in data directory.

Samples are attached in this file.
'''

import cv2
from random import *
import os

sign = cv2.imread("C:/Users/user/Desktop/sign.jpg", cv2.IMREAD_COLOR)
road = cv2.imread("C:/Users/user/Desktop/road.jpg", cv2.IMREAD_COLOR) #road, sign이미지 불러오기

height, width, channel = road.shape

#cv2.imshow("sign", sign)

cropped = sign[90:190, 25:130] #road sign을 crop하기

#cv2.imshow("cropped", cropped)

os.mkdir('C:/Users/user/Desktop/data') #data directory만들기

for i in range (1,101):
    copied = road.copy() #원본은 유지하기 위해 road이미지를 copy한다
    x = randrange(height-99)
    y = randrange(width-104) #난수 생성(random하게 이미지를 합성하기 위해)
    copied[x:x+100, y:y+105] = cropped #이미지 합성
    if i<10:
        cv2.imwrite("C:/Users/user/Desktop/data/road_00%d.jpg" %i, copied)
    elif i<100:
        cv2.imwrite("C:/Users/user/Desktop/data/road_0%d.jpg" %i, copied)
    else:
        cv2.imwrite("C:/Users/user/Desktop/data/road_100.jpg", copied) #합성된 이미지저장
