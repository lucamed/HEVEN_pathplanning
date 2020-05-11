'''
The main problem of this HW is to detect both lines in a lane and its center line.

1. Open the given videos.
2. There are several ways to solve this. You can google and study about lane detection.
	HSV colors, HoughlinesP, CannyEdge and GaussianBlur are some of the functions you might need.
	Usage of OpenCV is more than recommended.

3. Draw the left side line as RED and the right side BLUE. Also, find the middle point (desired path) and draw a line in GREEN
4. Use addWeighted to add all masks on the original image.
5. The program should work for finding the lanes in at least YW.mp4 and YW.mp4


Check the attached example output videos, it will be helpful in understanding the question.
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    print(image.shape)
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            '''
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
                '''
            left_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    #right_fit_average = np.average(right_fit, axis=0)
    #left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, left_fit_average)
    return np.array([right_line])

def canny(image):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def display_lines_blue(image, lines):
    line_image = np.zeros_like(image)   #create black image
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

def display_lines_red(image, lines):
    line_image = np.zeros_like(image)   #create black image
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 10)
    return line_image


def region_of_interest_left(image):
    height = image.shape[0]
    polygons = np.array([
        [(100, height), (500, height), (500, 300)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def region_of_interest_right(image):
    height = image.shape[0]
    polygons = np.array([
        [(500, height), (900, height), (500, 300)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

#def middle_line

cap = cv2.VideoCapture("YW.mp4")
while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image_left = region_of_interest_left(canny_image)
    cropped_image_right = region_of_interest_right(canny_image)
    lines_left = cv2.HoughLinesP(cropped_image_left, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    lines_right = cv2.HoughLinesP(cropped_image_right, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    #averaged_lines_right = average_slope_intercept(frame, lines_right)     #TypeError: 'numpy.float64' object is not iterable 오류가 자꾸 생겨서 실행하지 못헀습니다...
    line_image_left = display_lines_red(frame, lines_left)
    line_image_right = display_lines_blue(frame, lines_right)
    lines_added = cv2.addWeighted(line_image_left, 1, line_image_right, 1, 1)
    combo_image = cv2.addWeighted(frame, 0.8, lines_added, 1, 1)
    #combo_image = cv2.addWeighted(combo_image_1, 0.8, line_image_right, 1, 1)
    cv2.imshow("result", combo_image)
    if cv2.waitKey(10) & 0xFF == ord('q'): #wait 10ms btw each frame
        break
cap.release()
cv2.destroyAllWindows()


##plt.show()
