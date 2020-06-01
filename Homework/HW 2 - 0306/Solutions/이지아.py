import cv2

image = cv2.imread("500x500image.jpg")
cropped_image = image[200:300, 250:320]

cv2.imshow("cropped", cropped_image)
cv2.imwrite("cropped_cat.jpg", cropped_image)
cv2.waitkey(0)
cv2.destroyAllWindows()

