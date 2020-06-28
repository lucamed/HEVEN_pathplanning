import cv2
import numpy as np

video = cv2.VideoCapture('./parking_right3.avi')

# Every color except white
low = np.array([0, 0, 240])
high = np.array([255, 40, 255])


while video.isOpened():
    _, frame = video.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # create the Mask
    mask = cv2.inRange(hsv_frame, low, high)
    _, conts, _ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for cont in conts:
        cv2.drawContours(frame, cont, -1, (0, 0, 255), 3)

    cv2.imshow("mask", mask)
    cv2.imshow("video", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
