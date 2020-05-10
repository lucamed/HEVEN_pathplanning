import cv2
import numpy as np
#빨간선 테두리 찾기
def yellow_lane_finder(img):
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    low_yellow = np.array([18,94,140])
    up_yellow = np.array([48,255,255])
    yellow_mask = cv2.inRange(hsv_img, low_yellow, up_yellow)
    yellow_edge = cv2.Canny(yellow_mask, 75, 150)
    return yellow_edge

#흰선 테두리 찾기
def white_lane_finder(img):
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    low_white = np.array([200,200,200])
    up_white = np.array([255,255,255])
    white_mask = cv2.inRange(blur, low_white, up_white)
    white_edge = cv2.Canny(white_mask, 75, 150)
    return white_edge

#관심영역찾기
def ROI(edge):
    mask = np.zeros_like(edge)
    height, width = edge.shape
    vertices = np.array([[(100, height), (450, 320), (550, 320), (width - 20, height)]], dtype=np.int32)
    cv2.fillPoly(mask, vertices, (255))
    edge = cv2.bitwise_and(edge, mask)
    return edge
#선그리기
def draw_line(white_edge, yellow_edge, img):
    y_point = cv2.HoughLinesP(yellow_edge, 1, np.pi / 180, 100, minLineLength=20, maxLineGap=100)
    w_point = cv2.HoughLinesP(white_edge, 1, np.pi / 180, 20, minLineLength=20, maxLineGap=100)

    #노란선 연장하여 그리기
    Y_y1 = 540
    Y_y2 = 320
    Y_x1 = int((Y_y1-y_point[0][0][1])*(y_point[0][0][0]-y_point[0][0][2])/(y_point[0][0][1]-y_point[0][0][3])+y_point[0][0][0])
    Y_x2 = int((Y_y2-y_point[0][0][1])*(y_point[0][0][0]-y_point[0][0][2])/(y_point[0][0][1]-y_point[0][0][3])+y_point[0][0][0])
    cv2.line(img, (Y_x1,Y_y1), (Y_x2, Y_y2), (0, 0, 255), 5)

    #흰선 연장하여 그리기
    w_y1 = 540
    w_y2 = 320
    w_x1 = int(
        (w_y1 - w_point[0][0][1]) * (w_point[0][0][0] - w_point[0][0][2]) / (w_point[0][0][1] - w_point[0][0][3]) + w_point[0][0][0])
    w_x2 = int((w_y2 - w_point[0][0][1]) * (w_point[0][0][0] - w_point[0][0][2]) / (w_point[0][0][1] - w_point[0][0][3]) +
        w_point[0][0][0])
    cv2.line(img, (w_x1, w_y1), (w_x2, w_y2), (255,0,0), 5)

    #중심선 그리기
    c_y1 = 540
    c_y2 = 320
    c_x1 = int((Y_x1+w_x1)/2)
    c_x2 = int((Y_x2 + w_x2) / 2)
    cv2.line(img, (c_x1, c_y1), (c_x2, c_y2), (0, 255, 0), 5)
    return img


cap = cv2.VideoCapture('YW.MP4')
fourcc = cv2.VideoWriter_fourcc(*'FMP4')
width = int(cap.get(3))
height = int(cap.get(4))
writer = cv2.VideoWriter('YW_out.mp4', fourcc, 30.0, (width, height))
while (cap.isOpened()):
    ret, frame = cap.read()
    #파일끝나면 break
    if ret == False:
        break
    copy = frame.copy()
    y_edge = yellow_lane_finder(copy)
    w_edge = white_lane_finder(copy)
    y_edge = ROI(y_edge)
    w_edge = ROI(w_edge)
    copy = draw_line(w_edge,y_edge,copy)
    writer.write(copy)
cap.release()
writer.release()