
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math

#mathplotlib inline

img=mpimg.imread('WW1.jpg')
print('This image is:',type(img),'with dimensions',img.shape)
#plt.figure(figsize=(10,8))
#plt.imshow(img)
#plt.show()


#grayscale#
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

gray = grayscale(img)
#plt.figure(figsize=(10,8))
#plt.imshow(gray, cmap='gray')
#plt.show()


#gaussian blur
def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

kernel_size=5
blur_gray=gaussian_blur(gray, kernel_size)

#plt.figure(figsize=(10,8))
#plt.imshow(blur_gray,cmap='gray')
#plt.show

def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)

low_threshold=50
high_threshold=50
edges=canny(blur_gray, low_threshold, high_threshold)

#plt.figure(figsize=(10,8))
#plt.imshow(edges, cmap='gray')
#plt.show()

#필요한 부분만 따내기#
def region_of_interest(img, vertices):
    mask=np.zeros_like(img)

    if len(img.shape)>2:
        channel_count=img.shape[2]
        ignore_mask_color=(255,) * channel_count
    else:
        ignore_mask_color=255

    cv2.fillPoly(mask, vertices, ignore_mask_color)

    masked_image = cv2.bitwise_and(img, mask)
    return masked_image
            
imshape = img.shape
vertices = np.array([[(100,imshape[0]),
                      (450,320),
                      (550,320),
                      (imshape[1]-20,imshape[0])]], dtype=np.int32)
mask = region_of_interest(edges, vertices)

#plt.figure(figsize=(10,8))
#plt.imshow(mask,cmap='gray')
#plt.show()


#선 긋기#
def draw_lines(img, lines, color=[255,0,0], thickness=5):
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1,y1), (x2,y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines=cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
                          minLineLength=min_line_len,
                          maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1],3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

rho = 2
theta = np.pi/180
threshold = 90
min_line_len = 120
max_line_gap = 150

lines = hough_lines(mask, rho, theta, threshold,
                    min_line_len, max_line_gap)

#plt.figure(figsize=(10,8))
#plt.imshow(lines,cmap='gray')
#plt.show()

def weighted_img(img, initial_img, α=0.8, β=1., γ=0. ):
    return cv2.addWeighted(initial_img, α, img, β, γ)

lines_edges = weighted_img(lines, img,α=0.8, β=1., γ=0. )

plt.figure(figsize=(10,8))
plt.imshow(lines_edges)
plt.show()




#https://youngest-programming.tistory.com/92 참고
# 노란색을 감지하고 흰색 감지하고 따로따로 선을
#감지하는걸로 이해했는데 여기서부턴 코드를 완성 못했습니다. 
##color = [0, 255, 255]
#pixel = np.uint8([[color]])
#hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
#hsv = hsv[0][0]
#print("bgr: ", color)
#print("hsv: ", hsv)
#img_color = cv2.imread('YW1.jpg')
#height,width = img_color.shape[:2]
#img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
#lower_yellow = (30,120-10,120-10)
#upper_yellow = (255,120+10,120+10)
#img_mask = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
#img_result = cv2.bitwise_and(img_color, img_color, mask = img_mask)
#cv2.imshow('img_color', img_color)
#cv2.imshow('img_mask', img_mask)
#cv2.imshow('img_result', img_result)

#만약 HSV로 선을 따로 분리했다면#
#def draw_lines(img, lines, color=[255,0,0], thickness=5):
#의 rgb값을 바꿔주어 선 색을 변경할 생각입니다.
#이후 hough_lines을 활용하여 중앙선을 그을 수 있다고 생각합니다..
#처음 접해보는 것이라 어려움이 많았고 모두 해결하진 못했지만 차근차근 하나씩 다시 공부해보겠습니다.
#처음엔 왼쪽 오른쪽 나눠서 잘라내고 선마다 다른 색을 입히고 둘을 붙이는 생각도 해보았는데 이에 대해서도 다시 한 번 공부해보겠습니다. 감사합니다.
