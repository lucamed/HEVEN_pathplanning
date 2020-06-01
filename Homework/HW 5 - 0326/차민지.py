import numpy as np
from PIL import ImageGrab
import cv2
import numpy
import os

cap = cv2.VideoCapture("data/YW.mp4")

while cap.isOpened():
    ret, frame = cap.read()

    if ret is False:
        break

    h, w, _ = frame.shape

    # Convert to gray image
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur Image. remoces noise and unnecessary edges
    blur_gray = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Canny
    low_threshlod = 50
    high_threshold = 150

    edges = cv2.Canny(blur_gray, low_threshlod, high_threshold)

    # ROI mask
    imshape = frame.shape
    mask = np.zeros_like(frame)
    vertices = np.array([[(0, imshape[0]), (450, 320), (520, 320), (imshape[1], imshape[0])]], dtype=np.int32)
    cv2.fillPoly(mask, vertices, (255, 255, 255))
    cv2.imshow("MM", mask)
    gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    masked_edges = cv2.bitwise_and(edges, gray_mask)

    # HoughLines
    rho = 2  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 40  # minimum number of pixels making up a line
    max_line_gap = 30  # maximum gap in pixels between connectable line segments
    line_image = np.copy(frame) * 0  # creating a blank to draw lines on

    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    # left_x1, left_x2, left_y1, left_y2, right_x1, right_x2, right_y1, right_y2
    values = [0] * 8
    l_cnt = 0
    r_cnt = 0

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = abs((y2 - y1) / (x2 - x1))
            if slope < 0.5:
                continue
            l_flag = True
            r_flag = True
            if y1 > y2:
                if l_flag:
                    dots = [x1, x2, y1, y2]
                    values[0:4] = dots
                    l_flag = False

                if x1 < values[0]:
                    values[0] = x1
                if x2 > values[1]:
                    values[1] = x2
                if y1 < values[2]:
                    values[2] = y1
                if y2 > values[3]:
                    values[3] = y2

                # l_cnt += 1
                # values[0:4] = [sum(x) for x in zip(values[0:4], [x1, y1, x2, y2])]
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
            else:
                if r_flag:
                    dots = [x1, x2, y1, y2]
                    values[4:] = dots
                    r_flag = False

                if x1 < values[4]:
                    values[4] = x1
                if x2 > values[5]:
                    values[5] = x2
                if y1 < values[6]:
                    values[6] = y1
                if y2 > values[7]:
                    values[7] = y2

                # r_cnt += 1
                # values[4:] = [sum(x) for x in zip(values[4:], [x1, y1, x2, y2])]
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 10)
    print("FIN", values)
    cv2.line(line_image, (int((values[0] + values[4]) / 2), int((values[2] + values[6]) / 2)),
             (int((values[1] + values[5]) / 2), int((values[3] + values[7]) / 2)), (0, 255, 0), 10)

    lines_edges = cv2.addWeighted(frame, 0.8, line_image, 1, 0)

    cv2.imshow("lines", lines_edges)
    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
