"""
1. Crop the center 500x500 size image using Pillow or OpenCV library in python.

2. Save the cropped image.

You can use any image that you want, but I attached some sample images as example.
"""


import cv2


photo=cv2.imread("cat.jpg",cv2.IMREAD_COLOR)
[a,b,c]=photo.shape
i=a//2
j=b//2
cropped=photo.copy()
cropped=photo[i-250:i+250,j-250:j+250]
cv2.imshow("photo",photo)
cv2.imshow("cropped",cropped)

cv2.imwrite('cropcat500.jpg',cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
