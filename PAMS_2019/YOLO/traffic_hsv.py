import numpy as np
import cv2

# Red range HSV - Hue Saturation Value
lower_red = np.array([140, 40, 40])
upper_red = np.array([179, 255, 255])
lower_red2 = np.array([1, 60, 60])
upper_red2 = np.array([34, 255, 255])

# Green range HSV
lower_green = np.array([60, 40, 40])
upper_green = np.array([98, 255, 255])


def verticalProjection(img):
    # Return a list containing the sum of the pixels in each column
    (h, w) = img.shape[:2]
    sumCols = []
    for j in range(w):
        col = img[0:h, j:j + 1]  # y1:y2, x1:x2
        sumCols.append(np.sum(col))
    return sumCols

# Inout img and coordinates of the bounding box given by yolo
def lightsParser(imgin, xmin, xmax, ymin, ymax):
                      #   0      1      2
    flag = [0, 0, 0]  # [RED, ARROW, GREEN]

    img = imgin[ymin:ymax, xmin:xmax]   # Crop BB

    orig = img.copy()
    if img.any():
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)              # Change to hsv

        hsv_red = cv2.inRange(hsv, lower_red, upper_red)
        hsv_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        hsv_red = hsv_red + hsv_red2

        hsv_green = cv2.inRange(hsv, lower_green, upper_green)

        og_array = verticalProjection(orig)                     # Histogram of original img in order to find its size
        size = int((len(og_array)) / 10)

        # Size has to be odd positive number
        if size % 2 == 0:
            size += 1

        if size <= 3:                               # Very small detections need smaller threshold
            size = 1
            threshold = 130
        else:
            threshold = 250

        mask_red = cv2.GaussianBlur(hsv_red, (size, size), 0)
        mask_green = cv2.GaussianBlur(hsv_green, (size, size), 0)

        r_array = verticalProjection(mask_red)
        g_array = verticalProjection(mask_green)

        r_mean = np.mean(r_array)
        g_mean = np.mean(g_array)

        # *** DEBUGGING ***
        cv2.imshow('OG', img)
        cv2.imshow('RED', mask_red)
        cv2.imshow('GREEN', mask_green)
        print(r_mean, g_mean, threshold)

        if r_mean > threshold:  # Red LED on
            flag[0] = 1
            if g_mean > threshold * 0.6:  # If the red LED is on check for arrow LED
                flag[1] = 1
        else:                   # If RED is off means that green is on
            flag[2] = 1
        return flag
