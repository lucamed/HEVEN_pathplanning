#hw2

import cv2

image = cv2.imread("cat.jpg", cv2.IMREAD_COLOR)

crop = image.copy() 

height, width, channel = image.shape

crop_size = 500

crop = image[height//2 - crop_size//2 : height//2 + crop_size//2, width//2 - crop_size//2 : width//2 + crop_size//2]

cv2.imshow("image", image)
cv2.imshow("crop", crop)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("center.jpg", crop)
