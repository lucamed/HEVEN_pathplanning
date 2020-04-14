import cv2
import numpy
image = cv2.imread('cat.jpg',cv2.IMREAD_UNCHANGED)
(a1,a2) = image.shape[:2]
crop = image[round(a1/2)-250:round(a1/2)+250,round(a2/2)-250:round(a2/2)+250]
cv2.imwrite('crop.jpg',crop)
