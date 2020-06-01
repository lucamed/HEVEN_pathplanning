'''
이지아 HW3
'''
import os
import cv2
import numpy as np
import random

#Cropping Road Sign
sign = cv2.imread("sign.jpg", 1)
cropped_sign = sign[205:305, 132:248]
cv2.imwrite("cropped_sign.jpg", cropped_sign)

#Create Directory
dirName = 'data'
parent_dir = "C:/Users/Gia Lee/Desktop/HEAVEN"
path = os.path.join(parent_dir, dirName)
os.mkdir(path)

for i in range(100):
    num = str(i+1)
    file = 1
    a = random.randint(1, 100)  # a, b random numbers to choose position
    b = random.randint(1, 150)
    file_path = "C:/Users/Gia Lee/Desktop/HEAVEN/data"
    
    if int(num) < 10:
        file = "road_00"
    elif int(num) < 100:
        file = "road_0"
    else:
        file = "road_"

    road = cv2.imread("road.jpg", 1)
    h1, w1 = cropped_sign.shape[:2]

    h = 10*a
    w = 10*b

    #Overlaying the Road and Sign
    road[h:h+h1, w:w+w1] = cropped_sign

    name = '%s%s.jpg' % (str(file), num)
    cv2.imwrite(os.path.join(file_path, name), road)
