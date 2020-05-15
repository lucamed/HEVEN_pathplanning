import cv2

image=cv2.imread("image.jpg")

y=image.shape[0]/2
x=image.shape[1]/2
crop=image[int(y-250):int(y+250),int(x-250):int(x+250)]

cv2.imwrite("crop.jpg",crop)
