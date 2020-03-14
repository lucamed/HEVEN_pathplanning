import cv2


image = cv2.imread("cat.jpg")
cropping = image[250:750, 250:750]
cv2.imshow("crop", cropping)
cv2.waitKey(0)

cv2.imwrite("cropcat500.jpg", cropping)

