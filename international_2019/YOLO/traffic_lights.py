import numpy as np
import cv2
import matplotlib.pyplot as plt

def verticalProjection(img):
    #Return a list containing the sum of the pixels in each column

    (h, w) = img.shape[:2]
    sumCols = []
    for j in range(w):
        col = img[0:h, j:j+1] # y1:y2, x1:x2
        sumCols.append(np.sum(col))
    return sumCols

def removeBackground(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    img[thresh == 255] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    erosion = cv2.erode(img, kernel, iterations=1)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)

def trafficLights(img, xmin, xmax, ymin, ymax):
    img = img[ymin:ymax, xmin:xmax]
    removeBackground(img)

    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, img) = cv2.threshold(grayImage, 115, 255, cv2.THRESH_BINARY)
    img_info = verticalProjection(img)

    flag = [0,0,0,0]
    size = int((len(img_info))/4)
    mean = np.mean(img_info)

    p0 = 0
    p1 = size
    p11 = size*2
    p2 = size*3
    p22 = size*4
    p3 = size*5
    p4 = size*6
    red_check = np.array(e[p:p11])
    yellow_check = np.array(e[p11:p2])
    arrow_check = np.array(e[p2:p22])
    green_check = np.array(e[p22:p3])
    if np.mean(red_check) > mean_red:
        flag[0] = 1
    if np.mean(yellow_check) > mean:
        flag[1] = 1
    if np.mean(arrow_check) > mean*0.8:
        flag[2] = 1
    if np.mean(green_check) > mean:
        flag[3] = 1
    return flag
