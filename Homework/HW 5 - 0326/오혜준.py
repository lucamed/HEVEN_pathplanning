import numpy as np
from PIL import Image
import cv2


def final_line_list(line_list, isleft):
    final_list = [0, 0, 0, 0]
    for line in line_list:
        if isleft:
            final_list[0] += line[0]
            final_list[1] += line[1]
            final_list[2] += line[2]
            final_list[3] += line[3]
        else:
            final_list[0] += line[2]
            final_list[1] += line[3]
            final_list[2] += line[0]
            final_list[3] += line[1]
    if len(line_list) !=0:
        final_list = [int(x / len(line_list)) for x in final_list]
        return final_list


# call the video source
cap = cv2.VideoCapture('YW.mp4')

while (cap.isOpened()):
    ret, road = cap.read()
    x = cap.get(3)
    y = cap.get(4)

    gray_image = cv2.cvtColor(road, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(road, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 100, 100], dtype="uint8")
    upper_yellow = np.array([30, 255, 255], dtype="uint8")
    mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(gray_image, 200, 255)
    mask_yw = cv2.bitwise_or(mask_white, mask_yellow)
    mask_yw_image = cv2.bitwise_and(gray_image, mask_yw)

    # Gaussian blur will help to suppress noise in Canny Edge Detection by averaging out the pixel values in a neighborhood.
    gauss_gray = cv2.GaussianBlur(mask_yw_image, (5, 5), 0)

    # Canny Edge Detection
    low_threshold = 50
    high_threshold = 150
    canny_edges = cv2.Canny(gauss_gray, low_threshold, high_threshold)

    # create region of interest (ROI) mask
    # y range, x range
    gray_road = cv2.cvtColor(road, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(gray_road.shape, np.int8)
    mask[285:] = 255
    image = np.array(Image.fromarray(mask.astype('uint8'), 'L'))

    img_result = cv2.bitwise_and(image, image, mask=canny_edges)

    lines = cv2.HoughLines(img_result, 1, np.pi / 180, 80)

    left_list = []
    left_cnt = 0
    right_list = []
    right_cnt = 0
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        slope = (y2 - y1) / (x2 - x1)

        # 왜 slope < 0 left -> opencv 좌표는 왼쪽 위가 0,0
        if slope < 0:
            new_x = x2
            while y2 < 285:
                new_x -= 1
                y2 -= slope
            y2 = int(y2)

            while y1 > y:
                x1 += 1
                y1 += slope

            left_list.append([x1, y1, new_x, y2])
            left_cnt += 1
            # cv2.line(road, (x1, y1), (new_x, y2), (0, 255, 0), 2)
        if slope > 0:
            y1 = 0
            new_x = x2
            while y1 < 285:
                new_x -= 1
                y1 = y2 - slope * new_x
            y1 = int(y1)

            while y2 > y:
                x2 -= 1
                y2 -= slope

            right_list.append([new_x, y1, x2, y2])
            right_cnt += 1
            # cv2.line(road, (new_x, y1), (x2, y2), (0, 0, 255), 2)

    final_left_list = final_line_list(left_list, True)
    final_right_list = final_line_list(right_list, False)

    # 왼쪽 G, 오른쪽 R
    if final_left_list and final_right_list is not None:

        cv2.line(road, (final_left_list[0], final_left_list[1]), (final_left_list[2], final_left_list[3]), (0, 255, 0), 2)
        cv2.line(road, (final_right_list[0], final_right_list[1]), (final_right_list[2], final_right_list[3]), (0, 0, 255),
             2)

        center_list = [int((final_left_list[i] + final_right_list[i]) / 2) for i in range(4)]

        cv2.line(road, (center_list[0], center_list[1]), (center_list[2], center_list[3]), (255, 0, 0), 2)
        cv2.imshow('image', road)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
road.release()
cv2.destroyAllWindows()