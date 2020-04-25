#Q4-Diva
import cv2,os
import numpy as np
from PIL import Image, ImageDraw
img = cv2.imread("YW1.jpg") #callimage
grayimg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #gray scale convert
imge = cv2.equalizeHist(grayimg) #contrast change
out2 =cv2.inRange(imge, 200, 255) #white color detection
dst = cv2.GaussianBlur(out2,(5,5),cv2.BORDER_DEFAULT) #guasion blur
edges = cv2.Canny(dst,100,200,apertureSize = 3) #canny for edge
cv2.imshow('img5', edges)
a, b, chan = img.shape #image dimensions
pts = np.array([[0, a], [500, 290], [b, a]], dtype=np.int32) #triangle polygon mask
mask = np.zeros((edges.shape[0], edges.shape[1]))
cv2.fillConvexPoly(mask, pts, 1) #fill in remain with black
mask = mask.astype(np.bool)
out = np.zeros_like(edges)
out[mask] = edges[mask] #image combine with mask
lines = cv2.HoughLinesP(out,1,theta=np.pi/60,threshold=50,lines=np.array([]),minLineLength=20,maxLineGap=100) #houghlines
for line in lines: #display all lines on image
    for x1,y1,x2,y2 in line:
         if ((x2-x1)/(y2-y1))<0: #right lane then blue
             cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
         else:
             cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3) #left lane then red
#avg the first two lines
x1a=int((lines[0][0][0]+lines[1][0][2])/2)
y1a=int((lines[0][0][1]+lines[1][0][3])/2)
x2a=int((lines[0][0][2]+lines[1][0][0])/2)
y2a=int((lines[0][0][3]+lines[1][0][1])/2)
cv2.line(img, (x1a, y1a), (x2a, y2a), (0, 255, 0), 3) #display desired path in green
cv2.imshow('path.jpg', img)
cv2.waitKey(100000)
