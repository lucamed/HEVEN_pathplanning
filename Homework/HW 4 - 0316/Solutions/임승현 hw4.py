# -*- coding: cp949 -*-
"""
The main problem of this HW is to detect both lines in a lane and its center line.

1. Open the given images.
2. There are several ways to solve this. You can google and study about lane detection. 
	HSV colors, HoughlinesP, CannyEdge and GaussianBlur are some of the functions you might need.
	Usage of OpenCV is more than recommended.

3. Draw the left side line as RED and the right side BLUE. Also, find the middle point (desired path) and draw a line in GREEN
4. Use addWeighted to add all masks on the original image.
5. The program should work for finding the lanes in at least YW1.jpg and YW2.jpg
	WW3.jpg is extra question, if you solve for it... I'll be happy.

Check the attached example [EX] images, it will be helpful in understanding the question.

"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
    
#이미지 읽기
YW1=cv2.imread("C:\\Users\임승현\Desktop\HEVEN\week3\YW1.jpg",cv2.IMREAD_COLOR)
#image 열기
print("This image is:",type(YW1),"with dimensions:",YW1.shape)
cv2.imshow("YW1",YW1)
cv2.waitKey(0)

#흑백으로 이미지 편집
gray_image=cv2.cvtColor(YW1,cv2.COLOR_RGB2GRAY)
#황색선 추출
img_hsv = cv2.cvtColor(YW1, cv2.COLOR_BGR2HSV)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
yellow_line=cv2.inRange(img_hsv,lower_yellow,upper_yellow)
#흰색선도 추출
white_line=cv2.inRange(gray_image,200,255)
mask_yw=cv2.bitwise_or(yellow_line,white_line)
mask_yw_image=cv2.bitwise_and(gray_image,mask_yw)
cv2.imshow("d",mask_yw_image)
cv2.waitKey(0)
#Canny Edge Detection 이용
canny_edges = cv2.Canny(mask_yw_image,50,150,apertureSize=3)
cv2.imshow("canny_edges",canny_edges)
cv2.waitKey(0)
#관심있는 부분만 잘라내기(삼각형으로)
(height,width,channel)=YW1.shape
region_of_interest_vertices = [
    (0, height),
    (width / 2, height / 2),
    (width, height),
]
def region_of_interest(img, vertices):
    # 까만색 마스크 생성
    mask = np.zeros_like(img)
    # 흰색 마스크 생성
    match_mask_color = (255)
    cv2.fillPoly(mask, vertices, match_mask_color)
    # 삼각형 안의 이미지만 남기기
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image
cropped_image=region_of_interest(
    canny_edges,np.array([region_of_interest_vertices],np.int32),)
cv2.imshow("cropped_image",cropped_image)
cv2.waitKey(0)
blur=cv2.GaussianBlur(cropped_image,(5,5),0)
#Hough line
lines=cv2.HoughLinesP(blur,6,np.pi/60,160,np.array([]),40,25)
print(lines) #(x1,y1,x2,y2)

def draw_lines(img,lines,color):
    img=img.copy()
    #라인을 만들기
    line_img=np.zeros((img.shape[0],img.shape[1],3),dtype=np.uint8,)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_img, (x1,y1),(x2,y2),color,5)
    
    return line_img
##왼쪽선과 오른쪽 선을 각각 만들기
left_line_x = []
left_line_y = []
right_line_x = []
right_line_y = []
center_line_x=[]  #중간점도 라인으로 만들기
center_line_y=[]

min_y=YW1.shape[0]*0.6 ##y값 최대 최소값 조정
max_y=YW1.shape[0]
for line in lines:
    for x1,y1,x2,y2 in line:
        slope=-(y1-y2) #x1-x2<0
        if slope>=0 : #왼쪽 라인
            left_line_x.extend([x1,x2])
            left_line_y.extend([y1,y2])
        else: #오른쪽 라인
            right_line_x.extend([x1,x2])
            right_line_y.extend([y1,y2])
                        
print(left_line_x)
print(right_line_x)

poly_left=np.poly1d(np.polyfit(left_line_y,left_line_x,deg=1))
left_x_start=poly_left(max_y)
left_x_end=poly_left(min_y) ## 왼쪽 선분 만들기
poly_right=np.poly1d(np.polyfit(right_line_y,right_line_x,deg=1))
right_x_start=poly_right(max_y)
right_x_end=poly_right(min_y)##오른쪽 선분
##교차점 찾기
left=np.polyfit(left_line_y,left_line_x,deg=1)
right=np.polyfit(right_line_y,right_line_x,deg=1)
intersection_x=(right[1]-left[1])/(left[0]-right[0])
intersection_y=(right[1]-left[1])*left[0]/(left[0]-right[0])+left[1]
print(intersection_x)
print(intersection_y)
##가운데 직선 만들기
tangent_of_centerline=(left[0]+right[0])/2
yaxis=tangent_of_centerline*(-1)*intersection_x+intersection_y
poly_center=np.poly1d(np.array([tangent_of_centerline,yaxis]))
print(poly_left)
print(poly_right)
print(poly_center)
center_x_start=poly_center(max_y)
center_x_end=poly_center(min_y)

##선을 각각 해당되는 색깔로 칠하기
left_array=np.array([[[left_x_start,max_y,left_x_end,min_y]]],np.int32)
right_array=np.array([[[right_x_start,max_y,right_x_end,min_y]]],np.int32)
center_array=np.array([[[center_x_start,max_y,center_x_end,min_y]]],np.int32)
left_final=draw_lines(YW1,left_array,[255,0,0])
right_final=draw_lines(YW1,right_array,[0,0,255])
center_final=draw_lines(YW1,center_array,[0,255,0])
lines_final=cv2.add(cv2.add(left_final,right_final),center_final,)
img=cv2.addWeighted(YW1,0.8,lines_final,1.0,0.0)
cv2.imshow("finalYW1.jpg",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#### ######################################################
##YW2

#이미지 읽기
YW2=cv2.imread("C:\\Users\임승현\Desktop\HEVEN\week3\YW2.jpg",cv2.IMREAD_COLOR)
#image 열기
print("This image is:",type(YW2),"with dimensions:",YW2.shape)
cv2.imshow("YW1",YW2)
cv2.waitKey(0)

#흑백으로 이미지 편집
gray_image=cv2.cvtColor(YW2,cv2.COLOR_RGB2GRAY)
#황색선 추출
img_hsv = cv2.cvtColor(YW1, cv2.COLOR_BGR2HSV)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])
yellow_line=cv2.inRange(img_hsv,lower_yellow,upper_yellow)
#흰색선도 추출
white_line=cv2.inRange(gray_image,200,255)
mask_yw=cv2.bitwise_or(yellow_line,white_line)
mask_yw_image=cv2.bitwise_and(gray_image,mask_yw)
cv2.imshow("d",mask_yw_image)
cv2.waitKey(0)
#Canny Edge Detection 이용
canny_edges = cv2.Canny(mask_yw_image,50,150,apertureSize=3)
cv2.imshow("canny_edges",canny_edges)
cv2.waitKey(0)
#관심있는 부분만 잘라내기(삼각형으로)
(height,width,channel)=YW2.shape
region_of_interest_vertices = [
    (0, height),
    (width / 2, height / 2),
    (width, height),
]
def region_of_interest(img, vertices):
    # 까만색 마스크 생성
    mask = np.zeros_like(img)
    # 흰색 마스크 생성
    match_mask_color = (255)
    cv2.fillPoly(mask, vertices, match_mask_color)
    # 삼각형 안의 이미지만 남기기
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image
cropped_image=region_of_interest(
    canny_edges,np.array([region_of_interest_vertices],np.int32),)
cv2.imshow("cropped_image",cropped_image)
cv2.waitKey(0)
blur=cv2.GaussianBlur(cropped_image,(5,5),0)
#Hough line
lines=cv2.HoughLinesP(blur,6,np.pi/60,160,np.array([]),40,25)
print(lines) #(x1,y1,x2,y2)

def draw_lines(img,lines,color):
    img=img.copy()
    #라인을 만들기
    line_img=np.zeros((img.shape[0],img.shape[1],3),dtype=np.uint8,)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_img, (x1,y1),(x2,y2),color,5)
    
    return line_img
##왼쪽선과 오른쪽 선을 각각 만들기
left_line_x = []
left_line_y = []
right_line_x = []
right_line_y = []
min_y=YW2.shape[0]*0.6 ##y값 최대 최소값 조정
max_y=YW2.shape[0]
for line in lines:
    for x1,y1,x2,y2 in line:
        slope=-(y1-y2) #x1-x2<0
        if slope>=0 : #왼쪽 라인
            left_line_x.extend([x1,x2])
            left_line_y.extend([y1,y2])
           
        else: #오른쪽 라인
            right_line_x.extend([x1,x2])
            right_line_y.extend([y1,y2])
                        
print(left_line_x)
print(right_line_x)
poly_left=np.poly1d(np.polyfit(left_line_y,left_line_x,deg=1))
left_x_start=poly_left(max_y)
left_x_end=poly_left(min_y) ## 왼쪽 선분 만들기
poly_right=np.poly1d(np.polyfit(right_line_y,right_line_x,deg=1))
right_x_start=poly_right(max_y)
right_x_end=poly_right(min_y)##오른쪽 선분
left_tangent=np.polyfit(left_line_y,left_line_x,deg=1)
right_tangent=np.polyfit(right_line_y,right_line_x,deg=1)
##가운데 직선 만들기
tangent_of_centerline=(left[0]+right[0])/2
yaxis=tangent_of_centerline*(-1)*intersection_x+intersection_y
poly_center=np.poly1d(np.array([tangent_of_centerline,yaxis]))
print(poly_left)
print(poly_right)
print(poly_center)
center_x_start=poly_center(max_y)
center_x_end=poly_center(min_y)
##선을 각각 해당되는 색깔로 칠하기
left_array=np.array([[[left_x_start,max_y,left_x_end,min_y]]],np.int32)
right_array=np.array([[[right_x_start,max_y,right_x_end,min_y]]],np.int32)
center_array=np.array([[[center_x_start,max_y,center_x_end,min_y]]],np.int32)
left_final=draw_lines(YW2,left_array,[255,0,0])
right_final=draw_lines(YW2,right_array,[0,0,255])
center_final=draw_lines(YW2,center_array,[0,255,0])
lines_final=cv2.add(cv2.add(left_final,right_final),center_final,)
img=cv2.addWeighted(YW2,0.8,lines_final,1.0,0.0)
cv2.imshow("finalYW2.jpg",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
                     
            
