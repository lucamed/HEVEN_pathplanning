'''
1. Crop the center 500x500 size image using Pillow or OpenCV library in python.

2. Save the cropped image.

You can use any image that you want, but I attached some sample images as example.
'''

import cv2

src = cv2.imread("C:/Users/user/Desktop/cat.jpg", cv2.IMREAD_COLOR)

cv2.imshow("cat", src)

height, width, channel = src.shape

cropped = src[(int)(height/2)-250:(int)(height/2)+250, (int)(width/2)-250:(int)(width/2)+250]

cv2.imwrite("C:/Users/user/Desktop/cropped.jpg", cropped)
cv2.imshow("cropped", cropped)
cv2.waitKey(0)

cv2.destroyAllWindows()

