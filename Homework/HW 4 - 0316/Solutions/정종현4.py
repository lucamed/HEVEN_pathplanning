import cv2
import numpy as np

#이미지 불러오고 복사하기
img = cv2.imread('./data/YW1.jpg')
copy = img.copy()

#노란선 찾기
hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
low_yellow = np.array([18,94,140])
up_yellow = np.array([48,255,255])
yellowmask = cv2.inRange(hsv_img, low_yellow, up_yellow)
yellowedge = cv2.Canny(yellowmask, 75, 150)
#ROI만들기
mask = np.zeros_like(yellowedge)
height,width = yellowedge.shape
vertices = np.array([[(100,height),(450,320),(550,320),(width-20,height)]],dtype=np.int32)
cv2.fillPoly(mask,vertices,(255))
yellowedge = cv2.bitwise_and(yellowedge,mask)
#HoughlinesP함수로 선좌표 찾고 그리기
yellowlines = cv2.HoughLinesP(yellowedge, 1, np.pi/180, 150, minLineLength = 20, maxLineGap=100)
for line in yellowlines:
    cv2.line(copy,(line[0][0],line[0][1]), (line[0][2], line[0][3]),(0,0,255),5)

#흰선찾기
blur = cv2.GaussianBlur(img, (5, 5), 0)
low_white = np.array([200,200,200])
up_white = np.array([255,255,255])
whitemask = cv2.inRange(blur, low_white, up_white)
whiteedge = cv2.Canny(whitemask, 75, 150)
#ROI만들기
mask = np.zeros_like(whiteedge)
height,width = whiteedge.shape
vertices = np.array([[(100,height),(450,320),(550,320),(width-20,height)]],dtype=np.int32)
cv2.fillPoly(mask,vertices,(255))
whiteedge = cv2.bitwise_and(whiteedge,mask)
#흰선따라 좌표찾고 그리기
whitelines = cv2.HoughLinesP(whiteedge, 1, np.pi/180, 100, minLineLength = 20, maxLineGap=100)
for line in whitelines:
    cv2.line(copy,(line[0][0],line[0][1]), (line[0][2], line[0][3]),(255,0,0),5)

#녹색선 그리기(whitelines와 yellowlines의 중점을 넣기.)(미완성 ㅠㅠ)
w0 = whitelines[0][0][:2]
w1 = whitelines[0][0][2:]
y0 = yellowlines[0][0][:2]
y1 = yellowlines[0][0][2:]
print(w0,w1,y0,y1)
cv2.line(copy,(int((w0[0]+y1[0])/2),height-200),(int((w1[0]+y0[0])/2),height),(0,255,0),5) #(x,y)
cv2.imshow('',copy)
cv2.waitKey()