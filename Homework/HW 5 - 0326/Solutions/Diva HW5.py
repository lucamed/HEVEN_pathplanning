#HW5-Diva
import cv2,os
import numpy as np
from PIL import Image, ImageDraw
#cap = cv2.VideoCapture("WW.mp4") #get video
while(cap.isOpened()):
    ret, frame = cap.read()  #get ret and frame
    img=frame
    if ret is False:
        print("end") #video has ended when ret is false
        break;
    else:
        grayimg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #gray scale convert
        i = cv2.equalizeHist(grayimg)
        imge = cv2.equalizeHist(i) #contrast change
        out2 =cv2.inRange(imge, 200, 255) #white color detection
        dst = cv2.GaussianBlur(out2,(5,5),cv2.BORDER_DEFAULT) #guasion blur
        edges = cv2.Canny(dst,100,200,apertureSize = 3) #canny for edge
        cv2.imshow('img5', edges)
        a, b, chan = img.shape  # image dimensions
        pts = np.array([[0, a], [500, 290], [b, a]], dtype=np.int32)  # triangle polygon mask
        mask = np.zeros((edges.shape[0], edges.shape[1]))
        cv2.fillConvexPoly(mask, pts, 1)  # fill in remain with black
        mask = mask.astype(np.bool)
        out = np.zeros_like(edges)
        out[mask] = edges[mask]  # image combine with mask
        lines = cv2.HoughLinesP(out, 1, theta=np.pi / 60, threshold=33, lines=np.array([]), minLineLength=50,maxLineGap=200)  # houghlines
     #create list for different points.
        x_right2 = []
        x_left2 = []
        y_right2 = []
        y_left2 = []
        for line in lines:  # display all lines on image
            for x1, y1, x2, y2 in line:
                if (y2 - y1)/(x2-x1)!=0:
                    if ((x2 - x1) / (y2 - y1)) < -1:  # right lane then blue
                        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        x_right2.append(x2)
                        y_right2.append(y2)
                    elif (((x2 - x1) / (y2 - y1))) > 1:
                        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)  # left lane then red
                        x_left2.append(x1)
                        y_left2.append(y1)
        x2a = int((sorted(x_right2)[-1] + sorted(x_left2)[0]) / 2)
        y2a = int((sorted(y_right2)[0] + sorted(y_left2)[0]) / 2)
        cv2.line(img, (x2a, y2a), (int(b / 2), int(a)), (0, 255, 0), 3)  # display desired path in green
        cv2.imshow('path.jpg', img)
        cv2.waitKey(10)
