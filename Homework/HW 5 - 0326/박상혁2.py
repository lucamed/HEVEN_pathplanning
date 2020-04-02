import matplotlib.pylab as plt
import cv2
import numpy as np

def do_canny(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 100, 200)
    return canny

def do_segment(frame):
    height = frame.shape[0]
    width = frame.shape[1]
    polygons = np.array([
                            [(0, height), (width, height), (500, 300)]
                        ])
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, polygons, 255)
    segment = cv2.bitwise_and(frame, mask)
    return segment

def calculate_lines(frame, lines):
    left = []
    right = []    
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)         
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        y_intercept = parameters[1]
        if slope < 0:
            left.append((slope, y_intercept))
        else:
            right.append((slope, y_intercept))
            
    left_avg = np.average(left, axis = 0)
    right_avg = np.average(right, axis = 0)
    left_line = calculate_coordinates(frame, left_avg)
    right_line = calculate_coordinates(frame, right_avg)
    return np.array([left_line, right_line])

def calculate_coordinates(frame, parameters):
    try:
        slope, intercept = parameters
    except TypeError:
        slope, intercept = 0.001, 0

    y1 = frame.shape[0]
    y2 = int(y1 - 180)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def visualize_lines(frame, lines):
    lines_visualize = np.zeros_like(frame)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(lines_visualize, (x1, y1), (x2, y2), (0, 0, 255), 5)
    return lines_visualize

cap = cv2.VideoCapture("WW.mp4")
while (cap.isOpened()):
    _, frame = cap.read()
    canny = do_canny(frame)
    #cv2.imshow("canny", canny)
    segment = do_segment(canny)
    hough = cv2.HoughLinesP(segment, 2, np.pi/180, 100, np.array([]), minLineLength = 40, maxLineGap = 50)
    lines = calculate_lines(frame, hough)
    lines_visualize = visualize_lines(frame, lines)
    #cv2.imshow("hough", lines_visualize)
    output = cv2.addWeighted(frame, 0.8, lines_visualize, 1, 1)
    cv2.imshow("output", output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv.destroyAllWindows()
