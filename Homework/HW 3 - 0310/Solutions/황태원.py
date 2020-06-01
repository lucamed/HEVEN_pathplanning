import cv2
import random
image = cv2.imread("sign.jpg")#표지판 파일을 image로 받음#
cut = image[80:200, 25:125] #횡단보도 표지판 부분만  cut#
cv2.imshow("cut", cut) #표지판 확인#
[a, b, c] = cut.shape  #자른 표지판  이미지의 크기를 좌표로 저장#
image2= cv2.imread("road.jpg") #도로 이미지를 image2로 받음#
[d, e, f] = image2.shape #도로 이미지의 크기를 좌표로 저장#
for i in range(1, 101): #1~100까지 반복#
 x = random.randint(0, d-a) #0부터 도로 이미지 세로길이에서 자른 표지판 이미지의 세로길이를 뺀 값 까지의 랜덤 정수 생성# 
 y = random.randint(0, e-b) #0부터 도로 이미지 가로길이에서 자른 표지판 이미지의 가로길이를 뺀 값 까지의 랜덤 정수 생성#
 image3= cv2.imread("road.jpg") #도로 이미지를 이미지3으로 저장#
 image3[x:x+a, y:y+b] = cut #이미지 3의 x~x+a열과 y~y+b행은 자른 이미지로 저장#
 cv2.imwrite("road_00%d.jpg" %i, image3) #이미지3을 출력#
 
 
