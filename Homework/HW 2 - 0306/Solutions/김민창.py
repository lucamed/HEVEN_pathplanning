import cv2

photo=cv2.imread("cat.jpg",cv2.IMREAD_COLOR)

[x,y,z]=photo.shape
i=x//2;
j=y//2;

crop = photo.copy()
crop = photo[i-250:i+250 , i-250:i+250]

cv2.imshow("photo",photo)
cv2.imshow("crop", crop)


cv2.waitKey(0)
cv2.destroyAllWindows()
