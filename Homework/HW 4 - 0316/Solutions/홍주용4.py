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

def draw_lines(img, lines, color=[0, 0, 255], thickness=3): 
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap): 
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)

    return line_img

def weighted_img(img, initial_img, α=1, β=1., λ=0.): 
    return cv2.addWeighted(initial_img, α, img, β, λ)

image = cv2.imread('YW1.jpg') 
height, width = image.shape[:2] 

gray_img = grayscale(image) 
    
blur_img = gaussian_blur(gray_img, 3) 
        
canny_img = canny(blur_img, 70, 210) 

vertices = np.array([[(50,height),(width/2-45, height/2+60), (width/2+45, height/2+60), (width-50,height)]], dtype=np.int32)
ROI_img = region_of_interest(canny_img, vertices) 

hough_img = hough_lines(ROI_img, 1, 1 * np.pi/180, 30, 10, 20) 

result = weighted_img(hough_img, image) 
cv2.imshow('result',result)
cv2.waitKey(0) 
