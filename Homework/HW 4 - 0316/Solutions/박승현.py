import matplotlib.pyplot as plt
import matplotlib.imge as mpimg
import cv2
import numpy as np
%matplotlib inline

img=mpimg.imread("YW1.jpg")
img1=mpimg.imread("YW2.jpg")

def region_of_interest(img, vertices):#올블랙처리 차선 찾을 곳

mask=np.zeros_like(img)

if len(img.shape)>2:
    channel_count=img.shape[2]
    ignore_mask_color=(255,)*channel_count
else:
    ignore_mask_color=255

imshape=img.shape

vertices=np.array([[(100,imshape[0]),
                    (452, 320),
                    (550, 320),
                    (imshape[1]-20,imshape[0])]], dtype=np.int32)
cv2.fillPoly(mask, vertices, ignore_mask_color)

def draw_lines(img, lines, color[255, 0, 0], thickness=5):#빨간선을 그리기
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def draw_lines(img, lines, color[255, 0, 0], thickness=5):#파란선을 그리기
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_lines(img, rho, thetha, threshold, min_line_len, max_line_gap):
    lines=cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
                          minLineLength=min_line_len,
                          maxLineGap=max_line_gap)
line_img=np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
draw_lines(line_img, lines)
return line_img

rho=2
theta=np.pi/180
threshold=90
min_line_len=120
max_line_gap=150

def weighted_img(img, initial_img, α=1, β=1., λ=0):#이미지 병
    return cv.addWeighted(initial_img, α, img, β, λ)

lines_edges=weighted_img(lines, img, α=1, β=1., λ=0)

