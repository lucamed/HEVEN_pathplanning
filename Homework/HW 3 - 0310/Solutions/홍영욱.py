import cv2
import numpy as np
import random
import os

road = cv2.imread('road.jpg')
sign = cv2.imread('sign.jpg')

cut = sign[80:200, 20:140] #표지판 cut하기


a, b = road.shape[:2] #road.jpg 파일의 가로 세로 길이 측정
c, d = cut.shape[:2] #cut한 사진의 가로 세로 길이 측정

os.makedirs('data') #data 폴더 만들기


for i in range(1,101):
    x = random.randint(0, a-c) #random으로 표지판이 잘리지 않는 범위에서 세로값 받기
    y = random.randint(0, b-d) #random으로 표지판이 잘리지 않는 범위에서 가로값 받기
    copy = road.copy() #원본 road.jpg파일이 변하지 않게 복사파일 만들기
    copy[x:x+c,y:y+d] = cut #random으로 정해진 위치에 cut한 사진 넣기
    if i<10:
        cv2.imwrite('data/00%d.jpg' %i , copy) #형식에 맞추어 수정된 사진 저장하기
    if 9<i<100:
        cv2.imwrite('data/0%d.jpg' %i , copy)
    if i==100:
        cv2.imwrite('data/%d.jpg' %i , copy)

cv2.wiatKey(0)
cv2.destroyAllWindows()
