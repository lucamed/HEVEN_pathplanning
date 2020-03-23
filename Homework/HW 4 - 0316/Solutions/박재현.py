import cv2 
import numpy as np

def grayscale(img): 
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def canny(img, low_threshold, high_threshold): 
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices, color3=(255,255,255), color1=255): 
    mask = np.zeros_like(img) 
    if len(img.shape) > 2:
        color = color3
    else:
        color = color1
    cv2.fillPoly(mask, vertices, color)
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image

def draw_r_lines(img, lines, color=[0, 0, 255], thickness=2): # 빨간 선 그리기
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)
def draw_b_lines(img, lines, color=[255, 0, 0], thickness=2): # 파란 선 그리기
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)
def draw_g_lines(img, lines, color=[0, 255, 0], thickness=2) : # 초록 선 그리기
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    #line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    #draw_lines(line_img, lines)

    return lines

def weighted_img(img, initial_img, α=1, β=1., λ=0.): 
    return cv2.addWeighted(initial_img, α, img, β, λ)

image = cv2.imread('YW1.jpg') 
height, width = image.shape[:2]

gray_img = grayscale(image) 
    
blur_img = gaussian_blur(gray_img, 3) 
        
canny_img = canny(blur_img, 70, 210) 

vertices = np.array([[(50,height),(width/2-45, height/2+60), (width/2+45, height/2+60), (width-50,height)]], dtype=np.int32)
ROI_img = region_of_interest(canny_img, vertices)

line_arr = hough_lines(ROI_img, 1, 1 * np.pi/180, 30, 10, 20) 
line_arr = np.squeeze(line_arr)
    

slope_degree = (np.arctan2(line_arr[:,1] - line_arr[:,3], line_arr[:,0] - line_arr[:,2]) * 180) / np.pi


line_arr = line_arr[np.abs(slope_degree)<160]
slope_degree = slope_degree[np.abs(slope_degree)<160]

line_arr = line_arr[np.abs(slope_degree)>95]
slope_degree = slope_degree[np.abs(slope_degree)>95]

L_lines, R_lines = line_arr[(slope_degree>0),:], line_arr[(slope_degree<0),:]
temp = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
L_lines, R_lines = L_lines[:,None], R_lines[:,None]

draw_r_lines(temp, L_lines)
draw_b_lines(temp, R_lines)

result = weighted_img(temp, image) 
cv2.imshow('result',result) 
cv2.waitKey(0)

#가운데 선그리기 부분을 해결하지 못했습니다..
