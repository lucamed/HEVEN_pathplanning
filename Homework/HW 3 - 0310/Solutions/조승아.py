import os
import cv2
import random

p="C:\\Users\\USER\\Desktop\\헤븐\\HW2\\data"
os.mkdir(p)

sign=cv2.imread("sign.jpg")
crop_sign=sign[90:190,140:240]

for i in range(1,101):
    y=random.randrange(0,1031)
    x=random.randrange(0,1596)
    road=cv2.imread("road.jpg")
    road[y:y+100,x:x+100]=crop_sign
    j=str(i).zfill(3)
    cv2.imwrite("data/road_%s.jpg"%j,road)


