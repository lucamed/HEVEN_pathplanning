import cv2

im=cv2.imread("cat.jpg",cv2.imread_color)

[a,b,c]=im.shape

i=a//2
j=b//2

dst=im.copy()

dst=im[i-250:i+250,j-250:j+250]

cv2.imshow("im",im)

cv2.imshow("dst",dst)

cv2.waitkey(0)

cv2.destroyallwindows()
