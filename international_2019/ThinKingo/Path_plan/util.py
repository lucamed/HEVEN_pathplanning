# -*- coding: utf-8 -*-
import numpy as np
import cv2
#색상 범위 HSV
boundaries = [
    (np.array([161, 155, 84], dtype="uint8"), np.array([179, 255, 255], dtype="uint8")), # red1
    (np.array([0, 100, 70], dtype="uint8"), np.array([20, 255, 255], dtype="uint8")), # red2
    (np.array([94, 80, 200], dtype="uint8"), np.array([126, 255, 255], dtype="uint8")), # blue
    (np.array([10, 30, 50], dtype="uint8"), np.array([25, 255, 255], dtype="uint8")), #yellow
    (np.array([0, 0, 180], dtype="uint8"), np.array([180, 25, 255], dtype="uint8")) # white
]


def reg_of_int(img): # 이미지에서 roi 잘라내기
    height, width = img.shape[:2]
    #roi설정을 위한 vertics, 위부터 차례대로 왼쪽 위, 왼쪽 아래, 오른쪽 아래, 오른쪽 위다.
        
    vertics = np.array([[(int(0.4*width), int(0.05*height)),
                          (int(-2*width), int(0.8*height)),
                          (int(3*width), int(0.8*height)),
                          (int(0.6*width), int(0.05*height))]])
    
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertics, (255,255,255))
    mask = cv2.bitwise_and(img, mask)
    return mask

def draw_points(img, x_points, y_points, color, thickness):

    try:
        for i in range(len(x_points)):
            if(x_points[i]!=None):
                cv2.line(img, (int(x_points[i]), int(y_points[i])), (int(x_points[i]), int(y_points[i])),
                         color, thickness=3)
    except:
        print("error2")

def warp_image(img,display): # 이미지 원근 변환
    
    height, width = img.shape[:2]
    
    pts1 = np.float32([(0.45*width, 0.07*height),
                       (0.1*width, 0.4*height),
                       (0.9*width, 0.4*height),
                       (0.55*width, 0.07*height)])
    
    temp1,temp2 = display[:2]
    
    pts2 = np.float32([(0.4*temp1, -0.4*temp2),
                       (0.4*temp1, 1*temp2),
                       (0.6*temp1, 1*temp2),
                       (0.6*temp1, -0.4*temp2)])
    
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped_img = cv2.warpPerspective(img, M, display,flags=cv2.INTER_CUBIC+cv2.INTER_LINEAR)
    return warped_img

def get_birdview(img,display = (800,600)):
    mtx = np.array([[1.03223922e+03, 0.00000000e+00, 3.83576223e+02],
                    [0, 1.09843870e+03, 3.16372021e+02],
                    [0, 0, 1.00000000e+00]])
    dist = np.array([[1.50968260e-01, -2.00958085e+00, -6.04807148e-03, -4.80908654e-03,
                      7.14436124e+00]])

    pts1 = np.float32([(348, 28),
                       (18, 263),
                       (798, 263),
                       (463, 28)])

    pts2 = np.float32([(348, 0),
                       (348, 600),
                       (463, 600),
                       (463, 0)])
    #img = cv2.undistort(img, mtx, dist, None, mtx)
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped_img = cv2.warpPerspective(img, M, display, flags=cv2.INTER_CUBIC+cv2.INTER_LINEAR)
    return warped_img


def Detect(img):
    #th_sobelx, th_sobely, th_mag, th_dir = (35, 100), (30, 255), (30, 255), (0.7, 1.3)
    #th_h, th_l, th_s = (10, 100), (0, 60), (85, 255)
    #combined_gradient = gradient_combine(img, th_sobelx, th_sobely, th_mag, th_dir)
    combined_hsv = cv2.cvtColor(np.zeros_like(img), cv2.COLOR_BGR2GRAY)
    
    for color in ['w', 'b']:
        detected = detectcolor(img, color)
        combined_hsv = cv2.bitwise_or(combined_hsv, detected)
        
    #blur_img = cv2.GaussianBlur(img, (7,7), 10)
    #L2 정규화 추가로 noise 제거
    #img2 = cv2.cvtColor(img,cv2.COLOR_HSV2BGR)
    #canny_img = cv2.Canny(img2, 150, 230, edges = None, apertureSize = 3, L2gradient=True)
    #combined_result = comb_result(canny_img, combined_hsv)
    return combined_hsv
    
    
def detectcolor(img, color): # color = b, r, w, y / 이미지 상에서 색을 찾아 리턴
    minRange, maxRange = 0, 0
    if color == "w":
        (minRange, maxRange) = boundaries[4]
        mask = cv2.inRange(img, minRange, maxRange)
    elif color == "y":
        (minRange, maxRange) = boundaries[3]
        mask = cv2.inRange(img, minRange, maxRange)
    elif color == "b":
        (minRange, maxRange) = boundaries[2]
        mask = cv2.inRange(img, minRange, maxRange)
    elif color == "r":
        (minRange, maxRange) = boundaries[0]
        mask = cv2.inRange(img, minRange, maxRange)
        (minRange, maxRange) = boundaries[1]
        mask = mask + cv2.inRange(img, minRange, maxRange)
    else:
        print("In Image_util.py DetectColor - Wrong color Argument")
    return mask

def closeimage(img,kernel = np.ones((7,7), np.uint8)):
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

def comb_result(grad, hls):
    """ give different value to distinguish them """
    result = np.zeros_like(hls).astype(np.uint8)
    #result[((grad > 1) | (hls > 1))] = 255
    result[(grad > 1)] = 100
    result[(hls > 1)] = 255

    return result

def smoothing(lines, pre_lines=3, display = (800,600)):
    # collect lines & print average line
    lines = np.squeeze(lines)
    avg_line = np.zeros((display[1]))

    for ii, line in enumerate(reversed(lines)):
        if ii == pre_lines:
            break
        avg_line += line
    avg_line = avg_line / pre_lines

    return avg_line

def make_binary(original_img,display): # 이진화 이미지를 만드는 함수
    img = reg_of_int(original_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #get_color(img, display)
    img = Detect(img)
    #img = self.closeimage(img,7)
    img = warp_image(img,display)
    #img = get_birdview(img,display)
          
    return img

def get_color(img, display):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    left_high = (int(0.2*img.shape[1]), int(0.8*img.shape[0]))
    right_low = (int(0.8*img.shape[1]), int(1*img.shape[0]))
    img1 = img[left_high[1]:right_low[1], left_high[0]:right_low[0]]
    img = cv2.rectangle(img, left_high, right_low, (0, 255, 0), 2)
    img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    # cv2.imshow('img1', img)
    h, s, v = cv2.split(img1)
    avg = np.mean(h)
    # print(avg)
    if(avg > 171 or avg<10):
        return True
    else:
        return False
