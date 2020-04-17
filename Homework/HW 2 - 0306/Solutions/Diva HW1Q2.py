#Q2
import cv2
img = cv2.imread("cat.jpg")
cv2.imshow('first',img)
cv2.waitKey(1000)
w, h,chan = img.shape
print(img.shape)
crop_img = img[int((w/2))-250:int((w/2))+250,int((h/2))-250:int((h/2))+250 ]
print(int((w/2)),int((w/2)),int((h/2)),int((h/2)))
cv2.imshow("cropped", crop_img)
print(crop_img.shape)
cv2.waitKey(1000)