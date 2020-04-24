#hw4_2017315484_이주헌

import matplotlib.pyplot as plt         #maplotlib 사용하기 위해 import하고 plt로 정의
import matplotlib.image as mpimg
import numpy as np
import cv2
import math

#mathplotlib inline

img=mpimg.imread('YW2.jpg')         #사진을 불러온다

#plt.figure(figsize=(10,8))         #진행상황을 확인하기 위한 코드
#plt.imshow(img)
#plt.show()

def grayscale(img):                 #사진을 gray로 변경하는 함수
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)        #OpenCV를 이용해 gray로 변경

gray = grayscale(img)           #gray로 만들어주는 사용자정의함수 사용

#plt.figure(figsize=(10,8))             #진행상황을 확인하기 위한 코드
#plt.imshow(gray, cmap='gray')
#plt.show()

def gaussian_blur(img, kernel_size):        #차선을 명확하게 보기 위해 차선이외의 배경은 가우시안블러로 흐릿하게 해주기
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

kernel_size=5
blur_gray=gaussian_blur(gray, kernel_size)          #가우시안블러를 실행하는 사용자정의함수 사용

#plt.figure(figsize=(10,8))             #진행상황을 확인하기 위한 코드
#plt.imshow(blur_gray,cmap='gray')
#plt.show

def canny(img, low_threshold, high_threshold):          #canny edge detection을 적용
    return cv2.Canny(img, low_threshold, high_threshold)        #edge로 판단된 부분만 남기고 나머지는 지워서 선으로 표현해주기

low_threshold=50
high_threshold=50
edges=canny(blur_gray, low_threshold, high_threshold)       #canny edge detection algorithm 실행하는 사용자정의함수 사용

#plt.figure(figsize=(10,8))             #진행상황을 확인하기 위한 코드
#plt.imshow(edges, cmap='gray')
#plt.show()

def region_of_interest(img, vertices):          #모든 영역이 아닌 차선부분의 영역만 인식이 되도록 관심영역설정 함수만들기
    mask=np.zeros_like(img)

    if len(img.shape)>2:
        channel_count=img.shape[2]
        ignore_mask_color=(255,) * channel_count
    else:
        ignore_mask_color=255

    cv2.fillPoly(mask, vertices, ignore_mask_color)     #폴리곤을 그리는 함수를 사용하여 오각형 외곽선과 내부가 채워진 오각형을 그린다

    masked_image = cv2.bitwise_and(img, mask)       #mask가 pixel이 nonzero일 경우에만 return을 해준다
    return masked_image
            
imshape = img.shape
vertices = np.array([[(100,imshape[0]),             #관심영역을 vertices에 저장하기
                      (450,320),
                      (550,320),
                      (imshape[1]-20,imshape[0])]], dtype=np.int32)
mask = region_of_interest(edges, vertices)

#plt.figure(figsize=(10,8))             #진행상황을 확인하기 위한 코드
#plt.imshow(mask,cmap='gray')
#plt.show()

def draw_lines(img, lines, color=[0,0,255], thickness=5):           #인식을 통해서 얻은 도로에 파란색의 선을 긋도록 하는 함수
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1,y1), (x2,y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):        #draw_lines 함수를 포함한 직접 선을 그리는 함수를 생성한
    lines=cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
                          minLineLength=min_line_len,
                          maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1],3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

rho = 2             #라인을 그리기 위해서 필요한 변수들을 입력
theta = np.pi/180
threshold = 90
min_line_len = 120
max_line_gap = 150

lines = hough_lines(mask, rho, theta, threshold,        #hough_lines
                    min_line_len, max_line_gap)

#plt.figure(figsize=(10,8))         #진행상황을 확인하기 위한 코드
#plt.imshow(lines,cmap='gray')
#plt.show()

def weighted_img(img, initial_img, α=0.8, β=1., γ=0. ):         #처음 불러왔던 이미지에 영상인식으로 그린 라인을 입히기
    return cv2.addWeighted(initial_img, α, img, β, γ)

lines_edges = weighted_img(lines, img,α=0.8, β=1., γ=0. )

plt.figure(figsize=(10,8))          #진행상황을 확인하기 위한 코드
plt.imshow(lines_edges)
plt.show()

