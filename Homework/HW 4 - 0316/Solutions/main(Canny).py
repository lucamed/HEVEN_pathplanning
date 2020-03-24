'''
This program uses the base of CannyEdge to detect yellow and white lane lines. There are many other solutions to this.
It also separates between left and right ROI giving the following color relationship: 
    Left-Red Middle-Green Right-Blue 

1. Opens the image. Transform into gray.
2. Extracts edges by CannyEdge.
3. Sums both detection masks and split into Right and Left masks.
4. In the function drawLines, HoughLinesP is used to find lines in both masks and draw the respective color .
    It also finds in function pointC an extention of the line, in order to give a better visualization of the drawn lines.
    Given 2 points by HoughLinesP, its calculated a 3 point with a given length.

5. Find the point where both lines intersect giving then an expected goal path. With that coordinate we can find the needed (X,Y) for the green line.
6. Find a cooresponding x for a given y in the line. Like this its possible to decide x (middle point) of the green line by calculating distLine1-distLine2/2.
7. Draw the green line as following.
    x1 y1: halfway point of both lane lines
    x2 y2: based on the end point of the lines and intersection of both lines.

8. Add the lines into the original frame.

Luca Medeiros 03/24/2020

'''

import cv2
import numpy as np


# HSV Parameters
low_yellow = np.array([18, 94, 140])
up_yellow = np.array([48, 255, 255])

sens = 25
low_white = np.array([0, 0, 255-sens])
up_white = np.array([255, sens, 255])


def intersect_helper(a) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# Intersection of both lines (path target)
def seg_intersect(a1, a2, b1, b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = intersect_helper(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )

    # Returns x, y
    return (num / denom.astype(float))*db + b1

# Given 2 points, find a 3rd at certain distance
def pointC(p1, p2):
    lenAB = np.sqrt(np.power(p1[0] - p2[0], 2)+np.power(p1[1] - p2[1], 2))
    length = 220 - lenAB
    
    
    cx = p2[0] + (p2[0] - p1[0]) / lenAB * length
    cy = p2[1] + (p2[1] - p1[1]) / lenAB * length

    p1, p2 = p2, p1
    length = 220 
    cx2 = p2[0] + (p2[0] - p1[0]) / lenAB * length
    cy2 = p2[1] + (p2[1] - p1[1]) / lenAB * length

    return cx, cy, cx2, cy2

def drawLines(line_image, mask, side):

    rho = 3 # distance resolution in pixels of the Hough grid
    theta = np.pi/180 # angular resolution in radians of the Hough grid
    threshold = 160     # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 40  #minimum number of pixels making up a line
    max_line_gap = 150    # maximum gap in pixels between connectable line segments

    lines_ = cv2.HoughLinesP(mask, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
    dot1 = np.array([lines_[:][:][0][0][2], lines_[:][:][0][0][3]])
    dot2 = np.array([lines_[:][:][0][0][0], lines_[:][:][0][0][1]])
    
    if side == 'left':
        color = (0, 0, 255)
        # Swaps points in order to maintain format: dot1 being on the bottom and dot2 end of line
        dot1, dot2 = dot2, dot1

    elif side == 'right':
        color = (255, 0, 0)

    cx, cy, cx2, cy2 = pointC(dot1, dot2)
    cv2.line(line_image,(int(cx2), int(cy2)), (int(cx), int(cy)), color, 10)

    for line in lines_:
        for x1,y1,x2,y2 in line:
            cv2.line(line_image, (x1,y1), (x2,y2), color, 10)

    return line_image, dot1, dot2

def ROI(frame):
    # Mask ROI for left and right 
    maskR_ = np.zeros_like(frame)  
    maskL_ = np.zeros_like(frame)  

    ignore_mask_color = 255

    imshape = frame.shape
    
    verticesL = np.array([[(0, imshape[0]),(int(imshape[1]/2), int(40+imshape[0]/2)), (int(imshape[0]/2), imshape[1]), (0, imshape[1])]], dtype=np.int32)
    verticesR = np.array([[(imshape[1], imshape[0]),(int(imshape[1]/2), int(40+imshape[0]/2)), (int(imshape[0]/2), imshape[1]), (imshape[1], imshape[1])]], dtype=np.int32)

    cv2.fillPoly(maskR_, verticesR, ignore_mask_color)
    cv2.fillPoly(maskL_, verticesL, ignore_mask_color)

    maskR = cv2.bitwise_and(frame, maskR_)
    maskL = cv2.bitwise_and(frame, maskL_)

    return maskL, maskR


frame = cv2.imread('data/WW1.jpg')
line_image = np.copy(frame)*0 # creating a blank to draw lines on
frame = cv2.GaussianBlur(frame, (5, 5), 0)

gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
canny_image = cv2.Canny(gray_image, 100, 200)

mask_left, mask_right = ROI(canny_image)

cv2.imshow('finalL', mask_left)
cv2.imshow('fin3al', mask_right)

line_image, dotL1, dotL2 = drawLines(line_image, mask_left, 'left')
line_image, dotR1, dotR2 = drawLines(line_image, mask_right, 'right')


inter = seg_intersect(dotL1, dotL2, dotR1, dotR2)
cv2.circle(line_image,(int(inter[0]), dotL2[1]), 10, (255,160,255))
y_findR = dotL1[1]
y_findL = dotR1[1]
slopeR = (dotR2[1] - dotR1[1])/(dotR2[0] - dotR1[0])
slopeL = (dotL2[1] - dotL1[1])/(dotL2[0] - dotL1[0])
x_of_yR = dotR1[0] + (y_findR - dotR1[1])/slopeR
x_of_yL = dotL1[0] + (y_findL - dotL1[1])/slopeL


cv2.line(line_image,(int(x_of_yL+((dotR1[0]-x_of_yL)/2)), dotR1[1]),(int(inter[0]), dotL2[1]), (0,255,0), 6)


final = cv2.addWeighted(frame, 0.8, line_image, 1, 0)


cv2.imshow('final', final)
cv2.waitKey(0)
