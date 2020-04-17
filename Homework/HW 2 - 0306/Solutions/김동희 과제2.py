import cv2

img=cv2.imread("beer.jpg")
crop_img=img[0:500,0:500]


cv2.imshow("crop",crop_img)
cv2.waitKey(0)
cv2.imwrite('crop.jpg',crop_img)
