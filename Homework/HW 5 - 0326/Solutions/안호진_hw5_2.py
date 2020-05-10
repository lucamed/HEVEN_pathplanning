import cv2
import numpy as np

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def canny(img, low, high):
    return cv2.Canny(img, low, high)

def gaussian_blur(img, size):
    return cv2.GaussianBlur(img, (size, size), 0)

def roi(img, vertices):

    mask = np.zeros_like(img)
    
    if len(img.shape) > 2:
        color = (255,255,255)
    else:
        color = 255

    cv2.fillPoly(mask, vertices, color)

    roi_image = cv2.bitwise_and(img, mask)
    return roi_image

def draw_lines(img, lines):
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), [0, 0, 255], 2)

def hough(img, rho, theta, threshold, len_min, gap_max):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), len_min, gap_max)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    draw_lines(line_img, lines)

    return line_img

def overlap(img, initial_img):
    return cv2.addWeighted(initial_img, 1, img, 1, 0)

cap = cv2.VideoCapture('WW.mp4')

while(cap.isOpened()):
    ret, image = cap.read()

    height, width = image.shape[:2]

    gray = grayscale(image)
    
    blur = gaussian_blur(gray, 3)
        
    canny_img = canny(blur, 70, 210)

    vertices = np.array([[(50,height),(width/2-45, height/2+60), (width/2+45, height/2+60), (width-50,height)]], np.int32)
    roi_img = roi(canny_img, vertices)

    new_img = hough(roi_img, 1, 1 * np.pi/180, 30, 10, 20)

    result = overlap(new_img, image)
    cv2.imshow('result',result)
    
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

cap.release()
cv2.destroyAllWindows()
